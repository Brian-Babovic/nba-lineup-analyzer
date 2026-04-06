import os
import pandas as pd
from nba_api.stats.endpoints import leaguedashlineups


def get_lineup_data(season):
    """
    Fetch 5-man lineup data from the NBA API for a given season,
    clean it up, filter it, and save it to a CSV.

    Args:
        season (str): Season string in 'YYYY-YY' format, e.g. '2023-24'
        min_minutes (int): Minimum minutes played to include a lineup (default 100)

    Returns:
        pd.DataFrame: Filtered and cleaned lineup data
    """

    # Hit the leaguedashlineups endpoint for 5-man lineups
    lineup_data = leaguedashlineups.LeagueDashLineups(
        season=season,
        measure_type_detailed_defense="Advanced",
        per_mode_detailed="Per100Possessions",
        group_quantity=5,
    )

    # Convert the first (and only) result set to a DataFrame
    df = lineup_data.get_data_frames()[0]

    # Rename columns to more readable names
    df = df.rename(columns={
        "GROUP_NAME": "lineup",
        "MIN": "minutes",
        "OFF_RATING": "off_rtg",
        "DEF_RATING": "def_rtg",
        "NET_RATING": "net_rtg",
        "TEAM_ABBREVIATION": "team",
    })

    # Convert minutes and rating columns to numeric, coercing any bad values to NaN
    for col in ["minutes", "off_rtg", "def_rtg", "net_rtg"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Save the result to a CSV in the data/ directory
    output_path = f"data/lineups_{season}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} lineups to {output_path}")

    return df


def load_or_fetch(season):
    """
    Load lineup data from a cached CSV if it exists, otherwise fetch
    it from the NBA API and save it.

    Args:
        season (str): Season string in 'YYYY-YY' format, e.g. '2023-24'

    Returns:
        pd.DataFrame: Lineup data for the given season
    """

    csv_path = f"data/lineups_{season}.csv"

    if os.path.exists(csv_path):
        # Cache hit — load from disk instead of calling the API
        print(f"Loading cached data from {csv_path}")
        return pd.read_csv(csv_path)
    else:
        # Cache miss — fetch from the API and save
        print(f"No cached data found for {season}, fetching from NBA API...")
        return get_lineup_data(season)
