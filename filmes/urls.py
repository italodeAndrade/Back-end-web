from django.urls import include, path
from .views import lista_filmes

app_name = 'filmes'

urlpatterns = [
    path('filmes/', lista_filmes, name='lista_filmes'),
]
