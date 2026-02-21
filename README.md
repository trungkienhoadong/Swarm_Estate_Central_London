# Swarm Estate: Autonomous AI Agents for PCL Real Estate

> Bringing Quantitative Finance logic to Prime Central London (PCL) property acquisition.

![Swarm Estate Architecture](https://img.shields.io/badge/Status-Prototype-blue) ![Python](https://img.shields.io/badge/Python-3.11-yellow) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B) ![AI](https://img.shields.io/badge/AI-Gemini%20%7C%20Dust-purple)

## The Problem
Institutional real estate investment in Prime Central London is traditionally slow, relying on manual analysis and static reports. By the time a high-yield, low-risk asset is identified, the market has already moved.

## Our Solution
Swarm Estate is an autonomous algorithmic engine that treats real estate acquisition like high-frequency quantitative trading. Instead of manual screening, we deploy a "swarm" of AI agents to continuously scan, filter, and lock onto properties that meet strict, dynamically updated risk-reward thresholds.

## Core Architecture & Tech Stack
The system operates in a seamless pipeline, minimizing human latency:

1. **The Oracle (Dust AI - RAG):** Ingests live institutional reports (e.g., Savills Autumn 2025) to extract current market baselines (Yield floors, Risk caps) for specific PCL postcodes (W11, W2, NW8).
2. **The Engine (Python + NumPy):** Generates a multi-dimensional spatial simulation. Properties are treated as mathematical vectors.
3. **The Swarm (Plotly + Streamlit):** Three tiers of autonomous agents interact with the dataset:
   * **Scouts:** Survey the entire data landscape.
   * **Shield Veto:** Instantly eliminate properties exceeding the Composite Risk Index (Market, Policy, ESG).
   * **Hunters:** Lock onto the surviving assets that exceed the Target Yield Threshold.
4. **The Brain (Google Gemini - DeepMind):** Performs rapid qualitative analysis on the "Hunted" assets to confirm the asymmetrical risk-reward profile.
5. **The Executor (CodeWords + FastAPI):** Triggers an automated webhook, formatting the AI's analysis and instantly emailing the Chief Investment Officer (CIO) for final acquisition sign-off.

## The Philosophy: Why Swarms?
Rather than relying on a single, monolithic AI to make one slow decision, we utilize swarm intelligence logic. By breaking down the evaluation process into specialized, lightweight agents, the system can filter thousands of data points in real-time. It is a fundamental data structure approach: pruning the search tree aggressively before applying heavy computational analysis (LLMs) only to the absolute best candidates.

## How to Run (Local Development)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/swarm-estate.git](https://github.com/your-username/swarm-estate.git)
   cd swarm-estate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Ensure you have your Google Gemini API key configured in a `.streamlit/secrets.toml` file or as an environment variable.

4. **Launch the Swarm:**
   ```bash
   streamlit run app.py
   ```

## Future Roadmap
While currently a Hackathon prototype, the architecture is designed for scalability. Future iterations will include direct API integrations with Rightmove/Zoopla for live market data ingestion and smart-contract execution for automated escrow funding.
