import aioboto3
import os

# Set your AWS credentials
ENDPOINT_URL = 'http://localhost:4566'
AWS_ACCESS_KEY_ID = 'mock'
AWS_SECRET_ACCESS_KEY = 'mock'
AWS_REGION = 'ap-southeast-1'
BUCKET_NAME = 'poc-s3-bucket'
UPLOAD_KEY = 'multipart_key'
FILE_PATH = '../IMG_0012.MOV'


class S3Client:
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
            self.upload_id = None
            return response
