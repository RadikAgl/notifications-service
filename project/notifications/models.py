import pytz
from django.core.validators import RegexValidator
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Client(ExportModelOperationsMixin('client'), models.Model):
    """"Модель клиента"""
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone_regex = RegexValidator(
        regex=r"^7\+?1?\d{10}$",
        message="Номер телефона должен быть в формате: '7ХХХХХХХХХХ', где Х - цифры от 0 до 9"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True, verbose_name='номер телефона')
    operator = models.PositiveIntegerField(verbose_name='код оператора')
    tag = models.CharField(max_length=20, verbose_name='тег')
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return f'{self.phone_number}'


class Mailing(ExportModelOperationsMixin('mailing'), models.Model):
    """Модель рассылки"""
    message_text = models.TextField(verbose_name='Текст сообщения')
    mailing_start_time = models.DateTimeField(verbose_name='дата и время старта рассылки')
    mailing_end_time = models.DateTimeField(verbose_name='дата и время окончания рассылки')
    operator = models.PositiveIntegerField(verbose_name='код оператора')
    tag = models.CharField(max_length=20, verbose_name='тег')
    is_sent = models.BooleanField(default=False, verbose_name='рассылка завершена')

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailing'

    def __str__(self):
        return self.message_text[:20]


class Message(ExportModelOperationsMixin('message'), models.Model):
    """Модель сообщения"""
    STATES = [
        ('1', 'ready'),
        ('2', 'in progress'),
        ('3', 'in progress'),
        ('4', 'sent'),
        ('5', 'send error'),
    ]
    sending_time = models.DateTimeField(null=True, blank=True, verbose_name='время отправки сообщения')
    client = models.ForeignKey(Client, verbose_name='клиент', on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, verbose_name='рассылка', on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATES, default='1', verbose_name='статус сообщения')
