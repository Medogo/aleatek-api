# Generated by Django 3.2.19 on 2024-08-13 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Dashbord', '0001_initial'),
        ('adresse', '0001_initial'),
        ('entreprise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='tutored',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutorals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='planaffaire',
            name='affaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord.affaire'),
        ),
        migrations.AddField(
            model_name='entrepriseaffaire',
            name='affaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord.affaire'),
        ),
        migrations.AddField(
            model_name='entrepriseaffaire',
            name='entreprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entreprise.entreprise'),
        ),
        migrations.AddField(
            model_name='chantier',
            name='adresse',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adresse.adress'),
        ),
        migrations.AddField(
            model_name='chantier',
            name='batiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Dashbord.batiment'),
        ),
        migrations.AddField(
            model_name='chantier',
            name='plan_affaire',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Dashbord.planaffaire'),
        ),
        migrations.AddField(
            model_name='affaire',
            name='assistant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DashbordAffaireassistant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='affaire',
            name='charge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DashbordAffairecharge', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='affaire',
            name='chef',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DashbordAffairechef', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='affaire',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='entreprise.entreprise'),
        ),
        migrations.AddField(
            model_name='affaire',
            name='produit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DashbordProduit', to='Dashbord.produit'),
        ),
        migrations.AddConstraint(
            model_name='entrepriseaffaire',
            constraint=models.UniqueConstraint(fields=('entreprise', 'affaire'), name='unique_entreprise_affaire'),
        ),
    ]