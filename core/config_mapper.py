import yaml
from monitor_agents import gworkspace_monitor

def load_controls():
    with open("resources/controls.yaml", "r") as f:
        return yaml.safe_load(f)

def check_control(control_id, control_def, system_config):
    findings = []

    if control_id == "A.9.2.3":
        if len(system_config["admin_users"]) > control_def["expected_state"]["admin_users_max"]:
            findings.append("Too many admin users.")
        if not all(user in system_config["mfa_users"] for user in system_config["admin_users"]):
            findings.append("Some admin users do not have MFA enabled.")

    elif control_id == "A.10.1.1":
        if system_config["password_policy"]["min_length"] < control_def["expected_state"]["min_length"]:
            findings.append("Password minimum length is too low.")
        if system_config["password_policy"]["rotation_days"] > control_def["expected_state"]["rotation_days"]:
            findings.append("Password rotation period is too long.")

    return findings

def run_config_mapping():
    controls = load_controls()
    config = gworkspace_monitor.fetch_current_config()

    for cid, cdef in controls.items():
        issues = check_control(cid, cdef, config)
        if issues:
            print(f"Violations for {cid} - {cdef['name']}:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print(f"{cid} passed.")

def run():
    run_config_mapping()


if __name__ == "__main__":
    run()
