from django.urls import path
from . import views

urlpatterns = [
    path('assistant', views.assistant, name='assistant'),
    path('chat_history', views.chat_history, name='chat_history'),
]