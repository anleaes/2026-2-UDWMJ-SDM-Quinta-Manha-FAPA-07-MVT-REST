from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import AgendamentoForm
from .models import Agendamento
from .serializer import AgendamentoSerializer


@login_required(login_url='/contas/login/')
def add_agendamento(request):
    template_name = 'agendamentos/add_agendamento.html'
    context = {}
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Agendamento cadastrado com sucesso.')
            return redirect('agendamentos:list_agendamentos')
    else:
        # Permite abrir o formulário já preenchido (ex.: ?horario=3)
        initial = {chave: request.GET[chave] for chave in ('horario', 'cliente') if request.GET.get(chave)}
        form = AgendamentoForm(initial=initial)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_agendamentos(request):
    template_name = 'agendamentos/list_agendamento.html'
    busca = request.GET.get('q', '').strip()
    agendamentos = Agendamento.objects.all().select_related('cliente', 'horario', 'horario__jogo')
    if busca:
        agendamentos = agendamentos.filter(Q(codigo__icontains=busca) | Q(codigo_confirmacao__icontains=busca) | Q(cliente__nome__icontains=busca) | Q(horario__jogo__nome__icontains=busca))
    status = request.GET.get('status', '')
    if status:
        agendamentos = agendamentos.filter(status=status)

    paginator = Paginator(agendamentos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'agendamentos': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
        'status': status,
        'status_choices': Agendamento.STATUS_CHOICES,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_agendamento(request, id_agendamento):
    template_name = 'agendamentos/add_agendamento.html'
    context = {}
    agendamento = get_object_or_404(Agendamento, id=id_agendamento)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, request.FILES, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso.')
            return redirect('agendamentos:list_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_agendamento(request, id_agendamento):
    agendamento = get_object_or_404(Agendamento, id=id_agendamento)
    try:
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o agendamento está sendo usado por outros registros.')
    return redirect('agendamentos:list_agendamentos')


@login_required(login_url='/contas/login/')
def cancel_agendamento(request, id_agendamento):
    agendamento = get_object_or_404(Agendamento, id=id_agendamento)
    if agendamento.status in ('pendente', 'confirmado'):
        agendamento.status = 'cancelado'
        agendamento.save()  # o model devolve as vagas ao horário
        messages.success(request, 'Reserva cancelada. As vagas voltaram para o horário.')
    else:
        messages.error(request, 'Só é possível cancelar reservas pendentes ou confirmadas.')
    return redirect('agendamentos:list_agendamentos')


# --------------------------- REST -----------------------------

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
