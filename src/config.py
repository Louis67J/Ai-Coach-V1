# config.py - loads config from env and example file
import os
import yaml
from pathlib import Path
"""
config.py
→ Contient les infos sensibles.
→ Tu peux éditer ce fichier directement.
→ Ne PAS le pousser sur GitHub si tu mets tes clés ici !
"""

# --- OPENAI ---
# modèle gratuit : gpt-4.2-mini
# modèle meilleur : gpt-5.0 (si tu as accès)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-5.0"

# --- INTERVALS ---
INTERVALS_BASE_URL = "https://intervals.icu/api/v1"
INTERVALS_API_KEY = os.getenv("INTERVALS_API_KEY")

# --- EMAIL ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "louis.jeuch@gmail.com"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
USER_EMAIL = "louis.jeuch@gmail.com"

# --- DISCORD ---
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")  # pas une info sensible
