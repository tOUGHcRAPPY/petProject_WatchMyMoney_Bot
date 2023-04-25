from django.urls import path

from app.telegram.views import webhook

urlpatterns = [
    path("", webhook),
]