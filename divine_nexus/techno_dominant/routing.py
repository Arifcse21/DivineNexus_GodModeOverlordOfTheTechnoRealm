from django.urls import path
from techno_dominant.consumers import DominantConsumer

websocket_urlpatterns = [
    path("ws/command/", DominantConsumer.as_asgi(), name="ws-command"),
]
