"""
Конфигурация URL-ов проекта
"""
from django.urls import path, include


urlpatterns = [
    path('api/', include('api.urls')),
]
