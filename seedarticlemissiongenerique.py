# import django.conf as settings
import django
import os  # Ajout de l'import pour utiliser os.path
from sys import argv

# Configure Django
django.setup()
# settings.configure()

from mission.models import Article, ArticleMission

# Vérifiez que le nombre d'arguments est correct (au moins 3)
if len(argv) < 3:
    print("Utilisation : python script.py fichier_d_entree.txt mission_id")
    exit(1)

# Récupérez les arguments de la ligne de commande
input_file = argv[1]
mission_id = int(argv[2])

# Vérifiez si le fichier d'entrée existe
if not os.path.isfile(input_file):
    print(f"Le fichier d'entrée '{input_file}' n'existe pas.")
    exit(1)

with open(input_file, 'r') as f:
    lines = f.readlines()
    idsupper = []
    idfirstlevel = []
    idsenconlevel = []
    try:
        for i, line in enumerate(lines):
            print(line)
            
            if line.strip().isupper():  # Utilisez strip pour retirer les espaces et les sauts de ligne
                if Article.objects.filter(titre=line.strip()).exists():
                    id = Article.objects.get(titre=line.strip()).id
                    ArticleMission(article_id=id, mission_id=mission_id).save()
                    if id not in idsupper:
                        idsupper.append(id)
                else:
                    data = Article(titre=line.strip(), article_parent_id=None, commentaire='')
                    data.save()
                    idsupper.append(data.id)
                    ArticleMission(article_id=data.id, mission_id=mission_id).save()
            
            elif line.startswith("\t\t- "):
                if Article.objects.filter(titre=line.strip().replace('\n', '').replace('\t', '')).exists():
                    id = Article.objects.get(titre=line.strip().replace('\n', '').replace('\t', '')).id
                    ArticleMission(article_id=id, mission_id=mission_id).save()
                else:
                    data = Article(titre=line.strip().replace('\n', '').replace('\t', ''), article_parent_id=idsenconlevel[-1],
                                commentaire='')
                    data.save()
                    ArticleMission(article_id=data.id, mission_id=mission_id).save()
            
            elif line.startswith("\t\t"):
                if Article.objects.filter(titre=line.strip().replace('\n', '').replace('\t', '')).exists():
                    id = Article.objects.get(titre=line.strip().replace('\n', '').replace('\t', '')).id
                    ArticleMission(article_id=id, mission_id=mission_id).save()
                    if id not in idsenconlevel:
                        idsenconlevel.append(id)
                else:
                    data = Article(titre=line.strip().replace('\n', '').replace('\t', ''), article_parent_id=idfirstlevel[-1],
                                commentaire='')
                    data.save()
                    idsenconlevel.append(data.id)
                    ArticleMission(article_id=data.id, mission_id=mission_id).save()
            
            elif line.startswith("\t"):
                if Article.objects.filter(titre=line.strip().replace('\n', '').replace('\t', '')).exists():
                    id = Article.objects.get(titre=line.strip().replace('\n', '').replace('\t', '')).id
                    ArticleMission(article_id=id, mission_id=mission_id).save()
                    if id not in idfirstlevel:
                        idfirstlevel.append(id)
                else:
                    data = Article(titre=line.strip().replace('\n', '').replace('\t', ''), article_parent_id=idsupper[-1],
                                commentaire='')
                    data.save()
                    idfirstlevel.append(data.id)
                    ArticleMission(article_id=data.id, mission_id=mission_id).save()
            else:
                print(line)
    except Exception as ex:
        print(f"Erreur dans le fichier {input_file}")
        print(ex)
        Article.objects.all().delete()
