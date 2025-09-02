import os
import sys
import logging
from typing import Dict, Any
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
import time
import json
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from config import config
from tests.utils.data_loader import data_loader

load_dotenv()  # loads .env if present

@pytest.fixture(scope="session")
def base_url() -> str:
    return config.base_url

@pytest.fixture()
def http():
    """Enhanced HTTP session with retry strategy and error handling."""
    session = requests.Session()
    
    # Retry strategy for transient failures
    retry_strategy = Retry(
        total=config.retry_count,
        backoff_factor=config.retry_backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"]
    )
    
    # Mount adapters with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set default headers
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": "QA-Portfolio-Tests/1.0",
        "x-api-key": "reqres-free-v1"
    })
    
    # Set default timeout
    session.timeout = config.timeout
    
    try:
        yield session
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
        raise
    finally:
        session.close()

@pytest.fixture(autouse=True)
def setup_logging():
    """Setup structured logging for tests."""
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / 'test_results.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

@pytest.fixture()
def context() -> Dict[str, Any]:
    """A mutable dict to share data between steps."""
    return {}

@pytest.fixture(scope="session")
def test_data():
    """Load all test data."""
    return {
        'auth': data_loader.get_auth_data(),
        'users': data_loader.get_user_data(),
        'resources': data_loader.get_resource_data()
    }

@pytest.fixture(scope="session")
def auth_data():
    """Load authentication test data."""
    return data_loader.get_auth_data()

@pytest.fixture(scope="session")
def user_data():
    """Load user test data."""
    return data_loader.get_user_data()

@pytest.fixture(scope="session")
def resource_data():
    """Load resource test data."""
    return data_loader.get_resource_data()

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    print(f"[{feature.name} - {scenario.name}] ✔ {step.keyword} {step.name}")

@pytest.fixture(autouse=True)
def _timer(context):
    context["__start_ts"] = time.time()
    yield
    context["__duration_ms"] = int((time.time() - context["__start_ts"]) * 1000)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call":
        return

    record_property = item.funcargs.get("record_property", None)
    ctx = item.funcargs.get("context", {}) if hasattr(item, "funcargs") else {}
    resp = ctx.get("response")

    if callable(record_property):
        if resp is not None:
            record_property("request.method", resp.request.method)
            record_property("request.url", resp.request.url)
            record_property("response.status", resp.status_code)
            record_property("response.elapsed_ms", int(resp.elapsed.total_seconds() * 1000))
        dur = ctx.get("__duration_ms")
        if dur is not None:
            record_property("test.duration_ms", dur)

    if resp is not None:
        try:
            body = json.dumps(resp.json(), indent=2, ensure_ascii=False)
        except Exception:
            body = (resp.text or "")[:10000]
        print(f"\nHTTP {resp.request.method} {resp.request.url} -> {resp.status_code}\n{body}\n")