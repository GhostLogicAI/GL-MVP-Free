# GhostLogic Free - MacBook Quickstart Guide

## Evidence Collection with Cloud Upload/Download

This guide will help you initiate evidence collection on your MacBook with Cloudflare R2 and KV storage for upload/download functionality.

---

## Prerequisites

- macOS 10.13 or later
- Python 3.7+ installed (`python3 --version`)
- Cloudflare account with R2 and Workers KV configured

---

## Step 1: Install Dependencies

Open Terminal and navigate to the project directory:

```bash
cd /path/to/GL-MVP-Free
pip3 install -r requirements.txt
```

---

## Step 2: Configure Cloudflare Credentials for Upload/Download

Create a `.env` file or export environment variables for cloud storage:

```bash
# Cloudflare Account Settings
export CLOUDFLARE_ACCOUNT_ID="your_account_id"
export CLOUDFLARE_ACCESS_KEY="your_api_token"
export CLOUDFLARE_SECRET_KEY="your_r2_secret_key"

# R2 Storage (for file uploads)
export CLOUDFLARE_R2_BUCKET="your-bucket-name"
export CLOUDFLARE_R2_PREFIX="optional/path/prefix"

# Workers KV (for metadata and file downloads)
export CLOUDFLARE_KV_NAMESPACE="your_kv_namespace_id"
export CLOUDFLARE_KV_PREFIX="optional_key_prefix"
```

### How to Get Credentials:

1. **Account ID**: Cloudflare Dashboard → Workers & Pages → Overview (right sidebar)
2. **R2 Bucket**: Cloudflare Dashboard → R2 → Create bucket
3. **API Token**: Cloudflare Dashboard → My Profile → API Tokens → Create Token
   - Use "Edit Cloudflare Workers" template
   - Add "R2 Edit" permission
4. **R2 Access Keys**: R2 → Manage R2 API Tokens → Create API token
   - Provides `CLOUDFLARE_ACCESS_KEY` and `CLOUDFLARE_SECRET_KEY`
5. **KV Namespace**: Workers & Pages → KV → Create namespace
   - Copy the Namespace ID

### Persistent Configuration (Optional):

Add exports to your `~/.zshrc` or `~/.bash_profile`:

```bash
echo 'export CLOUDFLARE_ACCOUNT_ID="your_account_id"' >> ~/.zshrc
echo 'export CLOUDFLARE_R2_BUCKET="your-bucket-name"' >> ~/.zshrc
# ... (add all other exports)
source ~/.zshrc
```

---

## Step 3: Initiate Evidence Collection

### Option A: Run Agent Directly (Manual Mode)

```bash
python3 ghostlogic_free.py
```

This will:
- Create a `watch/` directory
- Start monitoring for file changes
- Upload files ≤ 5 MB to Cloudflare R2 and KV
- Log all events to `evidence_log.jsonl`

### Option B: Run with Supervisor (Auto-Restart Mode)

```bash
python3 supervisor.py
```

This will:
- Automatically restart the agent if it crashes
- Provide continuous monitoring
- Display restart timestamps

---

## Step 4: Collect Evidence Immediately

### Add Files to Monitor:

```bash
# Create or copy files into the watch directory
echo "Evidence document" > watch/important_file.txt
cp /path/to/sensitive_file.pdf watch/
```

### Verify Evidence Collection:

```bash
# View collected evidence
tail -f evidence_log.jsonl

# Or use Python to format output
tail -1 evidence_log.jsonl | python3 -m json.tool
```

### View Dashboard:

```bash
# In a new terminal, start the dashboard
python3 dashboard.py
```

Then open: http://localhost:4242

Dashboard features:
- View all events: `/events`
- Download evidence log: `/export`
- System info: `/info`

---

## Step 5: Verify Cloud Upload/Download

### Check R2 Uploads:

Files are uploaded to R2 with this structure:
```
R2 Bucket:
├── events/{sequence_id}.json     (Event metadata)
└── files/{sha256}.gz              (Gzipped file contents)
```

### Check KV Uploads:

Metadata is also stored in Workers KV:
```
KV Namespace:
├── {sequence_id}        (Event metadata, base64 encoded)
└── file:{sha256}        (File contents, base64 encoded)
```

### Test Upload:

```bash
# Create a test file
echo "Upload test" > watch/upload_test.txt

# Check the log for upload status
tail -1 evidence_log.jsonl | grep -o '"file_upload":"[^"]*"'
```

Should show: `"file_upload":"success"`

---

## Troubleshooting

### No Cloudflare Credentials

If you don't configure Cloudflare credentials:
- Evidence will still be collected locally in `evidence_log.jsonl`
- File uploads will fail silently
- `file_upload` field will show `"failed"` or `"skipped_large"`

### Files Not Being Uploaded

Check:
1. File size (must be ≤ 5 MB)
2. Cloudflare credentials are exported
3. Internet connectivity
4. R2 bucket and KV namespace exist

### Agent Not Starting

```bash
# Check for errors
python3 ghostlogic_free.py

# Verify dependencies
pip3 list | grep -E 'watchdog|psutil|boto3|requests|flask'
```

---

## What Gets Collected

For every file event (create/modify/delete), the system collects:

- **Timestamp**: ISO 8601 UTC timestamp
- **Event Type**: `create`, `modify`, or `delete`
- **File Path**: Full path to the file
- **File Metadata**: Size, modification time, owner
- **File Hash**: SHA-256 checksum
- **System Context**: Platform, agent version, username
- **Process Snapshot**: List of all running processes at event time
- **File Contents**: Uploaded to R2 and KV (if ≤ 5 MB)

---

## Stopping Evidence Collection

```bash
# Press Ctrl+C in the terminal running the agent
# Or kill the process:
pkill -f ghostlogic_free.py
```

---

## Next Steps

- **Review Evidence**: Open dashboard at http://localhost:4242
- **Export Data**: Download `evidence_log.jsonl` from dashboard or copy the file
- **Build Installer**: Run `./make_pkg.sh` to create a macOS .pkg installer
- **Configure Auto-Start**: Add to Login Items or use launchd

---

## Quick Reference

```bash
# Install dependencies
pip3 install -r requirements.txt

# Set Cloudflare credentials
export CLOUDFLARE_ACCOUNT_ID="..."
export CLOUDFLARE_R2_BUCKET="..."
export CLOUDFLARE_KV_NAMESPACE="..."
# ... (other credentials)

# Start agent
python3 ghostlogic_free.py

# Start dashboard (in new terminal)
python3 dashboard.py

# Add evidence
echo "Evidence" > watch/file.txt

# View evidence
tail -f evidence_log.jsonl

# Stop agent
pkill -f ghostlogic_free.py
```

---

## Support

For issues or questions, visit: https://ghostlogic.ai
