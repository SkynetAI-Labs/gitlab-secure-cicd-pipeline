"""Black-box checks for an already running container; accepts a localhost base URL."""

import json
import sys
import time
import urllib.error
import urllib.request


def call(base, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        base + path, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


def main(base):
    for _attempt in range(30):
        try:
            if call(base, "/healthz") == (200, {"status": "ok"}):
                break
        except OSError, ValueError:
            pass
        time.sleep(1)
    else:
        raise SystemExit("Health check failed")
    summary = dict(critical=0, high=0, medium=1, low=2, tests_passed=True, secrets_found=False)
    if call(base, "/evaluate", summary) != (200, {"decision": "allow", "reasons": []}):
        raise SystemExit("Clean release decision failed")
    summary["high"] = 1
    if call(base, "/evaluate", summary) != (
        200,
        {"decision": "block", "reasons": ["high_findings"]},
    ):
        raise SystemExit("Blocked release decision failed")
    if call(base, "/evaluate", {"unexpected": True})[0] != 400:
        raise SystemExit("Invalid-input check failed")
    print("PASS: container health, allow, block, and invalid-input checks")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080")
