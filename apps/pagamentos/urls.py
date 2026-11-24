from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'pagamentos'

router = routers.SimpleRouter()
router.register('api', views.PagamentoViewSet, basename='pagamento')

urlpatterns = [
    path('listar/', views.list_pagamentos, name='list_pagamentos'),
    path('adicionar/', views.add_pagamento, name='add_pagamento'),
    path('editar/<int:id_pagamento>/', views.edit_pagamento, name='edit_pagamento'),
    path('excluir/<int:id_pagamento>/', views.delete_pagamento, name='delete_pagamento'),

    # API REST (JSON): /pagamentos/api/
    path('', include(router.urls)),
]
