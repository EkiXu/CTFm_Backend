from notification import models
from notification import serializers
from djangochannelsrestframework.permissions import AllowAny
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.mixins import ListModelMixin,RetrieveModelMixin
from djangochannelsrestframework.observer import model_observer

class NotificationListConsumer(ListModelMixin,ObserverModelInstanceMixin,GenericAsyncAPIConsumer):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = (AllowAny,)

    # Subscribing
    @model_observer(models.Notification)
    async def model_activity(self, message, observer=None, **kwargs):
        # send activity to your frontend
        await self.send_json(message)
