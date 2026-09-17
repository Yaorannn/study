"""Small, dependency-free fixture for GitHub function import checks."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

MARKER = "github-import-20260917-v1"

def payload(method="GET", path="/", body=""):
    return {"ok": True, "marker": MARKER, "method": method, "path": path,
            "body": body, "test_env": os.environ.get("FC_GITHUB_TEST", "missing")}

def handler(context, start_response=None):
    if start_response is not None:
        body = context["wsgi.input"].read(int(context.get("CONTENT_LENGTH") or 0)).decode()
        result = json.dumps(payload(context.get("REQUEST_METHOD"), context.get("PATH_INFO"), body)).encode()
        start_response("200 OK", [("Content-Type", "application/json")])
        return [result]
    request = context.request
    return json.dumps(payload(request.method, request.path, request.get_data(as_text=True))), 200, {"Content-Type": "application/json"}

def event_handler(event, context=None):
    value = event.cloud_event.data if hasattr(event, "cloud_event") else event
    if isinstance(value, bytes):
        value = value.decode()
    return {"ok": True, "marker": MARKER, "event": value, "test_env": os.environ.get("FC_GITHUB_TEST", "missing")}

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        data = json.dumps(payload(self.command, self.path)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()
        data = json.dumps(payload(self.command, self.path, body)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "9000"))), Server).serve_forever()
