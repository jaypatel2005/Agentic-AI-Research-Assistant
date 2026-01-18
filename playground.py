import streamlit as st
from agent import app

st.set_page_config(
    page_title="AI Research Playground",
    layout="wide",
    page_icon="🧪"
)

st.title("🔬 Research Agent Playground")
st.caption(
    "Enter a scientific topic. The agent will plan, verify, refine, "
    "and produce a short research brief."
)

if "master_state" not in st.session_state:
    st.session_state.master_state = None

if "run_complete" not in st.session_state:
    st.session_state.run_complete = False

with st.sidebar:
    st.header("Playground Info")
    st.markdown("""
    **This demo showcases:**
    - User-driven research topics
    - Autonomous refinement loops
    - Tool use (ArXiv + Search)
    - Critic-controlled termination
    """)

    if st.button("Clear Session"):
        st.session_state.master_state = None
        st.session_state.run_complete = False
        st.rerun()

user_prompt = st.text_input(
    "Enter a research topic",
    placeholder="Solid State Batteries, Quantum Sensors, Bio-plastics..."
)

if st.button("🚀 Generate Research", use_container_width=True):

    if not user_prompt.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    st.session_state.master_state = {
        "domain": user_prompt.strip(),
        "questions": [],
        "research_notes": [],
        "hypothesis": "",
        "experiment_design": "",
        "confidence_score": 0.0,
        "iteration_count": 0,
        "final_paper": "",
        "status_updates": []
    }

    st.session_state.run_complete = False

    try:
        with st.status("🤖 Agents are collaborating...", expanded=True) as status:

            log_container = st.container()

            for output in app.stream(st.session_state.master_state):
                for node_name, node_update in output.items():

                    st.session_state.master_state.update(node_update)

                    if "status_updates" in node_update:
                        log_container.markdown(
                            f"**{node_name.upper()}** — "
                            f"{node_update['status_updates'][-1]}"
                        )

            status.update(
                label="Research Complete",
                state="complete",
                expanded=False
            )

        st.session_state.run_complete = True

    except Exception as e:
        st.error("🚨 An error occurred during execution.")
        st.exception(e)
        st.stop()

if st.session_state.run_complete and st.session_state.master_state:

    res = st.session_state.master_state

    st.divider()

    st.download_button(
        label="📥 Download Markdown",
        data=res["final_paper"],
        file_name="research.md",
        mime="text/markdown",
        use_container_width=True
    )

    tab1, tab2, tab3 = st.tabs(
        ["💡 Questions", "🧪 Experiment", "📖 Final Paper"]
    )

    with tab1:
        if res["questions"]:
            for q in res["questions"]:
                st.markdown(f"- {q}")
        else:
            st.info("No questions generated.")

    with tab2:
        st.markdown(res["experiment_design"] or "No design available.")

    with tab3:
        st.markdown(res["final_paper"] or "No paper generated.")

    st.divider()
    c1, c2, c3 = st.columns(3)

    c1.metric("Iterations", res["iteration_count"])
    c2.metric("Confidence", f"{res['confidence_score'] * 100:.0f}%")
    c3.success("Verified by Critic Agent")


st.markdown("---")
st.caption(
    "Note: This system uses free-tier APIs. "
    "If execution stalls, rate limits may be the cause."
)
