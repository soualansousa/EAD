# Generated by Django 5.1.2 on 2024-11-11 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0009_remove_polo_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordenador',
            name='edicao',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='coordenador',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='coordenador',
            name='publicacao',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='coordenador',
            name='situacao',
            field=models.CharField(choices=[('CEAD', 'CEAD'), ('COOPOLO', 'Coordenador Polo'), ('COOCURSO', 'Coordenador Curso'), ('COO', 'Coordenador')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='coordenador',
            name='telefone',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='edicao',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='publicacao',
            field=models.DateField(auto_now_add=True, default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='curso',
            name='sobre',
            field=models.TextField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noticia',
            name='arquivo',
            field=models.FileField(default=True, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='noticia',
            name='edicao',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='polo',
            name='edicao',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=100)),
                ('telefone', models.CharField(max_length=11)),
                ('matricula', models.CharField(max_length=50)),
                ('assunto', models.CharField(max_length=255)),
                ('mensagem', models.TextField()),
                ('publicacao', models.DateField(auto_now_add=True)),
                ('edicao', models.DateField(auto_now=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cead.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('ementa', models.TextField()),
                ('modulo', models.CharField(choices=[('1', '1º'), ('2', '2º'), ('3', '3º')], max_length=10)),
                ('ch', models.IntegerField()),
                ('arquivo', models.FileField(upload_to='')),
                ('publicacao', models.DateField(auto_now_add=True)),
                ('edicao', models.DateField(auto_now=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cead.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('arquivo', models.FileField(upload_to='')),
                ('publicacao', models.DateField(auto_now_add=True)),
                ('edicao', models.DateField(auto_now=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cead.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Perguntas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.CharField(max_length=255)),
                ('resposta', models.TextField()),
                ('arquivo', models.FileField(upload_to='')),
                ('publicacao', models.DateField(auto_now_add=True)),
                ('edicao', models.DateField(auto_now=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cead.curso')),
            ],
        ),
    ]
