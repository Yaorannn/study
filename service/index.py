"""Dependency-free FC HTTP and event sample fixture."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

MARKER = "fc-sample-matrix-0918-python"

def payload(method="GET", path="/", body=""):
    return {"ok": True, "marker": MARKER, "method": method, "path": path, "body": body}

def handler(context, start_response=None):
    if start_response is not None:
        raw = context["wsgi.input"].read(int(context.get("CONTENT_LENGTH") or 0)).decode()
        data = json.dumps(payload(context.get("REQUEST_METHOD"), context.get("PATH_INFO"), raw)).encode()
        start_response("200 OK", [("Content-Type", "application/json")])
        return [data]
    if hasattr(context, "request"):
        request = context.request
        return json.dumps(payload(request.method, request.path, request.get_data(as_text=True))), 200, {"Content-Type": "application/json"}
    event = context.cloud_event.data if hasattr(context, "cloud_event") else context
    if isinstance(event, bytes):
        event = event.decode()
    return {"ok": True, "marker": MARKER, "event": event}

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond("")
    def do_POST(self):
        self.respond(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
    def respond(self, body):
        data = json.dumps(payload(self.command, self.path, body)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Server).serve_forever()
