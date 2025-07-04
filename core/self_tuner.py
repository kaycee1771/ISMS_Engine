import json
import os
import datetime
from river import stats
from monitor_agents import gworkspace_monitor

LEARNING_FILE = "logs/self_tuning_state.json"
THRESHOLDS_FILE = "logs/self_tuning_thresholds.json"

# Parameters to track over time
MONITORED_PARAMS = {
    "A.10.1.1": {
        "min_length": stats.Mean(),
        "rotation_days": stats.Mean()
    },
    "A.9.2.3": {
        "admin_count": stats.Mean()
    }
}

def run():
    print("[SelfTuner] Starting self-tuning threshold monitor...")

    config = gworkspace_monitor.fetch_current_config()

    # Load existing state if available
    if os.path.exists(LEARNING_FILE):
        with open(LEARNING_FILE, "r") as f:
            saved = json.load(f)
        for cid, stat_map in saved.items():
            for param, mean_state in stat_map.items():
                mean_val = mean_state.get("mean", 0.0)
                count_val = mean_state.get("count", 0)

                try:
                    MONITORED_PARAMS[cid][param] = stats.Mean._from_state(mean_val, count_val)
                except Exception as e:
                    print(f"[SelfTuner] Warning: Failed to restore state for {cid}/{param}: {e}")
                    MONITORED_PARAMS[cid][param] = stats.Mean()

    # Feed latest config
    MONITORED_PARAMS["A.10.1.1"]["min_length"].update(config["password_policy"]["min_length"])
    MONITORED_PARAMS["A.10.1.1"]["rotation_days"].update(config["password_policy"]["rotation_days"])
    MONITORED_PARAMS["A.9.2.3"]["admin_count"].update(len(config["admin_users"]))

    # Save running state
    output_state = {}
    thresholds = {}

    for cid, stat_map in MONITORED_PARAMS.items():
        output_state[cid] = {}
        thresholds[cid] = {}
        for param, stat in stat_map.items():
            output_state[cid][param] = stat.__getstate__()
            thresholds[cid][param] = round(stat.get())

    with open(LEARNING_FILE, "w") as f:
        json.dump(output_state, f, indent=2)

    with open(THRESHOLDS_FILE, "w") as f:
        json.dump(thresholds, f, indent=2)

    print("[SelfTuner] Updated self-tuned thresholds:")
    for cid, param_map in thresholds.items():
        print(f"  - {cid}:")
        for k, v in param_map.items():
            print(f"      {k}: {v}")

if __name__ == "__main__":
    run()
