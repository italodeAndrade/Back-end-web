from django.db import models
from users.models import Cliente

class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ano_lancamento = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
