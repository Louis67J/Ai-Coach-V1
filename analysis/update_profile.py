# analysis/update_profile.py
"""
Script to fetch activities (24mo) and update athlete_profile.json
Utiliser depuis main.py ou GitHub Actions.
"""
import os
import json
from intervals import fetch_activities_last_2_years
from profile_utils import build_profile_from_activities, save_profile, load_profile

ATHLETE_ID = int(os.getenv("ATHLETE_ID", "0"))  # mettre 0/ton id via secret

def update_profile():
    activities = fetch_activities_last_2_years(ATHLETE_ID)
    profile = build_profile_from_activities(activities)
    save_profile(profile)
    return profile

if __name__ == "__main__":
    print("Updating profile...")
    p = update_profile()
    print("Saved profile with keys:", list(p.keys()))
