"""
Code execution via a local Python subprocess.

The user's solution is wrapped in a self-contained driver script and run in a
fresh interpreter (sys.executable -c ...). The child only talks to us through
stdout: it prints one marker line of JSON results, which we parse back out.

We run in a separate process (not exec() in-process) so a crash, sys.exit, or
runaway loop in the user's code can't take down the app — the subprocess gets a
hard wall-clock timeout instead.

The flow:
  1. build_harness() wraps the user's function with a test-runner driver.
  2. run_tests() runs that script and parses a single marker line of JSON
     results back out of stdout.
"""

import base64
import json
import subprocess
import sys

RESULT_MARKER = "__RESULTS__"
RUN_TIMEOUT = 10            # seconds of wall-clock before we kill the child


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
    """Execute user_code against tests in a local subprocess.

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

    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-c", script],
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return _fail(
            f"Your code timed out after {RUN_TIMEOUT}s (possible infinite loop).",
            total=len(tests),
        )
    except OSError as exc:
        return _fail(f"Could not start the code runner: {exc}", total=len(tests))

    stdout = proc.stdout or ""
    stderr = proc.stderr or ""

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
