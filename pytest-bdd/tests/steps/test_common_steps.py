from pathlib import Path
import json
from typing import Any, Dict

from pytest_bdd import scenarios, when, then, parsers
from jsonschema import validate

# Helperspytest
ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = ROOT / "tests" / "schemas"

scenarios("../features")

def _build_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + path

def _request(http, method: str, url: str, *, params=None, json_body=None, timeout=15):
    method = method.upper()
    if method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
        raise AssertionError(f"Unsupported method: {method}")
    return getattr(http, method.lower())(url, params=params, json=json_body, timeout=timeout)

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
    resp = context["response"]
    body = resp.json()
    schema_path = SCHEMAS_DIR / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate(instance=body, schema=schema)

@then(parsers.cfparse('the field "{path}" should be an array with at least {min_items:d} item'))
def then_array_min_items(context: Dict[str, Any], path: str, min_items: int):
    body = context["response"].json()
    value = body.get(path)
    assert isinstance(value, list), f"Field '{path}' is not an array: {type(value)}"
    assert len(value) >= min_items, f"Expected at least {min_items} items, got {len(value)}"