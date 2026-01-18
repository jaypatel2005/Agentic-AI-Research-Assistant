# 🔬 Autonomous AI Research Assistant (v1.0)

---

## 🚀 Project Overview

The **Autonomous AI Research Assistant** is a fully agentic, multi-agent research system designed to operate with **zero human intervention after initialization**. The system autonomously discovers formulates original research questions, gathers and cleans data from public sources, and produces a structured, peer-review-style **mini research paper**.

Unlike traditional RAG pipelines or single-agent chains, this project demonstrates **true agency**: long-horizon planning, dynamic tool use, iterative self-criticism, confidence-based refusal, and persistent memory across reasoning cycles.

**Live Demo(for prompt "one hyper-specific emerging scientific breakthrough post-2024"):**  
https://agentic-ai-research-assistant-8zzto5fd99bpayvgmvfysq.streamlit.app/

---

## 🏗️ Agentic Architecture

The system is implemented using a **StateGraph architecture (LangGraph)** and consists of multiple specialized agents collaborating in a cyclic, self-correcting loop:

- **Domain Scout Agent**  
  Identifies emerging scientific domains (post-January 2024) using real-time search, detecting signals such as patent surges and newly formed ArXiv categories.

- **Question Generator Agent**  
  Produces 3–5 non-trivial research questions, scored for novelty, feasibility, and scientific relevance.

- **Data Alchemist Agent**  
  Interfaces with the ArXiv API to retrieve, clean, normalize, and preprocess heterogeneous academic data sources.

- **Experiment Designer Agent**  
  Formulates hypotheses and proposes structured, three-step experimental methodologies grounded in retrieved evidence.

- **Critic Agent**  
  Performs adversarial evaluation of assumptions, data quality, and methodology. If the confidence score drops below 60%, the system is forced into re-planning (up to five iterations).

- **Writer Agent**  
  Synthesizes validated outputs into a structured Markdown research paper, including automated *Limitations* and *Confidence* sections.

---

## 🧪 Playground Mode

A dedicated interactive **Playground Mode** is included (`playground.py`) for experimentation and inspection.

- **Manual Trigger**  
  Provide a specific scientific topic or allow the system to select one autonomously.

- **Real-Time Transparency**  
  Observe internal agent reasoning, execution logs, and status updates during runtime.

- **Graceful Failure Handling**  
  Robust exception management for API quota limits, null values, and partial data availability—ensuring UI stability under failure conditions.

---

## 🛠️ Technical Stack (Free-Tier Only)

This project strictly adheres to a **zero-cost deployment constraint**:

- **LLM Backbone:** Groq (Llama-3.3-70B) for high-throughput, open-weights inference  
- **Agent Orchestration:** LangGraph (cyclic, state-driven multi-agent workflows)  
- **Search Engine:** Tavily API (agent-optimized semantic search)  
- **Data Acquisition:** ArXiv API client with regex-based cleaning and LLM parsing  
- **Visualization:** Interactive Plotly dashboards  
- **Deployment:** Dockerized Streamlit application  

---

## 📦 Setup & Execution

### 1. Prerequisites

- Python **3.10+**
- Groq API key
- Tavily API key

---

### 2. Installation
```bash
git clone https://github.com/jaypatel2005/Agentic-AI-Research-Assistant.git
cd Agentic-AI-Research-Assistant
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root:

```plaintext
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### 4. Run Locally

# Run the main research dashboard
```bash
streamlit run main.py
```

# Run the Playground mode
```bash
streamlit run playground.py
```

---

## 📈 Core Innovations & Challenges

Closed-Loop Self-Correction
A confidence-driven feedback mechanism forces re-planning whenever evidence is weak, contradictory, or incomplete.

Uncertainty Quantification
Each research cycle produces a confidence score (0–100%). If validation remains below 60% after five iterations, the system refuses to generate a paper.

Context Optimization Under Constraints
Long-form scientific documents are processed within free-tier token limits using custom summarization, chunking, and data-cleaning pipelines.

---

## 📄 Documentation

For detailed technical documentation—including deployment pipelines, JSON schemas, and multi-stage Dockerfile design—refer to DOCUMENTATION.md.

## Author: Jay Patel
## Status: Actively maintained and extensible
