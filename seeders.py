import os
import re
from django.db import transaction
from your_app.models import Mission  # Assurez-vous que ce chemin d'importation est correct

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def generate_code(prefix, counter):
    return f"{prefix}{counter:03d}"

def parse_and_seed_file(file_path):
    mission_counter = 0
    current_mission = None
    current_sub_mission = None

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with transaction.atomic():
        for line in lines:
            line = clean_text(line)
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
                    code_mission=generate_code("M", mission_counter),
                    libelle=line
                )
                current_sub_mission = None
            elif indent_level > 0:
                # Sous-mission
                mission_counter += 1
                new_mission = Mission.objects.create(
                    code_mission=generate_code("M", mission_counter),
                    libelle=line,
                    mission_parent=current_sub_mission if indent_level > 1 else current_mission
                )
                if indent_level == 1:
                    current_sub_mission = new_mission

def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Assurez-vous que vos fichiers ont l'extension .txt
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {filename}")
            parse_and_seed_file(file_path)

if __name__ == "__main__":
    directory_path = "path/to/your/directory"  # Remplacez ceci par le chemin de votre répertoire contenant les fichiers
    process_directory(directory_path)