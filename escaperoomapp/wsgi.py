"""Configuração WSGI do projeto Escape Room."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escaperoomapp.settings')

application = get_wsgi_application()
