from notification.models import Notification
from notification import serializers
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin
)

class NotificationConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Notification.objects.all()
    serializer_class = serializers.Notification
    permission_classes = (permissions.IsAuthenticated,)