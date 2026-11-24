from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .forms import HorarioForm
from .models import Horario
from .serializer import HorarioSerializer


@login_required(login_url='/contas/login/')
def add_horario(request):
    template_name = 'horarios/add_horario.html'
    context = {}
    if request.method == 'POST':
        form = HorarioForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            messages.success(request, 'Horário cadastrado com sucesso.')
            return redirect('horarios:list_horarios')
    else:
        # Permite abrir o formulário já preenchido (ex.: ?jogo=3)
        initial = {chave: request.GET[chave] for chave in ('jogo',) if request.GET.get(chave)}
        form = HorarioForm(initial=initial)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_horarios(request):
    template_name = 'horarios/list_horario.html'
    busca = request.GET.get('q', '').strip()
    horarios = Horario.objects.all().select_related('jogo', 'jogo__sala')
    if busca:
        horarios = horarios.filter(Q(jogo__nome__icontains=busca) | Q(jogo__sala__nome__icontains=busca))
    status = request.GET.get('status', '')
    if status:
        horarios = horarios.filter(status=status)

    paginator = Paginator(horarios, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'horarios': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
        'status': status,
        'status_choices': Horario.STATUS_CHOICES,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_horario(request, id_horario):
    template_name = 'horarios/add_horario.html'
    context = {}
    horario = get_object_or_404(Horario, id=id_horario)
    if request.method == 'POST':
        form = HorarioForm(request.POST, request.FILES, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário atualizado com sucesso.')
            return redirect('horarios:list_horarios')
    else:
        form = HorarioForm(instance=horario)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_horario(request, id_horario):
    horario = get_object_or_404(Horario, id=id_horario)
    try:
        horario.delete()
        messages.success(request, 'Horário excluído com sucesso.')
    except ProtectedError:
        messages.error(request, 'Não é possível excluir: o horário está sendo usado por outros registros.')
    return redirect('horarios:list_horarios')


# --------------------------- REST -----------------------------

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
