from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'pessoas'

router = routers.SimpleRouter()
router.register('api', views.PessoaViewSet, basename='pessoa')

urlpatterns = [
    path('listar/', views.list_pessoas, name='list_pessoas'),

    # API REST (JSON): /pessoas/api/
    path('', include(router.urls)),
]
