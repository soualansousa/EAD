# Generated by Django 5.1.2 on 2024-11-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0013_alter_coordenador_situacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordenador',
            name='telefone',
            field=models.IntegerField(default='7499999999'),
        ),
    ]