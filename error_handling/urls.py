'''
    Script mapping URLS to specific views in the error_handling application.
'''
from django.urls import path
from . import views

urlpatterns = [
    path('custom_400/', views.custom_400, name='custom_400'),
    path('custom_401/', views.custom_401, name='custom_401'),
    path('custom_403/', views.custom_403, name='custom_403'),
    path('custom_404/', views.custom_404, name='custom_404'),
    path('custom_405/', views.custom_405, name='custom_405'),
    path('custom_408/', views.custom_408, name='custom_408'),
    path('custom_500/', views.custom_500, name='custom_500'),
]
