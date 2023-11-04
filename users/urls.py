'''
    Script mapping URLS to specific views in the users application.
'''

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

from rest_framework import routers
from .views import (
    UserListCreateView,
    ProfileListCreateView,
    UserDetailView,
    ProfileDetailView,
)

router = routers.DefaultRouter()

router.register(r'user', UserListCreateView)
router.register(r'profile', ProfileListCreateView)

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('help', views.help, name='help'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('signUp', views.signUp, name='signUp'),
    path('signIn', views.signIn, name='signIn'),
    path('logout', views.logOut, name='logOut'),
    path('settings/<str:profile_id>/', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('search', views.search, name='search_results'),
    path('reminders', views.reminders, name='reminders'),
    path('notifications', views.notifications, name='notifications'),
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Change Password
    path('password_change/', views.custom_password_change, name='password_change'),
    path('password_change/done/', views.custom_password_change_done, name='password_change_done'),
    # Deactivate Account
    path('deactivate_account/', views.deactivate_account, name='deactivate_account'),
    path('account_deactivated/', views.account_deactivated, name='account_deactivated'),
    # API
    path('api/user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
]