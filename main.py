import streamlit as st
import time
import random
import plotly.express as px
from agent import app

st.set_page_config(
    page_title="Live Research Agent Demo",
    layout="wide"
)

st.title("🎬 Live Demo — Autonomous Research Agent")
st.caption("Click Run to watch agents think, argue, and produce research in real time.")

if "running" not in st.session_state:
    st.session_state.running = False

if "state" not in st.session_state:
    st.session_state.state = None

domain = st.text_input(
    "Research topic",
    placeholder="Solid State Batteries, Quantum Sensors, Bio-plastics"
)

run_clicked = st.button("🚀 Run Live Demo", use_container_width=True)

if run_clicked and domain.strip():
    st.session_state.running = True

    st.session_state.state = {
        "domain": domain.strip(),
        "questions": [],
        "research_notes": [],
        "hypothesis": "",
        "experiment_design": "",
        "confidence_score": 0.0,
        "iteration_count": 0,
        "final_paper": "",
        "status_updates": []
    }

    log_box = st.empty()
    status_box = st.empty()

    jokes = [
        "Consulting the arXiv spirits…",
        "Arguing with itself about methodology…",
        "Pretending to read 200 papers at once…",
        "Running peer review in its head…",
        "Double-checking confidence levels…"
    ]

    with st.status("🤖 Agents running...", expanded=True) as status:
        for output in app.stream(st.session_state.state):
            for node, update in output.items():
                st.session_state.state.update(update)

                if "status_updates" in update:
                    log_box.markdown(
                        f"**{node.upper()}** — {update['status_updates'][-1]}"
                    )
                else:
                    log_box.markdown(random.choice(jokes))

                status_box.info(f"Active node: {node}")
                time.sleep(0.3)

        status.update(
            label="✅ Research Complete",
            state="complete",
            expanded=False
        )

    st.session_state.running = False

if st.session_state.state and not st.session_state.running:
    res = st.session_state.state

    st.divider()
    st.header("📄 Final Research Output")

    tab1, tab2, tab3 = st.tabs(
        ["📘 Paper", "📊 Metrics", "🧠 Process"]
    )

    with tab1:
        st.markdown(res["final_paper"] or "No paper generated.")

    with tab2:
        confidence = res["confidence_score"]

        fig = px.pie(
            values=[confidence, 1 - confidence],
            names=["Confidence", "Uncertainty"],
            hole=0.7
        )
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("Confidence Score", f"{confidence * 100:.0f}%")
        c2.metric("Iterations", res["iteration_count"])

    with tab3:
        st.markdown("### Agent Messages")
        for msg in res["status_updates"]:
            st.markdown(f"- {msg}")
