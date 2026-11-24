from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'salas'

router = routers.SimpleRouter()
router.register('api', views.SalaViewSet, basename='sala')

urlpatterns = [
    path('listar/', views.list_salas, name='list_salas'),
    path('adicionar/', views.add_sala, name='add_sala'),
    path('editar/<int:id_sala>/', views.edit_sala, name='edit_sala'),
    path('excluir/<int:id_sala>/', views.delete_sala, name='delete_sala'),

    # API REST (JSON): /salas/api/
    path('', include(router.urls)),
]
