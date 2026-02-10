# 📘 Technical Documentation: Autonomous AI Research Assistant (v2.0)

## 📑 Table of Contents
1. [System Architecture](#system-architecture)
2. [Agent Logic & Workflow](#agent-logic--workflow)
3. [State Management](#state-management)
4. [Deployment Pipelines](#deployment-pipelines)
5. [Docker & Containerization](#docker--containerization)
6. [Local Development (Dev Containers)](#local-development)
7. [Troubleshooting](#troubleshooting)

---

## 🏗 System Architecture

The application is built on a **StateGraph** architecture using `LangGraph`. Unlike linear chains, this system uses a cyclic graph where agents can loop back, self-correct, and refine their outputs based on confidence scores.

### High-Level Data Flow
1.  **User Input:** Topic enters via Streamlit UI.
2.  **State Initialization:** A `ResearchState` dictionary is created.
3.  **Graph Execution:** Nodes (Agents) process the state and pass it forward.
4.  **Streaming:** The `src.crew.stream_research_crew` generator yields real-time updates to the UI.
5.  **Termination:** The workflow ends when the **Critic** is satisfied (Confidence > 60%) or max iterations are reached.

---

## 🤖 Agent Logic & Workflow

The system is composed of **6 specialized agents** residing in `src/nodes.py`.

| Agent | Role | Input | Output |
| :--- | :--- | :--- | :--- |
| **Scout** | Domain Refinement | Raw user topic | Cleaned, specific scientific domain |
| **Planner** | Question Generation | Refined domain | 3 targeted research questions |
| **Alchemist** | Data Retrieval | Research questions | Summarized papers (ArXiv/Tavily) |
| **Designer** | Experimentation | Evidence + Questions | 3-step experimental design |
| **Critic** | Quality Control | Draft content | Confidence Score (0.0 - 1.0) |
| **Writer** | Reporting | Final State | Markdown Report |

### The "Critic" Loop
The **Critic Agent** is the gatekeeper. It evaluates the "density" and "relevance" of the gathered information.
* **If Score < 0.6:** The graph routes back to the **Scout** node to restart/refine the search (up to 3 times).
* **If Score ≥ 0.6:** The graph proceeds to the **Writer** node to finalize the paper.

---

## 🧠 State Management

The entire application state is typed and managed via `src/state.py`. This ensures data consistency across all agents.

```python
class ResearchState(TypedDict):
    domain: str                 # The active research topic
    questions: List[str]        # Generated research questions
    research_notes: List[str]   # Raw data gathered from external APIs
    hypothesis: str             # Formulated scientific hypothesis
    experiment_design: str      # Proposed methodology
    confidence_score: float     # Critic's evaluation (0.0 - 1.0)
    iteration_count: int        # Loop counter (Max 3)
    final_paper: str            # The final Markdown output
    status_updates: List[str]   # Live logs for the UI