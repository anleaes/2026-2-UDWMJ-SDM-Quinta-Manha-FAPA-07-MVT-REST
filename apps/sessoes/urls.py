from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'sessoes'

router = routers.SimpleRouter()
router.register('api', views.SessaoViewSet, basename='sessao')

urlpatterns = [
    path('listar/', views.list_sessoes, name='list_sessoes'),
    path('adicionar/', views.add_sessao, name='add_sessao'),
    path('editar/<int:id_sessao>/', views.edit_sessao, name='edit_sessao'),
    path('excluir/<int:id_sessao>/', views.delete_sessao, name='delete_sessao'),
    path('iniciar/<int:id_sessao>/', views.start_sessao, name='start_sessao'),
    path('finalizar/<int:id_sessao>/', views.finish_sessao, name='finish_sessao'),

    # API REST (JSON): /sessoes/api/
    path('', include(router.urls)),
]
