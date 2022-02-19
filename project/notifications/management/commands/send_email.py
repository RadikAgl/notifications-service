from django.core.mail import mail_admins
from django.core.management.base import BaseCommand, CommandError

from notifications.models import Mailing, Message


class Command(BaseCommand):
    help = "Отправка статистики на почту"

    def handle(self, *args, **options):
        mailing_count = Mailing.objects.all().count()
        mailing_sent_count = Mailing.objects.filter(is_sent=True).count()
        messages_sent_count = Message.objects.all().count()
        messages_count = Message.objects.filter(state='4').count()
        error_messages_count = Message.objects.filter(state='4').count()

        message = (f'Общее количество рассылок: {mailing_count}'
                   f'Количество завершенных рассылок: {mailing_sent_count}'
                   f'Количество подготовленных сообщений: {messages_sent_count}'
                   f'Общее количество отправленных сообщений: {messages_count}'
                   f'Количество неотправленных сообщений: {error_messages_count}')
        subject = 'Общая статистика по рассылкам'
        mail_admins(subject=subject, message=message, html_message=None)

        self.stdout.write("Статистика отправлена на почту")

