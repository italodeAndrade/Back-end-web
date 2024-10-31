from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.contrib.auth.models import Group

class ClienteManager(BaseUserManager):
    def create_user(self, email, senha=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        
        clientes_group, created = Group.objects.get_or_create(name='Clientes')
        user.groups.add(clientes_group)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Cliente(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=90, unique=True)
    nome = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ClienteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='clientes',  
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='clientes',  
        blank=True
    )

    def __str__(self):
        return self.email
