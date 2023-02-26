import os
import telebot
from botocore.exceptions import ClientError
from loguru import logger
import boto3
import json


class Bot:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token, threaded=False)
        self.bot.set_update_listener(self._bot_internal_handler)

        self.current_msg = None

    def _bot_internal_handler(self, messages):
        """Bot internal messages handler"""
        for message in messages:
            self.current_msg = message
            self.handle_message(message)

    def start(self):
        """Start polling msgs from users, this function never returns"""
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        logger.info('Telegram Bot information')
        logger.info(self.bot.get_me())

        self.bot.infinity_polling()

    def send_text(self, text):
        self.bot.send_message(self.current_msg.chat.id, text)

    def send_text_with_quote(self, text, message_id):
        self.bot.send_message(self.current_msg.chat.id, text, reply_to_message_id=message_id)

    def is_current_msg_photo(self):
        return self.current_msg.content_type == 'photo'

    def download_user_photo(self, quality=0):
        """
        Downloads photos sent to the Bot to `photos` directory (should be existed)
        :param quality: integer representing the file quality. Allowed values are [0, 1, 2]
        :return:
        """
        if self.current_msg.content_type != 'photo':
            raise RuntimeError(f'Message content of type \'photo\' expected, but got {self.current_msg["content_type"]}')

        file_info = self.bot.get_file(self.current_msg.photo[quality].file_id)
        data = self.bot.download_file(file_info.file_path)

        with open(file_info.file_path, 'wb') as f:
            f.write(data)

    def handle_message(self, message):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {message}')
        self.send_text(f'Your original message: {message.text}')


class QuoteBot(Bot):
    def handle_message(self, message):
        if message.text != 'Don\'t quote me please':
            self.send_text_with_quote(message.text, message_id=message.message_id)


class YoutubeBot(Bot):
    def handle_message(self, message):
        if self.current_msg.content_type == 'photo':
            self.download_user_photo(quality=2)
        else:
            try:
                response = workers_queue.send_message(
                    MessageBody=message.text,
                    MessageAttributes={
                        'chat_id': {'StringValue': str(message.chat.id), 'DataType': 'String'}
                    }
                )
                logger.info(f'msg {response.get("MessageId")} has been sent to queue')
                self.send_text('Your message is being processed...')
            except ClientError as error:
                logger.error(error)
                self.send_text('Something went wrong, please try again...')


def get_telegram_token_secret():
    secrets_manager = boto3.client('secretsmanager', region_name=config.get('aws_region'))
    secret_value = secrets_manager.get_secret_value(
        SecretId=config.get('telegram_token_secret_name')
    )
    return json.loads(secret_value['SecretString'])['telegramToken']


if __name__ == '__main__':
    env = os.environ['ENV']
    with open(f'config-{env}.json') as f:
        config = json.load(f)

    sqs = boto3.resource('sqs', region_name=config.get('aws_region'))
    workers_queue = sqs.get_queue_by_name(
        QueueName=config.get('bot_to_worker_queue_name')
    )

    telegram_token = get_telegram_token_secret()

    my_bot = YoutubeBot(telegram_token)
    my_bot.start()
