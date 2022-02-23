from rest_framework import serializers

from notifications.models import Client, Mailing


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone_number', 'operator', 'tag', 'timezone']


class MailingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mailing
        fields = ['id', 'message_text', 'mailing_start_time', 'mailing_end_time', 'operator', 'tag']


class Statistics:
    def __init__(self,
                 mailing_count=0,
                 total_messages_count=0,
                 sent_messages_count=0,
                 not_sent_messages_count=0,
                 error_messages_count=0,
                 messages_in_progress_count=0):
        self.mailing_count = mailing_count
        self.total_messages_count = total_messages_count
        self.sent_messages_count = sent_messages_count
        self.not_sent_messages_count = not_sent_messages_count
        self.error_messages_count = error_messages_count
        self.messages_in_progress_count = messages_in_progress_count


class StatisticsSerializer(serializers.Serializer):
    mailing_count = serializers.IntegerField()
    total_messages_count = serializers.IntegerField()
    sent_messages_count = serializers.IntegerField()
    error_messages_count = serializers.IntegerField()
    messages_in_progress_count = serializers.IntegerField()


class StatisticsDetail:
    def __init__(self,
                 mailing_text,
                 total_messages_count=0,
                 sent_messages_count=0,
                 not_sent_messages_count=0,
                 error_messages_count=0,
                 messages_in_progress_count=0):
        self.mailing_text = mailing_text
        self.total_messages_count = total_messages_count
        self.sent_messages_count = sent_messages_count
        self.not_sent_messages_count = not_sent_messages_count
        self.error_messages_count = error_messages_count
        self.messages_in_progress_count = messages_in_progress_count


class StatisticsDetailSerializer(serializers.Serializer):
    mailing_text = serializers.CharField()
    total_messages_count = serializers.IntegerField()
    sent_messages_count = serializers.IntegerField()
    error_messages_count = serializers.IntegerField()
    messages_in_progress_count = serializers.IntegerField()
