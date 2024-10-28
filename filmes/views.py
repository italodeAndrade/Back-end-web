import logging
import random
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.hashers import check_password
from .models import Cliente, Filme
from django.urls import reverse
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
def get_username(request):
    return request.user.email if request.user.is_authenticated else "Usuário anônimo"

@login_required
def lista_filmes(request):
    if not request.user.groups.filter(name='Clientes').exists():
        logger.warning(f"[Lista Filmes] Usuário '{request.user.email}' não pertence ao grupo 'Clientes'. Acesso negado.")
        return HttpResponseForbidden("Acesso negado.")
    
    key_words = ['space', 'love', 'war', 'future', 'dark', 'light', 'dream', 'city', "lost", "crime"]
    termo = random.choice(key_words)
    url = f'http://www.omdbapi.com/?s={termo}&apikey=19cee984'
    user = get_username(request)
    logger.info(f"[Lista Filmes] Usuário '{user}' requisitou URL: {url} com termo '{termo}'")

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        filmes_externos = data.get('Search', [])
        logger.info(f"[Lista Filmes] Usuário '{user}' encontrou {len(filmes_externos)} filmes com termo '{termo}'")
    else:
        filmes_externos = []
        logger.error(f"[Lista Filmes] Usuário '{user}' encontrou erro na requisição para URL {url}: Status {response.status_code}")

    filmes = Filme.objects.all()
    return render(request, 'filmes/lista_filmes.html', {'filmes': filmes, 'filmes_externos': filmes_externos})

@login_required
def lista_pessoal(request):
    if not request.user.groups.filter(name='Clientes').exists():
        logger.warning(f"[Lista Pessoal] Usuário '{request.user.email}' não pertence ao grupo 'Clientes'. Acesso negado.")
        return HttpResponseForbidden("Acesso negado.")
    
    filmes_pessoais = request.session.get('filmes_pessoais', [])
    username = get_username(request)
    logger.info(f"[Lista Pessoal] Usuário '{username}' acessou a lista pessoal de filmes. Total de filmes: {len(filmes_pessoais)}")
    return render(request, 'filmes/lista_pessoal.html', {'filmes_pessoais': filmes_pessoais})

@login_required
def adicionar_filme_pessoal(request, filme_id):
    if not request.user.groups.filter(name='Clientes').exists():
        logger.warning(f"[Adicionar Filme Pessoal] Usuário '{request.user.email}' não pertence ao grupo 'Clientes'. Acesso negado.")
        return HttpResponseForbidden("Acesso negado.")
    
    filme = request.POST.get('filme_nome')
    filmes_pessoais = request.session.get('filmes_pessoais', [])
    filmes_pessoais.append(filme)
    request.session['filmes_pessoais'] = filmes_pessoais

    username = get_username(request)
    logger.info(f"[Adicionar Filme Pessoal] Usuário '{username}' adicionou filme '{filme}' à lista pessoal. Total de filmes: {len(filmes_pessoais)}")
    
    return redirect('filmes:lista_pessoal')

@login_required
def remover_filme_pessoal(request, filme_nome):
    if not request.user.groups.filter(name='Clientes').exists():
        logger.warning(f"[Remover Filme Pessoal] Usuário '{request.user.email}' não pertence ao grupo 'Clientes'. Acesso negado.")
        return HttpResponseForbidden("Acesso negado.")

    filmes_pessoais = request.session.get('filmes_pessoais', [])
    username = get_username(request)
    
    if filme_nome in filmes_pessoais:
        filmes_pessoais.remove(filme_nome)
        request.session['filmes_pessoais'] = filmes_pessoais
        logger.info(f"[Remover Filme Pessoal] Usuário '{username}' removeu o filme '{filme_nome}' da lista pessoal. Total de filmes: {len(filmes_pessoais)}")
    else:
        logger.warning(f"[Remover Filme Pessoal] Usuário '{username}' tentou remover filme '{filme_nome}' que não está na lista pessoal.")
    
    return redirect('filmes:lista_pessoal')

@login_required
def verificar_senha(request):
    if request.method == 'POST':
        senha = request.POST.get('senha')
        username = get_username(request)

        if not request.user.is_authenticated:
            logger.error(f"[Verificar Senha] Usuário não autenticado tentou verificar senha.")
            return JsonResponse({'success': False, 'error': 'Usuário não autenticado.'})

        cliente = request.user
        logger.info(f"[Verificar Senha] Usuário '{username}' verificando senha.")

        if check_password(senha, cliente.password):
            logger.info(f"[Verificar Senha] Senha verificada com sucesso para usuário '{username}' (ID: {cliente.id})")
            return JsonResponse({'success': True})
        else:
            logger.warning(f"[Verificar Senha] Senha incorreta para usuário '{username}' (ID: {cliente.id})")
            return JsonResponse({'success': False, 'error': 'Senha incorreta'})

    logger.error(f"[Verificar Senha] Usuário '{username}' realizou uma requisição de método inválido")
    return JsonResponse({'success': False, 'error': 'Método inválido'})

def inicio(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Clientes').exists():
            logger.info(f"[Início] Usuário '{request.user.email}' acessou a página inicial de filmes.")
            return render(request, 'filmes/inicio.html', {'username': request.user.nome})
        else:
            logger.warning(f"[Início] Usuário '{request.user.email}' não pertence ao grupo 'Clientes'. Acesso negado.")
    else:
        logger.warning("[Início] Usuário não autenticado. Acesso negado.")

    return HttpResponseForbidden("Acesso negado.")
import logging
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponseForbidden


def user_logout(request):
    if request.user.is_authenticated:
        logger.info(f"[Logout] Usuário '{request.user.email}' fez logout.")
        logout(request)
    else:
        logger.warning("[Logout] Tentativa de logout por usuário não autenticado.")
    
    return redirect('users:home')  

