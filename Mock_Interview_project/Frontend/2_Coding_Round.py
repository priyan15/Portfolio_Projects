"""
Coding Round — pick a DSA problem, write code in an editor, run it against tests
on Piston, and get an (eventually LLM-powered) review.

Reached from the sidebar, or after configuring a session on the Home page.
"""

import streamlit as st

from src.execution import run_tests
from src.problems import load_dsa_problems, filter_problems
from src.review import llm_code_review

# A real code editor if streamlit-ace is installed; otherwise a plain text area.
try:
    from streamlit_ace import st_ace
    HAS_ACE = True
except ImportError:
    HAS_ACE = False

st.set_page_config(page_title="Coding Round", layout="wide")


def code_editor(initial: str, key: str) -> str:
    """Render an editor and return its current contents."""
    if HAS_ACE:
        return st_ace(
            value=initial,
            language="python",
            theme="monokai",
            keybinding="vscode",
            font_size=14,
            min_lines=18,
            key=key,
        )
    st.caption("Install `streamlit-ace` for a syntax-highlighted editor.")
    return st.text_area("Your solution", value=initial, height=360, key=key)


def render_results(result: dict) -> None:
    """Show the pass/fail summary and a per-test breakdown."""
    if not result["ok"]:
        st.error(result["error"])
        if result.get("stderr"):
            with st.expander("Runner output"):
                st.code(result["stderr"])
        return

    passed, total = result["passed"], result["total"]
    if passed == total:
        st.success(f"✓ All {total} tests passed!")
    else:
        st.warning(f"{passed}/{total} tests passed.")

    for i, r in enumerate(result["results"], start=1):
        icon = "✅" if r["ok"] else "❌"
        with st.expander(f"{icon} Test {i}", expanded=not r["ok"]):
            st.write("**Input:**", r["input"])
            st.write("**Expected:**", r["expected"])
            st.write("**Got:**", r["got"])


def main() -> None:
    st.title("Coding Round")

    problems = load_dsa_problems()
    if not problems:
        st.error("No problems found in Data_Layer/static_questions/dsa/.")
        return

    # If the user configured a session on the Home page, pre-filter the bank.
    config = st.session_state.get("interview_config")
    if config and config.get("category") == "DSA / Coding":
        problems = filter_problems(problems, difficulty=config.get("difficulty")) or problems

    titles = [f"{p['title']}  ·  {p['difficulty']}" for p in problems]
    choice = st.selectbox("Problem", options=range(len(problems)), format_func=lambda i: titles[i])
    problem = problems[choice]

    left, right = st.columns([1, 1])

    # ---- Left: problem statement -----------------------------------------
    with left:
        st.subheader(problem["title"])
        st.markdown(problem["statement"])

        if problem.get("examples"):
            st.markdown("**Examples**")
            for ex in problem["examples"]:
                st.markdown(f"- Input: `{ex['input']}` → Output: `{ex['output']}`")
                if ex.get("explanation"):
                    st.caption(ex["explanation"])

        if problem.get("constraints"):
            st.markdown("**Constraints**")
            for c in problem["constraints"]:
                st.markdown(f"- {c}")

        if problem.get("leetcode_link"):
            st.markdown(f"[Practice a similar one on LeetCode →]({problem['leetcode_link']})")

    # ---- Right: editor + actions -----------------------------------------
    with right:
        st.subheader("Your solution")
        # Key by problem id so switching problems resets the editor.
        code = code_editor(problem["starter_code"], key=f"editor_{problem['id']}")

        run_col, submit_col = st.columns(2)
        run_clicked = run_col.button("▶ Run samples", use_container_width=True)
        submit_clicked = submit_col.button("Submit", type="primary", use_container_width=True)

        if run_clicked:
            with st.spinner("Running sample tests..."):
                result = run_tests(code, problem["function_name"], problem["sample_tests"])
            render_results(result)

        if submit_clicked:
            all_tests = problem["sample_tests"] + problem["hidden_tests"]
            with st.spinner("Running full test suite..."):
                result = run_tests(code, problem["function_name"], all_tests)
            render_results(result)
            st.divider()
            st.subheader("Review")
            st.markdown(llm_code_review(problem, code, result))


if __name__ == "__main__":
    main()
