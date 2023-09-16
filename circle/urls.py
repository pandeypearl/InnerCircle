from django.urls import path
from . import views

urlpatterns = [
    path('group_list', views.group_list, name='group_list'),
    path('group_detail/<str:group_id>/', views.group_detail, name='group_detail'),
    path('create_group', views.create_group, name='create_group'),
    path('edit_group/<str:pk>/edit', views.edit_group, name='edit_group'),
    path('member_list', views.member_list, name='member_list'),
    path('member_detail/<str:member_id>/', views.member_detail, name='member_detail'),
    path('create_member', views.create_member, name='create_member'),
    path('edit_member/<str:pk>/edit', views.edit_member, name='edit_member'),
]