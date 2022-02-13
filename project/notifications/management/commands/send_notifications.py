import json
import os

import requests
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

from notifications.models import Mailing, Client, Message

logger = get_task_logger(__name__)

load_dotenv()
TOKEN = os.getenv("TOKEN")
logger.info(f"TOKEN {TOKEN}")

def get_clients(mailing):
    operator = mailing.operator
    tag = mailing.tag

    return Client.objects.filter(operator=operator).filter(tag=tag)


def send_message(msg, data):
    try:
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': "Bearer " + TOKEN}
        response = requests.post(f'https://probe.fbrq.cloud/v1/send/{msg.id}',
                                 data=json.dumps(data),
                                 headers=headers, )
        logger.info(f'response: {response.status_code}')

        if response.status_code == 200:
            msg.state = 'ST'
        else:
            msg.state = 'SE'
    except requests.exceptions.RequestException:
        msg.state = 'SE'
    msg.save()


class Command(BaseCommand):
    help = "Запрос на отправку уведомления"

    def handle(self, *args, **options):
        now = timezone.now()

        mls = Mailing.objects.\
            filter(mailing_start_time__lte=now).\
            filter(mailing_end_time__gte=now).\
            filter(is_sent=False)
        if mls:
            mls = mls[0]
            mls.is_sent = True
            mls.save()
            clients = get_clients(mls)
            message = mls.message_text
            for client in clients:
                new_msg = Message.objects.create(sending_time=now, client=client, mailing=mls)
                data = {'id': new_msg.id, "phone": int(client.phone_number), "text": message}
                send_message(new_msg, data)
