from django.urls import path, include
from . import views

from rest_framework import routers
from.views import BroadcastListCreateView, BroadcastDetailView

router = routers.DefaultRouter()

router.register(r'broadcast', BroadcastListCreateView)

urlpatterns = [
    path('broadcast_list', views.broadcast_list, name='broadcast_list'),
    path('broadcast_detail/<str:broadcast_id>', views.broadcast_detail, name='broadcast_detail'),
    path('create_broadcast', views.create_broadcast, name='create_broadcast'),
    path('send_broadcast_draft/<int:draft_id>/', views.send_broadcast_draft, name='send_broadcast_draft'),
    path('edit_broadcast/<str:broadcast_id>/edit', views.edit_broadcast, name='edit_broadcast'),
    path('delete_broadcast/<str:pk>/delete', views.delete_broadcast, name='delete_broadcast'),
    path('read_broadcast/<int:broadcast_id>/<int:member_id>/', views.read_broadcast, name='read_broadcast'),
    #API
    path('api/broadcast/<int:pk>/', BroadcastDetailView.as_view(), name='broadcast-detail')
]