# Generated by Django 4.2 on 2023-06-02 00:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ouvrage', '0002_entrepriseaffaireouvrage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affaireouvrage',
            name='statut',
            field=models.CharField(choices=[(0, 'En cours'), (1, 'Accepté'), (2, 'Classé'), (4, 'diffusé')], default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='affaireouvrage',
            name='validateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]