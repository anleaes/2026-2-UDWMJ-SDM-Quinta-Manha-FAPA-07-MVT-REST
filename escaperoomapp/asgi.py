"""Configuração ASGI do projeto Escape Room."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escaperoomapp.settings')

application = get_asgi_application()
