import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

CONTROL_LIBRARY = {
    "A.10.1.1": {
        "name": "Password policy enforcement",
        "description": "Ensure password length and expiration are enforced."
    },
    "A.9.2.3": {
        "name": "Management of privileged access rights",
        "description": "Ensure that privileged access (admin rights) are controlled and reviewed."
    }
}

def build_prompt(violation, control_id, current_value=None, expected_value=None):
    control = CONTROL_LIBRARY.get(control_id, {})
    prompt = f"""
You are a cybersecurity compliance assistant. A system has violated ISO27001 control {control_id} - {control.get("name", "")}.
Description: {control.get("description", "")}
Violation: {violation}
Current Value: {current_value}
Expected Value: {expected_value}

Explain the issue, its security impact, and recommend a remediation step in plain English.
"""
    return prompt

def suggest_fix(violation, control_id, current_value=None, expected_value=None):
    prompt = build_prompt(violation, control_id, current_value, expected_value)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in ISO27001 and DevSecOps remediation."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM Error] {e}"

def suggest_prioritized_fixes(top_n=2):
    FITNESS_FILE = "logs/control_fitness.json"

    if not os.path.exists(FITNESS_FILE):
        print("[LLM Brain] No control fitness data found.")
        return

    with open(FITNESS_FILE, "r") as f:
        fitness = json.load(f)

    sorted_controls = sorted(fitness.items(), key=lambda x: x[1]["score"])
    selected = sorted_controls[:top_n]

    for cid, info in selected:
        print(f"\n🔎 Control {cid} → Score: {info['score']}")
        vtype = "Password" if "A.10" in cid else "Admin"
        suggestion = suggest_fix(
            violation=f"Risky control state detected: {vtype} policy may be weak.",
            control_id=cid
        )
        print("[LLM Recommendation]")
        print(suggestion)

# Script Generator + Logger + Approval
def generate_script(violation, control_id, current_value=None, expected_value=None, lang="python"):
    prompt = f"""
You are a DevSecOps assistant. Generate a {lang} script that remediates this ISO27001 control violation.

Control ID: {control_id}
Violation: {violation}
Current Value: {current_value}
Expected Value: {expected_value}
Control Description: {CONTROL_LIBRARY.get(control_id, {}).get("description", "")}

Please only return the raw code with no explanation.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You generate ISO27001 remediation scripts for SaaS platforms."},
                {"role": "user", "content": prompt}
            ]
        )
        script_code = response.choices[0].message.content.strip()

        filename = f"remediation_scripts/generated_fix_{control_id.replace('.', '_')}.py"
        with open(filename, "w") as f:
            f.write(script_code)

        print(f"[LLM Generator] Script generated: {filename}")

        # Log to trace file
        trace_entry = {
            "control_id": control_id,
            "violation": violation,
            "prompt": prompt.strip(),
            "script_file": filename,
            "generated_code": script_code
        }
        trace_file = "logs/generated_script_trace.json"
        trace_data = []

        if os.path.exists(trace_file):
            with open(trace_file, "r") as tf:
                try:
                    trace_data = json.load(tf)
                except json.JSONDecodeError:
                    pass

        trace_data.append(trace_entry)
        with open(trace_file, "w") as tf:
            json.dump(trace_data, tf, indent=2)

        return filename
    except Exception as e:
        print(f"[LLM Generator] Failed to generate script: {e}")
        return None
