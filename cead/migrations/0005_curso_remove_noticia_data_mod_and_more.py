# Generated by Django 5.1.2 on 2024-11-04 12:09

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0004_alter_noticia_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='Data_mod',
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='Data_pub',
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='Descrição',
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='Título',
        ),
        migrations.AddField(
            model_name='noticia',
            name='descricao',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='noticia',
            name='edicao',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='noticia',
            name='publicacao',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='noticia',
            name='titulo',
            field=models.CharField(default='title default', max_length=255),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='noticia',
            name='id_curso',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='cead.curso'),
        ),
    ]