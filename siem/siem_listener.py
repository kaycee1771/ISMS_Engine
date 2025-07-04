import json
import os
from datetime import datetime

LOG_FILE = "logs/siem_events.json"

def mock_siem_event():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "source": "SIEM",
        "event_type": "brute_force_attempt",
        "severity": "high",
        "details": {
            "user": "alice",
            "ip": "192.168.1.101",
            "control_violated": "A.9.2.3",
            "description": "Multiple failed admin logins detected"
        }
    }

def run_once():
    print("[SIEM] Listening for external security alerts...")
    
    if not os.path.exists("logs"):
        os.makedirs("logs")

    event = mock_siem_event()
    print(f"[SIEM] New event: {event['event_type']} on {event['details']['user']}")

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                existing = json.load(f)
        else:
            existing = []

        existing.append(event)

        with open(LOG_FILE, "w") as f:
            json.dump(existing, f, indent=2)

        print("[SIEM] Event saved to logs/siem_events.json")
    except Exception as e:
        print(f"[SIEM] Failed to log SIEM event: {e}")

if __name__ == "__main__":
    run_once()
