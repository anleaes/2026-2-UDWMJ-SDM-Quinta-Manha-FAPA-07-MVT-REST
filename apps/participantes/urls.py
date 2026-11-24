from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'participantes'

router = routers.SimpleRouter()
router.register('api', views.ParticipanteViewSet, basename='participante')

urlpatterns = [
    path('listar/', views.list_participantes, name='list_participantes'),
    path('adicionar/', views.add_participante, name='add_participante'),
    path('editar/<int:id_participante>/', views.edit_participante, name='edit_participante'),
    path('excluir/<int:id_participante>/', views.delete_participante, name='delete_participante'),

    # API REST (JSON): /participantes/api/
    path('', include(router.urls)),
]
