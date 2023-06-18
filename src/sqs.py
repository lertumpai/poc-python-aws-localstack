import boto3
import time

from config import env


class SQS:
    def __init__(self):
        self.isRunning = False
        self.sqs = boto3.client(
            'sqs',
            endpoint_url=env["ENDPOINT_URL"],
            region_name=env["AWS_REGION"],
            aws_access_key_id=env["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"]
        )

    def start(self):
        self.isRunning = True
        while self.isRunning:
            print("Read message", self.isRunning)

            # Receive messages from the SQS queue
            response = self.sqs.receive_message(
                QueueUrl=env["QUEUE_URL"],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5
            )

            # Process received messages
            for message in response.get('Messages', []):
                # Print the message body
                print('Received message:', message['Body'])

                # Delete the message from the queue
                self.sqs.delete_message(
                    QueueUrl=env["QUEUE_URL"],
                    ReceiptHandle=message['ReceiptHandle']
                )

            # Add a delay before the next poll
            time.sleep(1)

    def stop(self):
        self.isRunning = False
