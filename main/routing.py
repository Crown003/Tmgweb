from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path("ws/ac/", consumers.MyAsyncConsumer.as_asgi()),
    re_path(
        r"ws/notification/(?P<room_name>\w+)/$",
        consumers.NotificationConsumer.as_asgi(),
    ),
]
