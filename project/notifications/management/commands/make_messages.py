import os

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from notifications.models import Mailing, Client, Message


class Command(BaseCommand):
    help = "Подготовка сообщений"

    def handle(self, *args, **options):
        now = timezone.now()

        mailings = Mailing.objects. \
            filter(mailing_start_time__lte=now). \
            filter(mailing_end_time__gte=now). \
            filter(is_sent=False)

        if mailings:
            for mailing in mailings:
                clients = get_clients(mailing)
                for client in clients:
                    Message.objects.create(client=client, mailing=mailing, state='1')
                mailing.is_sent = True
                mailing.save()


def get_clients(mailing):
    operator = mailing.operator
    tag = mailing.tag

    return Client.objects.filter(operator=operator).filter(tag=tag)

