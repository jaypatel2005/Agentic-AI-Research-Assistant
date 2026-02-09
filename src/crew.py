from langgraph.graph import StateGraph, END
from src.state import ResearchState
from src.nodes import (
    domain_scout, question_generator, data_alchemist, 
    experiment_designer, critic_agent, writer_agent
)

# --- Build the Graph ---
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
    {"scout": "scout", "writer": "writer"}
)
workflow.add_edge("writer", END)

app_graph = workflow.compile()

# --- The Streaming Function ---
def stream_research_crew(topic: str):
    """
    Generator that yields updates from the agents live.
    """
    initial_state = {
        "domain": topic,
        "iteration_count": 0,
        "questions": [],
        "research_notes": [],
        "status_updates": [],
        "confidence_score": 0.0,
        "final_paper": ""
    }
    
    # Stream the updates!
    for output in app_graph.stream(initial_state):
        yield output