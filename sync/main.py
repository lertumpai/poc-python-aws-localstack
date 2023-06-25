import asyncio
import os

from upload_file_to_s3 import upload_file_to_s3

FILE_PATH = '/Users/sorawitlertumpaisakulwong/Desktop/poc-python-aws-localstack/IMG_0012.MOV'


async def main():
    await upload_file_to_s3(file_path=FILE_PATH)


asyncio.run(main())
