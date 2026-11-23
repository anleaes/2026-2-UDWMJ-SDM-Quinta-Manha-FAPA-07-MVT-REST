"""
Context processor: deixa o menu lateral e alguns links disponíveis em TODOS os templates.

Ideia: o menu é montado aqui, e só mostra os itens dos apps que JÁ estão instalados
(ou seja, cujo "include" já foi liberado em urls.py). Assim, quando cada pessoa liga o
seu app, o botão dele aparece sozinho no menu, sem precisar mexer no base.html.
"""
from django.apps import apps
from django.urls import NoReverseMatch, reverse

# (título do grupo, [(nome no menu, namespace do app, nome da url, ícone), ...])
MENU = [
    ('Visão geral', [
        ('Painel', 'core', 'core:home', 'i-dashboard'),
    ]),
    ('Operação', [
        ('Agendamentos', 'agendamentos', 'agendamentos:list_agendamentos', 'i-calendar'),
        ('Horários', 'horarios', 'horarios:list_horarios', 'i-clock'),
        ('Sessões', 'sessoes', 'sessoes:list_sessoes', 'i-play'),
        ('Pagamentos', 'pagamentos', 'pagamentos:list_pagamentos', 'i-card'),
        ('Avaliações', 'avaliacoes', 'avaliacoes:list_avaliacoes', 'i-star'),
    ]),
    ('Catálogo', [
        ('Salas', 'salas', 'salas:list_salas', 'i-door'),
        ('Temas', 'temas', 'temas:list_temas', 'i-mask'),
        ('Jogos', 'jogos', 'jogos:list_jogos', 'i-puzzle'),
    ]),
    ('Pessoas', [
        ('Clientes', 'clientes', 'clientes:list_clientes', 'i-user'),
        ('Funcionários', 'funcionarios', 'funcionarios:list_funcionarios', 'i-badge'),
        ('Participantes', 'participantes', 'participantes:list_participantes', 'i-ticket'),
        ('Grupos', 'grupos', 'grupos:list_grupos', 'i-group'),
        ('Todas as pessoas', 'pessoas', 'pessoas:list_pessoas', 'i-people'),
    ]),
]


def _url(nome):
    """Devolve a URL ou None se o app ainda não foi ligado em urls.py."""
    try:
        return reverse(nome)
    except NoReverseMatch:
        return None


def enigma(request):
    match = getattr(request, 'resolver_match', None)
    namespace_atual = match.namespace if match else ''

    grupos = []
    if request.user.is_authenticated:
        for titulo, itens in MENU:
            visiveis = []
            for nome, namespace, url_name, icone in itens:
                url = _url(url_name)
                if url:
                    visiveis.append({
                        'nome': nome,
                        'url': url,
                        'icone': icone,
                        'ativo': namespace == namespace_atual,
                    })
            if visiveis:
                grupos.append({'titulo': titulo, 'itens': visiveis})

    profile_url = None
    if request.user.is_authenticated:
        try:
            profile_url = reverse('accounts:user_change_information', args=[request.user.username])
        except NoReverseMatch:
            profile_url = None

    return {
        'menu_groups': grupos,
        'home_url': _url('core:home') or '/',
        'logout_url': _url('accounts:user_logout'),
        'password_url': _url('accounts:user_change_password'),
        'profile_url': profile_url,
        # lista com os apps instalados (usada para mostrar botões entre apps)
        'apps_ativos': [config.name for config in apps.get_app_configs()],
    }
