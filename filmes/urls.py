from django.urls import path
from . import views

app_name = 'filmes'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('lista_filmes/', views.lista_filmes, name='lista_filmes'),
    path('lista_pessoal/', views.lista_pessoal, name='lista_pessoal'),
    path('adicionar_filme_pessoal/<str:filme_id>/', views.adicionar_filme_pessoal, name='adicionar_filme_pessoal'),
    path('remover_filme_pessoal/<str:filme_nome>/', views.remover_filme_pessoal, name='remover_filme_pessoal'),
    path('verificar_senha/', views.verificar_senha, name='verificar_senha'),
]
