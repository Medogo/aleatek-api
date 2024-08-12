 # import_superusers_from_json.py
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Importe des superutilisateurs depuis un fichier JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Chemin vers le fichier JSON')

    def handle(self, *args, **options):
        json_file = options['json_file']

        with open(json_file, 'r') as f:
            superusers_data = json.load(f)

        for superuser_data in superusers_data:
            username = superuser_data['username']
            password = superuser_data['password']
            email = superuser_data['email']

            # Vérifiez si l'utilisateur existe déjà
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, password=password, email=email)
                self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé avec succès."))
            else:
                self.stdout.write(self.style.WARNING(f"Superutilisateur '{username}' existe déjà. Ignoré."))

        self.stdout.write(self.style.SUCCESS('Tous les superutilisateurs ont été importés avec succès.'))
