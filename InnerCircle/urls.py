"""
URL configuration for InnerCircle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('circle.urls')),
    path('', include('events.urls')),
    path('', include('broadcasts.urls')),
    path('', include('lists.urls')),
    path('', include('assistant.urls')),
    path('', include('error_handling.urls')),
    path('api/', include(router.urls)),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# configuring custom error views
handler400 = 'error_handling.views.custom_400'
handler401 = 'error_handling.views.custom_401'
handler403 = 'error_handling.views.custom_403'
handler404 = 'error_handling.views.custom_404'
handler405 = 'error_handling.views.custom_405'
handler408 = 'error_handling.views.custom_408'
handler500 = 'error_handling.views.custom_500'
    