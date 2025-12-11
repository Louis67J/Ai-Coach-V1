# agent/agent_core.py
"""
Lightweight agent scaffold:
- tools: get_training_data, compute_profile, make_plan, send_report
- main decide() uses heuristics + LLM to finalize decisions
"""
import os
from pathlib import Path
import json
from analysis.profile_utils import load_profile, save_profile
from analysis.update_profile import update_profile
from charts.generate_charts import plot_ctl_atl, plot_power_curve
from coach import ask_ai_for_plan

OUT = Path(__file__).resolve().parent.parent / "outputs"

def tool_fetch_data():
    # update profile and return it
    profile = update_profile()
    return profile

def tool_make_plan(profile, horizon_days=7):
    # ask LLM for a weekly plan given profile (delegated to coach.ask_ai_for_plan)
    plan_text = ask_ai_for_plan(profile, horizon_days)
    return plan_text

def tool_send_report(subject, body, attachments=None, emailer=None, webhook=None):
    # stream: send via email or webhook (implemented in main pipeline)
    if emailer:
        emailer.send_email(subject, body)
    if webhook:
        # simple HTTP POST to webhook url
        import requests
        requests.post(webhook, json={"content": body})
    # save locally also
    p = OUT / "agent_report.txt"
    p.write_text(subject + "\n\n" + body)

def decide_and_act(emailer=None, webhook=None):
    profile = tool_fetch_data()
    # simple heuristic: if avg_weekly_tss jumped, trigger recovery plan
    avg = profile.get("avg_weekly_tss",0)
    # ask AI for recommendation
    plan = tool_make_plan(profile, horizon_days=7)
    subj = "AI-Agent weekly recommendation"
    tool_send_report(subj, plan, emailer=emailer, webhook=webhook)
    return {"subject":subj, "plan":plan}
