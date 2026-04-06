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
    options=["2025-26", "2024-25", "2023-24", "2022-23"],
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
    df = load_or_fetch(season)

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

# Preserve the full unfiltered DataFrame before applying the team filter
# so we can calculate league-wide averages for comparison
df_all = df.copy()

# Apply team filter if a specific team is selected
if selected_team != "All Teams":
    df = df[df["team"] == selected_team]

# --- Team summary metrics (only shown when a specific team is selected) ---
if selected_team != "All Teams":
    best_row = df.loc[df["net_rtg"].idxmax()]
    best_net_rtg = round(best_row["net_rtg"], 1)
    best_minutes = round(best_row["minutes"], 1)
    best_lineup_name = best_row["lineup"]

    st.subheader(f"📊 {selected_team} Lineup Summary")
    col1, col2 = st.columns(2)
    col1.metric("Best Lineup Net Rtg", best_net_rtg)
    col2.metric("Minutes Played (Best Lineup)", best_minutes)
    st.caption(f"Best Lineup: {best_lineup_name}")

# --- Lineup Rankings table ---
st.subheader("Lineup Rankings")

display_cols = ["team", "lineup", "minutes", "off_rtg", "def_rtg", "net_rtg"]
ranked = df[display_cols].sort_values("net_rtg", ascending=False).reset_index(drop=True)

def color_net_rtg(val):
    if val > 0:
        intensity = min(val / 40, 1.0)
        g = int(100 + 155 * intensity)
        return f"background-color: rgb(0, {g}, 60); color: white"
    elif val < 0:
        intensity = min(abs(val) / 40, 1.0)
        r = int(100 + 155 * intensity)
        return f"background-color: rgb({r}, 0, 30); color: white"
    else:
        return "background-color: rgb(80, 80, 80); color: white"

st.dataframe(
    ranked.style.format({
        "minutes": "{:.1f}",
        "off_rtg": "{:.1f}",
        "def_rtg": "{:.1f}",
        "net_rtg": "{:.1f}",
    }).map(color_net_rtg, subset=["net_rtg"]),
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
