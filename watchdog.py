#!/usr/bin/env python3

import sys
import subprocess
import time
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agent_script = os.path.join(script_dir, 'ghostlogic_free.py')

    if not os.path.exists(agent_script):
        if getattr(sys, 'frozen', False):
            agent_exe = os.path.join(script_dir, 'ghostlogic_free')
            if os.name == 'nt':
                agent_exe += '.exe'
            if os.path.exists(agent_exe):
                agent_script = agent_exe

    print(f"GhostLogic Watchdog - Monitoring: {agent_script}")

    while True:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting agent...")
            if agent_script.endswith('.py'):
                result = subprocess.run([sys.executable, agent_script])
            else:
                result = subprocess.run([agent_script])

            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Agent exited with code {result.returncode}")
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Restarting in 2 seconds...")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\nWatchdog stopped by user")
            break
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}")
            time.sleep(2)

if __name__ == '__main__':
    main()
