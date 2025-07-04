import json
import datetime
import os

LOG_FILE = "logs/audit.log"
QUEUE_FILE = "event_bus/violations.queue"

def run():
    print("[Phase 4] Audit Logger Running...")

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(QUEUE_FILE):
        print("[✓] No new violations to log.")
        return

    with open(QUEUE_FILE, "r") as f:
        violations = [v.strip() for v in f.readlines() if v.strip()]

    if not violations:
        print("[✓] Queue was empty, nothing to log.")
        return

    audit_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "violations": violations,
        "status": "remediated"
    }

    with open(LOG_FILE, "r+") as f:
        log = json.load(f)
        log.append(audit_entry)
        f.seek(0)
        json.dump(log, f, indent=2)

    print(f"[+] Audit entry recorded with {len(violations)} item(s).")

if __name__ == "__main__":
    run()
