import hashlib
import gzip
import json
import os
from datetime import datetime, timezone

_sequence_counter = 0
_sequence_lock = None

def get_sequence_lock():
    global _sequence_lock
    if _sequence_lock is None:
        import threading
        _sequence_lock = threading.Lock()
    return _sequence_lock

def get_next_sequence():
    global _sequence_counter
    with get_sequence_lock():
        _sequence_counter += 1
        return _sequence_counter

def get_utc_timestamp():
    return datetime.now(timezone.utc).isoformat()

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return None

def gzip_file(filepath):
    try:
        with open(filepath, 'rb') as f_in:
            return gzip.compress(f_in.read())
    except:
        return None

def append_to_jsonl(filepath, data):
    try:
        with open(filepath, 'a') as f:
            f.write(json.dumps(data) + '\n')
        return True
    except:
        return False
