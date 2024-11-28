# Generated by Django 5.1.1 on 2024-11-27 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0036_mediadorcursopolos_delete_mediacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediadorcursopolos',
            name='curso_polos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MediadorCursoPolos', to='cead.cursopolo'),
        ),
        migrations.AlterField(
            model_name='mediadorcursopolos',
            name='mediador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MediadorCursoPolos', to='cead.mediador'),
        ),
    ]