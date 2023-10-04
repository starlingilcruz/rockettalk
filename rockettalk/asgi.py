"""
ASGI config for rockettalk project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from whitenoise import WhiteNoise

from apps.chats import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rockettalk.settings')
# Importing Django ASGI application early to avoid issues importing dependent code
django_asgi_app =  get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    routing.websocket_urlpatterns
                )
            )
        )
    }
)