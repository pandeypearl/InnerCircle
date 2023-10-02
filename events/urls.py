from django.urls import path, include
from . import views

from rest_framework import routers
from .views import (
    EventListCreateView,
    RSVPListCreateView,
    EventDetailView,
    RSVPDetailView,
)

router = routers.DefaultRouter()

router.register(r'event', EventListCreateView)
router.register(r'rsvp', RSVPListCreateView)

urlpatterns = [
    path('event_list', views.event_list, name='event_list'),
    path('event_detail/<str:event_id>', views.event_detail, name='event_detail'),
    path('create_event', views.create_event, name='create_event'),
    path('update_event/<str:event_id>/edit', views.update_event, name='update_event'),
    path('delete_event/<str:pk>/delete', views.delete_event, name='delete_event'),
    path('rsvp/<int:event_id>/<int:member_id>/', views.rsvp_view, name='rsvp'),
    path('rsvp_done/<int:event_id>/<int:member_id>', views.rsvp_done, name='rsvp_done'),
    # API
    path('api/event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('api/rsvp/<int:pk>', RSVPDetailView.as_view(), name='rsvp-detail'),
]