from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from djangochannelsrestframework.consumers import view_as_consumer
from notification.consumers import NotificationConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^notification/$", view_as_consumer(NotificationConsumer)),
        ])
    ),
 })