from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from apps.loja.models import Pedido

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('email'),
                            password=request.POST.get('senha'))
        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        messages.error(request, _('E-mail ou senha incorretos.'))
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:home')

@login_required
def dashboard(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'accounts/dashboard.html', {'pedidos': pedidos})
