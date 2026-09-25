import json
import os

PROFILES_DIR = os.path.join(os.path.dirname(__file__), "trade_profiles")

def load_trade_profile(trade: str = "hvac") -> dict:
    """Loads trade configuration, prompt instructions, and triage criteria."""
    file_path = os.path.join(PROFILES_DIR, f"{trade.lower()}.json")
    if not os.path.exists(file_path):
        file_path = os.path.join(PROFILES_DIR, "hvac.json")
        
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
