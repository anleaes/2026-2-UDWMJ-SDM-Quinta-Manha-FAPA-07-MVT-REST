from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import SalaForm
from .models import Sala
from .serializer import SalaSerializer


@login_required(login_url='/contas/login/')
def add_sala(request):
    template_name = 'salas/add_sala.html'
    context = {}
    if request.method == 'POST':
        form = SalaForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Sala cadastrada com sucesso.')
            return redirect('salas:list_salas')
    else:
        form = SalaForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_salas(request):
    template_name = 'salas/list_sala.html'
    busca = request.GET.get('q', '').strip()
    salas = Sala.objects.filter()
    if busca:
        salas = salas.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca))

    paginator = Paginator(salas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'salas': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_sala(request, id_sala):
    template_name = 'salas/add_sala.html'
    context = {}
    sala = get_object_or_404(Sala, id=id_sala)
    if request.method == 'POST':
        form = SalaForm(request.POST, request.FILES, instance=sala)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sala atualizada com sucesso.')
            return redirect('salas:list_salas')
    else:
        form = SalaForm(instance=sala)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_sala(request, id_sala):
    sala = get_object_or_404(Sala, id=id_sala)
    try:
        sala.delete()
        messages.success(request, 'Sala excluída com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: a sala está sendo usada por outros registros.')
    return redirect('salas:list_salas')


# --------------------------- REST -----------------------------

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
