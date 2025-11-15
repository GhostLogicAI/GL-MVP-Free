#!/usr/bin/env python3

from flask import Flask, jsonify, send_file, Response
import os
import json
import platform

app = Flask(__name__)

AGENT_VERSION = "1.0.0"
LOG_PATH = os.path.join(os.path.dirname(__file__), 'evidence_log.jsonl')

@app.route('/')
def index():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>GhostLogic Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: monospace; margin: 20px; background: #111; color: #0f0; }
        a { color: #0ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        h1 { color: #0f0; }
        .menu { margin: 20px 0; }
        .menu a { display: block; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>GhostLogic Free Dashboard</h1>
    <div class="menu">
        <a href="/events">View Events (JSON)</a>
        <a href="/export">Download Log (JSONL)</a>
        <a href="/info">System Info</a>
    </div>
    <p>Auto-refresh: 5s</p>
</body>
</html>"""
    return html

@app.route('/events')
def events():
    events_list = []
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                for line in f:
                    if line.strip():
                        events_list.append(json.loads(line))
    except:
        pass
    return jsonify(events_list)

@app.route('/export')
def export():
    if os.path.exists(LOG_PATH):
        return send_file(LOG_PATH, as_attachment=True, download_name='evidence_log.jsonl')
    return "No log file found", 404

@app.route('/info')
def info():
    file_count = 0
    latest_seq = 0

    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                for line in f:
                    if line.strip():
                        file_count += 1
                        try:
                            data = json.loads(line)
                            seq = data.get('sequence_id', 0)
                            if seq > latest_seq:
                                latest_seq = seq
                        except:
                            pass
    except:
        pass

    info_data = {
        'platform': platform.system(),
        'agent_version': AGENT_VERSION,
        'file_count': file_count,
        'latest_sequence_id': latest_seq
    }
    return jsonify(info_data)

if __name__ == '__main__':
    print("GhostLogic Dashboard starting on http://localhost:4242")
    app.run(host='0.0.0.0', port=4242, debug=False)
