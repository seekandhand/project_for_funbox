import os

import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'django_visits.settings'

django.setup()
