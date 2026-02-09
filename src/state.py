import operator
from typing import Annotated, List, TypedDict

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