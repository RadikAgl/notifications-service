import json
import os

import requests
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

from notifications.models import Mailing, Message


load_dotenv()
logger = get_task_logger(__name__)

TOKEN = os.getenv("TOKEN")
logger.info(f"token {TOKEN}")


class Command(BaseCommand):
    help = "Запрос на отправку уведомления"

    def handle(self, *args, **options):
        messages = get_messages()

        if messages:
            for message in messages:
                data = {'id': message.id, "phone": int(message.client.phone_number),
                        "text": message.mailing.message_text}
                send_message(message, data)


def get_messages():
    return Message.objects.filter(state__in=['1', '2', '3'])


def send_message(msg, data):
    try:
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': "Bearer " + "TOKEN"}
        response = requests.post(f'https://probe.fbrq.cloud/v1/send/{msg.id}',
                                 data=json.dumps(data),
                                 headers=headers,)

        if response.status_code == 200:
            msg.state = '4'  # state = 'sent'
            msg.sending_time = timezone.now()
        elif msg.state == '3':  # 'last attempt'
            msg.state = '5'  # 'send error'
        else:
            msg.state = str(int(msg.state) + 1)

    except requests.exceptions.RequestException:
        if msg.state == '3':
            msg.state = '5'  # 'send error'
        else:
            msg.state = str(int(msg.state) + 1)
    msg.save()
