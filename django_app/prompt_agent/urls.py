"""URL configuration for the prompt agent app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/submit/', views.submit_prompt_ajax, name='submit_prompt_ajax'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<int:pk>/edit/', views.session_edit, name='session_edit'),
    path('history/', views.history, name='history'),
    path('prompt/<int:pk>/', views.prompt_detail, name='prompt_detail'),
]
