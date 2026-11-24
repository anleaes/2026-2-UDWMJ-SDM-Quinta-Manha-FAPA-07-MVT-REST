from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import JogoForm
from .models import Jogo
from .serializer import JogoSerializer


@login_required(login_url='/contas/login/')
def add_jogo(request):
    template_name = 'jogos/add_jogo.html'
    context = {}
    if request.method == 'POST':
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Jogo cadastrado com sucesso.')
            return redirect('jogos:list_jogos')
    else:
        form = JogoForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_jogos(request):
    template_name = 'jogos/list_jogo.html'
    busca = request.GET.get('q', '').strip()
    jogos = Jogo.objects.all().select_related('sala', 'tema')
    if busca:
        jogos = jogos.filter(Q(nome__icontains=busca) | Q(sala__nome__icontains=busca) | Q(tema__nome__icontains=busca) | Q(historia__icontains=busca))

    paginator = Paginator(jogos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'jogos': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_jogo(request, id_jogo):
    template_name = 'jogos/add_jogo.html'
    context = {}
    jogo = get_object_or_404(Jogo, id=id_jogo)
    if request.method == 'POST':
        form = JogoForm(request.POST, request.FILES, instance=jogo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo atualizado com sucesso.')
            return redirect('jogos:list_jogos')
    else:
        form = JogoForm(instance=jogo)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_jogo(request, id_jogo):
    jogo = get_object_or_404(Jogo, id=id_jogo)
    try:
        jogo.delete()
        messages.success(request, 'Jogo excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o jogo está sendo usado por outros registros.')
    return redirect('jogos:list_jogos')


# --------------------------- REST -----------------------------

class JogoViewSet(viewsets.ModelViewSet):
    queryset = Jogo.objects.all()
    serializer_class = JogoSerializer
