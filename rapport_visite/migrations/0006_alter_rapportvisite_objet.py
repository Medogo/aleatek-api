# Generated by Django 3.2.19 on 2023-06-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rapport_visite', '0005_auto_20230617_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapportvisite',
            name='objet',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]