"""URL Configuration for the prompt agent application."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_app.prompt_agent.urls')),
]
