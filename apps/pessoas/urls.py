from django.urls import path
from . import views

app_name = 'pessoas'

urlpatterns = [
    path('listar/', views.list_pessoas, name='list_pessoas'),
]
