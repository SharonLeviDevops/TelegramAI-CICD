import json
import time
import boto3
from botocore.exceptions import ClientError
from loguru import logger
from utils import search_download_youtube_video
import os

env = os.environ['ENV']
with open(f'config-{env}.json') as f:
    config = json.load(f)

sqs = boto3.resource('sqs', region_name=config.get('aws_region'))
queue = sqs.get_queue_by_name(
    QueueName=config.get('bot_to_worker_queue_name')
)

s3 = boto3.client("s3")


def process_msg(msg):
    videos = search_download_youtube_video(msg)

    for video in videos:
        name = video['filename']
        s3.upload_file(name, config.get('videos_bucket'), name)
        os.remove(name)
        logger.info(f'{name} has been successfully uploaded')


def main():
    while True:
        try:
            messages = queue.receive_messages(
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )
            for msg in messages:
                logger.info(f'processing message {msg}')
                process_msg(msg.body)

                # delete message from the queue after is was handled
                response = queue.delete_messages(Entries=[{
                    'Id': msg.message_id,
                    'ReceiptHandle': msg.receipt_handle
                }])
                if 'Successful' in response:
                    logger.info(f'msg {msg} has been handled successfully')

        except ClientError as err:
            logger.exception(f"Couldn't receive messages {err}")
            time.sleep(10)


def lambda_handler(event, context):
    logger.info(f'New event {event}')

    for record in event['Records']:
        process_msg(str(record["body"]))


if __name__ == '__main__':
    main()
