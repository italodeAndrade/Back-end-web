import logging
from django.shortcuts import render, redirect
from .forms import ClienteForm
from django.contrib.auth.hashers import check_password
from .models import Cliente
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login
logger = logging.getLogger(__name__)
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth import logout
import logging


def user_logout(request):
    username = request.user.username if request.user.is_authenticated else "Usuário anônimo"
    logger.info(f"[Logout] Usuário '{username}' fez logout.")
    logout(request)
    return redirect('filmes:inicio')

def register(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"[{datetime.now()}] Novo cliente registrado: {form.cleaned_data['email']} do IP: {request.META.get('REMOTE_ADDR')}")
            return redirect('users:login')
        else:
            logger.warning(f"[{datetime.now()}] Falha no registro - formulário inválido do IP: {request.META.get('REMOTE_ADDR')}")
    else:
        form = ClienteForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        logger.info(f"[Login] Tentativa de login recebida para o email: {email}")

        try:
            cliente = Cliente.objects.get(email=email)

            if check_password(password, cliente.password):  # Verifica a senha
                auth_login(request, cliente)  # Loga o cliente
                
                # Certifique-se de que o grupo 'Clientes' existe
                clientes_group, created = Group.objects.get_or_create(name='Clientes')
                if not cliente.groups.filter(name='Clientes').exists():
                    cliente.groups.add(clientes_group)
                    logger.info(f"[Login] Usuário '{email}' adicionado ao grupo 'Clientes'")

                logger.info(f"[Login] Login bem-sucedido para o cliente: {email} (ID: {cliente.id})")
                return redirect(reverse('filmes:inicio'))
            else:
                logger.warning(f"[Login] Senha incorreta para o cliente: {email}")
                return render(request, 'users/login.html', {'error': 'Senha incorreta'})

        except Cliente.DoesNotExist:
            logger.error(f"[Login] Email não encontrado: {email}")
            return render(request, 'users/login.html', {'error': 'Email não encontrado'})

    logger.error("[Login] Método inválido na requisição de login.")
    return render(request, 'users/login.html', {'error': 'Método inválido'})



def home(request):
    logger.info(f"[{datetime.now()}] Acesso à home pelo IP: {request.META.get('REMOTE_ADDR')}")
    return render(request, 'users/home.html')
