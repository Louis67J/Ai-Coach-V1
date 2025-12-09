# config.py - loads config from env and example file
import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load example config for non-secret defaults
cfg_path = BASE_DIR.parent / "example_config.yaml"
with open(cfg_path, "r") as f:
    DEFAULTS = yaml.safe_load(f)

INTERVALS_BASE = os.getenv("INTERVALS_BASE", DEFAULTS.get("INTERVALS_BASE", "https://intervals.icu/api/v1"))
DAYS_LOOKBACK = int(os.getenv("DAYS_LOOKBACK", DEFAULTS.get("DAYS_LOOKBACK", 300)))

OPENAI_MODEL = os.getenv("OPENAI_MODEL", DEFAULTS.get("OPENAI_MODEL", "gpt-4o-mini"))
ATHLETE = DEFAULTS.get("ATHLETE", {})

# Output folder
OUTPUT_DIR = BASE_DIR.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
