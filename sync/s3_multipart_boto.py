import boto3
from boto3.s3.transfer import TransferConfig

from config import env


def upload_progress_callback(bytes_transferred):
    print(f"Uploaded {bytes_transferred / 1024} mb")


def upload_large_file_to_s3(bucket_name, file_path, key_name):
    s3 = boto3.client(
        's3',
        endpoint_url=env["ENDPOINT_URL"],
        region_name=env["AWS_REGION"],
        aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]

    )

    config = TransferConfig(
        max_concurrency=5,
        multipart_threshold=int(env["PART_SIZE_IN_MB"]) * 1024 * 1024,
        multipart_chunksize=int(env["PART_SIZE_IN_MB"]) * 1024 * 1024,
        use_threads=True
    )

    # Upload the file
    s3.upload_file(
        file_path,
        bucket_name,
        key_name,
        Config=config,
        Callback=upload_progress_callback
    )


# Example usage
bucket_name = env["BUCKET_NAME"]
file_path = "/Users/sorawitlertumpaisakulwong/Desktop/poc-python-aws-localstack/Untitled.mov"
key_name = env["UPLOAD_KEY"]

upload_large_file_to_s3(bucket_name, file_path, key_name)
