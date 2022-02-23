from django.utils import timezone
from rest_framework.decorators import action
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Client, Mailing, Message
from notifications.serializers import ClientSerializer, MailingSerializer, \
    Statistics, StatisticsSerializer, StatisticsDetailSerializer, StatisticsDetailSerializer


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

    @action(detail=False, methods=['get'], url_path='active')
    def get_active_mailing(self, request):
        now = timezone.now()
        queryset = Mailing.objects. \
            filter(mailing_end_time__gte=now). \
            filter(is_sent=False)
        serializer = MailingSerializer(queryset, many=True)
        return Response(serializer.data)


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


class StatisticsDetail(APIView):
    """Представление для просмотра детальной статистики по рассылкам"""
    def get(self, request, pk):
        mailing = Mailing.objects.filter(id=pk)[0]
        messages_count = Message.objects.filter(mailing=mailing).count()
        sent_messages_count = Message.objects.filter(mailing=mailing).filter(state='4').count()
        messages_in_progress_count = Message.objects.filter(mailing=mailing).filter(state__in=['1', '2', '3']).count()
        error_messages_count = Message.objects.filter(mailing=mailing).filter(state='5').count()

        statistics = StatisticsDetail(
            mailing_text=mailing.message_text,
            total_messages_count=messages_count,
            sent_messages_count=sent_messages_count,
            error_messages_count=error_messages_count,
            messages_in_progress_count=messages_in_progress_count
        )
        serializer = StatisticsDetailSerializer(statistics)

        return Response(serializer.data)
