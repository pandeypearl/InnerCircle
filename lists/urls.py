from django.urls import path, include
from . import views

from rest_framework import routers
from .views import ListListCreateView, ListItemListCreateView, CheckItemListCreateView

router.register(r'list', ListListCreateView)
router.register(r'list_item', ListItemListCreateView)
router.register(r'check_item', CheckItemListCreateView)

urlpatterns = [
    path('lists', views.lists, name='lists'),
    path('list_detail/<str:list_id>', views.list_detail, name='list_detail'),
    path('create_list', views.create_list, name='create_list'),
    path('edit_list/<str:list_id>/edit', views.edit_list, name='edit_list'),
    path('delete_list/<str:pk>/delete', views.delete_list, name='delete_list'),
    path('check_list/<int:list_id>/<int:recipient_id>/', views.check_list_item, name='check_list'),
    # API
    path('api/', include(router.urls)),
]