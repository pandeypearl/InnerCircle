from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signUp', views.signUp, name='signUp'),
    path('signIn', views.signIn, name='signIn'),
    path('logout', views.logOut, name='logOut'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),

]