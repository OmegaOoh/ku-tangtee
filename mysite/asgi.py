"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels import routing, auth
from chat import routing as chat_routing
from activities import routing as act_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = routing.ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": auth.AuthMiddlewareStack(
        routing.URLRouter(
            chat_routing.websocket_urlpatterns + act_routing.websocket_urlpatterns
        )
    )
})
