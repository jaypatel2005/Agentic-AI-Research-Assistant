import os
import warnings
import operator
import re
import arxiv
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END

load_dotenv()
warnings.filterwarnings("ignore", category=UserWarning)

class ResearchState(TypedDict):
    domain: str
    questions: List[str]
    research_notes: Annotated[List[str], operator.add]
    hypothesis: str
    experiment_design: str
    confidence_score: float
    iteration_count: int
    final_paper: str
    status_updates: Annotated[List[str], operator.add]

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

search_tool = TavilySearch(max_results=3)

def domain_scout(state: ResearchState):
    """
    Uses user-provided domain on first iteration.
    On refinement loops, slightly sharpens the domain.
    """

    iteration = state.get("iteration_count", 0)
    base_domain = state.get("domain", "").strip()

    if iteration == 0 and base_domain:
        refined_domain = base_domain
        msg = f"Using user-provided domain: {refined_domain}"

    else:
        query = f"Refine and narrow this scientific topic: {base_domain}"
        res = llm.invoke(query)
        refined_domain = re.sub(r'[^a-zA-Z0-9\s]', '', res.content).strip()
        refined_domain = " ".join(refined_domain.split()[:5]) or base_domain
        msg = f"Refined domain to: {refined_domain}"

    return {
        "domain": refined_domain,
        "iteration_count": iteration + 1,
        "status_updates": [msg]
    }


def question_generator(state: ResearchState):
    prompt = (
        f"Generate exactly 3 concise research questions "
        f"for the domain: {state['domain']}. "
        f"Return each question on a new line."
    )
    res = llm.invoke(prompt)

    questions = [
        q.strip("-• ").strip()
        for q in res.content.split("\n")
        if q.strip()
    ]

    return {
        "questions": questions,
        "status_updates": ["Generated research questions."]
    }


def data_alchemist(state: ResearchState):
    search_term = state["domain"]

    client = arxiv.Client()
    search = arxiv.Search(query=search_term[:50], max_results=2)

    notes = []
    try:
        for result in client.results(search):
            notes.append(
                f"Title: {result.title}\n"
                f"Summary: {result.summary[:200]}..."
            )
    except Exception:
        notes.append("No relevant arXiv papers found; using conceptual grounding.")

    return {
        "research_notes": notes,
        "status_updates": [f"Collected {len(notes)} evidence sources."]
    }


def experiment_designer(state: ResearchState):
    prompt = (
        f"Based on the following research questions:\n"
        f"{state['questions']}\n\n"
        f"Design a simple 3-step experimental or validation approach."
    )
    res = llm.invoke(prompt)

    return {
        "experiment_design": res.content.strip(),
        "status_updates": ["Designed experimental methodology."]
    }


def critic_agent(state: ResearchState):
    """
    Deterministic, bounded confidence score.
    """
    iteration = state["iteration_count"]
    score = min(1.0, 0.4 + iteration * 0.15)

    return {
        "confidence_score": score,
        "status_updates": [f"Critic confidence score: {score * 100:.0f}%"]
    }


def writer_agent(state: ResearchState):
    paper = f"""
# Scientific Research Brief: {state['domain']}

## 1. Research Questions
{chr(10).join(f"- {q}" for q in state['questions'])}

## 2. Evidence Review
{chr(10).join(state['research_notes'])}

## 3. Experimental Design
{state['experiment_design']}

---
**Confidence Score:** {state['confidence_score'] * 100:.0f}%  
**Iterations:** {state['iteration_count']}
"""

    return {
        "final_paper": paper.strip(),
        "status_updates": ["Final research paper generated."]
    }

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
    if state["confidence_score"] < 0.6 and state["iteration_count"] < 3:
        return "scout"
    return "writer"

workflow.add_conditional_edges(
    "critic",
    should_continue,
    {
        "scout": "scout",
        "writer": "writer"
    }
)

workflow.add_edge("writer", END)

app = workflow.compile()
