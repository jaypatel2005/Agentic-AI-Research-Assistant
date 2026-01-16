import streamlit as st
import plotly.express as px
from agent import app  # Import your compiled graph from agent.py
import time

# --- UI Configuration ---
st.set_page_config(page_title="Autonomous Research AI", layout="wide", page_icon="🔬")

st.title("🔬 Autonomous AI Research Assistant")
st.markdown("---")

# Sidebar for metadata and status
with st.sidebar:
    st.header("Agent Status")
    status_box = st.empty()
    st.info("Searching for post-2024 emerging scientific domains...")
    
# Initialize session state to store research results
if "final_results" not in st.session_state:
    st.session_state.final_results = None

# --- Main Execution ---
if st.button("🚀 Start Autonomous Research Pipeline", use_container_width=True):
    # Placeholders for real-time updates
    with st.status("Agents collaborating...", expanded=True) as status:
        log_container = st.container()
        
        # Initial State
        inputs = {
            "domain": "", 
            "iteration_count": 0, 
            "research_notes": [], 
            "status_updates": ["Initializing multi-agent system..."]
        }
        
        # Stream the graph execution
        # Requirement: Real-time messages (can even be jokes)
        for output in app.stream(inputs):
            for node_name, value in output.items():
                if "status_updates" in value:
                    msg = value["status_updates"][-1]
                    log_container.write(f"**[{node_name.upper()}]**: {msg}")
                    status_box.write(f"Current: {node_name.capitalize()}")
                
                # Capture the final state once the loop ends
                st.session_state.final_results = value
        
        status.update(label="Research Complete!", state="complete", expanded=False)

# --- Display Results ---
if st.session_state.final_results:
    res = st.session_state.final_results
    
    # Requirement: Multi-column Dashboard & Visualization
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("📄 Research Findings")
        st.markdown(f"### Target Domain: {res.get('domain', 'Analyzing...')}")
        
        # Display Research Questions & Design
        st.subheader("Research Questions")
        st.write(res.get("questions", ["Developing..."])[0])
        
        st.subheader("Hypothesis & Experimental Design")
        st.info(res.get("experiment_design", "Synthesizing..."))
        
    with col2:
        st.header("📊 Metrics")
        
        # Requirement: Interactive Plotly Dashboard (Confidence Score)
        conf = res.get("confidence_score", 0.0)
        fig = px.pie(
            values=[conf, 1-conf], 
            names=["Confidence", "Uncertainty"],
            hole=0.6,
            color_discrete_sequence=["#2ecc71", "#e74c3c"]
        )
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Final Confidence", f"{conf*100:.0f}%")
        st.metric("Iterations", res.get("iteration_count", 0))

    # Requirement: Final Markdown Paper
    st.divider()
    st.subheader("📝 Scientific Summary")
    st.markdown(f"""
    **Autonomous Analysis Summary**
    The multi-agent system has concluded its research on **{res.get('domain')}**. 
    After {res.get('iteration_count')} self-correction cycles, the Critic agent 
    has verified the methodology with a confidence score of {conf*100:.1f}%.
    """)