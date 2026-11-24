from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import ParticipanteForm
from .models import Participante
from .serializer import ParticipanteSerializer


@login_required(login_url='/contas/login/')
def add_participante(request):
    template_name = 'participantes/add_participante.html'
    context = {}
    if request.method == 'POST':
        form = ParticipanteForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Participante cadastrado com sucesso.')
            return redirect('participantes:list_participantes')
    else:
        form = ParticipanteForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_participantes(request):
    template_name = 'participantes/list_participante.html'
    busca = request.GET.get('q', '').strip()
    participantes = Participante.objects.filter()
    if busca:
        participantes = participantes.filter(Q(nome__icontains=busca) | Q(email__icontains=busca) | Q(documento__icontains=busca))

    paginator = Paginator(participantes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'participantes': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_participante(request, id_participante):
    template_name = 'participantes/add_participante.html'
    context = {}
    participante = get_object_or_404(Participante, id=id_participante)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST, request.FILES, instance=participante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participante atualizado com sucesso.')
            return redirect('participantes:list_participantes')
    else:
        form = ParticipanteForm(instance=participante)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_participante(request, id_participante):
    participante = get_object_or_404(Participante, id=id_participante)
    try:
        participante.delete()
        messages.success(request, 'Participante excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o participante está sendo usado por outros registros.')
    return redirect('participantes:list_participantes')


# --------------------------- REST -----------------------------

class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer
