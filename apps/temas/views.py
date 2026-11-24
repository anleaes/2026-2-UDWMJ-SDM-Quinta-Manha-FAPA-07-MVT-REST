from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import TemaForm
from .models import Tema
from .serializer import TemaSerializer


@login_required(login_url='/contas/login/')
def add_tema(request):
    template_name = 'temas/add_tema.html'
    context = {}
    if request.method == 'POST':
        form = TemaForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Tema cadastrado com sucesso.')
            return redirect('temas:list_temas')
    else:
        form = TemaForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_temas(request):
    template_name = 'temas/list_tema.html'
    busca = request.GET.get('q', '').strip()
    temas = Tema.objects.filter()
    if busca:
        temas = temas.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca) | Q(ambientacao__icontains=busca))

    paginator = Paginator(temas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'temas': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_tema(request, id_tema):
    template_name = 'temas/add_tema.html'
    context = {}
    tema = get_object_or_404(Tema, id=id_tema)
    if request.method == 'POST':
        form = TemaForm(request.POST, request.FILES, instance=tema)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tema atualizado com sucesso.')
            return redirect('temas:list_temas')
    else:
        form = TemaForm(instance=tema)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_tema(request, id_tema):
    tema = get_object_or_404(Tema, id=id_tema)
    try:
        tema.delete()
        messages.success(request, 'Tema excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o tema está sendo usado por outros registros.')
    return redirect('temas:list_temas')


# --------------------------- REST -----------------------------

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer
