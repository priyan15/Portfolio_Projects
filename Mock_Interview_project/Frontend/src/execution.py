"""
Code execution via the public Piston API (https://github.com/engineer-man/piston).

Piston runs untrusted code in a sandbox and returns stdout/stderr. It's free and
needs no API key. We never exec user code locally — it always goes to Piston.

The flow:
  1. build_harness() wraps the user's function with a test-runner driver.
  2. run_tests() ships that to Piston and parses a single marker line of JSON
     results back out of stdout.
"""

import base64
import json

import requests

PISTON_URL = "https://emkc.org/api/v2/piston/execute"
PISTON_LANGUAGE = "python"
PISTON_VERSION = "3.10.0"   # widely available on the public Piston instance
RESULT_MARKER = "__RESULTS__"
REQUEST_TIMEOUT = 20        # seconds for the HTTP call itself


def build_harness(user_code: str, function_name: str, tests: list) -> str:
    """Wrap user code with a driver that runs each test and prints JSON results.

    Test cases are base64-encoded into the script to sidestep any quoting issues.
    Comparison is done on json.dumps(..., sort_keys=True) so list order is
    respected while dict key order is not.
    """
    encoded = base64.b64encode(json.dumps(tests).encode()).decode()
    return f'''
import json, base64, traceback

{user_code}

def __norm(value):
    return json.dumps(value, sort_keys=True, default=str)

__tests = json.loads(base64.b64decode("{encoded}").decode())
__out = []
for __t in __tests:
    __args = __t["input"]
    __expected = __t["expected"]
    try:
        __got = {function_name}(*__args)
        __ok = __norm(__got) == __norm(__expected)
    except Exception:
        __got = "ERROR: " + (traceback.format_exc().strip().splitlines() or ["unknown"])[-1]
        __ok = False
    __out.append({{"input": __args, "expected": __expected, "got": __got, "ok": __ok}})

print("{RESULT_MARKER}" + json.dumps(__out, default=str))
'''


def run_tests(user_code: str, function_name: str, tests: list) -> dict:
    """Execute user_code against tests on Piston.

    Returns a dict:
      {
        "ok": bool,              # did the run complete and produce results?
        "results": [ {input, expected, got, ok}, ... ],
        "passed": int, "total": int,
        "error": str | None,     # set when we couldn't get results back
        "stderr": str,
      }
    """
    script = build_harness(user_code, function_name, tests)
    payload = {
        "language": PISTON_LANGUAGE,
        "version": PISTON_VERSION,
        "files": [{"name": "main.py", "content": script}],
        "run_timeout": 5000,
    }

    try:
        resp = requests.post(PISTON_URL, json=payload, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        run = resp.json().get("run", {})
    except requests.RequestException as exc:
        return _fail(f"Could not reach the code runner: {exc}", total=len(tests))

    stdout = run.get("stdout", "") or ""
    stderr = run.get("stderr", "") or ""

    marker_line = next(
        (ln for ln in stdout.splitlines() if ln.startswith(RESULT_MARKER)), None
    )
    if marker_line is None:
        # No results => the user's code almost certainly errored (syntax, etc.).
        return _fail(stderr.strip() or "Your code did not run.", total=len(tests), stderr=stderr)

    results = json.loads(marker_line[len(RESULT_MARKER):])
    passed = sum(1 for r in results if r["ok"])
    return {
        "ok": True,
        "results": results,
        "passed": passed,
        "total": len(results),
        "error": None,
        "stderr": stderr,
    }


def _fail(message: str, total: int = 0, stderr: str = "") -> dict:
    return {
        "ok": False,
        "results": [],
        "passed": 0,
        "total": total,
        "error": message,
        "stderr": stderr,
    }
