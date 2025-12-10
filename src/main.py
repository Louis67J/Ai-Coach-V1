from intervals import fetch_activities_last_2_years
from analysis import compute_profile
from coach import generate_coaching
from emailer import send_email
from discord_bot import run_discord_bot

ATHLETE_ID = 000000  # <<< mettre ton ID Intervals

def run_analysis():
    acts = fetch_activities_last_2_years(ATHLETE_ID)
    profile = compute_profile(acts)
    report = generate_coaching(profile)
    send_email("Ton rapport cycliste – AI Coach", report)

if __name__ == "__main__":
    # lance seulement l'analyse + email
    run_analysis()

    # si tu veux lancer le bot Discord en même temps :
    # run_discord_bot()
