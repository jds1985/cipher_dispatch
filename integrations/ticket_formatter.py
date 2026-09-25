def format_sms_alert(ticket: dict) -> str:
    """Formats triage data into a compact SMS for technicians."""
    urgency_tag = "🚨 EMERGENCY" if ticket.get("urgency") == "emergency" else "📋 STANDARD CALL"
    
    return (
        f"{urgency_tag}\n"
        f"Customer: {ticket.get('customer_name', 'Unknown')}\n"
        f"Phone: {ticket.get('phone', 'N/A')}\n"
        f"Address: {ticket.get('address', 'N/A')}\n"
        f"Equipment: {ticket.get('equipment', 'Not specified')}\n"
        f"Symptom: {ticket.get('symptom', 'No details provided')}\n"
        f"Breaker Status: {ticket.get('breaker_checked', 'Unknown')}"
    )
