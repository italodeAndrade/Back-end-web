from django.shortcuts import render, redirect
import random
import requests
import uuid
import logging
from .models import Cliente 
from django.contrib.auth.hashers import check_password
import uuid
logger = logging.getLogger(__name__)

def lista_filmes(request):
    key_words = ['space', 'love', 'war', 'future', 'dark', 'light', 'dream', 'city', "lost", "crime"]
    termo = random.choice(key_words)
    
    url = f'http://www.omdbapi.com/?s={termo}&apikey=19cee984'
    logger.info(f"Requisição para URL: {url} com termo '{termo}'")

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        filmes = data.get('Search', [])
        logger.info(f"Filmes encontrados: {len(filmes)}")
    else:
        filmes = []
        logger.error(f"Erro na requisição: Status {response.status_code}")

    return render(request, 'filmes/lista_filmes.html', {'filmes': filmes})

def lista_pessoal(request):
    filmes_pessoais = request.session.get('filmes_pessoais', [])
    return render(request, 'filmes/lista_pessoal.html', {'filmes_pessoais': filmes_pessoais})

def adicionar_filme_pessoal(request, filme_id):
    filme = request.POST.get('filme_nome')  # Suponha que o nome do filme é enviado via POST

    filmes_pessoais = request.session.get('filmes_pessoais', [])
    filmes_pessoais.append(filme)
    request.session['filmes_pessoais'] = filmes_pessoais

    logger.info(f"Filme '{filme}' adicionado à lista pessoal")
    
    return redirect('filmes:lista_pessoal')

def inicio(request):
    return render(request, 'filmes/inicio.html')

from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

def remover_filme_pessoal(request, filme_nome):
    filmes_pessoais = request.session.get('filmes_pessoais', [])
    
    if filme_nome in filmes_pessoais:
        filmes_pessoais.remove(filme_nome)
        request.session['filmes_pessoais'] = filmes_pessoais

    return redirect('filmes:lista_pessoal')



def verificar_senha(request):
    if request.method == 'POST':
        senha = request.POST.get('senha')

        try:
            cliente = Cliente.objects.get(id=request.cliente.id)
        except cliente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'cliente não encontrado'})

        if check_password(senha, cliente.senha):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Senha incorreta'})

    return JsonResponse({'success': False, 'error': 'Método inválido'})


