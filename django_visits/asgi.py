"""
Точка входа проекта для ASGI-совместимых веб-серверов
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_visits.settings')

application = get_asgi_application()
