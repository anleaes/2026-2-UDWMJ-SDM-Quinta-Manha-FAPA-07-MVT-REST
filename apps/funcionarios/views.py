from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import FuncionarioForm
from .models import Funcionario
from .serializer import FuncionarioSerializer


@login_required(login_url='/contas/login/')
def add_funcionario(request):
    template_name = 'funcionarios/add_funcionario.html'
    context = {}
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Funcionário cadastrado com sucesso.')
            return redirect('funcionarios:list_funcionarios')
    else:
        form = FuncionarioForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_funcionarios(request):
    template_name = 'funcionarios/list_funcionario.html'
    busca = request.GET.get('q', '').strip()
    funcionarios = Funcionario.objects.filter()
    if busca:
        funcionarios = funcionarios.filter(Q(nome__icontains=busca) | Q(email__icontains=busca) | Q(matricula__icontains=busca))

    paginator = Paginator(funcionarios, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'funcionarios': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_funcionario(request, id_funcionario):
    template_name = 'funcionarios/add_funcionario.html'
    context = {}
    funcionario = get_object_or_404(Funcionario, id=id_funcionario)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso.')
            return redirect('funcionarios:list_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id=id_funcionario)
    try:
        funcionario.delete()
        messages.success(request, 'Funcionário excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o funcionário está sendo usado por outros registros.')
    return redirect('funcionarios:list_funcionarios')


# --------------------------- REST -----------------------------

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
