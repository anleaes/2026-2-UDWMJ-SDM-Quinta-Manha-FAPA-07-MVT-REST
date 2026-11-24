from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'agendamentos'

router = routers.SimpleRouter()
router.register('api', views.AgendamentoViewSet, basename='agendamento')

urlpatterns = [
    path('listar/', views.list_agendamentos, name='list_agendamentos'),
    path('adicionar/', views.add_agendamento, name='add_agendamento'),
    path('editar/<int:id_agendamento>/', views.edit_agendamento, name='edit_agendamento'),
    path('excluir/<int:id_agendamento>/', views.delete_agendamento, name='delete_agendamento'),
    path('cancelar/<int:id_agendamento>/', views.cancel_agendamento, name='cancel_agendamento'),

    # API REST (JSON): /agendamentos/api/
    path('', include(router.urls)),
]
