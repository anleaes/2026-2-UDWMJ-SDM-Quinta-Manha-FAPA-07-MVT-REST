from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'jogos'

router = routers.SimpleRouter()
router.register('api', views.JogoViewSet, basename='jogo')

urlpatterns = [
    path('listar/', views.list_jogos, name='list_jogos'),
    path('adicionar/', views.add_jogo, name='add_jogo'),
    path('editar/<int:id_jogo>/', views.edit_jogo, name='edit_jogo'),
    path('excluir/<int:id_jogo>/', views.delete_jogo, name='delete_jogo'),

    # API REST (JSON): /jogos/api/
    path('', include(router.urls)),
]
