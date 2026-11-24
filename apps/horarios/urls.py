from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'horarios'

router = routers.SimpleRouter()
router.register('api', views.HorarioViewSet, basename='horario')

urlpatterns = [
    path('listar/', views.list_horarios, name='list_horarios'),
    path('adicionar/', views.add_horario, name='add_horario'),
    path('editar/<int:id_horario>/', views.edit_horario, name='edit_horario'),
    path('excluir/<int:id_horario>/', views.delete_horario, name='delete_horario'),

    # API REST (JSON): /horarios/api/
    path('', include(router.urls)),
]
