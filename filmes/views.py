import requests
from django.shortcuts import render
import random
import logging

logger = logging.getLogger(__name__)

def lista_filmes(request):
    key_words = ['space', 'love', 'war', 'future', 'dark', 'light', 'dream', 'city', "lost", "crime"]
    generos = ['Action', 'Comedy', 'Drama', 'Horror', 'Thriller', 'Romance', 'Sci-Fi', 'Adventure']
    
    termo = random.choice(key_words)
    genero_escolhido = random.choice(generos)
    
    url = f'http://www.omdbapi.com/?s={termo}&apikey=19cee984'
    logger.info(f"Requisição para URL: {url} com termo '{termo}' e gênero '{genero_escolhido}'")

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'Search' in data:
            filmes = [filme for filme in data['Search'] if genero_escolhido in filme.get('Genre', '')]
            if not filmes:
                filmes = data['Search']
                logger.info(f"Exibindo filmes fora do gênero.")
            else:
                logger.info(f"Filmes encontrados  '{genero_escolhido}': {len(filmes)}")
        else:
            filmes = []
            logger.warning("Nenhum filme encontrado na resposta.")
    else:
        filmes = []
        logger.error(f"Erro na requisição: Status {response.status_code}")

    return render(request, 'filmes/lista_filmes.html', {'filmes': filmes, 'genero': genero_escolhido})
