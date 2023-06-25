import os

import boto3
from boto3.s3.transfer import TransferConfig

from config import env

progress_upload_mb = 0
file_size_mb = 0


def upload_progress_callback(bytes_transferred):
    global progress_upload_mb
    global file_size_mb

    transferred_mb = (bytes_transferred / 1024) / 1024
    progress_upload_mb += transferred_mb
    print(f"Uploaded {progress_upload_mb} / {file_size_mb} mb")


def upload_large_file_to_s3(bucket_name, file_path, key_name):
    global file_size_mb

    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / 1024 / 1024

    s3 = boto3.client(
        's3',
        endpoint_url=env["ENDPOINT_URL"],
        region_name=env["AWS_REGION"],
        aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]

    )

    config = TransferConfig(
        max_concurrency=1,
        multipart_chunksize=int(env["PART_SIZE_IN_MB"]) * 1024 * 1024,
        # io_chunksize=int(env["PART_SIZE_IN_MB"]) * 1024 * 1024,
        use_threads=True
    )

    # Upload the file
    s3.upload_file(
        Filename=file_path,
        Bucket=bucket_name,
        Key=key_name,
        Config=config,
        Callback=upload_progress_callback
    )


# Example usage
bucket_name = env["BUCKET_NAME"]
file_path = "/Users/sorawitlertumpaisakulwong/Desktop/poc-python-aws-localstack/Untitled.mov"
key_name = env["UPLOAD_KEY"]

upload_large_file_to_s3(bucket_name, file_path, key_name)
