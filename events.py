import os
import stat
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import utils
import process_snapshot
import upload_r2
import upload_kv

AGENT_VERSION = "1.0.0"
MAX_FILE_SIZE = 5 * 1024 * 1024

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, log_path):
        self.log_path = log_path

    def on_created(self, event):
        if not event.is_directory:
            self.process_event('create', event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_event('modify', event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.process_event('delete', event.src_path)

    def get_file_metadata(self, filepath):
        metadata = {}
        try:
            stat_info = os.stat(filepath)
            metadata['size'] = stat_info.st_size
            metadata['mtime'] = stat_info.st_mtime

            if hasattr(stat_info, 'st_uid'):
                try:
                    import pwd
                    metadata['owner'] = pwd.getpwuid(stat_info.st_uid).pw_name
                except:
                    metadata['owner'] = str(stat_info.st_uid)
            else:
                metadata['owner'] = 'unknown'
        except:
            metadata['size'] = 0
            metadata['mtime'] = 0
            metadata['owner'] = 'unknown'

        return metadata

    def process_event(self, event_type, filepath):
        sequence_id = utils.get_next_sequence()
        timestamp = utils.get_utc_timestamp()

        event_data = {
            'timestamp': timestamp,
            'event_type': event_type,
            'file_path': filepath,
            'platform': process_snapshot.get_platform(),
            'agent_version': AGENT_VERSION,
            'sequence_id': sequence_id,
            'session_username': process_snapshot.get_session_username(),
            'process_list': process_snapshot.get_process_list()
        }

        if event_type != 'delete':
            metadata = self.get_file_metadata(filepath)
            event_data['file_size'] = metadata['size']
            event_data['mtime'] = metadata['mtime']
            event_data['owner'] = metadata['owner']

            sha256 = utils.compute_sha256(filepath)
            event_data['sha256'] = sha256

            if metadata['size'] <= MAX_FILE_SIZE and sha256:
                gzipped = utils.gzip_file(filepath)
                if gzipped:
                    upload_r2.upload_to_r2(f"files/{sha256}.gz", gzipped, 'application/gzip')
                    upload_kv.upload_to_kv(f"file:{sha256}", gzipped)
                    event_data['file_upload'] = 'success'
                else:
                    event_data['file_upload'] = 'failed'
            else:
                event_data['file_upload'] = 'skipped_large'
        else:
            event_data['sha256'] = None
            event_data['file_size'] = None
            event_data['mtime'] = None
            event_data['owner'] = None
            event_data['file_upload'] = 'skipped_delete'

        utils.append_to_jsonl(self.log_path, event_data)

        import json
        event_json = json.dumps(event_data)
        upload_r2.upload_to_r2(f"events/{sequence_id}.json", event_json)
        upload_kv.upload_to_kv(str(sequence_id), event_json)

def start_monitoring(watch_dir, log_path):
    event_handler = FileEventHandler(log_path)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()
    return observer
