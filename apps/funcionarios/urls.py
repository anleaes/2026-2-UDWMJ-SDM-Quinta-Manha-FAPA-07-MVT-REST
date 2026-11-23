from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    path('listar/', views.list_funcionarios, name='list_funcionarios'),
    path('adicionar/', views.add_funcionario, name='add_funcionario'),
    path('editar/<int:id_funcionario>/', views.edit_funcionario, name='edit_funcionario'),
    path('excluir/<int:id_funcionario>/', views.delete_funcionario, name='delete_funcionario'),
]
