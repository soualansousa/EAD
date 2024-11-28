# Generated by Django 5.1.1 on 2024-11-28 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0033_remove_noticia_curso'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='gestorpolos',
            name='unique_gestor_polo',
        ),
        migrations.RenameField(
            model_name='gestorpolos',
            old_name='publicacao',
            new_name='entrada',
        ),
        migrations.RemoveField(
            model_name='gestorpolos',
            name='edicao',
        ),
        migrations.RemoveField(
            model_name='polo',
            name='coordenador',
        ),
        migrations.AddField(
            model_name='gestorpolos',
            name='saida',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='polo',
            name='gestor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cead.gestor'),
            preserve_default=False,
        ),
    ]