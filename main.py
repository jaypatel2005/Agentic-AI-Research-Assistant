import streamlit as st
import plotly.express as px
from agent import app
import time

# --- UI Configuration ---
st.set_page_config(page_title="Autonomous Research AI", layout="wide", page_icon="🔬")

st.title("Autonomous AI Research Assistant")
st.markdown("---")

# Initialize session state for persistence
if "master_state" not in st.session_state:
    st.session_state.master_state = {
        "domain": "Initializing...",
        "iteration_count": 0,
        "confidence_score": 0.0,
        "research_notes": [],
        "questions": [],
        "experiment_design": "Developing...",
        "final_paper": ""
    }

if "run_complete" not in st.session_state:
    st.session_state.run_complete = False

# Sidebar for live tracking
with st.sidebar:
    st.header("🕵️ Agent Status")
    status_placeholder = st.empty()
    st.divider()
    if st.session_state.run_complete:
        st.success("Research Phase Complete")
        # --- Requirement: Final Markdown Export ---
        st.download_button(
            label="Download Research Paper",
            data=st.session_state.master_state.get("final_paper", ""),
            file_name=f"research_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True
        )

# --- Main Execution ---
if st.button("🚀 Start Autonomous Research Pipeline", use_container_width=True):
    st.session_state.run_complete = False
    
    with st.status("Agents collaborating...", expanded=True) as status:
        log_container = st.container()
        
        # Initial inputs for LangGraph
        inputs = {
            "domain": "", 
            "iteration_count": 0, 
            "research_notes": [], 
            "status_updates": ["System Online..."],
            "questions": [],
            "confidence_score": 0.0
        }
        
        # Stream the graph execution
        for output in app.stream(inputs):
            for node_name, node_update in output.items():
                # --- Requirement: Persistent State Tracking ---
                # This ensures values like 'domain' aren't lost when 'critic' runs
                st.session_state.master_state.update(node_update)
                
                # Update UI logs
                if "status_updates" in node_update:
                    msg = node_update["status_updates"][-1]
                    log_container.write(f"**[{node_name.upper()}]**: {msg}")
                    status_placeholder.info(f"**Active:** {node_name.capitalize()}")
        
        status.update(label="Research Complete!", state="complete", expanded=False)
        st.session_state.run_complete = True
        st.rerun() # Refresh to show the dashboard

# --- Display Dashboard (Only if research is done or in progress) ---
if st.session_state.run_complete:
    res = st.session_state.master_state
    conf = res.get("confidence_score", 0.0)
    
    # Requirement: Multi-column Dashboard
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header(f"📄 Results: {res.get('domain')}")
        
        tabs = st.tabs(["Research Questions", "Hypothesis & Design", "Full Paper"])
        
        with tabs[0]:
            st.write(res.get("questions", ["Questions pending..."])[0])
            
        with tabs[1]:
            st.info(res.get("experiment_design", "Design pending..."))
            
        with tabs[2]:
            st.markdown(res.get("final_paper", "Generating paper..."))
            
    with col2:
        st.header("📊 Metrics")
        
        # Requirement: Interactive Plotly Gauge
        fig = px.pie(
            values=[conf, 1.0 - conf if conf <= 1.0 else 0], 
            names=["Confidence", "Uncertainty"],
            hole=0.7,
            color_discrete_sequence=["#2ecc71", "#34495e"]
        )
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Confidence Score", f"{conf*100:.1f}%")
        st.metric("Research Cycles", res.get("iteration_count", 0))

    # Requirement: Handle Conflict/Ambiguity visualization
    if conf < 0.6:
        st.warning("⚠️ Note: The Critic requested additional depth due to limited ArXiv data.")