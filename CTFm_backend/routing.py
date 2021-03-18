from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from djangochannelsrestframework.consumers import view_as_consumer
from notification.consumers import NotificationListConsumer
from challenge.consumers import ChangllengeConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/api/v1/notification/$", NotificationListConsumer.as_asgi()),
            url(r"^ws/api/v1/challenge/$", ChangllengeConsumer.as_asgi()),
        ])
    ),
 })