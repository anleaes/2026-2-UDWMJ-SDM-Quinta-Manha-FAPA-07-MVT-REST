from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'avaliacoes'

router = routers.SimpleRouter()
router.register('api', views.AvaliacaoViewSet, basename='avaliacao')

urlpatterns = [
    path('listar/', views.list_avaliacoes, name='list_avaliacoes'),
    path('adicionar/', views.add_avaliacao, name='add_avaliacao'),
    path('editar/<int:id_avaliacao>/', views.edit_avaliacao, name='edit_avaliacao'),
    path('excluir/<int:id_avaliacao>/', views.delete_avaliacao, name='delete_avaliacao'),

    # API REST (JSON): /avaliacoes/api/
    path('', include(router.urls)),
]
