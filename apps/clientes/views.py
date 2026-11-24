from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import ClienteForm
from .models import Cliente
from .serializer import ClienteSerializer


@login_required(login_url='/contas/login/')
def add_cliente(request):
    template_name = 'clientes/add_cliente.html'
    context = {}
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            return redirect('clientes:list_clientes')
    else:
        form = ClienteForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_clientes(request):
    template_name = 'clientes/list_cliente.html'
    busca = request.GET.get('q', '').strip()
    clientes = Cliente.objects.filter()
    if busca:
        clientes = clientes.filter(Q(nome__icontains=busca) | Q(email__icontains=busca) | Q(cpf__icontains=busca) | Q(cidade__icontains=busca) | Q(telefone__icontains=busca))

    paginator = Paginator(clientes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'clientes': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_cliente(request, id_cliente):
    template_name = 'clientes/add_cliente.html'
    context = {}
    cliente = get_object_or_404(Cliente, id=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso.')
            return redirect('clientes:list_clientes')
    else:
        form = ClienteForm(instance=cliente)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    try:
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o cliente está sendo usado por outros registros.')
    return redirect('clientes:list_clientes')


# --------------------------- REST -----------------------------

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
