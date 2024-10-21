import requests
from django.shortcuts import render
import random

def lista_filmes(request):
    key_words = ['space', 'love', 'war', 'future', 'dark', 'light', 'dream', 'city']

    termo= random.choice(key_words)
    url = f'http://www.omdbapi.com/?s={termo}&apikey=19cee984'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'Search' in data:
            filmes = data['Search']
        else:
            filmes = []
            print("Nenhum filme encontrado.")
    else:
        filmes = []
        print(f"Erro na requisição: {response.status_code}")


    return render(request, 'filmes/lista_filmes.html', {'filmes': filmes})
