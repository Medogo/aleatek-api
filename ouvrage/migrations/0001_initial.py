# Generated by Django 3.2.19 on 2024-08-31 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Dashbord', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AffaireOuvrage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diffusion', models.BooleanField(default=False)),
                ('rename', models.CharField(blank=True, default='', max_length=200)),
                ('id_affaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord.affaire')),
            ],
        ),
        migrations.CreateModel(
            name='Aso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('statut', models.CharField(blank=True, choices=[(0, 'En cours'), (1, 'Accepté'), (2, 'Classé'), (3, 'Diffuse')], default=0, max_length=10, null=True)),
                ('order_in_affaire', models.IntegerField()),
                ('affaireouvrage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.affaireouvrage')),
                ('redacteur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('dossier', models.CharField(choices=[('Execution', 'Execution'), ('Conception', 'Conception')], default='Execution', max_length=200)),
                ('nature', models.CharField(choices=[('TOUS', 'TOUS'), ('Descriptif', 'Descriptif'), ('AT/DTA', 'AT/DTA'), ('Attestation Incendie', 'Attestation Incendie'), ('Carnet', 'Carnet'), ('Certificat', 'Certificat'), ('Certificat incendie', 'Certificat incendie'), ('Compte rendue', 'Compte rendu'), ('Courrier', 'Courrier'), ('fiche techinique', 'Fiche Technique'), ('Note', 'Note'), ('Note de calcule', 'Note de calcule'), ('Notice', 'Notice'), ('Plan', 'Plan'), ('PV', 'PV'), ('PV Incendie', 'PV Incendie'), ('Rapport', 'Rapport'), ('Schéma', 'Schéma')], max_length=30)),
                ('indice', models.CharField(blank=True, max_length=5, null=True)),
                ('date_indice', models.DateField(blank=True, null=True)),
                ('date_reception', models.DateField(blank=True, null=True)),
                ('titre', models.CharField(blank=True, max_length=500, null=True)),
                ('numero_externe', models.IntegerField(blank=True, null=True)),
                ('aso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ouvrage.aso')),
                ('createur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ouvrageDocumentscreateur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RemarqueAso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('aso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.aso')),
                ('redacteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ouvrage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=200)),
                ('affaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Dashbord.affaire')),
            ],
        ),
        migrations.CreateModel(
            name='FichierAttache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=250)),
                ('fichier', models.FileField(upload_to='fichierattachedocument')),
                ('date', models.DateField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.documents')),
            ],
        ),
        migrations.CreateModel(
            name='EntrepriseAffaireOuvrage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diffusion', models.BooleanField(default=False)),
                ('affaire_entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord.entrepriseaffaire')),
                ('affaire_ouvrage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.affaireouvrage')),
            ],
        ),
        migrations.AddField(
            model_name='documents',
            name='emetteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.entrepriseaffaireouvrage'),
        ),
        migrations.AddField(
            model_name='documents',
            name='validateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ouvrageDocumentsvalidateur', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DocumentAffectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collaborateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.documents')),
            ],
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codification', models.CharField(choices=[('F', 'F'), ('RMQ', 'RMQ'), ('HM', 'HM'), ('VI', 'VI')], max_length=23)),
                ('collaborateurs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.documents')),
            ],
        ),
        migrations.AddField(
            model_name='affaireouvrage',
            name='id_ouvrage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ouvrage.ouvrage'),
        ),
        migrations.AddConstraint(
            model_name='entrepriseaffaireouvrage',
            constraint=models.UniqueConstraint(fields=('affaire_ouvrage', 'affaire_entreprise'), name='unique_entreprise_ouvrage'),
        ),
        migrations.AddConstraint(
            model_name='documentaffectation',
            constraint=models.UniqueConstraint(fields=('document', 'collaborateur'), name='unique_document_affectation'),
        ),
        migrations.AddConstraint(
            model_name='avis',
            constraint=models.UniqueConstraint(fields=('id_document', 'collaborateurs'), name='unique_avis_collaborateur'),
        ),
        migrations.AddConstraint(
            model_name='affaireouvrage',
            constraint=models.UniqueConstraint(fields=('id_affaire', 'id_ouvrage'), name='unique_affaire_document'),
        ),
    ]
