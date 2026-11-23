from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse
from django.utils import timezone


def _modelo(app_label, nome):
    """Busca um model pelo nome. Devolve None se o app ainda não está instalado."""
    try:
        return apps.get_model(app_label, nome)
    except LookupError:
        return None


def _url(nome):
    try:
        return reverse(nome)
    except NoReverseMatch:
        return None


def _brl(valor):
    """Formata como dinheiro brasileiro: 1234.5 -> R$ 1.234,50"""
    texto = f'{valor or 0:,.2f}'
    return 'R$ ' + texto.replace(',', 'X').replace('.', ',').replace('X', '.')


@login_required(login_url='/contas/login/')
def home(request):
    template_name = 'core/home.html'
    hoje = timezone.localdate()

    Sala = _modelo('salas', 'Sala')
    Jogo = _modelo('jogos', 'Jogo')
    Cliente = _modelo('clientes', 'Cliente')
    Horario = _modelo('horarios', 'Horario')
    Agendamento = _modelo('agendamentos', 'Agendamento')
    Pagamento = _modelo('pagamentos', 'Pagamento')
    Sessao = _modelo('sessoes', 'Sessao')
    Avaliacao = _modelo('avaliacoes', 'Avaliacao')

    # Cartões de números (só aparecem os dos apps já instalados)
    cards = []
    if Sala:
        cards.append({'label': 'Salas ativas', 'valor': Sala.objects.filter(ativa=True).count(),
                      'icone': 'i-door', 'url': _url('salas:list_salas')})
    if Jogo:
        cards.append({'label': 'Jogos ativos', 'valor': Jogo.objects.filter(ativo=True).count(),
                      'icone': 'i-puzzle', 'url': _url('jogos:list_jogos')})
    if Cliente:
        cards.append({'label': 'Clientes', 'valor': Cliente.objects.count(),
                      'icone': 'i-user', 'url': _url('clientes:list_clientes')})
    if Agendamento:
        ativos = Agendamento.objects.exclude(status='cancelado').count()
        cards.append({'label': 'Reservas ativas', 'valor': ativos,
                      'icone': 'i-calendar', 'url': _url('agendamentos:list_agendamentos')})
    if Pagamento:
        total = Pagamento.objects.filter(status='pago').aggregate(s=Sum('valor'))['s']
        cards.append({'label': 'Receita recebida', 'valor': _brl(total),
                      'icone': 'i-coin', 'url': _url('pagamentos:list_pagamentos')})
    if Sessao:
        cards.append({'label': 'Sessões concluídas', 'valor': Sessao.objects.filter(status='concluida').count(),
                      'icone': 'i-flag', 'url': _url('sessoes:list_sessoes')})
    if Avaliacao:
        media = Avaliacao.objects.aggregate(m=Avg('nota'))['m']
        cards.append({'label': 'Nota média', 'valor': f'{media:.1f}'.replace('.', ',') if media else '—',
                      'icone': 'i-star', 'url': _url('avaliacoes:list_avaliacoes')})

    # Próximos horários livres
    proximos = None
    if Horario:
        proximos = (Horario.objects
                    .filter(data__gte=hoje, status='disponivel')
                    .select_related('jogo', 'jogo__sala')
                    .order_by('data', 'hora_inicio')[:6])

    # Últimas reservas
    ultimos = None
    if Agendamento:
        ultimos = (Agendamento.objects
                   .select_related('cliente', 'horario', 'horario__jogo')
                   .order_by('-criado_em')[:6])

    # Reservas por situação (barras)
    por_status = None
    if Agendamento:
        contagem = dict(Agendamento.objects.values_list('status').annotate(q=Count('id')))
        maior = max(contagem.values()) if contagem else 0
        por_status = []
        for valor, nome in Agendamento.STATUS_CHOICES:
            qtd = contagem.get(valor, 0)
            por_status.append({
                'status': valor,
                'label': nome,
                'qtd': qtd,
                'pct': int(qtd * 100 / maior) if maior else 0,
            })

    context = {
        'hoje': hoje,
        'cards': cards,
        'proximos': proximos,
        'ultimos': ultimos,
        'por_status': por_status,
        'url_novo_agendamento': _url('agendamentos:add_agendamento'),
        'url_novo_horario': _url('horarios:add_horario'),
    }
    return render(request, template_name, context)
