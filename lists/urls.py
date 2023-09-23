from django.urls import path
from . import views

urlpatterns = [
    path('lists', views.lists, name='lists'),
    path('list_detail/<str:list_id>', views.list_detail, name='list_detail'),
    path('create_list', views.create_list, name='create_list'),
    path('edit_list/<str:list_id>/edit', views.edit_list, name='edit_list'),
    path('delete_list/<str:pk>/delete', views.delete_list, name='delete_list'),
]