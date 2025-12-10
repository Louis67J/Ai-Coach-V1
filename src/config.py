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
OPENAI_MODEL = "gpt-5.0"

# --- INTERVALS ---
INTERVALS_BASE_URL = "https://intervals.icu/api/v1"

# --- EMAIL ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "louis.jeuch@gmail.com"
USER_EMAIL = "louis.jeuch@gmail.com"

# --- DISCORD ---
