import os
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from mission.models import Mission  # Assurez-vous que ce chemin est correct

class Command(BaseCommand):
    help = 'Seed missions from a text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the text file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        self.parse_and_seed_file(file_path)

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def generate_code(self, prefix, counter):
        return f"{prefix}{counter:03d}"

    def parse_and_seed_file(self, file_path):
        mission_counter = 0
        current_mission = None
        current_sub_mission = None

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with transaction.atomic():
            for line in lines:
                line = self.clean_text(line)
                if not line:
                    continue

                indent_level = len(line) - len(line.lstrip())
                line = line.strip()

                if line.startswith('-'):
                    line = line[1:].strip()  # Remove the dash and any leading space

                if indent_level == 0:
                    # Nouvelle mission principale
                    mission_counter += 1
                    current_mission = Mission.objects.create(
                        code_mission=self.generate_code("M", mission_counter),
                        libelle=line
                    )
                    current_sub_mission = None
                elif indent_level > 0:
                    # Sous-mission
                    mission_counter += 1
                    new_mission = Mission.objects.create(
                        code_mission=self.generate_code("M", mission_counter),
                        libelle=line,
                        mission_parent=current_sub_mission if indent_level > 1 else current_mission
                    )
                    if indent_level == 1:
                        current_sub_mission = new_mission

        self.stdout.write(self.style.SUCCESS(f"Processed file: {file_path}"))
        self.stdout.write(self.style.SUCCESS(f"Total missions created: {mission_counter}"))