from django.urls import path
from rest_framework.routers import DefaultRouter

from notifications.views import ClientViewSet, MailingViewSet, StatisticsList

router = DefaultRouter()
router.register('clients', ClientViewSet, basename='clients')
router.register('mailing', MailingViewSet, basename='mailing')
urlpatterns = router.urls
urlpatterns.append(path('statistics/', StatisticsList.as_view(), name='statistics'))