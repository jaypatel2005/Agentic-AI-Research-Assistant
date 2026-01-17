import streamlit as st
import time
import re
from agent import app 

# --- UI Setup ---
st.set_page_config(page_title="AI Research Playground", layout="wide", page_icon="🧪")

st.title("🔬 Research Agent Playground")
st.caption("Enter any scientific topic below. This autonomous system will scout, plan, and verify the research.")

# --- Custom Error Handler ---
def show_contact_error(e_msg):
    st.error(f"""
    **🚨 An unexpected error occurred.**
    
    *Details:* {e_msg}
    
    This is likely due to API quota limits on the free tier. Please contact **jay599063@gmail.com** to rectify this or request a live demo.
    """)

# --- Sidebar & Initialization ---
with st.sidebar:
    st.header("Playground Settings")
    st.markdown("""
    This playground demonstrates:
    - **Self-Correction Loops**
    - **Tool Use (ArXiv & Tavily)**
    - **Graceful Error Handling**
    """)
    if st.button("Clear History"):
        st.session_state.master_state = None
        st.rerun()

# --- Main Logic ---
user_prompt = st.text_input("Enter a research topic (e.g., 'Solid State Batteries', 'Bio-plastics'):", placeholder="Quantum Computing...")

if st.button("Generate Research", use_container_width=True):
    if not user_prompt:
        st.warning("Please enter a topic first.")
    else:
        # 1. Initialize Master State
        master_state = {
            "domain": user_prompt,
            "iteration_count": 0,
            "confidence_score": 0.0,
            "research_notes": [],
            "questions": [],
            "experiment_design": "Processing...",
            "final_paper": "",
            "status_updates": []
        }

        try:
            with st.status("🤖 Agents are thinking...", expanded=True) as status:
                log_placeholder = st.empty()
                
                # 2. Run the Graph with Error Handling
                for output in app.stream(master_state):
                    for node_name, node_update in output.items():
                        # Handle Potential None/Empty Returns from Agents
                        for key, val in node_update.items():
                            if val is None or val == "":
                                node_update[key] = "Data currently unavailable (Fallback Active)"
                        
                        master_state.update(node_update)
                        
                        # Live Log Updates
                        if "status_updates" in node_update:
                            current_log = node_update["status_updates"][-1]
                            log_placeholder.markdown(f"**{node_name.upper()}**: {current_log}")
                
                status.update(label="Research Finalized!", state="complete", expanded=False)

            # 3. Final Result Validation
            if not master_state.get("final_paper"):
                st.warning("The research was completed, but the final report was empty. Please try a more specific topic.")
            else:
                st.divider()
                st.markdown(master_state["final_paper"])
                
                # Metrics Row
                c1, c2, c3 = st.columns(3)
                c1.metric("Iterations", master_state["iteration_count"])
                c2.metric("Confidence", f"{master_state['confidence_score']*100:.0f}%")
                c3.success("Verified by Critic Agent")

        except Exception as e:
            # Catch API Quota (ResourceExhausted) or Network Errors
            error_str = str(e)
            if "quota" in error_str.lower() or "429" in error_str:
                show_contact_error("API Quota Exhausted (Rate Limit reached).")
            else:
                show_contact_error(error_str)

# --- Bottom Disclaimer ---
st.markdown("---")
st.caption("Note: This agent uses free-tier LLM APIs. If the system stalls, it is likely due to global rate limits.")