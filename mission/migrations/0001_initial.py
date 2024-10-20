# Generated by Django 3.2.19 on 2024-08-31 06:55

import datetime
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
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=500, unique=True)),
                ('commentaire', models.TextField(blank=True)),
                ('article_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sous_articles', to='mission.article')),
            ],
        ),
        migrations.CreateModel(
            name='MissionActive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_mission', models.CharField(max_length=10, unique=True)),
                ('libelle', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('mission_parent', models.ForeignKey(blank=True, limit_choices_to={'mission_parent__isnull': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sous_missions', to='mission.mission')),
            ],
        ),
        migrations.CreateModel(
            name='InterventionTechnique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.date.today)),
                ('affecteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ITAffecteur', to=settings.AUTH_USER_MODEL)),
                ('id_collaborateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ITAffecter', to=settings.AUTH_USER_MODEL)),
                ('id_mission_active', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.missionactive')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleSelect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affaire_article_select', to='Dashbord.affaire')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_article_select', to='mission.article')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='mission.article')),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mission', to='mission.mission')),
            ],
        ),
        migrations.AddConstraint(
            model_name='interventiontechnique',
            constraint=models.UniqueConstraint(fields=('id_mission_active', 'id_collaborateur'), name='unique_IT'),
        ),
        migrations.AddConstraint(
            model_name='articleselect',
            constraint=models.UniqueConstraint(fields=('article', 'affaire'), name='unique_affaire_article'),
        ),
        migrations.AddConstraint(
            model_name='articlemission',
            constraint=models.UniqueConstraint(fields=('article', 'mission'), name='unique_article_mission'),
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('titre',), name='unique_titre'),
        ),
    ]
