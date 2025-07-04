import time
import os
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core import policy_injector

WATCH_PATH = "policy_engine"
WATCH_FILE = "policies.yaml"
WATCH_FULL_PATH = os.path.join(WATCH_PATH, WATCH_FILE)

class PolicyChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(WATCH_FILE):
            print(f"[GitOps] Detected change in {WATCH_FILE}. Re-injecting policies...")
            try:
                policy_injector.run()
                print("[GitOps] Policy sync complete.")
            except Exception as e:
                print(f"[GitOps] Error during policy injection: {e}")

def run():
    print(f"[GitOps] Watching {WATCH_PATH}/{WATCH_FILE} for changes...")
    observer = Observer()
    handler = PolicyChangeHandler()
    observer.schedule(handler, path=WATCH_PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[GitOps] Stopping watcher...")
        observer.stop()
    observer.join()

def run_once():
    print(f"[GitOps] One-time check of {WATCH_FULL_PATH}...")

    if not os.path.exists(WATCH_FULL_PATH):
        print(f"{WATCH_FULL_PATH} not found.")
        return

    try:
        with open(WATCH_FULL_PATH, "r") as f:
            data = yaml.safe_load(f)
            print(f"{WATCH_FILE} parsed. Sample controls: {list(data.keys())[:2]}")
        policy_injector.run()
        print("[GitOps] Policy sync injected (manual trigger).")
    except Exception as e:
        print(f"[GitOps] Error during manual policy load: {e}")

if __name__ == "__main__":
    run()
