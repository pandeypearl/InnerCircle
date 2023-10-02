from django.urls import path, include
from . import views

from rest_framework import routers
from .views import (
    MemberListCreateView,
    GroupListCreateView,
    NoteListCreateView,
    MemberDetailView,
    GroupDetailView,
    NoteDetailView,
)

router = routers.DefaultRouter()

router.register(r'member', MemberListCreateView)
router.register(r'group', GroupListCreateView)
router.register(r'note', NoteListCreateView)

urlpatterns = [
    path('group_list', views.group_list, name='group_list'),
    path('group_detail/<str:group_id>/', views.group_detail, name='group_detail'),
    path('create_group', views.create_group, name='create_group'),
    path('edit_group/<str:group_id>/edit', views.edit_group, name='edit_group'),
    path('delete_group/<str:pk>/delete', views.delete_group, name='delete_group'),
    path('member_list', views.member_list, name='member_list'),
    path('member_detail/<str:member_id>/', views.member_detail, name='member_detail'),
    path('create_member', views.create_member, name='create_member'),
    path('edit_member/<str:member_id>/edit', views.edit_member, name='edit_member'),
    path('delete_member/<str:pk>/delete', views.delete_member, name='delete_member'),
    # APi
    path('api/member/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('api/group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('api/note/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
]