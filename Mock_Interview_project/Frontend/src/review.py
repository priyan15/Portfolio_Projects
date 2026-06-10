"""
LLM code review — STUB.

This is intentionally a placeholder so the coding round runs end-to-end without
an API key. When you build Ml_Layer/evaluation, replace `llm_code_review` with a
real call: feed it the problem, the user's code, and the test results, and ask
the model to critique correctness, time/space complexity, and readability
against your fixed metrics.
"""


def llm_code_review(problem: dict, user_code: str, run_result: dict) -> str:
    """Return human-readable feedback. Currently a heuristic placeholder."""
    passed = run_result.get("passed", 0)
    total = run_result.get("total", 0)
    lines = [
        "_(Placeholder review — connect Ml_Layer/evaluation to make this real.)_",
        "",
        f"- **Correctness:** {passed}/{total} tests passed.",
        f"- **Reference approach:** {problem.get('reference_complexity', 'n/a')}",
        f"- **Your solution length:** {len(user_code.splitlines())} lines.",
    ]
    if total and passed == total:
        lines.append("- All tests pass. A real reviewer would now critique your "
                     "time/space complexity and naming against the reference.")
    elif passed:
        lines.append("- Some tests fail — check the failing cases above for edge conditions.")
    return "\n".join(lines)
