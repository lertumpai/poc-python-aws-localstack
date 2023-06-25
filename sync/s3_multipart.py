import aioboto3

from config import env


async def create_multipart_upload():
    async with aioboto3.Session().client(
            service_name='s3',
            endpoint_url=env["ENDPOINT_URL"],
            region_name=env["AWS_REGION"],
            aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]
    ) as s3:
        response = await s3.create_multipart_upload(Bucket=env["BUCKET_NAME"], Key=env["UPLOAD_KEY"])
        return response['UploadId']


async def upload_part(part_number, upload_id, data):
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
            UploadId=upload_id
        )

        print("done upload part", part_number)
        return {'PartNumber': part_number, 'ETag': response['ETag']}


async def complete_multipart_upload(parts, upload_id):
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
            UploadId=upload_id
        )
        return response
