
import msal
import os
import requests
from datetime import datetime

def get_token():
    app = msal.PublicClientApplication(
        os.getenv("CLIENT_ID"),
        authority=f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"
    )
    result = app.acquire_token_interactive(scopes=["User.Read", "Mail.Read", "Calendars.Read"])
    return result["access_token"]

def get_emails(token):
    url = "https://graph.microsoft.com/v1.0/me/messages?$top=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("value", [])

def get_events(token):
    today = datetime.utcnow().isoformat()
    end = today[:10] + "T23:59:59Z"
    url = f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={today}&enddatetime={end}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("value", [])
