from django.db import models
from users.models import Cliente
from django.conf import settings

class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ano_lancamento = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
class FilmePessoal(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome