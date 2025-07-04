import yaml
from monitor_agents import gworkspace_monitor
from core.config_mapper import check_control

def load_controls():
    with open("resources/controls.yaml", "r") as f:
        return yaml.safe_load(f)

def run():
    print("[Phase 4] Feedback Verifier Running...")
    controls = load_controls()
    config = gworkspace_monitor.fetch_current_config()

    verified = True
    for cid, cdef in controls.items():
        issues = check_control(cid, cdef, config)
        if issues:
            verified = False
            print(f"Control {cid} still violated:")
            for i in issues:
                print(f"    - {i}")
        else:
            print(f"Control {cid} OK")

    return verified
