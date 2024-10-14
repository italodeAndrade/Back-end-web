from django.db import models

class cliente(models.Model):
    
    email = models.CharField(max_length=90)
    nome = models.CharField(max_length =200)
    senha = models.CharField(max_length=50)

    def __str__(self):
        return self.email
        return self.nome
    




