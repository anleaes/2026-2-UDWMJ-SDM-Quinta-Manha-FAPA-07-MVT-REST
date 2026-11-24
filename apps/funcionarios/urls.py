from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'funcionarios'

router = routers.SimpleRouter()
router.register('api', views.FuncionarioViewSet, basename='funcionario')

urlpatterns = [
    path('listar/', views.list_funcionarios, name='list_funcionarios'),
    path('adicionar/', views.add_funcionario, name='add_funcionario'),
    path('editar/<int:id_funcionario>/', views.edit_funcionario, name='edit_funcionario'),
    path('excluir/<int:id_funcionario>/', views.delete_funcionario, name='delete_funcionario'),

    # API REST (JSON): /funcionarios/api/
    path('', include(router.urls)),
]
