from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import GrupoForm
from .models import Grupo
from .serializer import GrupoSerializer


@login_required(login_url='/contas/login/')
def add_grupo(request):
    template_name = 'grupos/add_grupo.html'
    context = {}
    if request.method == 'POST':
        form = GrupoForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Grupo cadastrado com sucesso.')
            return redirect('grupos:list_grupos')
    else:
        form = GrupoForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_grupos(request):
    template_name = 'grupos/list_grupo.html'
    busca = request.GET.get('q', '').strip()
    grupos = Grupo.objects.all().select_related('cliente').prefetch_related('participantes')
    if busca:
        grupos = grupos.filter(Q(nome__icontains=busca) | Q(cliente__nome__icontains=busca))

    paginator = Paginator(grupos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'grupos': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_grupo(request, id_grupo):
    template_name = 'grupos/add_grupo.html'
    context = {}
    grupo = get_object_or_404(Grupo, id=id_grupo)
    if request.method == 'POST':
        form = GrupoForm(request.POST, request.FILES, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo atualizado com sucesso.')
            return redirect('grupos:list_grupos')
    else:
        form = GrupoForm(instance=grupo)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_grupo(request, id_grupo):
    grupo = get_object_or_404(Grupo, id=id_grupo)
    try:
        grupo.delete()
        messages.success(request, 'Grupo excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o grupo está sendo usado por outros registros.')
    return redirect('grupos:list_grupos')


# --------------------------- REST -----------------------------

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
