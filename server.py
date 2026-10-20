"""Custom Python runtime: python server.py; listen on all interfaces."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from index import response_payload


class Handler(BaseHTTPRequestHandler):
    def respond(self):
        size = int(self.headers.get("Content-Length", "0"))
        request_body = self.rfile.read(size).decode("utf-8") if size else ""
        payload = response_payload()
        payload.update(method=self.command, path=self.path, body=request_body)
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = respond
    do_POST = respond


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9000"))
    print("FC fixture listening on 0.0.0.0:%s" % port, flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
