import os

# Ensure the settings module is set for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Schoolweb.settings')

# Load the Django WSGI application
from django.core.wsgi import get_wsgi_application

# The WSGI callable that gunicorn will use
app = get_wsgi_application()
