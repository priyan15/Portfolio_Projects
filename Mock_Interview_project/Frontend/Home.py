"""
Mock Interview — Homepage / Setup screen.

This is the Streamlit entry point. Run it with:
    cd /Users/priyankapawar/Desktop/Priyanka/Portfolio_Projects/Mock_Interview_project/Frontend/pages
    streamlit run Home.py

It collects the user's interview configuration (category, area, difficulty,
number of questions, question sources) and stashes it in st.session_state so the
next page (the interview itself) can read it.
"""

import streamlit as st

from src.taxonomy import CATEGORIES, DIFFICULTY_LEVELS, QUESTION_SOURCES

# --------------------------------------------------------------------------- #
# Page configuration
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="Mock Interviews",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def init_state() -> None:
    """Seed session_state defaults so reruns don't lose the config."""
    st.session_state.setdefault("interview_config", None)


# --------------------------------------------------------------------------- #
# Header / hero
# --------------------------------------------------------------------------- #
def render_hero() -> None:
    st.title("Mock Interviews")
    st.markdown(
        "Practice real interview rounds, **record your answers by voice**, and "
        "get **rubric-based feedback** on how you did."
    )
    st.divider()


# --------------------------------------------------------------------------- #
# Setup form
# --------------------------------------------------------------------------- #
def render_setup_form() -> None:
    st.subheader("Set up your session")

    # Category lives OUTSIDE the form so the area dropdown can react to it.
    category = st.selectbox(
        "Category",
        options=list(CATEGORIES.keys()),
        help="The interview round you want to practice.",
    )

    with st.form("interview_setup", border=True):
        area = st.selectbox(
            "Specific area",
            options=CATEGORIES[category],
            help="Narrow the focus, e.g. Reinforcement Learning or Linear Regression.",
        )

        col1, col2 = st.columns(2)
        with col1:
            difficulty = st.select_slider(
                "Difficulty",
                options=DIFFICULTY_LEVELS,
                value="Medium",
            )
        with col2:
            num_questions = st.number_input(
                "Number of questions",
                min_value=1,
                max_value=30,
                value=5,
                step=1,
            )

        sources = st.multiselect(
            "Question sources",
            options=QUESTION_SOURCES,
            default=QUESTION_SOURCES,
            help="Mix curated questions, book-sourced ones, and freshly LLM-generated ones.",
        )

        submitted = st.form_submit_button("Start interview →", use_container_width=True)

    if submitted:
        if not sources:
            st.error("Pick at least one question source.")
            return

        st.session_state.interview_config = {
            "category": category,
            "area": area,
            "difficulty": difficulty,
            "num_questions": int(num_questions),
            "sources": sources,
        }
        st.success("Session configured! Scroll down to review, then begin.")


# --------------------------------------------------------------------------- #
# Confirmation summary
# --------------------------------------------------------------------------- #
def render_summary() -> None:
    config = st.session_state.get("interview_config")
    if not config:
        return

    st.divider()
    st.subheader("Your session")

    c1, c2, c3 = st.columns(3)
    c1.metric("Category", config["category"])
    c2.metric("Difficulty", config["difficulty"])
    c3.metric("Questions", config["num_questions"])

    st.write(f"**Focus area:** {config['area']}")
    st.write(f"**Sources:** {', '.join(config['sources'])}")

    # Once you add a pages/ folder (e.g. pages/1_Interview.py), this jumps to it.
    # st.page_link("pages/1_Interview.py", label="Begin →", icon="▶️")
    st.button("Begin →", type="primary", use_container_width=True)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    init_state()
    render_hero()
    render_setup_form()
    render_summary()


if __name__ == "__main__":
    main()
