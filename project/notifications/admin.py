from django.contrib import admin

from notifications.models import Client, Mailing


class ClientAdmin(admin.ModelAdmin):
    """Отображение клиентов в интерфейсе администратора"""
    list_display = ['id', 'phone_number', 'timezone']


class MailingAdmin(admin.ModelAdmin):
    """Отображение рассылок в интерфейсе администратора"""
    list_display = ['message_text', 'mailing_start_time', 'mailing_end_time']


admin.site.register(Client, ClientAdmin)
admin.site.register(Mailing, MailingAdmin)