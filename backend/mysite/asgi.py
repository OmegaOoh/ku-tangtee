"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

django_asgi_app = get_asgi_application()

from channels import auth, routing
from chat import routing as chat_routing

application = routing.ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": auth.AuthMiddlewareStack(
        routing.URLRouter(
            chat_routing.websocket_urlpatterns
        )
    )
})
