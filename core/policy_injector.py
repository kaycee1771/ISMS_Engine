import yaml
import os

POLICY_SOURCE = "policy_engine/policies.yaml"
CONTROL_FILE = "resources/controls.yaml"

def run():
    print("[Phase 0] Policy Loader Running...")

    try:
        with open(POLICY_SOURCE, "r") as f:
            raw = yaml.safe_load(f)

    
        policies = raw.get("policies", raw)

        with open(CONTROL_FILE, "w") as f:
            yaml.dump(policies, f, sort_keys=False, default_flow_style=False)

        print("Policy injection complete into controls.yaml.")
    except Exception as e:
        print(f"Failed to inject policies: {e}")

if __name__ == "__main__":
    run()
