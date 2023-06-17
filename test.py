import asyncio
import boto3

import aioboto3

# Set your AWS credentials
ENDPOINT_URL = 'http://localhost:4566'
AWS_ACCESS_KEY_ID = 'mock'
AWS_SECRET_ACCESS_KEY = 'mock'
AWS_REGION = 'ap-southeast-1'
BUCKET_NAME = 'poc-s3-bucket'
UPLOAD_KEY = 'multipart_key_3'
FILE_PATH = './IMG_0012.MOV'


async def my_async_function():
    async with aioboto3.Session().client(
            service_name='s3',
            endpoint_url=ENDPOINT_URL,
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    ) as s3:
        # Perform asynchronous operations with the customized S3 client
        response = await s3.list_objects(Bucket=BUCKET_NAME)
        print(response)


asyncio.run(my_async_function())
