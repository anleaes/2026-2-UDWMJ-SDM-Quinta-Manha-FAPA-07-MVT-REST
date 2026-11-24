from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from agendamentos.models import Agendamento

from .forms import PagamentoForm
from .models import Pagamento
from .serializer import PagamentoSerializer


@login_required(login_url='/contas/login/')
def add_pagamento(request):
    template_name = 'pagamentos/add_pagamento.html'
    context = {}
    if request.method == 'POST':
        form = PagamentoForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Pagamento cadastrado com sucesso.')
            return redirect('pagamentos:list_pagamentos')
    else:
        # Permite abrir o formulário já preenchido (ex.: ?agendamento=3)
        initial = {chave: request.GET[chave] for chave in ('agendamento',) if request.GET.get(chave)}
        # Se veio de uma reserva, já sugere o valor que falta pagar
        if initial.get('agendamento'):
            reserva = Agendamento.objects.filter(pk=initial['agendamento']).first()
            if reserva and reserva.saldo > 0:
                initial['valor'] = reserva.saldo

        form = PagamentoForm(initial=initial)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_pagamentos(request):
    template_name = 'pagamentos/list_pagamento.html'
    busca = request.GET.get('q', '').strip()
    pagamentos = Pagamento.objects.all().select_related('agendamento', 'agendamento__cliente')
    if busca:
        pagamentos = pagamentos.filter(Q(codigo_transacao__icontains=busca) | Q(agendamento__codigo__icontains=busca) | Q(agendamento__cliente__nome__icontains=busca))
    status = request.GET.get('status', '')
    if status:
        pagamentos = pagamentos.filter(status=status)

    paginator = Paginator(pagamentos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'pagamentos': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
        'status': status,
        'status_choices': Pagamento.STATUS_CHOICES,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_pagamento(request, id_pagamento):
    template_name = 'pagamentos/add_pagamento.html'
    context = {}
    pagamento = get_object_or_404(Pagamento, id=id_pagamento)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, request.FILES, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso.')
            return redirect('pagamentos:list_pagamentos')
    else:
        form = PagamentoForm(instance=pagamento)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_pagamento(request, id_pagamento):
    pagamento = get_object_or_404(Pagamento, id=id_pagamento)
    try:
        pagamento.delete()
        messages.success(request, 'Pagamento excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o pagamento está sendo usado por outros registros.')
    return redirect('pagamentos:list_pagamentos')


# --------------------------- REST -----------------------------

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
