import requests
from django.shortcuts import render
import random

def lista_filmes(request):
    key_words = ['space', 'love', 'war', 'future', 'dark', 'light', 'dream', 'city', "lost", "crime"]
    generos = ['Action', 'Comedy', 'Drama', 'Horror', 'Thriller', 'Romance', 'Sci-Fi', 'Adventure']
    
    termo = random.choice(key_words)
    genero_escolhido = random.choice(generos)
    
    url = f'http://www.omdbapi.com/?s={termo}&apikey=19cee984'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'Search' in data:
            filmes = [filme for filme in data['Search'] if genero_escolhido in filme.get('Genre', '')]
            if not filmes:
                filmes = data['Search']
        else:
            filmes = []
    else:
        filmes = []

    return render(request, 'filmes/lista_filmes.html', {'filmes': filmes, 'genero': genero_escolhido})
