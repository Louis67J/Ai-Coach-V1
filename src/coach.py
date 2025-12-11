# src/coach.py
import os, json
from openai import OpenAI
from pathlib import Path

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")
client = OpenAI(api_key=OPENAI_KEY)

# load profile for context
PROFILE_PATH = Path(__file__).resolve().parent.parent / "analysis_data" / "athlete_profile.json"

SYSTEM_PROMPT = """
You are a senior cycling coach. Use the athlete profile and recent training history to propose plans,
assess fatigue and recommend nutrition. Answer concisely and provide a JSON section with keys:
summary, readiness, recommendation (single session), week_plan (list), nutrition, notes.
"""

def _load_profile_small():
    if PROFILE_PATH.exists():
        return json.loads(PROFILE_PATH.read_text())
    return {}

def ask_ai_for_plan(profile, horizon_days=7):
    # profile can be dict or JSON string
    prof_text = json.dumps(profile, default=str) if isinstance(profile, dict) else str(profile)
    prompt = SYSTEM_PROMPT + "\n\nAthlete profile:\n" + prof_text + f"\n\nProduce a {horizon_days}-day plan and explanations."
    resp = client.responses.create(model=MODEL, input=prompt, max_output_tokens=1000)
    try:
        return resp.output_text
    except Exception:
        return str(resp)

def ask_ai_freeform(question, extra_context=None):
    ctx = ""
    if PROFILE_PATH.exists():
        ctx = PROFILE_PATH.read_text()[:4000]
    input_text = f"Context:\n{ctx}\n\nQuestion:\n{question}"
    resp = client.responses.create(model=MODEL, input=input_text, max_output_tokens=800)
    return getattr(resp, "output_text", str(resp))
