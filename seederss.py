import os
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aleatek.settings')
django.setup()
from mission.models import Mission
def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    missions = []
    current_parent = None
    code_counter = {}  # Dictionnaire pour suivre les compteurs de chaque niveau

    for line in lines:
        stripped_line = line.rstrip()  # Supprime les espaces à droite
        indentation_level = len(line) - len(stripped_line)  # Calcule l'indentation
        
        # Détermine le niveau d'indentation (par exemple, 0 pour aucune indentation)
        level = indentation_level // 4  # Supposons que l'indentation est de 4 espaces
        
        # Met à jour le compteur pour le niveau actuel
        if level not in code_counter:
            code_counter[level] = 1
        else:
            code_counter[level] += 1
        
        # Génère le code de mission basé sur la numérotation
        code_mission = '.'.join(str(code_counter[i]) for i in range(level + 1))

        # Crée un dictionnaire pour la mission
        mission_data = {
            'libelle': stripped_line,
            'code_mission': code_mission,
            'parent': current_parent
        }
        missions.append(mission_data)

        # Met à jour le parent pour le niveau actuel
        current_parent = code_mission if level > 0 else None

    return missions

def create_mission(libelle, parent, code_mission):
    existing_mission = Mission.objects.filter(code_mission=code_mission).first()
    
    if existing_mission:
        print(f"La mission avec le code {code_mission} existe déjà.")
        return existing_mission

    mission = Mission.objects.create(libelle=libelle, mission_parent=parent, code_mission=code_mission)
    return mission

def save_missions(missions):
    for mission_data in missions:
        libelle = mission_data['libelle']
        parent = mission_data['parent']
        code_mission = mission_data['code_mission']
        
        create_mission(libelle, parent, code_mission)

def import_missions_from_file(file_path):
    missions = parse_file(file_path)
    save_missions(missions)

# Utilisation
file_path = 'data/articlemissionAV.txt'  # Remplacez par le chemin de votre fichier
import_missions_from_file(file_path)
