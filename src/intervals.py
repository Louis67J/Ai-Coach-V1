import requests
from datetime import datetime, timedelta
from config import INTERVALS_API_KEY, INTERVALS_BASE_URL

def fetch_activities_last_2_years(athlete_id: int):
    """
    Récupère 24 mois d'historique Intervals (approx. 730 jours)
    """
    end = datetime.utcnow().date()
    start = end - timedelta(days=730)

    url = f"{INTERVALS_BASE_URL}/athlete/{athlete_id}/activities"

    params = {
        "start": start.isoformat(),
        "end": end.isoformat()
    }

    print(f"Fetching activities from {start} to {end}")

    response = requests.get(
        url,
        params=params,
        headers={"Authorization": f"Bearer {INTERVALS_API_KEY}"}
    )
    response.raise_for_status()

    return response.json()
