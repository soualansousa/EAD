# Generated by Django 5.1.1 on 2024-11-26 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0032_alter_coordenadorcurso_saida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='curso',
        ),
    ]
