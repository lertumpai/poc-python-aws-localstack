import boto3
import os

# Set your AWS credentials
ENDPOINT_URL = 'http://localhost:4566'
AWS_ACCESS_KEY_ID = 'mock'
AWS_SECRET_ACCESS_KEY = 'mock'
AWS_REGION = 'ap-southeast-1'
BUCKET_NAME = 'poc-s3-bucket'
UPLOAD_KEY = 'multipart_key'
FILE_PATH = './IMG_0012.MOV'

# Create an S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    endpoint_url=ENDPOINT_URL
)

# Initiate the multipart upload
response = s3.create_multipart_upload(Bucket=BUCKET_NAME, Key=UPLOAD_KEY)

# Retrieve the upload ID
upload_id = response['UploadId']

# Set the part size (5MB in this example)
part_size = 100 * 1024 * 1024
part_number = 1
parts = []

# Open the file
with open(FILE_PATH, 'rb') as file:
    while True:
        print("start upload part", part_number)

        # Read a part of the file
        data = file.read(part_size)

        if not data:
            break

        # Upload the part
        response = s3.upload_part(
            Body=data,
            Bucket=BUCKET_NAME,
            Key=UPLOAD_KEY,
            PartNumber=part_number,
            UploadId=upload_id
        )

        print("done upload part", part_number)

        # Store the ETag for later use
        parts.append({'PartNumber': part_number, 'ETag': response['ETag']})
        part_number += 1

# Complete the multipart upload
response = s3.complete_multipart_upload(
    Bucket=BUCKET_NAME,
    Key=UPLOAD_KEY,
    MultipartUpload={'Parts': parts},
    UploadId=upload_id
)

# Print the upload response
print("Response >>>>")
print("part_number", part_number)
print("parts", parts)
print(response)
