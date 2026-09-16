"""
Interactive Streamlit dashboard for the ABM simulation.

Run:
    streamlit run dashboard.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.model import SafetyModel


st.set_page_config(
    page_title="ABM Construction Safety",
    page_icon="🏗️",
    layout="wide",
)


st.title("🏗️ Agent-Based Simulation of Construction Worker Safety")
st.markdown(
    "Based on **Zhang et al. (2025, ASCE JCEM)** — "
    "reproduces the paper's key result: *~90% safety rate.*"
)

# ============================================================
# SIDEBAR — controls
# ============================================================
st.sidebar.header("⚙️ Simulation parameters")

num_workers = st.sidebar.slider(
    "Number of workers",
    min_value=20, max_value=500, value=100, step=20,
)
num_managers = st.sidebar.slider(
    "Number of managers",
    min_value=1, max_value=10, value=3, step=1,
)
steps = st.sidebar.slider(
    "Simulation days",
    min_value=20, max_value=300, value=100, step=10,
)
seed = st.sidebar.number_input(
    "Random seed", min_value=0, max_value=9999, value=42,
)

run_button = st.sidebar.button("▶️ Run simulation", type="primary")

# ============================================================
# RESULTS
# ============================================================
if run_button:
    with st.spinner(f"Running simulation: {num_workers} workers x "
                    f"{num_managers} managers x {steps} days..."):
        model = SafetyModel(
            num_workers=num_workers,
            num_managers=num_managers,
            seed=seed,
        )
        model.run(steps=steps)

    # ---- Metric cards ----
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Initial safe rate",
                f"{model.safety_rate_history[0]:.1%}")
    col2.metric("Final safe rate",
                f"{model.safety_rate_history[-1]:.1%}")
    col3.metric("Paper reference", "90.4%")
    delta = (model.safety_rate_history[-1] - 0.904) * 100
    col4.metric("Difference from paper", f"{delta:+.1f} pp")

    st.markdown("---")

    # ---- Plot 1: Safe behavior over time ----
    st.subheader("📈 Safe Behavior over Time")

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    days = np.arange(1, steps + 1)
    ax1.plot(days, [r * 100 for r in model.safety_rate_history],
             color='#007bff', linewidth=2.5)
    ax1.axhline(y=90.4, color='red', linestyle='--',
                label='Zhang et al. (2025): 90.4%')
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Safe behavior rate (%)")
    ax1.grid(alpha=0.3)
    ax1.legend()
    ax1.set_ylim(0, 105)
    st.pyplot(fig1)

    # ---- Plot 2: Worker attributes ----
    st.subheader("🧠 Worker Attributes over Time")

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(days, model.avg_SA_history,
             label="SA (awareness)", color='#28a745', linewidth=2.5)
    ax2.plot(days, model.avg_SK_history,
             label="SK (knowledge)", color='#fd7e14', linewidth=2.5)
    ax2.plot(days, model.avg_reference_point_history,
             label="A (reference point)", color='#6f42c1', linewidth=2.5)
    ax2.axhline(y=0.6, color='red', linestyle='--',
                alpha=0.5, label="Cognitive threshold (0.6)")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Average value")
    ax2.grid(alpha=0.3)
    ax2.legend()
    ax2.set_ylim(0, 1)
    st.pyplot(fig2)

    # ---- Raw data (expandable) ----
    with st.expander("🔍 View raw data"):
        st.dataframe({
            "Day": days,
            "Safe rate": [f"{r:.2%}" for r in model.safety_rate_history],
            "Avg SA": [f"{v:.3f}" for v in model.avg_SA_history],
            "Avg SK": [f"{v:.3f}" for v in model.avg_SK_history],
            "Avg A": [f"{v:.3f}" for v in model.avg_reference_point_history],
        })
else:
    st.info("👈 Set parameters in the sidebar and press **Run simulation**.")
    st.markdown(
        """
        **About the model:**

        - **Workers** decide safe vs unsafe behavior through a 3-stage
          cognitive process (SA → SK → intention).
        - **Managers** influence workers through 5 behaviors
          (ET, IR, SI, SM, HEM).
        - **CPT** (Cumulative Prospect Theory) models the decision stage.

        **Expected result:** ~90% final safe rate (matching the paper).
        """
    )
