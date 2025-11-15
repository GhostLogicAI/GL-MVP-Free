import platform
import getpass
import psutil

def get_platform():
    return platform.system()

def get_session_username():
    try:
        return getpass.getuser()
    except:
        return "unknown"

def get_process_list():
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username']
                })
            except:
                pass
    except:
        pass
    return processes
