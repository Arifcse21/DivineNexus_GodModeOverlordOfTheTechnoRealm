from django.urls import path
from techno_dominant.views import *

urlpatterns = [
    path("cli/", DominantCliView.as_view(), name="cli-list-create"),
    path("cli/<int:pk>/", DominantCliRetView.as_view(), name="cli-retrieve"),
    path("cli/clear/", ClearCliHistoryView.as_view(), name="clear-command-hitstory"),
]