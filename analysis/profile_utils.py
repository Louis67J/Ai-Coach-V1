# analysis/profile_utils.py
import json
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

OUT = Path(__file__).resolve().parent.parent / "analysis_data"
OUT.mkdir(exist_ok=True, parents=True)
PROFILE_PATH = OUT / "athlete_profile.json"

def save_profile(d):
    PROFILE_PATH.write_text(json.dumps(d, indent=2, ensure_ascii=False))

def load_profile():
    if PROFILE_PATH.exists():
        return json.loads(PROFILE_PATH.read_text())
    return {}

def build_profile_from_activities(activities):
    """
    activities: list of interval.icu activity dicts
    Retourne un profile résumé (json-serializable)
    """
    # basic aggregates
    total_s = sum(a.get('moving_time',0) for a in activities)
    total_h = round(total_s/3600,1)
    total_dist_km = round(sum(a.get('distance',0) for a in activities)/1000,1)
    # compute TSS per day if available
    tss_list = []
    for a in activities:
        tss = a.get('icu_training_load') or a.get('tss') or 0
        start = a.get('start_date_local') or a.get('start_date')
        tss_list.append((start, tss))
    df = pd.DataFrame(tss_list, columns=['date','tss'])
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        daily = df.groupby(df['date'].dt.date)['tss'].sum()
        avg_weekly_tss = round(daily.resample("W").sum().mean(),1) if not daily.empty else 0
    else:
        avg_weekly_tss = 0

    # power bests stub: try to take from activity fields if present
    power_bests = {}
    for a in activities:
        if a.get('icu_pm_p_max'):
            # skip: example
            pass
    # simple CPs - try derive from activity entries 'pm' fields if present
    # fallback: empty
    profile = {
        "build_date": datetime.utcnow().isoformat(),
        "total_hours_24mo": total_h,
        "total_distance_km_24mo": total_dist_km,
        "avg_weekly_tss": avg_weekly_tss,
        "notes": "Profile generated automatically.",
        "power_bests": power_bests
    }
    return profile
