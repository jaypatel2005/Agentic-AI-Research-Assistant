import streamlit as st
import time
import json
import markdown
import plotly.express as px
from datetime import datetime
from xhtml2pdf import pisa  
from io import BytesIO 
from src import stream_research_crew 
from src.config import Config

st.set_page_config(page_title="Agentic Research Assistant", layout="wide")

st.markdown("""
<style>
    .log-entry {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 5px solid #1f77b4;
        background-color: #f0f2f6; 
        color: #31333F; 
        font-family: "Source Code Pro", monospace;
        font-size: 0.9em;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .log-timestamp { color: #6c757d; font-size: 0.8em; margin-right: 10px; font-weight: bold; }
    .agent-tag { font-weight: 900; color: #0d6efd; margin-right: 5px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

AGENT_ICONS = {
    "scout": "🔭", "planner": "📝", "alchemist": "⚗️", 
    "designer": "📐", "critic": "⚖️", "writer": "✍️"
}

# --- PDF Generation Function ---
def generate_pdf(markdown_content):
    """Converts Markdown text to a PDF byte array."""
    # 1. Convert Markdown to HTML
    html_text = markdown.markdown(markdown_content)
    
    # 2. Add some basic styling for the PDF
    styled_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, sans-serif; font-size: 12pt; line-height: 1.5; }}
            h1 {{ color: #1f77b4; font-size: 24pt; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
            h2 {{ color: #1f77b4; font-size: 18pt; margin-top: 20px; }}
            p {{ margin-bottom: 10px; }}
            strong {{ color: #333; }}
        </style>
    </head>
    <body>
        {html_text}
    </body>
    </html>
    """
    
    # 3. Create PDF in memory
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(styled_html, dest=pdf_file)
    
    if pisa_status.err:
        return None
    return pdf_file.getvalue()

# --- Title Section ---
c1, c2 = st.columns([1, 6])
with c1: st.markdown("# 🤖")
with c2:
    st.title("Autonomous Research Agent")
    st.caption("Watch AI agents think, research, and debug in real-time.")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    topic = st.text_input("Research Topic", placeholder="e.g., Solid State Batteries")
    run_btn = st.button("🚀 Start Research")
    st.divider()
    show_debug = st.toggle("Show Debug Logs", value=True)

# --- Main Logic ---
if "final_state" not in st.session_state:
    st.session_state.final_state = None

if run_btn and topic:
    st.session_state.final_state = None
    status_container = st.status("🤖 Agents are working...", expanded=True)
    live_placeholder = st.empty()
    
    current_state = {}
    logs_html = "" 

    try:
        Config.validate()
        
        with live_placeholder.container():
            col_logs, col_debug = st.columns([1.5, 1])
            with col_logs: st.subheader("📜 Live Agent Logs"); log_placeholder = st.empty()
            with col_debug: st.subheader("🛠️ Debug Console"); debug_placeholder = st.empty()

            for step_output in stream_research_crew(topic):
                timestamp = datetime.now().strftime("%H:%M:%S")
                for node_name, state_update in step_output.items():
                    current_state.update(state_update)
                    
                    if "status_updates" in state_update:
                        for msg in state_update["status_updates"]:
                            icon = AGENT_ICONS.get(node_name, "🤖")
                            new_entry = f"""
                            <div class="log-entry">
                                <span class="log-timestamp">{timestamp}</span>
                                <span class="agent-tag">{icon} {node_name.upper()}</span>
                                <br/>{msg}
                            </div>
                            """
                            logs_html += new_entry 
                            log_placeholder.markdown(logs_html, unsafe_allow_html=True)
                    
                    if show_debug and debug_placeholder:
                        with debug_placeholder.container(): st.json(state_update)
                    time.sleep(0.5)

        status_container.update(label="✅ Research Complete!", state="complete", expanded=False)
        live_placeholder.empty()
        st.session_state.final_state = current_state

    except Exception as e:
        st.error(f"Error: {e}")

# --- Display Final Results ---
if st.session_state.final_state:
    res = st.session_state.final_state
    
    st.divider()
    st.subheader("Final Output")
    
    tab_paper, tab_metrics, tab_full_log = st.tabs(["📄 Final Paper", "📊 Metrics", "💾 Full State Dump"])
    
    with tab_paper:
        if "final_paper" in res:
            st.markdown(res["final_paper"])
            
            st.divider()
            col_dl1, col_dl2 = st.columns(2)
            
            # Button 1: Download Markdown
            with col_dl1:
                st.download_button(
                    label="📥 Download Markdown",
                    data=res["final_paper"],
                    file_name=f"research_{topic.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            
            # Button 2: Download PDF
            with col_dl2:
                # Generate PDF only when needed
                pdf_data = generate_pdf(res["final_paper"])
                if pdf_data:
                    st.download_button(
                        label="📄 Save as PDF",
                        data=pdf_data,
                        file_name=f"research_{topic.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Could not generate PDF.")
        else:
            st.warning("No paper was generated.")

    with tab_metrics:
        col1, col2 = st.columns(2)
        confidence = res.get("confidence_score", 0.5)
        with col1:
            fig = px.pie(values=[confidence, 1.0 - confidence], names=["Confidence", "Uncertainty"], 
                         hole=0.6, color_discrete_sequence=["#00CC96", "#EF553B"], title="Agent Confidence")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.metric("Iterations", res.get("iteration_count", 0))
            st.metric("Sources Found", len(res.get('research_notes', [])))

    with tab_full_log:
        st.info("Here is the complete debug data from the run:")
        st.json(res)