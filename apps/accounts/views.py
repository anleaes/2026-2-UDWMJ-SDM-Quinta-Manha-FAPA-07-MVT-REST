from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import UserForm, UserChangeInformationForm


def add_user(request):
    template_name = 'accounts/add_user.html'
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            return redirect('accounts:user_login')
    else:
        form = UserForm()
    context['form'] = form
    return render(request, template_name, context)


def user_login(request):
    template_name = 'accounts/user_login.html'
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                next_url = '/'
            return redirect(next_url)
        context['erro'] = 'Usuário ou senha inválidos.'
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


@login_required(login_url='/contas/login/')
def user_change_password(request):
    template_name = 'accounts/user_change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('core:home')
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def user_change_information(request, username):
    template_name = 'accounts/user_change_information.html'
    context = {}
    # Cada usuário só pode alterar os próprios dados
    if username != request.user.username:
        return redirect('accounts:user_change_information', username=request.user.username)
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UserChangeInformationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = UserChangeInformationForm(instance=user)
    context['form'] = form
    return render(request, template_name, context)
