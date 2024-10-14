from django.db import models
from django.contrib.auth.hashers import make_password

class Cliente(models.Model):
    email = models.EmailField(max_length=90, unique=True)
    nome = models.CharField(max_length=200)
    senha = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if self.senha:
            self.senha = make_password(self.senha)  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


