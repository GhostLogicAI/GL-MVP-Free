import os
import base64
import requests

def upload_to_kv(key, value):
    try:
        account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
        namespace_id = os.environ.get('CLOUDFLARE_KV_NAMESPACE')
        access_key = os.environ.get('CLOUDFLARE_ACCESS_KEY')
        prefix = os.environ.get('CLOUDFLARE_KV_PREFIX', '')

        if prefix:
            full_key = f"{prefix}:{key}"
        else:
            full_key = key

        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{full_key}"

        headers = {
            'Authorization': f'Bearer {access_key}',
            'Content-Type': 'application/json'
        }

        if isinstance(value, bytes):
            value = base64.b64encode(value).decode('utf-8')

        response = requests.put(url, headers=headers, data=value)
        return response.status_code == 200
    except Exception as e:
        print(f"KV upload error: {e}")
        return False
