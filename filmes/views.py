import requests
from django.shortcuts import render
import random

def lista_filmes(request):
    url = f'http://www.omdbapi.com/?i=tt3896198&apikey=19cee984'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'Search' in data:
            filmes = data['Search']
            random.shuffle(filmes)  # Embaralha os filmes
            filmes = filmes[:10]  
        else:
            filmes = []
            print("Nenhum filme encontrado ou problema na resposta da API.")
    else:
        filmes = []
        print(f"Erro na requisição: {response.status_code}")

    return render(request, 'filmes/lista_filmes.html', {'filmes': filmes})
