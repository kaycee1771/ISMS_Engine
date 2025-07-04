import json
from collections import Counter, defaultdict
import os
from datetime import datetime

AUDIT_LOG_PATH = "logs/audit.log"

def parse_log():
    if not os.path.exists(AUDIT_LOG_PATH):
        print("[LogAnalyzer] No audit log found.")
        return []

    with open(AUDIT_LOG_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[LogAnalyzer] Error parsing audit log.")
            return []

def analyze():
    print("[LogAnalyzer] Analyzing audit history...")
    data = parse_log()
    if not data:
        return

    violation_counter = Counter()
    remediation_failures = defaultdict(int)

    for entry in data:
        violations = entry.get("violations", [])
        timestamp = entry.get("timestamp", "")
        status = entry.get("status", "")

        for v in violations:
            violation_counter[v] += 1
            if status != "remediated":
                remediation_failures[v] += 1

    print("\n Top Violations:")
    for v, count in violation_counter.most_common(5):
        print(f"  - {v}: {count} times")

    if remediation_failures:
        print("\n Violations that failed remediation:")
        for v, fail_count in remediation_failures.items():
            print(f"  - {v}: {fail_count} failures")

    print("\n[LogAnalyzer] Suggest running deeper investigation if violations exceed thresholds.")

if __name__ == "__main__":
    analyze()
