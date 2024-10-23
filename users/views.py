import logging
from django.shortcuts import render, redirect
from .forms import ClienteForm
from django.contrib.auth.hashers import check_password
from .models import Cliente
from django.urls import reverse
import uuid

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"Novo cliente registrado com sucesso: {form.cleaned_data['email']}")
            return redirect('users:login')
        else:
            logger.warning("Falha ao registrar novo cliente. Formulário inválido.")
    else:
        form = ClienteForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            cliente = Cliente.objects.get(email=email)
            logger.info(f"Cliente encontrado com email: {email}")

            if check_password(senha, cliente.senha):
                # Gera um token único usando uuid
                token = str(uuid.uuid4())
                logger.info(f"Login bem-sucedido para o cliente: {email}. Token gerado: {token}")
                
                # Armazena o token na sessão do usuário
                request.session['auth_token'] = token
                
                return redirect(reverse('filmes:lista_filmes'))
            else:
                logger.warning(f"Tentativa de login com senha incorreta para o cliente: {email}")
                return render(request, 'users/login.html', {'error': 'Senha incorreta'})
        
        except Cliente.DoesNotExist:
            logger.error(f"Tentativa de login com email não registrado: {email}")
            return render(request, 'users/login.html', {'error': 'Email não encontrado'})
    
    return render(request, 'users/login.html')

def home(request):
    logger.info("Acesso à home.")
    return render(request, 'users/home.html')
