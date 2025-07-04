import yaml
import subprocess
import os
from llm import llm_reasoner

def load_remediation_map():
    with open("resources/remediation_map.yaml", "r") as f:
        return yaml.safe_load(f)

def run():
    print("[Phase 3] Auto-Remediation Engine Running...")

    queue_file = "event_bus/violations.queue"
    if not os.path.exists(queue_file):
        print("[✓] No violations to remediate.")
        return

    with open(queue_file, "r") as f:
        violations = [line.strip() for line in f if line.strip()]

    remediation_map = load_remediation_map()

    for violation in violations:
        script = remediation_map.get(violation)

        if script:
            script_path = os.path.join("remediation_scripts", script)
            if not os.path.exists(script_path):
                print(f"[!] Script not found: {script_path}")
                continue

            print(f"[~] Executing remediation for: {violation}")
            if script_path.endswith(".bat") or script_path.endswith(".sh"):
                result = subprocess.run([script_path], capture_output=True, text=True, shell=True)
            elif script_path.endswith(".py"):
                result = subprocess.run(["python", script_path], capture_output=True, text=True)
            else:
                print(f"[!] Unsupported script type: {script_path}")
                continue

            print(result.stdout)
        else:
            print(f"[!] No remediation script for: {violation}")
            print("[?] Asking LLM for guidance...")
            control_id = "A.10.1.1" if "Password" in violation else "A.9.2.3"

            suggestion = llm_reasoner.suggest_fix(
                violation=violation,
                control_id=control_id,
                current_value=8,
                expected_value=12
            )
            print("[LLM Suggestion]")
            print(suggestion)

            generated = llm_reasoner.generate_script(
                violation=violation,
                control_id=control_id,
                current_value=8,
                expected_value=12,
                lang="python"
            )

            if generated:
                print(f"[Auto-Remediator] Script saved as: {generated}")
                approval = input("[?] Execute the generated script now? (Y/n): ").strip().lower()
                if approval in ("y", "yes", ""):
                    result = subprocess.run(["python", generated], capture_output=True, text=True)
                    print(result.stdout)
                else:
                    print("[Auto-Remediator] Skipped execution by user choice.")


if __name__ == "__main__":
    run()
