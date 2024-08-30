from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os
import main.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(main.routing.websocket_urlpatterns)),
    }
)
