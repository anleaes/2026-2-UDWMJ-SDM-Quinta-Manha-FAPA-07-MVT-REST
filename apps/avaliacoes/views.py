from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from sessoes.models import Sessao

from .forms import AvaliacaoForm
from .models import Avaliacao
from .serializer import AvaliacaoSerializer


@login_required(login_url='/contas/login/')
def add_avaliacao(request):
    template_name = 'avaliacoes/add_avaliacao.html'
    context = {}
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Avaliação cadastrada com sucesso.')
            return redirect('avaliacoes:list_avaliacoes')
    else:
        # Permite abrir o formulário já preenchido (ex.: ?sessao=3)
        initial = {chave: request.GET[chave] for chave in ('sessao', 'cliente') if request.GET.get(chave)}
        # Se veio de uma sessão, já sugere o cliente da reserva
        if initial.get('sessao') and not initial.get('cliente'):
            sessao = Sessao.objects.filter(pk=initial['sessao']).select_related('agendamento').first()
            if sessao:
                initial['cliente'] = sessao.agendamento.cliente_id

        form = AvaliacaoForm(initial=initial)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_avaliacoes(request):
    template_name = 'avaliacoes/list_avaliacao.html'
    busca = request.GET.get('q', '').strip()
    avaliacoes = Avaliacao.objects.all().select_related('cliente', 'sessao', 'sessao__agendamento__horario__jogo')
    if busca:
        avaliacoes = avaliacoes.filter(Q(comentario__icontains=busca) | Q(cliente__nome__icontains=busca) | Q(sessao__codigo__icontains=busca))

    paginator = Paginator(avaliacoes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'avaliacoes': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_avaliacao(request, id_avaliacao):
    template_name = 'avaliacoes/add_avaliacao.html'
    context = {}
    avaliacao = get_object_or_404(Avaliacao, id=id_avaliacao)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, request.FILES, instance=avaliacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avaliação atualizada com sucesso.')
            return redirect('avaliacoes:list_avaliacoes')
    else:
        form = AvaliacaoForm(instance=avaliacao)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_avaliacao(request, id_avaliacao):
    avaliacao = get_object_or_404(Avaliacao, id=id_avaliacao)
    try:
        avaliacao.delete()
        messages.success(request, 'Avaliação excluída com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: a avaliação está sendo usada por outros registros.')
    return redirect('avaliacoes:list_avaliacoes')


# --------------------------- REST -----------------------------

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
