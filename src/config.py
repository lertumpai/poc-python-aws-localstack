from dotenv import load_dotenv
import os

load_dotenv()

env = {
    "ENDPOINT_URL": os.getenv('ENDPOINT_URL'),
    "AWS_ACCESS_KEY_ID": os.getenv('AWS_ACCESS_KEY_ID'),
    "AWS_SECRET_ACCESS_KEY": os.getenv('AWS_SECRET_ACCESS_KEY'),
    "AWS_REGION": os.getenv('AWS_REGION'),
    "BUCKET_NAME": os.getenv('BUCKET_NAME'),
    "UPLOAD_KEY": os.getenv('UPLOAD_KEY'),
    "FILE_PATH": os.getenv('FILE_PATH'),
    "PART_SIZE_IN_MB": os.getenv('PART_SIZE_IN_MB')
}
