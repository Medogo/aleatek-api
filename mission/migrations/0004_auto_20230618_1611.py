# Generated by Django 3.2.19 on 2023-06-18 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0003_interventiontechnique_affecteur_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='mission_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sous_missions', to='mission.mission'),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('commentaire', models.TextField(blank=True)),
                ('article_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sous_articles', to='mission.article')),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='mission.mission')),
            ],
        ),
    ]