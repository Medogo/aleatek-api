# Generated by Django 3.2.12 on 2023-08-21 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0012_alter_articlemission_mission'),
        ('RICT', '0011_auto_20230814_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisarticle',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.articlemission'),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.articlemission'),
        ),
    ]