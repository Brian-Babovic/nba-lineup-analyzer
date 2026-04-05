# 🏀 NBA Lineup Efficiency Analyzer

An interactive analytics dashboard for exploring five-man lineup performance across NBA teams and seasons — built to mirror the kind of rotation analysis used by real front offices.

## 📌 Project Motivation

Coaching decisions about which five players to put on the floor together are among the most impactful — and underanalyzed — strategic choices in basketball. This project surfaces lineup-level efficiency data to answer questions like:

- Which lineups generate the best net rating per team?
- How does a team's best lineup compare to the rest of the league?
- Which lineups are being over- or under-utilized relative to their performance?

## 📊 Key Metrics

| Metric | What it means |
| --- | --- |
| **Offensive Rating (ORtg)** | Points scored per 100 possessions |
| **Defensive Rating (DRtg)** | Points allowed per 100 possessions |
| **Net Rating** | ORtg minus DRtg — the core lineup quality metric |
| **Minutes Played** | Used to filter out small-sample lineups |
| **Pace** | Possessions per 48 minutes — affects how to contextualize ratings |

## 🛠️ Tech Stack

| Tool | Purpose |
| --- | --- |
| `nba_api` | Pull lineup data directly from stats.nba.com |
| `pandas` | Data cleaning and aggregation |
| `plotly` | Interactive charts |
| `streamlit` | Dashboard web app |

## 📁 Project Structure
nba-lineup-analyzer/
│
├── data/               # Cached API pulls
├── notebooks/          # Exploratory analysis (EDA)
├── app/
│   └── app.py          # Main Streamlit dashboard
├── src/
│   └── data_loader.py  # Functions to pull and clean lineup data
├── requirements.txt
└── README.md

## 🔍 Features

- Filter lineups by **team**, **season**, and **minimum minutes played**
- Rank lineups by net rating with a sortable table
- Visualize **offensive vs. defensive rating** in a scatter plot per lineup
- Compare a team's top lineup against the **league average**

## 💡 Future Enhancements

- Lineup vs. lineup matchup analysis
- Opponent-adjusted net ratings
- Clustering lineups by archetype (small-ball, traditional, etc.)