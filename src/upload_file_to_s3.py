import asyncio
import os

from s3_multipart_async import S3Client


class UploadFileToS3:
    def __init__(self, s3: S3Client):
        self.s3 = s3

    async def execute(self, file_path=""):
        await self.s3.create_multipart_upload()  # Set the part size (5MB in this example)
        part_size = 100 * 1024 * 1024
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
                    self.s3.upload_part(
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

        await self.s3.complete_multipart_upload(
            parts=parts
        )

        print("Done...")
