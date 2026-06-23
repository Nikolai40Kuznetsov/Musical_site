"""
URL configuration for jjango_start project.
"""
from django.contrib import admin
from django.urls import path, include
from kernel_app.views import page404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kernel_app.urls')),
]

handler404 = page404