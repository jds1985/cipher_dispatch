import os
import requests
from dotenv import load_dotenv
from integrations.ticket_formatter import format_sms_alert

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

def send_tech_dispatch_sms(to_phone: str, ticket_data: dict) -> bool:
    """
    Sends structured SMS ticket to the on-call technician via Twilio REST API.
    """
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
        print("[SMS Dispatch] Twilio credentials missing in environment. Logging ticket locally:")
        print(format_sms_alert(ticket_data))
        return False

    message_body = format_sms_alert(ticket_data)
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

    response = requests.post(
        url,
        data={
            "From": TWILIO_FROM_NUMBER,
            "To": to_phone,
            "Body": message_body
        },
        auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    )

    if response.status_code in [200, 201]:
        print(f"[SMS Dispatch] Successfully alerted technician at {to_phone}")
        return True
    else:
        print(f"[SMS Dispatch] Failed to send SMS: {response.text}")
        return False
