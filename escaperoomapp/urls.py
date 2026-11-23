"""URLs gerais do projeto. Cada app tem o seu próprio urls.py."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- URLS DOS APPS ---
    # Cada pessoa remove o "#" somente da linha do(s) seu(s) app(s).

    path('', include('core.urls', namespace='core')),

    path('contas/', include('accounts.urls', namespace='accounts')),

    # path('pessoas/', include('pessoas.urls', namespace='pessoas')),

    # path('clientes/', include('clientes.urls', namespace='clientes')),

    # path('funcionarios/', include('funcionarios.urls', namespace='funcionarios')),

    # path('participantes/', include('participantes.urls', namespace='participantes')),

    # path('salas/', include('salas.urls', namespace='salas')),

    # path('temas/', include('temas.urls', namespace='temas')),

    # path('jogos/', include('jogos.urls', namespace='jogos')),

    # path('horarios/', include('horarios.urls', namespace='horarios')),

    # path('grupos/', include('grupos.urls', namespace='grupos')),

    # path('agendamentos/', include('agendamentos.urls', namespace='agendamentos')),

    # path('pagamentos/', include('pagamentos.urls', namespace='pagamentos')),

    # path('sessoes/', include('sessoes.urls', namespace='sessoes')),

    # path('avaliacoes/', include('avaliacoes.urls', namespace='avaliacoes')),
]

# Caminho dos arquivos enviados por upload (fotos e documentos)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
