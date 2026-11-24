from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'grupos'

router = routers.SimpleRouter()
router.register('api', views.GrupoViewSet, basename='grupo')

urlpatterns = [
    path('listar/', views.list_grupos, name='list_grupos'),
    path('adicionar/', views.add_grupo, name='add_grupo'),
    path('editar/<int:id_grupo>/', views.edit_grupo, name='edit_grupo'),
    path('excluir/<int:id_grupo>/', views.delete_grupo, name='delete_grupo'),

    # API REST (JSON): /grupos/api/
    path('', include(router.urls)),
]
