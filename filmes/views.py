import logging
import random
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.hashers import check_password
from .models import Cliente, Filme, FilmePessoal
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
import json  
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
    
    filmes_pessoais = FilmePessoal.objects.filter(usuario=request.user)
    username = get_username(request)
    logger.info(f"[Lista Pessoal] Usuário '{username}' acessou a lista pessoal de filmes. Total de filmes: {len(filmes_pessoais)}")
    return render(request, 'filmes/lista_pessoal.html', {'filmes_pessoais': filmes_pessoais})

@login_required
def adicionar_filme_pessoal(request, filme_id):
    if not request.user.groups.filter(name='Clientes').exists():
        logger.warning(f"[Adicionar Filme Pessoal] Usuário '{request.user.email}' não pertence ao grupo 'Clientes'. Acesso negado.")
        return HttpResponseForbidden("Acesso negado.")
    
    nome_filme = request.POST.get('filme_nome')
    
    if nome_filme:
        try:
            FilmePessoal.objects.create(usuario=request.user, nome=nome_filme)
            logger.info(f"[Adicionar Filme Pessoal] Usuário '{request.user.email}' adicionou o filme '{nome_filme}' à lista pessoal.")
        except Exception as e:
            logger.error(f"[Adicionar Filme Pessoal] Erro ao adicionar o filme '{nome_filme}' para o usuário '{request.user.email}': {str(e)}")
    else:
        logger.warning(f"[Adicionar Filme Pessoal] Nenhum nome de filme fornecido para o usuário '{request.user.email}'.")

    return redirect('filmes:lista_filmes')


from urllib.parse import unquote

@login_required
def remover_filme_pessoal(request, filme_nome):
    if not request.user.groups.filter(name='Clientes').exists():
        logger.warning(f"[Remover Filme Pessoal] Usuário '{request.user.email}' não pertence ao grupo 'Clientes'. Acesso negado.")
        return HttpResponseForbidden("Acesso negado.")
    
    filme_nome_decodificado = unquote(filme_nome)
    email_usuario = request.user.email

    logger.info(f"[Remover Filme Pessoal] Tentativa de remover o filme '{filme_nome_decodificado}' para o usuário '{email_usuario}'.")

    try:
        filme = FilmePessoal.objects.get(usuario=request.user, nome=filme_nome_decodificado)
        filme.delete()
        logger.info(f"[Remover Filme Pessoal] Usuário '{email_usuario}' removeu o filme '{filme_nome_decodificado}' da lista pessoal.")
    except FilmePessoal.DoesNotExist:
        logger.warning(f"[Remover Filme Pessoal] Usuário '{email_usuario}' tentou remover filme '{filme_nome_decodificado}' que não está na lista pessoal.")
    except Exception as e:
        logger.error(f"[Remover Filme Pessoal] Erro ao remover o filme '{filme_nome_decodificado}' para o usuário '{email_usuario}': {str(e)}")

    return redirect('filmes:lista_pessoal')




def verificar_senha(request):
    if request.method == 'POST':

        data = json.loads(request.body) 
        senha = data.get('password')

        if not senha:
            return JsonResponse({'success': False, 'error': 'Senha não fornecida.'})

        if check_password(senha, request.user.password):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Senha incorreta'})

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

def user_logout(request):
    if request.user.is_authenticated:
        logger.info(f"[Logout] Usuário '{request.user.email}' fez logout.")
        logout(request)
    else:
        logger.warning("[Logout] Tentativa de logout por usuário não autenticado.")
    
    return redirect('users:home')  

