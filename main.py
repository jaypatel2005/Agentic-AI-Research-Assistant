import streamlit as st
import plotly.express as px
from agent import app
import time

# --- 1. UI Configuration ---
st.set_page_config(page_title="Autonomous Research AI", layout="wide", page_icon="🔬")

# --- 2. Error Handler ---
def show_contact_error(e_type, e_msg):
    st.error(f"**🚨 {e_type}**")
    st.info(f"Technical Note: `{e_msg}`\n\nPlease contact **yourname@email.com** to rectify or request a dedicated demo.")

# --- 3. State Management ---
if "master_state" not in st.session_state:
    st.session_state.master_state = {
        "domain": "Not Started",
        "iteration_count": 0,
        "confidence_score": 0.0,
        "research_notes": [],
        "questions": ["Developing..."],
        "experiment_design": "Synthesizing...",
        "final_paper": "",
        "status_updates": []
    }

if "run_complete" not in st.session_state:
    st.session_state.run_complete = False

st.title("Autonomous AI Research Assistant")
st.markdown("---")

# --- 4. Sidebar ---
with st.sidebar:
    st.header("🕵️ Agent Status")
    status_placeholder = st.empty()
    st.divider()
    
    if st.session_state.run_complete:
        st.success("Analysis Complete")
        # --- FEATURE: Download Research Paper ---
        st.download_button(
            label="📥 Download Research Paper (.md)",
            data=st.session_state.master_state.get("final_paper", ""),
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True
        )

# --- 5. Main Execution Loop ---
if st.button("🚀 Start Autonomous Research Pipeline", use_container_width=True):
    st.session_state.run_complete = False
    
    try:
        with st.status("Agents collaborating...", expanded=True) as status:
            log_container = st.container()
            
            # Reset and Start Graph
            inputs = {"domain": "", "iteration_count": 0, "research_notes": [], "questions": []}
            
            for output in app.stream(inputs):
                for node_name, node_update in output.items():
                    # --- FEATURE: Sanitizer (Prevents "None" from breaking UI) ---
                    for key, val in node_update.items():
                        if val is None or val == "":
                            node_update[key] = f"Pending {key}..."
                    
                    # Update Master State persistently
                    st.session_state.master_state.update(node_update)
                    
                    # Live Logging
                    if "status_updates" in node_update:
                        msg = node_update["status_updates"][-1]
                        log_container.write(f"**[{node_name.upper()}]**: {msg}")
                        status_placeholder.info(f"**Active Node:** {node_name.capitalize()}")
            
            status.update(label="Research Complete!", state="complete", expanded=False)
            st.session_state.run_complete = True
            st.rerun() # Refresh to show results dashboard

    except Exception as e:
        err = str(e).lower()
        if "quota" in err or "429" in err:
            show_contact_error("API Quota Reached", "Free-tier limits reached. Reset at midnight.")
        else:
            show_contact_error("System Interruption", e)

# --- 6. Results Dashboard (The Full Feature View) ---
if st.session_state.run_complete:
    res = st.session_state.master_state
    
    # Requirement: Multi-column Dashboard
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header(f"📄 Results: {res.get('domain')}")
        
        # FEATURE: Organized Tabs
        tab1, tab2, tab3 = st.tabs(["💡 Questions", "🧪 Design", "📖 Final Paper"])
        
        with tab1:
            st.markdown("### Research Questions")
            q_data = res.get("questions", ["Developing..."])
            st.write(q_data[0] if isinstance(q_data, list) else q_data)
            
        with tab2:
            st.markdown("### Hypothesis & Experimental Design")
            st.info(res.get("experiment_design", "Synthesizing..."))
            
        with tab3:
            st.markdown(res.get("final_paper", "Generating paper..."))
            
    with col2:
        st.header("📊 Metrics")
        
        # FEATURE: Confidence Gauge (Plotly)
        conf = res.get("confidence_score", 0.0)
        # Ensure values are plot-able
        safe_conf = max(0.01, min(conf, 1.0))
        
        fig = px.pie(
            values=[safe_conf, 1.0 - safe_conf], 
            names=["Confidence", "Gap"],
            hole=0.7,
            color_discrete_sequence=["#2ecc71", "#34495e"]
        )
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Critic Score", f"{conf*100:.0f}%")
        st.metric("Cycles", res.get("iteration_count", 0))

    st.divider()
    st.caption("Generated by Autonomous Multi-Agent Research System | 2026 Assessment")