'''
    Script mapping URLS to specific views in the assistant application.
'''
from django.urls import path
from . import views

urlpatterns = [
    path('assistant', views.assistant, name='assistant'),
    path('chat_history', views.chat_history, name='chat_history'),
]