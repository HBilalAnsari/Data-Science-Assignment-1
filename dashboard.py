#!/usr/bin/env python3
"""
NYC Congestion Pricing Review 2025
Launch with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
from PIL import Image
import os
from src.config import OUTPUT_FIGURES, DATA_PROCESSED

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NYC Congestion Review 2025",
    page_icon="🚕",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
# 🚕 NYC Congestion Pricing Review (2025)
### Visual Policy Evaluation Dashboard
*An independent analytical view of traffic, revenue & behavior*
""")

# ---------------- LOAD SUMMARY ----------------
try:
    summary_df = pd.read_csv(os.path.join(DATA_PROCESSED, 'summary_statistics.csv'))
    summary = summary_df.iloc[0]
except:
    st.error("⚠️ Required data not found. Please execute `pipeline.py` first.")
    st.stop()

# ---------------- TOP METRICS ----------------
st.markdown("## 📌 System Snapshot")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Revenue Collected", f"${summary['total_revenue']:,.0f}")
col2.metric("✅ Compliance Level", f"{summary['compliance_rate']:.1f}%")
col3.metric("👻 Ghost Trips", f"{summary['ghost_trip_count']:,.0f}")
col4.metric("🌧️ Rain Sensitivity", f"{summary['rain_elasticity']:.3f}")

st.markdown("---")

# ---------------- SECTION 1 ----------------
with st.expander("🗺️ Zone Boundary Behavior (Border Effect)", expanded=True):
    st.markdown("""
    **Objective:**  
    Examine whether riders intentionally terminate trips near congestion boundaries
    to avoid additional charges.
    """)

    img_path = os.path.join(OUTPUT_FIGURES, 'border_effect.png')
    if os.path.exists(img_path):
        st.image(Image.open(img_path), use_container_width=True)
    else:
        st.warning("Figure unavailable.")

    st.markdown("""
    **Key Observations**
    - Elevated activity near pricing boundaries
    - Sudden spikes may indicate toll avoidance behavior
    - Priority focus: zones exceeding 20% growth
    """)

# ---------------- SECTION 2 ----------------
with st.expander("🚦 Traffic Speed Comparison (Before vs After)"):
    st.markdown("**Did congestion pricing improve vehicle movement?**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ⏱️ Pre-Pricing (Q1 2024)")
        img_2024 = os.path.join(OUTPUT_FIGURES, 'speed_heatmap_2024.png')
        if os.path.exists(img_2024):
            st.image(Image.open(img_2024), use_container_width=True)

    with col2:
        st.markdown("#### ⚡ Post-Pricing (Q1 2025)")
        img_2025 = os.path.join(OUTPUT_FIGURES, 'speed_heatmap_2025.png')
        if os.path.exists(img_2025):
            st.image(Image.open(img_2025), use_container_width=True)

    st.info("Darker shades indicate improved average travel speeds during peak hours.")

# ---------------- SECTION 3 ----------------
with st.expander("💵 Driver Earnings & Tip Behavior"):
    st.markdown("""
    **Research Question:**  
    Do congestion surcharges reduce voluntary tipping?
    """)

    img_tip = os.path.join(OUTPUT_FIGURES, 'tip_vs_surcharge.png')
    if os.path.exists(img_tip):
        st.image(Image.open(img_tip), use_container_width=True)

    st.markdown("""
    **Discussion Points**
    - Is tip reduction correlated with toll increase?
    - Does this impact driver income sustainability?
    """)

    img_volume = os.path.join(OUTPUT_FIGURES, 'trip_volume_change.png')
    if os.path.exists(img_volume):
        st.image(Image.open(img_volume), use_container_width=True)

# ---------------- SECTION 4 ----------------
with st.expander("🌦️ Weather Impact on Demand"):
    st.markdown("**Assessing demand response under rainfall conditions**")

    img_rain = os.path.join(OUTPUT_FIGURES, 'rain_elasticity.png')
    if os.path.exists(img_rain):
        st.image(Image.open(img_rain), use_container_width=True)

    elasticity = summary['rain_elasticity']

    if elasticity > 0.3:
        st.success(f"High sensitivity detected ({elasticity:.3f}) → Rain boosts demand")
    elif elasticity < -0.3:
        st.error(f"Negative elasticity ({elasticity:.3f}) → Reduced demand")
    else:
        st.info(f"Low elasticity ({elasticity:.3f}) → Minimal weather influence")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "📂 Source: NYC TLC Trip Records | 🗓️ Coverage: 2024–2025 | "
    "Dashboard developed for academic analysis"
)
