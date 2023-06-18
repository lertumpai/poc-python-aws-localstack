import asyncio
import os

from s3_multipart_async import create_multipart_upload, complete_multipart_upload, upload_part
from config import env


async def upload_file_to_s3(file_path=""):
    upload_id = await create_multipart_upload()
    part_size = int(env["PART_SIZE_IN_MB"]) * 1024 * 1024
    part_number = 1
    parts = []
    upload_parts = []

    # Open the file
    with open(file_path, 'rb') as file:
        while True:
            # Read a part of the file
            data = file.read(part_size)

            if not data:
                break

            # create list of upload the part
            upload_parts.append(
                upload_part(
                    part_number=part_number,
                    data=data,
                    upload_id=upload_id
                )
            )
            part_number += 1

    # await all upload part and gather results
    results = await asyncio.gather(*upload_parts)

    # Store the ETag for later use
    for result in results:
        parts.append(result)

    await complete_multipart_upload(
        parts=parts,
        upload_id=upload_id
    )

    print("Done...")
