import asyncio
import os

from s3_multipart_async import S3Client
from upload_file_to_s3 import UploadFileToS3

# Set your AWS credentials
ENDPOINT_URL = 'http://localhost:4566'
AWS_ACCESS_KEY_ID = 'mock'
AWS_SECRET_ACCESS_KEY = 'mock'
AWS_REGION = 'ap-southeast-1'
BUCKET_NAME = 'poc-s3-bucket'
UPLOAD_KEY = 'multipart_key_7'
FILE_PATH = '../IMG_0012.MOV'


async def main():
    s3 = S3Client()
    upload_file = UploadFileToS3(s3=s3)
    await upload_file.execute(file_path=FILE_PATH)


asyncio.run(main())
