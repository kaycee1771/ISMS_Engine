import json
import hashlib
import datetime
import os

DRIFT_LOG = "event_bus/violations.queue"
SHARED_POOL = "logs/shared_drift_signatures.json"
LOCAL_POOL = "logs/local_drift_signatures.json"

def hash_violation(violation):
    return hashlib.sha256(violation.encode()).hexdigest()

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return []

def run():
    print("[Telemetry] Analyzing recent local drift violations...")

    if not os.path.exists(DRIFT_LOG):
        print("[Telemetry] No local drift found.")
        return

    with open(DRIFT_LOG, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    local_hashes = [hash_violation(v) for v in lines]

    # Save to local drift pool
    local_pool = load_json(LOCAL_POOL)
    for h in local_hashes:
        local_pool.append({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "hash": h
        })
    with open(LOCAL_POOL, "w") as f:
        json.dump(local_pool, f, indent=2)

    # Load shared telemetry pool
    shared_pool = load_json(SHARED_POOL)
    shared_hashes = {entry["hash"] for entry in shared_pool}

    print("\n[Telemetry] Drift Fingerprint Report:")
    for h in local_hashes:
        if h in shared_hashes:
            print(f" Match found in global drift database: {h[:12]}...")
        else:
            print(f" Novel drift fingerprint: {h[:12]}... (adding to shared pool)")
            shared_pool.append({
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "hash": h
            })

    # Save updated shared pool
    with open(SHARED_POOL, "w") as f:
        json.dump(shared_pool, f, indent=2)

    print(f"\n[Telemetry] Shared pool updated with {len(local_hashes)} new entries.")

if __name__ == "__main__":
    run()
