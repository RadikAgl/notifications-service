from django.core.management import call_command

from celery import shared_task


@shared_task
def send_email():
    call_command("send_email", )


@shared_task
def send_mailing():
    call_command("send_notifications", )


@shared_task
def make_messages():
    call_command('make_messages', )