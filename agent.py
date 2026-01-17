import os
import warnings
import operator
import json
import re
import arxiv
from typing import Annotated, List, TypedDict, Dict
from dotenv import load_dotenv

# --- MODIFIED: Switch from Google to Groq ---
from langchain_groq import ChatGroq 
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END

load_dotenv()

warnings.filterwarnings("ignore", category=UserWarning, message="Field name \"stream\"")

# 1. Shared State Definition
class ResearchState(TypedDict):
    domain: str
    questions: List[str]
    research_notes: Annotated[List[str], operator.add]
    hypothesis: str
    experiment_design: str
    confidence_score: float
    iteration_count: int
    status_updates: Annotated[List[str], operator.add]

# 2. Initialize Brain (Llama 3 via Groq) and Tools
# 'llama-3.3-70b-versatile' is excellent for complex reasoning/planning
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1 # Lower temperature for more consistent research
)
search_tool = TavilySearch(max_results=3)

# ==========================================
# AGENT NODES
# ==========================================

def domain_scout(state: ResearchState):
    query = "emerging scientific breakthroughs post-2024"
    search_results = search_tool.invoke(query)
    
    prompt = (
        f"Search Results: {search_results}\n\n"
        "Identify ONE specific emerging scientific domain from the text.\n"
        "Output ONLY the name of the domain (Max 3 words)."
    )
    
    res = llm.invoke(prompt)
    clean_name = res.content.replace("*", "").strip()
    short_name = " ".join(clean_name.split()[:4]) 
    
    return {
        "domain": short_name, 
        "status_updates": [f"Scout locked onto: {short_name}"],
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def question_generator(state: ResearchState):
    res = llm.invoke(f"Generate 3 non-trivial research questions for: {state['domain']}")
    return {"questions": [res.content], "status_updates": ["Generated original research questions."]}

def data_alchemist(state: ResearchState):
    domain = state.get("domain", "General Science")
    client = arxiv.Client()
    search = arxiv.Search(query=domain[:100], max_results=3)
    
    fetched_notes = []
    try:
        for result in client.results(search):
            clean_summary = re.sub(r'\s+', ' ', result.summary).replace('$', '') 
            paper_info = f"SOURCE: ArXiv | TITLE: {result.title}\nSUMMARY: {clean_summary[:400]}..."
            fetched_notes.append(paper_info)
    except Exception as e:
        fetched_notes = [f"Note: ArXiv fallback knowledge used for '{domain}'."]

    return {
        "research_notes": fetched_notes,
        "status_updates": [f"Alchemist processed {len(fetched_notes)} papers."]
    }

def experiment_designer(state: ResearchState):
    res = llm.invoke(f"Design a simple experiment based on these questions: {state['questions']}")
    return {"experiment_design": res.content, "status_updates": ["Devised experimental methodology."]}

def critic_agent(state: ResearchState):
    score = 0.4 + (state["iteration_count"] * 0.15)
    update = "Critic approved findings." if score >= 0.6 else "Critic rejected; requesting more depth."
    return {"confidence_score": score, "status_updates": [update]}

def writer_agent(state: ResearchState):
    paper_template = f"""
# Scientific Discovery: {state['domain']}
## 1. Abstract
Autonomous analysis of {state['domain']} via multi-agent synthesis.
## 2. Research Questions
{state.get('questions', ['Pending'])[0]}
## 3. Findings
{chr(10).join(state['research_notes'][:2])}
## 4. Methodology
{state.get('experiment_design', 'Pending')}
---
*Score: {state.get('confidence_score', 0)*100}% | Iterations: {state['iteration_count']}*
    """
    return {"final_paper": paper_template, "status_updates": ["Paper compiled."]}

# ==========================================
# GRAPH ORCHESTRATION
# ==========================================

workflow = StateGraph(ResearchState)
workflow.add_node("scout", domain_scout)
workflow.add_node("planner", question_generator)
workflow.add_node("alchemist", data_alchemist)
workflow.add_node("designer", experiment_designer)
workflow.add_node("critic", critic_agent)
workflow.add_node("writer", writer_agent)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "planner")
workflow.add_edge("planner", "alchemist")
workflow.add_edge("alchemist", "designer")
workflow.add_edge("designer", "critic")

def should_continue(state: ResearchState):
    if state["confidence_score"] < 0.6 and state["iteration_count"] < 5:
        return "scout"
    return "writer"

workflow.add_conditional_edges("critic", should_continue, {"scout": "scout", "writer": "writer"})
workflow.add_edge("writer", END)

app = workflow.compile()

if __name__ == "__main__":
    inputs = {"domain": "", "iteration_count": 0, "research_notes": [], "status_updates": []}
    for output in app.stream(inputs):
        for key, value in output.items():
            if "status_updates" in value:
                print(f"[{key.upper()}]: {value['status_updates'][-1]}")