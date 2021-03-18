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

    async def websocket_connect(self, message):

        # Super Save
        await super().websocket_connect(message)

        # Initialized operation
        await self.model_change.subscribe()

    # Subscribing
    @model_observer(models.Notification)
    async def model_change(self, message, action=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return serializers.NotificationSerializer(instance).data
