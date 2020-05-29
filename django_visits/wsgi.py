"""
Точка входа проекта для WSGI-совместимых веб-серверов
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_visits.settings')

application = get_wsgi_application()
