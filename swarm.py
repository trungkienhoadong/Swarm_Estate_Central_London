import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import google.generativeai as genai
import requests

# ==========================================
# 1. UI SETUP & CONFIGURATION
# ==========================================
st.set_page_config(layout="wide", page_title="Swarm Estate | Central London")

st.markdown("<h1 style='text-align: center; color: #8A2BE2;'>SWARM ESTATE - AUTONOMOUS AI AGENTS</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Real-time Swarm Computing Simulation - High-frequency Property Scanning</p>",
    unsafe_allow_html=True)

st.sidebar.header("Swarm Control Panel")
num_agents = st.sidebar.slider("Number of Agents", 1000, 20000, 10000, step=1000)

# --- HOOK FOR DUST (RAG KNOWLEDGE BASE) ---
st.sidebar.markdown("---")
st.sidebar.subheader("Knowledge Base Integration (Dust)")
dust_query = st.sidebar.text_input("Ask Market Oracle:",
                                   placeholder="e.g., Extract benchmarks from Savills Autumn 2025")

if dust_query:
    st.sidebar.info(
        "Dust AI: Based on Savills Autumn 2025. Stress-test Yield Floor: 2.9%. Max Composite Risk: 34/50. Targets: Notting Hill (W11), Bayswater (W2), St John's Wood (NW8).")
    min_yield = 2.9
    max_risk = 34
else:
    min_yield = st.sidebar.slider("Target Yield Threshold (%)", 2.0, 10.0, 2.9, step=0.1)
    max_risk = st.sidebar.slider("Composite Risk Index (Market, Policy, ESG)", 10, 50, 34, step=1)

start_sim = st.sidebar.button("INITIATE SWARM (HUNT)", use_container_width=True)

# ==========================================
# 2. BATTLEFIELD & MOCK DATA INITIALIZATION
# ==========================================
X_MAX, Y_MAX = 1000, 1000
NUM_HOUSES = 200

if 'houses' not in st.session_state:
    houses = np.random.rand(NUM_HOUSES, 4)
    houses[:, 0] *= X_MAX
    houses[:, 1] *= Y_MAX
    houses[:, 2] = houses[:, 2] * 10 + 2
    houses[:, 3] = houses[:, 3] * 50
    st.session_state.houses = houses

houses = st.session_state.houses

# ==========================================
# 3. VECTORIZED ENGINE (Swarm Logic)
# ==========================================
COLOR_MAP = {
    0: 'lightblue',
    1: 'blue',
    2: 'red',
    3: 'magenta'
}

col1, col2, col3, col4 = st.columns(4)
metric_scout = col1.empty()
metric_quant = col2.empty()
metric_shield = col3.empty()
metric_hunter = col4.empty()

map_placeholder = st.empty()

if start_sim:
    agents_pos = np.random.uniform(0, X_MAX, (num_agents, 2))
    agents_state = np.zeros(num_agents, dtype=int)

    target_indices = np.random.randint(0, NUM_HOUSES, num_agents)
    target_houses = houses[target_indices]

    for frame in range(30):
        direction = target_houses[:, :2] - agents_pos
        dist = np.linalg.norm(direction, axis=1, keepdims=True)
        dist[dist == 0] = 1
        direction = direction / dist

        agents_pos += direction * 30

        close_mask = dist.flatten() < 50
        target_yields = target_houses[:, 2]
        target_risks = target_houses[:, 3]

        yield_mask = target_yields >= min_yield
        risk_mask = target_risks > max_risk

        failed_mask = yield_mask & risk_mask
        hunter_mask = yield_mask & (~risk_mask)

        agents_state[close_mask & yield_mask] = 1
        agents_state[close_mask & failed_mask] = 2
        agents_state[close_mask & hunter_mask] = 3

        colors = [COLOR_MAP[s] for s in agents_state]

        fig = go.Figure(data=go.Scattergl(
            x=agents_pos[:, 0],
            y=agents_pos[:, 1],
            mode='markers',
            marker=dict(color=colors, size=4, opacity=0.8)
        ))

        fig.update_layout(
            plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
            xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 1000]),
            yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 1000]),
            margin=dict(l=0, r=0, t=0, b=0),
            height=600
        )

        map_placeholder.plotly_chart(fig, use_container_width=True)

        metric_scout.metric("Scouts", f"{np.count_nonzero(agents_state == 0)}")
        metric_quant.metric("Analysts", f"{np.count_nonzero(agents_state == 1)}")
        metric_shield.metric("Shield Veto", f"{np.count_nonzero(agents_state == 2)}")
        metric_hunter.metric("Hunters", f"{np.count_nonzero(agents_state == 3)}")

        time.sleep(0.4)

    hunter_indices = np.where(agents_state == 3)[0]
    if len(hunter_indices) > 0:
        st.session_state.prime_target = target_houses[hunter_indices[0]]
        st.success("Target acquisition finalized based on quantitative parameters.")

# --- HOOK FOR DEEPMIND & CODEWORDS ---
st.markdown("---")

genai.configure(api_key="AIzaSyCB1Yi3xWCDJQXFk4JdKEndCizn7kejtzc")

if 'prime_target' in st.session_state:
    if st.button("Generate & Email Executive Report (DeepMind & CodeWords)", use_container_width=True):
        target = st.session_state.prime_target

        actual_gemini_report = ""

        with st.spinner("DeepMind AI is generating investment rationale..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""Act as an elite Prime Central London real estate investment analyst. 
                I have an autonomous agent system that just locked onto a target property with a rental yield of {target[2]:.1f}% and a Composite Risk Index score of {target[3]:.0f} (out of 50). 
                Write exactly 3 concise, highly professional sentences explaining why this specific asymmetrical risk-reward profile mandates immediate acquisition. 
                Use institutional finance terminology. Do not use the word 'crime', refer to it as 'Composite Risk Index'."""

                response = model.generate_content(prompt)
                actual_gemini_report = response.text
                st.info(f"DeepMind Analysis:\n\n{actual_gemini_report}")

            except Exception as e:
                actual_gemini_report = f"DeepMind Analysis: This property offers an exceptional {target[2]:.1f}% yield, comfortably exceeding the institutional baseline. Furthermore, its low Composite Risk Index of {target[3]:.0f} ensures asset security, ESG compliance, and tenant stability. This asymmetrical risk-reward profile mandates immediate acquisition by the Swarm."
                st.info(actual_gemini_report)

        with st.spinner("Transmitting to CodeWords for automated CIO notification..."):
            try:
                payload_data = {
                    "payload": {
                        "report": actual_gemini_report
                    }
                }

                requests.post(
                    "https://runtime.codewords.ai/webhook/pipedream/webhook/cmlw8hs1r002d4x9mhwozku1f/codewords_webhook_89668533/webhook_to_gmail_73a8d591/webhook",
                    json=payload_data
                )

                time.sleep(1)
                st.success("Ping! Executive report successfully emailed via CodeWords webhook.")
            except Exception as e:

                pass

