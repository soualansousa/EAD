# Generated by Django 5.1.1 on 2024-12-04 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0047_alter_mediacao_curso_polos_alter_mediacao_mediador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='arquivo',
            field=models.FileField(upload_to='documentos/'),
        ),
    ]
