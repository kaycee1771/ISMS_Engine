import time
import os

QUEUE_FILE = "event_bus/violations.queue"

def run():
    print("Listening for drift events...")
    while True:
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, "r") as f:
                for line in f:
                    print(f"[event] {line.strip()}")
            os.remove(QUEUE_FILE)
        time.sleep(5)

if __name__ == "__main__":
    run()
