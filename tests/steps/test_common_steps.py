from pathlib import Path
import json
import logging
from typing import Any, Dict
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from pytest_bdd import scenarios, when, then, parsers
from jsonschema import validate, ValidationError

# Add project root to path for imports
import sys
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from config import config

# Helpers
ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = ROOT / "tests" / "schemas"

scenarios("../features")

logger = logging.getLogger(__name__)

def _build_url(base_url: str, path: str) -> str:
    """Build complete URL from base URL and path."""
    return base_url.rstrip("/") + path

def _request(http, method: str, url: str, *, params=None, json_body=None, timeout=None):
    """
    Enhanced HTTP request with better error handling and logging.
    
    Args:
        http: HTTP session
        method: HTTP method
        url: Request URL
        params: Query parameters
        json_body: JSON body for POST/PUT/PATCH
        timeout: Request timeout (uses config default if None)
    
    Returns:
        Response object
        
    Raises:
        AssertionError: For unsupported methods or validation errors
        RequestException: For HTTP request failures
    """
    method = method.upper()
    if method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
        raise AssertionError(f"Unsupported method: {method}")
    
    timeout = timeout or config.timeout
    
    try:
        logger.info(f"Making {method} request to {url}")
        if params:
            logger.debug(f"Query params: {params}")
        if json_body:
            logger.debug(f"JSON body: {json_body}")
            
        response = getattr(http, method.lower())(
            url, 
            params=params, 
            json=json_body, 
            timeout=timeout
        )
        
        logger.info(f"Response: {response.status_code} in {response.elapsed.total_seconds():.3f}s")
        return response
        
    except Timeout:
        logger.error(f"Request timeout after {timeout}s for {method} {url}")
        raise
    except ConnectionError as e:
        logger.error(f"Connection error for {method} {url}: {e}")
        raise
    except RequestException as e:
        logger.error(f"Request failed for {method} {url}: {e}")
        raise

########################## WHEN ##########################

@when(parsers.cfparse('I {method:w} "{path}" with query params:\n{table}'))
def when_with_query_table(http, base_url, context, method, path, table):
    params = {}
    for line in table.strip().splitlines():
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) >= 2:
            key, value = parts[0], parts[1]
            params[key] = int(value) if value.isdigit() else value

    url = base_url.rstrip("/") + path
    resp = _request(http, method, url, params=params)
    context["response"] = resp

@when(parsers.cfparse('I {method:w} "{path}" with json:\n{table}'))
def when_with_json_table(http, base_url, context, method, path, table):
    data = {}
    for line in table.strip().splitlines():
        parts = [p.strip() for p in line.strip().strip('|').split('|')]
        if len(parts) >= 2:
            data[parts[0]] = parts[1]
    url = base_url.rstrip("/") + path
    context["response"] = _request(http, method, url, json_body=data)

@when(parsers.cfparse('I GET "{path}"'))
def when_get_simple(http, base_url: str, context: Dict[str, Any], path: str):
    url = _build_url(base_url, path)
    resp = http.get(url, timeout=15)
    context["response"] = resp

@when(parsers.cfparse('I DELETE "{path}"'))
def when_delete(http, base_url: str, context: Dict[str, Any], path: str):
    url = _build_url(base_url, path)
    resp = http.delete(url, timeout=15)
    context["response"] = resp

########################## THEN ##########################

@then(parsers.cfparse("the response status code should be {code:d}"))
def then_status_is(context: Dict[str, Any], code: int):
    resp = context.get("response")
    assert resp is not None, "No response was captured."
    assert resp.status_code == code, f"Expected {code}, got {resp.status_code}: {resp.text}"

@then(parsers.cfparse('the response should match the schema "{schema_name}"'))
def then_schema(context: Dict[str, Any], schema_name: str):
    """Validate response against JSON schema with enhanced error handling."""
    resp = context["response"]
    
    try:
        body = resp.json()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in response: {e}")
        raise AssertionError(f"Response is not valid JSON: {e}")
    
    schema_path = SCHEMAS_DIR / schema_name
    if not schema_path.exists():
        raise AssertionError(f"Schema file not found: {schema_path}")
    
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to load schema {schema_name}: {e}")
        raise AssertionError(f"Failed to load schema {schema_name}: {e}")
    
    try:
        validate(instance=body, schema=schema)
        logger.info(f"Schema validation passed for {schema_name}")
    except ValidationError as e:
        logger.error(f"Schema validation failed for {schema_name}: {e.message}")
        logger.error(f"Failed at path: {'.'.join(str(p) for p in e.absolute_path) if e.absolute_path else 'root'}")
        raise AssertionError(f"Schema validation failed: {e.message}")

@then(parsers.cfparse('the field "{path}" should be an array with at least {min_items:d} item'))
def then_array_min_items(context: Dict[str, Any], path: str, min_items: int):
    body = context["response"].json()
    value = body.get(path)
    assert isinstance(value, list), f"Field '{path}' is not an array: {type(value)}"
    assert len(value) >= min_items, f"Expected at least {min_items} items, got {len(value)}"