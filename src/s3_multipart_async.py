import aioboto3

from config import env


class S3Client:
    def __init__(self):
        self.s3 = None
        self.upload_id = None

    async def create_multipart_upload(self):
        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url=env["ENDPOINT_URL"],
                region_name=env["AWS_REGION"],
                aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]
        ) as s3:
            response = await s3.create_multipart_upload(Bucket=env["BUCKET_NAME"], Key=env["UPLOAD_KEY"])
            self.upload_id = response['UploadId']

    async def upload_part(self, part_number, data):
        print("start upload part", part_number)

        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url=env["ENDPOINT_URL"],
                region_name=env["AWS_REGION"],
                aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]
        ) as s3:
            response = await s3.upload_part(
                Body=data,
                Bucket=env["BUCKET_NAME"],
                Key=env["UPLOAD_KEY"],
                PartNumber=part_number,
                UploadId=self.upload_id
            )

            print("done upload part", part_number)
            return {'PartNumber': part_number, 'ETag': response['ETag']}

    async def complete_multipart_upload(self, parts):
        # Complete the multipart upload
        async with aioboto3.Session().client(
                service_name='s3',
                endpoint_url=env["ENDPOINT_URL"],
                region_name=env["AWS_REGION"],
                aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]
        ) as s3:
            response = await s3.complete_multipart_upload(
                Bucket=env["BUCKET_NAME"],
                Key=env["UPLOAD_KEY"],
                MultipartUpload={'Parts': parts},
                UploadId=self.upload_id
            )
            self.upload_id = None
            return response
