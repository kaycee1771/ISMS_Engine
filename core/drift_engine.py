import json
from monitor_agents import gworkspace_monitor

def load_baseline():
    with open("resources/baseline_config.json", "r") as f:
        return json.load(f)

def compare_configs(baseline, current):
    drift = []

    if set(current["admin_users"]) != set(baseline["admin_users"]):
        drift.append("Admin user list has changed.")
    if set(current["mfa_users"]) != set(baseline["mfa_users"]):
        drift.append("MFA user list has changed.")
    
    pp = current["password_policy"]
    bp = baseline["password_policy"]
    if pp["min_length"] != bp["min_length"]:
        drift.append("Password min length has changed.")
    if pp["rotation_days"] != bp["rotation_days"]:
        drift.append("Password rotation period has changed.")
    
    return drift

def run():
    baseline = load_baseline()
    current = gworkspace_monitor.fetch_current_config()
    drift = compare_configs(baseline, current)

    if drift:
        print("Drift Detected:")
        for issue in drift:
            print(f"    - {issue}")
        with open("event_bus/violations.queue", "a") as f:
            for issue in drift:
                f.write(issue + "\n")
    else:
        print("No configuration drift detected.")

if __name__ == "__main__":
    run()
