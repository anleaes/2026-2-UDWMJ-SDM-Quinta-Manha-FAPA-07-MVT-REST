from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'clientes'

router = routers.SimpleRouter()
router.register('api', views.ClienteViewSet, basename='cliente')

urlpatterns = [
    path('listar/', views.list_clientes, name='list_clientes'),
    path('adicionar/', views.add_cliente, name='add_cliente'),
    path('editar/<int:id_cliente>/', views.edit_cliente, name='edit_cliente'),
    path('excluir/<int:id_cliente>/', views.delete_cliente, name='delete_cliente'),

    # API REST (JSON): /clientes/api/
    path('', include(router.urls)),
]
