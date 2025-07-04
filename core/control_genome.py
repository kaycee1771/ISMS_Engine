import json
import hashlib
import datetime
import os
from monitor_agents import gworkspace_monitor

GENOME_FILE = "logs/control_genomes.json"

def hash_dict(d):
    serialized = json.dumps(d, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()

def run():
    print("[Genome] Generating control genome fingerprints...")

    config = gworkspace_monitor.fetch_current_config()
    genome = {}

    # Password policy
    pp = config.get("password_policy", {})
    genome["A.10.1.1"] = {
        "fingerprint": hash_dict(pp),
        "config": pp,
        "tool": "Okta",
        "source": "google_workspace",
        "generated_at": datetime.datetime.utcnow().isoformat()
    }

    # Privileged access
    admin_users = set(config.get("admin_users", []))
    mfa_users = set(config.get("mfa_users", []))
    structure = {
        "admin_users": sorted(admin_users),
        "mfa_required_for_admins": sorted(admin_users.intersection(mfa_users)),
    }
    genome["A.9.2.3"] = {
        "fingerprint": hash_dict(structure),
        "config": structure,
        "tool": "Okta",
        "source": "google_workspace",
        "generated_at": datetime.datetime.utcnow().isoformat()
    }

    with open(GENOME_FILE, "w") as f:
        json.dump(genome, f, indent=2)

    print(f"[Genome] Genome fingerprints saved to {GENOME_FILE}")
    for cid, entry in genome.items():
        print(f"  - {cid}: {entry['fingerprint']}")

if __name__ == "__main__":
    run()
