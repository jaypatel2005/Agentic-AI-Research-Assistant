🔬 Autonomous AI Research Assistant (v1.0)
Agentic Scientific Discovery for Emerging Domains (Post-2024)
🚀 Project Overview
[cite_start]This system is a fully autonomous, multi-agent AI designed to operate with zero human intervention after startup. [cite_start]It discovers emerging scientific breakthroughs (post-2024), formulates original research questions, gathers/cleans data from public APIs, and generates a peer-reviewed "mini-research paper".   

[cite_start]This project demonstrates true agency—planning, tool use, self-criticism, and memory—avoiding the limitations of RAG-only or single-agent chains.   

[cite_start]

Live Application URL: (https://agentic-ai-research-assistant-8zzto5fd99bpayvgmvfysq.streamlit.app/)    

🏗️ Agentic Architecture
[cite_start]The system utilizes a StateGraph architecture (LangGraph) with 5+ specialized agents collaborating in a cyclic loop.   

[cite_start]

Domain Scout Agent: Discovers emerging fields post-Jan 2024 using real-time search (Tavily) to find "patent spikes" and "new ArXiv categories".   

[cite_start]

Question Generator Agent: Creates 3-5 non-trivial research questions rated for novelty and feasibility.   

[cite_start]

Data Alchemist Agent: Interfaces with the ArXiv API to find, clean, and process disparate data sources.   

[cite_start]

Experiment Designer Agent: Proposes hypotheses and devises 3-step experimental methodologies based on retrieved data.   

[cite_start]

Critic Agent: Ruthlessly attacks methodology and assumptions, forcing iteration (up to 5 cycles) if the confidence score is below 60%.   

[cite_start]

Writer Agent: Compiles all findings into a structured Markdown paper with automated "Limitations" sections.   

🧪 Playground
I have included a dedicated Playground Mode (playground.py).

[cite_start]

Manual Trigger: Paste a specific scientific topic or click "Start" to let the agent choose autonomously.   

[cite_start]

Real-time Interaction: View the "internal monologue" of the agents, including real-time status updates and agent humor/logs.   

Graceful Failures: Custom error handling for API quotas and "None" value fallbacks to ensure the UI remains professional even during rate-limiting events.

🛠️ Technical Stack (Free-Tier Only)
[cite_start]This project strictly adheres to the "zero-cost" requirement:   

[cite_start]

LLM Backbone: Groq (Llama-3.3-70B) for high-speed, open-weights inference.   

[cite_start]

Orchestration: LangGraph (for complex, cyclic agent loops).   

[cite_start]

Search Engine: Tavily API (Search-optimized for AI Agents).   

[cite_start]

Data Acquisition: ArXiv API Client (Cleaned via Regex & Llama-3 parsing).   

[cite_start]

Visualization: Interactive Plotly Dashboards.   

[cite_start]

Deployment: Dockerized Streamlit UI.   

📦 Setup & Execution
1. Prerequisites
Python 3.10+

Groq API Key

Tavily API Key

2. Installation
Bash

git clone https://github.com/jaypatel2005/Agentic-AI-Research-Assistant.git
cd Agentic-AI-Research-Assistant
pip install -r requirements.txt
3. Environment Variables
Create a .env file in the root directory:

Plaintext

GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
4. Run Locally
Bash

# To run the main research dashboard
streamlit run main.py

# To run the Recruiter Playground
streamlit run playground.py
📈 Core Innovations & Challenges
[cite_start]

Closed-Loop Self-Correction: The Critic agent manages a confidence threshold; if data is ambiguous or conflicting, it forces a re-plan by the Scout.   

[cite_start]

Uncertainty Quantification: Every research cycle includes a confidence score (0-100%); the agent will "refuse" to generate a paper if verification remains below 60% after 5 cycles.   

[cite_start]

Context Optimization: Successfully managed long-context scientific papers within free-tier token limits by implementing custom summarization and cleaning protocols.   

📄 Documentation
[cite_start]For detailed information on the deployment pipeline, JSON schemas, and multi-stage Dockerfile logic, please refer to the DOCUMENTATION.md file.