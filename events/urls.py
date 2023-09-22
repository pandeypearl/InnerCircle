from django.urls import path
from . import views

urlpatterns = [
    path('event_list', views.event_list, name='event_list'),
    path('event_detail/<str:event_id>', views.event_detail, name='event_detail'),
    path('create_event', views.create_event, name='create_event'),
    path('update_event/<str:event_id>/edit', views.update_event, name='update_event'),
    path('delete_event/<str:pk>/delete', views.delete_event, name='delete_event'),
    path('rsvp/<int:event_id>/<int:member_id>/', views.rsvp_view, name='rsvp'),
    path('rsvp_done/<str:event_id>/', views.rsvp_done, name='rsvp_done'),
]