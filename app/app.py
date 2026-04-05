import sys
import os

# Allow importing from src/ when running from the project root
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_or_fetch

# --- Page config ---
st.set_page_config(page_title="NBA Lineup Efficiency Analyzer", layout="wide")

# --- Sidebar ---
st.sidebar.header("Filters")

season = st.sidebar.selectbox(
    "Season",
    options=["2024-25", "2023-24", "2022-23"],
)

min_minutes = st.sidebar.slider(
    "Minimum Minutes",
    min_value=50,
    max_value=300,
    value=100,
    step=25,
)

# --- Load data ---
with st.spinner(f"Loading lineup data for {season}..."):
    df = load_or_fetch(season, min_minutes=min_minutes)

# Re-apply minutes filter in case cached CSV contains rows below the current threshold
df = df[df["minutes"] >= min_minutes].reset_index(drop=True)

# --- Team filter (populated dynamically from data) ---
teams = ["All Teams"] + sorted(df["team"].dropna().unique().tolist())
selected_team = st.sidebar.selectbox("Team", options=teams)

# --- Main area ---
st.title("NBA Lineup Efficiency Analyzer")
st.markdown(
    "**Net Rating** is a team's point differential per 100 possessions. "
    "A positive net rating means a lineup outscores opponents; negative means they get outscored."
)

# Apply team filter if a specific team is selected
if selected_team != "All Teams":
    df = df[df["team"] == selected_team]

# --- Lineup Rankings table ---
st.subheader("Lineup Rankings")

display_cols = ["team", "lineup", "minutes", "off_rtg", "def_rtg", "net_rtg"]
ranked = df[display_cols].sort_values("net_rtg", ascending=False).reset_index(drop=True)

st.dataframe(
    ranked.style.format({
        "minutes": "{:.1f}",
        "off_rtg": "{:.1f}",
        "def_rtg": "{:.1f}",
        "net_rtg": "{:.1f}",
    }).background_gradient(subset=["net_rtg"], cmap="RdYlGn"),
    use_container_width=True,
)

# --- Scatter plot ---
st.subheader("Offensive vs Defensive Rating")
st.caption("Note: Lower defensive rating is better — it means opponents score fewer points per 100 possessions.")

fig = px.scatter(
    df,
    x="off_rtg",
    y="def_rtg",
    color="net_rtg",
    hover_data=["lineup", "team"],
    color_continuous_scale="RdYlGn",  # green = high net rating (good), red = low (bad)
    labels={
        "off_rtg": "Offensive Rating",
        "def_rtg": "Defensive Rating",
        "net_rtg": "Net Rating",
    },
    title=f"Offensive vs Defensive Rating — {season}",
)

# Invert y-axis so better defensive ratings (lower values) appear at the top
fig.update_yaxes(autorange="reversed")

fig.update_layout(coloraxis_colorbar=dict(title="Net Rtg"))

st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("Data sourced from [stats.nba.com](https://www.stats.nba.com) via the `nba_api` Python library.")
