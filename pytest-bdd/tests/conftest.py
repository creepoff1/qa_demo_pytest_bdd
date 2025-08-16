import os
from typing import Dict, Any
import pytest
import requests
from dotenv import load_dotenv
import time
import json

load_dotenv()  # loads .env if present

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://reqres.in")

@pytest.fixture()
def http():
    """Simple wrapper around requests.Session for connection pooling."""
    with requests.Session() as s:
        s.headers.update({"Accept": "application/json", "x-api-key": "reqres-free-v1"})
        yield s

@pytest.fixture()
def context() -> Dict[str, Any]:
    """A mutable dict to share data between steps."""
    return {}

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