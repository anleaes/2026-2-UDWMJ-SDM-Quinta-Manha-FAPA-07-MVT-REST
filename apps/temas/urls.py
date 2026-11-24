from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'temas'

router = routers.SimpleRouter()
router.register('api', views.TemaViewSet, basename='tema')

urlpatterns = [
    path('listar/', views.list_temas, name='list_temas'),
    path('adicionar/', views.add_tema, name='add_tema'),
    path('editar/<int:id_tema>/', views.edit_tema, name='edit_tema'),
    path('excluir/<int:id_tema>/', views.delete_tema, name='delete_tema'),

    # API REST (JSON): /temas/api/
    path('', include(router.urls)),
]
