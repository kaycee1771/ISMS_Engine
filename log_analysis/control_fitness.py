import json
import os
import datetime
from collections import defaultdict

AUDIT_LOG = "logs/audit.log"
SCORE_LOG = "logs/control_fitness.json"
TREND_LOG = "logs/control_fitness_history.json"

def parse_log():
    if not os.path.exists(AUDIT_LOG):
        return []
    with open(AUDIT_LOG, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def calculate_score(violations, failures, total):
    if total == 0:
        return 100
    penalty = (violations / total) * 50 + (failures / total) * 50
    return max(0, int(100 - penalty))

def append_trend_snapshot(timestamp, scores):
    entry = {"timestamp": timestamp}
    entry.update(scores)

    history = []
    if os.path.exists(TREND_LOG):
        with open(TREND_LOG, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                pass

    history.append(entry)
    with open(TREND_LOG, "w") as f:
        json.dump(history, f, indent=2)

def run():
    print("[Fitness] Calculating Control Health Scores...")
    data = parse_log()
    control_stats = defaultdict(lambda: {"violations": 0, "failures": 0, "occurrences": 0})

    for entry in data:
        status = entry.get("status", "")
        for v in entry.get("violations", []):
            cid = "A.10.1.1" if "Password" in v else "A.9.2.3"
            control_stats[cid]["violations"] += 1
            if status != "remediated":
                control_stats[cid]["failures"] += 1
            control_stats[cid]["occurrences"] += 1

    score_report = {}
    score_snapshot = {}
    for cid, stats in control_stats.items():
        score = calculate_score(stats["violations"], stats["failures"], stats["occurrences"])
        score_report[cid] = {
            "score": score,
            "violations": stats["violations"],
            "failures": stats["failures"],
            "trend": "stable" if score >= 75 else "degrading"
        }
        score_snapshot[cid] = score

    with open(SCORE_LOG, "w") as f:
        json.dump(score_report, f, indent=2)

    now = datetime.datetime.utcnow().isoformat()
    append_trend_snapshot(now, score_snapshot)

    print("[Fitness] Latest control fitness:")
    for cid, data in score_report.items():
        print(f"  {cid} → Score: {data['score']} ({data['trend']})")

if __name__ == "__main__":
    run()
