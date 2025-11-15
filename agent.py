import os
import time
import events

def run_agent():
    watch_dir = os.path.join(os.path.dirname(__file__), 'watch')
    log_path = os.path.join(os.path.dirname(__file__), 'evidence_log.jsonl')

    os.makedirs(watch_dir, exist_ok=True)

    print(f"GhostLogic Free Agent v{events.AGENT_VERSION}")
    print(f"Monitoring: {watch_dir}")
    print(f"Log file: {log_path}")

    observer = events.start_monitoring(watch_dir, log_path)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
