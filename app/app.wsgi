import sys
sys.path.append('/var/www/django/app/');
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
