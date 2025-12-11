# src/main.py
import os, json
from pathlib import Path
from analysis.update_profile import update_profile
from analysis.profile_utils import load_profile, save_profile
from charts.generate_charts import plot_ctl_atl, plot_power_curve, plot_zone_distribution, plot_season_progression, plot_hr_vs_power
from coach import ask_ai_for_plan, ask_ai_freeform
from agent.agent_core import decide_and_act
from emailer import send_email  # assume exists and uses SMTP env vars

OUT = Path(__file__).resolve().parent.parent / "outputs"
OUT.mkdir(exist_ok=True, parents=True)

def run_pipeline():
    # 1) update profile (fetch 24 months)
    profile = update_profile()
    # 2) derive daily_tss if we saved in profile (or reconstruct quickly)
    # NOTE: update_profile already computed avg_weekly_tss; for charts we may reconstruct daily_tss from stored activities artifact.
    # Here we attempt to load activities.json saved by intervals fetch function
    acts_path = Path(__file__).resolve().parent.parent / "outputs" / "activities.json"
    activities = []
    if acts_path.exists():
        activities = json.loads(acts_path.read_text())
    # build simple daily_tss series
    import pandas as pd
    tss_list = []
    for a in activities:
        start = a.get('start_date_local') or a.get('start_date')
        tss = a.get('icu_training_load') or a.get('tss') or 0
        if start:
            tss_list.append((start, tss))
    if tss_list:
        df = pd.DataFrame(tss_list, columns=['date','tss'])
        df['date'] = pd.to_datetime(df['date'])
        daily = df.groupby(df['date'].dt.date)['tss'].sum()
        daily.index = pd.to_datetime(daily.index)
    else:
        daily = pd.Series(dtype=float)

    # 3) basic power bests extraction (stub)
    power_bests = profile.get("power_bests", {5:900, 30:600, 60:450, 180:400, 300:380, 1200:330})
    # 4) time in zones stub (if available)
    time_in_zones = profile.get("time_in_zones", {"Z1":300, "Z2":1200, "Z3":200, "Z4":50})
    # 5) generate charts
    p1 = plot_ctl_atl(daily)
    p2 = plot_power_curve(power_bests)
    p3 = plot_zone_distribution(time_in_zones)
    # 6) ask AI for plan/summary
    ai_text = ask_ai_for_plan(profile, horizon_days=7)
    # 7) save summary and outputs
    summary_path = OUT / "summary.json"
    summary_path.write_text(json.dumps({"profile": profile, "ai": ai_text}, ensure_ascii=False, indent=2))
    # save text summary for discord bot
    (OUT / "summary.txt").write_text(ai_text)
    # optionally send email with AI summary
    user_email = os.getenv("USER_EMAIL")
    if user_email and os.getenv("SMTP_USER"):
        try:
            send_email("AI Coach daily report", ai_text[:8000])
        except Exception as e:
            print("Email failed:", e)
    # optional: post to discord webhook
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook:
        import requests
        payload = {"content": "AI Coach report:\n" + ai_text[:1800]}
        requests.post(webhook, json=payload)
    return {"charts":[p1,p2,p3], "ai_text": ai_text}

if __name__ == "__main__":
    res = run_pipeline()
    print("Pipeline finished. AI summary len:", len(res.get("ai_text","")))
