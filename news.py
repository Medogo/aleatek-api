import os
import django
from django.db import transaction
from pathlib import Path

# Remplacer 'votre_projet' par le nom réel de votre projet
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aleatek.settings')
django.setup()

from mission.models import Mission

def get_indentation_level(line):
    """Retourne le niveau d'indentation (en fonction des tabulations)"""
    return len(line) - len(line.lstrip())

def parse_file(file_path):
    """Analyse le fichier et renvoie une liste structurée des missions"""
    missions = []
    stack = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            indent_level = get_indentation_level(line)
            mission = {
                'libelle': line,
                'sous_missions': [],
                'niveau': indent_level
            }
            
            while stack and stack[-1]['niveau'] >= indent_level:
                stack.pop()
                
            if stack:
                stack[-1]['sous_missions'].append(mission)
            else:
                missions.append(mission)
                
            stack.append(mission)
            
    return missions

def create_mission(libelle, parent=None):
    """Crée une mission dans la base de données"""
    mission = Mission.objects.create(libelle=libelle, mission_parent=parent)
    return mission

def save_missions(missions, parent=None):
    """Crée les missions de manière récursive dans la base de données"""
    for mission_data in missions:
        mission = create_mission(mission_data['libelle'], parent)
        save_missions(mission_data['sous_missions'], mission)

def import_missions_from_file(file_path):
    """Importe les missions depuis un fichier texte"""
    missions = parse_file(file_path)
    with transaction.atomic():
        save_missions(missions)

if __name__ == "__main__":
    # Spécifier ici le chemin vers le fichier texte à importer
    file_path = Path("data/articlemissionAV.txt")
    
    if file_path.exists():
        import_missions_from_file(file_path)
        print("Importation des missions terminée.")
    else:
        print(f"Fichier non trouvé : {file_path}")
