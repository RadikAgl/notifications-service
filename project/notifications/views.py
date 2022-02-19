from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Client, Mailing, Message
from notifications.serializers import ClientSerializer, MailingSerializer, Statistics, StatisticsSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    Представление для создания, редактирования и просмотра клиентов
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    """Представление для создания, редактирования и просмотра рассылок"""
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()


class StatisticsList(APIView):
    """Представление для просмотра общей статистики по рассылкам"""
    def get(self, request):
        mailing_count = Mailing.objects.all().count()
        messages_count = Message.objects.all().count()
        sent_messages_count = Message.objects.filter(state='4').count()
        messages_in_progress_count = Message.objects.filter(state__in=['1', '2', '3']).count()
        error_messages_count = Message.objects.filter(state='5').count()
        statistics = Statistics(
            mailing_count=mailing_count,
            total_messages_count=messages_count,
            sent_messages_count=sent_messages_count,
            error_messages_count=error_messages_count,
            messages_in_progress_count=messages_in_progress_count
        )
        serializer = StatisticsSerializer(statistics)
        return Response(serializer.data)
