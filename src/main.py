import asyncio
import os

from s3_multipart_async import S3Client
from upload_file_to_s3 import UploadFileToS3

FILE_PATH = '../IMG_0012.MOV'


async def main():
    s3 = S3Client()
    upload_file = UploadFileToS3(s3=s3)
    await upload_file.execute(file_path=FILE_PATH)


asyncio.run(main())
