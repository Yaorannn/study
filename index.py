"""Dependency-free FC handler fixture. No work runs during module import."""
import json
import os

MARKER = "fc-verified-python-20261012-v1"


def response_payload():
    return {"ok": True, "marker": MARKER,
            "test_env": os.environ.get("QA_TEST_ENV", "unset")}


def handler(context, start_response=None):
    """Support the WSGI adapter and the context-based HTTP adapter."""
    body = json.dumps(response_payload(), ensure_ascii=False)
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if start_response is None:
        return body, 200, headers
    start_response("200 OK", list(headers.items()))
    return [body.encode("utf-8")]


def event_handler(event, context=None):
    """Return a deterministic result without depending on the event format."""
    return response_payload()
