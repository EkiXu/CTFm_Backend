from notification.models import Notification
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from notification import serializers
# Create your views here.

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Notification viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdminNotificationViewSet(viewsets.ModelViewSet):
    """
    Notification viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAdminUser]