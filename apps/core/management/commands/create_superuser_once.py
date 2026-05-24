from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Cria superusuário padrão se ainda não existir'

    def handle(self, *args, **options):
        username = 'mnknopp'
        email = 'marcio@bk-engenharia.com'
        password = 'velhodomal1976'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superusuário "{username}" já existe — nenhuma ação tomada.'))
