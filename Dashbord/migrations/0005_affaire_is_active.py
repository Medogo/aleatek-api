# Generated by Django 3.2.19 on 2024-08-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord', '0004_batimentplanaffaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='affaire',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]