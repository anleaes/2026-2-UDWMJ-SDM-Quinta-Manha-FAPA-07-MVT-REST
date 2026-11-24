from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from .models import Pessoa
from .serializer import PessoaSerializer


@login_required(login_url='/contas/login/')
def list_pessoas(request):
    template_name = 'pessoas/list_pessoa.html'
    busca = request.GET.get('q', '').strip()
    pessoas = Pessoa.objects.filter()
    if busca:
        pessoas = pessoas.filter(Q(nome__icontains=busca) | Q(email__icontains=busca) | Q(telefone__icontains=busca))

    paginator = Paginator(pessoas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    parametros = request.GET.copy()
    parametros.pop('page', None)
    querystring = ('&' + parametros.urlencode()) if parametros else ''

    context = {
        'pessoas': page_obj,
        'page_obj': page_obj,
        'busca': busca,
        'querystring': querystring,
    }
    return render(request, template_name, context)


# --------------------------- REST -----------------------------

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
