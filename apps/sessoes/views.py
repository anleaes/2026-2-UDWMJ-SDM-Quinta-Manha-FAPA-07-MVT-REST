from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.utils import timezone

from .forms import SessaoForm
from .models import Sessao
from .serializer import SessaoSerializer


@login_required(login_url='/contas/login/')
def add_sessao(request):
    template_name = 'sessoes/add_sessao.html'
    context = {}
    if request.method == 'POST':
        form = SessaoForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Sessão cadastrada com sucesso.')
            return redirect('sessoes:list_sessoes')
    else:
        # Permite abrir o formulário já preenchido (ex.: ?agendamento=3)
        initial = {chave: request.GET[chave] for chave in ('agendamento',) if request.GET.get(chave)}
        form = SessaoForm(initial=initial)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_sessoes(request):
    template_name = 'sessoes/list_sessao.html'
    busca = request.GET.get('q', '').strip()
    sessoes = Sessao.objects.all().select_related('agendamento', 'agendamento__cliente', 'agendamento__horario__jogo', 'funcionario')
    if busca:
        sessoes = sessoes.filter(Q(codigo__icontains=busca) | Q(agendamento__cliente__nome__icontains=busca) | Q(agendamento__horario__jogo__nome__icontains=busca) | Q(funcionario__nome__icontains=busca))
    status = request.GET.get('status', '')
    if status:
        sessoes = sessoes.filter(status=status)

    paginator = Paginator(sessoes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'sessoes': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
        'status': status,
        'status_choices': Sessao.STATUS_CHOICES,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_sessao(request, id_sessao):
    template_name = 'sessoes/add_sessao.html'
    context = {}
    sessao = get_object_or_404(Sessao, id=id_sessao)
    if request.method == 'POST':
        form = SessaoForm(request.POST, request.FILES, instance=sessao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sessão atualizada com sucesso.')
            return redirect('sessoes:list_sessoes')
    else:
        form = SessaoForm(instance=sessao)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_sessao(request, id_sessao):
    sessao = get_object_or_404(Sessao, id=id_sessao)
    try:
        sessao.delete()
        messages.success(request, 'Sessão excluída com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: a sessão está sendo usada por outros registros.')
    return redirect('sessoes:list_sessoes')


@login_required(login_url='/contas/login/')
def start_sessao(request, id_sessao):
    sessao = get_object_or_404(Sessao, id=id_sessao)
    if sessao.status == 'agendada':
        sessao.status = 'em_andamento'
        sessao.inicio_real = timezone.now()
        sessao.save()
        messages.success(request, 'Sessão iniciada. Boa sorte aos jogadores!')
    return redirect('sessoes:list_sessoes')


@login_required(login_url='/contas/login/')
def finish_sessao(request, id_sessao):
    sessao = get_object_or_404(Sessao, id=id_sessao)
    if sessao.status == 'em_andamento':
        sessao.status = 'concluida'
        sessao.fim_real = timezone.now()
        sessao.save()
        messages.success(request, 'Sessão finalizada. Agora registre o resultado e a pontuação.')
        return redirect('sessoes:edit_sessao', id_sessao=sessao.id)
    return redirect('sessoes:list_sessoes')


# --------------------------- REST -----------------------------

class SessaoViewSet(viewsets.ModelViewSet):
    queryset = Sessao.objects.all()
    serializer_class = SessaoSerializer
