# Generated by Django 5.1.1 on 2024-11-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0013_alter_coordenador_situacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediador',
            name='situacao',
            field=models.CharField(choices=[('ATIVO', 'Ativo'), ('INATIVO', 'Inativo')], default='ATIVO', max_length=10),
        ),
    ]
