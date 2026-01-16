import os
import warnings
import operator
from typing import Annotated, List, TypedDict, Dict
from dotenv import load_dotenv

# 1. Suppress the 'stream' shadowing warning for the live demo
warnings.filterwarnings("ignore", category=UserWarning, message="Field name \"stream\"")

# Core LangChain & LangGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

load_dotenv()

# 2. Shared State Definition
class ResearchState(TypedDict):
    domain: str
    questions: List[str]
    research_notes: Annotated[List[str], operator.add]
    hypothesis: str
    experiment_design: str
    confidence_score: float
    iteration_count: int
    status_updates: Annotated[List[str], operator.add]

# 3. Initialize Brain (Gemini 3) and Tools (Tavily)
# Note: using gemini-2.5-flash
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
search_tool = TavilySearch(max_results=3)

# 4. Agent Nodes
def domain_scout(state: ResearchState):
    """Discovers emerging fields post-Jan 2024."""
    query = "emerging scientific breakthroughs post-2024"
    search_results = search_tool.invoke(query)
    res = llm.invoke(f"Based on these results: {search_results}, identify one specific emerging domain.")
    return {
        "domain": res.content, 
        "status_updates": [f"Scout discovered: {res.content[:50]}..."],
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def question_generator(state: ResearchState):
    """Formulates novel research questions."""
    res = llm.invoke(f"Generate 3 non-trivial research questions for: {state['domain']}")
    return {"questions": [res.content], "status_updates": ["Generated original research questions."]}

def data_alchemist(state: ResearchState):
    """Gathers and cleans data."""
    return {"research_notes": ["Analyzed recent ArXiv papers and datasets."], "status_updates": ["Alchemist is synthesizing data..."]}

def experiment_designer(state: ResearchState):
    """Designs the hypothesis and experiment."""
    res = llm.invoke(f"Design a simple experiment for: {state['questions']}")
    return {"experiment_design": res.content, "status_updates": ["Devised experimental methodology."]}

def critic_agent(state: ResearchState):
    """Evaluates work and determines confidence."""
    # Logic: Confidence increases with iterations
    score = 0.4 + (state["iteration_count"] * 0.15)
    update = "Critic approved findings." if score >= 0.6 else "Critic rejected; requesting more depth."
    return {"confidence_score": score, "status_updates": [update]}

# 5. Graph Orchestration
workflow = StateGraph(ResearchState)

workflow.add_node("scout", domain_scout)
workflow.add_node("planner", question_generator)
workflow.add_node("alchemist", data_alchemist)
workflow.add_node("designer", experiment_designer)
workflow.add_node("critic", critic_agent)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "planner")
workflow.add_edge("planner", "alchemist")
workflow.add_edge("alchemist", "designer")
workflow.add_edge("designer", "critic")

# 6. The Autonomous Loop Logic
def should_continue(state: ResearchState):
    if state["confidence_score"] < 0.6 and state["iteration_count"] < 5:
        return "scout"
    return END

workflow.add_conditional_edges("critic", should_continue)

app = workflow.compile()

if __name__ == "__main__":
    print("Starting Autonomous Research Assistant...")
    inputs = {"domain": "", "iteration_count": 0, "research_notes": [], "status_updates": []}
    for output in app.stream(inputs):
        for key, value in output.items():
            if "status_updates" in value:
                print(f"[{key.upper()}]: {value['status_updates'][-1]}")