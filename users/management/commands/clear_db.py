from django.core.management.base import BaseCommand
from users.models import Cliente
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Limpa o banco de dados'

    def handle(self, *args, **kwargs):
        Cliente.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Banco de dados limpo com sucesso!'))
