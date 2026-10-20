# FC GitHub import fixture

This isolated test branch uses Python's standard library only. Importing
`index.py` performs no network calls and does not start a server.

## Built-in Python 3.10 runtime

- Code directory (Subdir): leave empty.
- HTTP request handler: `index.handler`.
- Event request handler: `index.event_handler`.
- Use automatic cloud build.

The HTTP handler supports both a WSGI `environ, start_response` call and a
context-based call. The event handler accepts one or two arguments and returns
a fixed JSON-compatible result.

## Custom Python 3.10 runtime

- Code directory (Subdir): leave empty.
- Startup command: `python server.py`.
- Listening port: `9000`.
- Use automatic cloud build.
- The server binds `0.0.0.0`, supports GET and POST, and echoes method, path and body.

## Verification

Set `QA_TEST_ENV=github-verified-1012`. Responses contain `ok: true`,
`marker: fc-verified-python-20261012-v1` and the supplied test environment value.
No secrets are required. Do not put credentials in the test environment variable.
