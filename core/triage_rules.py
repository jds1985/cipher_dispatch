import json

def evaluate_emergency(symptoms: list[str], equipment_type: str, indoor_temp: int = None) -> dict:
    """
    Evaluates caller report against trade emergency rules.
    Returns urgency status and justification.
    """
    symptoms_lower = " ".join(symptoms).lower()
    
    # 1. Critical safety hazards - immediate dispatch
    critical_triggers = ["burning", "smoke", "spark", "gas", "smell", "carbon monoxide", "leak", "flooding"]
    for trigger in critical_triggers:
        if trigger in symptoms_lower:
            return {
                "urgency": "emergency",
                "reason": f"Critical safety or property risk detected: '{trigger}'"
            }
            
    # 2. Weather & Freeze protection
    if indoor_temp is not None and indoor_temp <= 50:
        return {
            "urgency": "emergency",
            "reason": f"Freeze hazard: Indoor temperature at or below {indoor_temp}°F"
        }

    # 3. Standard service queue
    return {
        "urgency": "standard",
        "reason": "System requires diagnosis but presents no immediate safety or freeze risk."
    }
