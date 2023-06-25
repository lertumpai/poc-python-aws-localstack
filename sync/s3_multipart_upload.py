import os

import boto3
from boto3.s3.transfer import TransferConfig

from config import env

progress_upload_mb = 0
file_size_mb = 0
filename = ""


def upload_progress_callback(bytes_transferred):
    global progress_upload_mb
    global file_size_mb
    global filename

    transferred_mb = (bytes_transferred / 1024) / 1024
    progress_upload_mb += transferred_mb
    progress_percent = progress_upload_mb / file_size_mb * 100
    print(f"Upload {filename}: progress {progress_percent:.2f} / 100.00 %")


def upload_large_file_to_s3(file_path, upload_key):
    global file_size_mb
    global filename

    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    file_size_mb = file_size / 1024 / 1024

    s3 = boto3.client(
        's3',
        endpoint_url=env["ENDPOINT_URL"],
        region_name=env["AWS_REGION"],
        aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]

    )

    config = TransferConfig(
        max_concurrency=5,
        multipart_chunksize=int(env["PART_SIZE_IN_MB"]) * 1024 * 1024,
        # use_threads=True
    )

    # Upload the file
    s3.upload_file(
        Filename=file_path,
        Bucket=env["BUCKET_NAME"],
        Key=upload_key,
        Config=config,
        Callback=upload_progress_callback
    )


# Example usage
file_path = "/Users/sorawitlertumpaisakulwong/Desktop/poc-python-aws-localstack/Untitled.mov"
upload_key = env["UPLOAD_KEY"]

upload_large_file_to_s3(file_path, upload_key)
