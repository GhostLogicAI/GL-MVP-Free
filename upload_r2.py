import os
import boto3
from botocore.client import Config

def get_r2_client():
    account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
    access_key = os.environ.get('CLOUDFLARE_ACCESS_KEY')
    secret_key = os.environ.get('CLOUDFLARE_SECRET_KEY')

    endpoint = f"https://{account_id}.r2.cloudflarestorage.com"

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4')
    )
    return s3

def upload_to_r2(key, data, content_type='application/json'):
    try:
        bucket = os.environ.get('CLOUDFLARE_R2_BUCKET')
        prefix = os.environ.get('CLOUDFLARE_R2_PREFIX', '')

        if prefix:
            full_key = f"{prefix}/{key}"
        else:
            full_key = key

        s3 = get_r2_client()

        if isinstance(data, str):
            data = data.encode('utf-8')

        s3.put_object(
            Bucket=bucket,
            Key=full_key,
            Body=data,
            ContentType=content_type
        )
        return True
    except Exception as e:
        print(f"R2 upload error: {e}")
        return False
