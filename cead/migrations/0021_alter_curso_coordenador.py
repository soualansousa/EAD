# Generated by Django 5.1.1 on 2024-11-14 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0020_curso_coordenador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='coordenador',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cead.coordenador'),
        ),
    ]
