import aioboto3
import asyncio
import os

# Set your AWS credentials
ENDPOINT_URL = 'http://localhost:4566'
AWS_ACCESS_KEY_ID = 'mock'
AWS_SECRET_ACCESS_KEY = 'mock'
AWS_REGION = 'ap-southeast-1'
BUCKET_NAME = 'poc-s3-bucket'
UPLOAD_KEY = 'multipart_key_6'
FILE_PATH = './IMG_0012.MOV'


class s3Client:
    def __init__(self):
        self.s3 = None
        self.upload_id = None

    async def create_multipart_upload(self):
        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url=ENDPOINT_URL,
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        ) as s3:
            response = await s3.create_multipart_upload(Bucket=BUCKET_NAME, Key=UPLOAD_KEY)
            self.upload_id = response['UploadId']

    async def upload_part(self, part_number, data):
        print("start upload part", part_number)

        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url=ENDPOINT_URL,
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        ) as s3:
            response = await s3.upload_part(
                Body=data,
                Bucket=BUCKET_NAME,
                Key=UPLOAD_KEY,
                PartNumber=part_number,
                UploadId=self.upload_id
            )
            print("done upload part", part_number)
            return {'PartNumber': part_number, 'ETag': response['ETag']}

    async def complete_multipart_upload(self, parts):
        # Complete the multipart upload
        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url=ENDPOINT_URL,
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        ) as s3:
            response = await s3.complete_multipart_upload(
                Bucket=BUCKET_NAME,
                Key=UPLOAD_KEY,
                MultipartUpload={'Parts': parts},
                UploadId=self.upload_id
            )
            return response


async def main():
    s3 = s3Client()
    await s3.create_multipart_upload()

    # Set the part size (5MB in this example)
    part_size = 100 * 1024 * 1024
    part_number = 1
    parts = []

    upload_parts = []

    # Open the file
    with open(FILE_PATH, 'rb') as file:
        while True:
            # Read a part of the file
            data = file.read(part_size)

            if not data:
                break

            # create list of upload the part
            upload_parts.append(
                s3.upload_part(
                    part_number=part_number,
                    data=data
                )
            )
            part_number += 1

    # await all upload part and gather results
    results = await asyncio.gather(*upload_parts)

    # Store the ETag for later use
    for result in results:
        parts.append(result)

    await s3.complete_multipart_upload(
        parts=parts
    )

    print("Done...")


asyncio.run(main())
