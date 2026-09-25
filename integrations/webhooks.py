import requests
import json

def dispatch_to_crm_webhook(webhook_url: str, ticket_data: dict) -> bool:
    """
    Sends structured job ticket to an external CRM, Zapier, or Make endpoint.
    Payload maps directly to standard work order intake schemas.
    """
    if not webhook_url:
        print("[Webhook] No webhook URL configured. Skipping external CRM dispatch.")
        return False

    payload = {
        "event": "new_dispatch_ticket",
        "customer": {
            "name": ticket_data.get("customer_name"),
            "phone": ticket_data.get("phone"),
            "address": ticket_data.get("address")
        },
        "diagnostic_details": {
            "trade": ticket_data.get("trade", "hvac"),
            "equipment": ticket_data.get("equipment"),
            "symptom": ticket_data.get("symptom"),
            "breaker_checked": ticket_data.get("breaker_checked", False)
        },
        "triage": {
            "urgency": ticket_data.get("urgency", "standard"),
            "dispatch_priority": "high" if ticket_data.get("urgency") == "emergency" else "normal"
        }
    }

    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=8
        )
        response.raise_for_status()
        print(f"[Webhook] Ticket successfully delivered to CRM (status: {response.status_code})")
        return True
    except Exception as e:
        print(f"[Webhook] Failed to deliver ticket to CRM: {e}")
        return False
