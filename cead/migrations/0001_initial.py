# Generated by Django 5.1.1 on 2024-10-08 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Título', models.CharField(max_length=65)),
                ('Descrição', models.TextField(max_length=165)),
                ('Data_pub', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]