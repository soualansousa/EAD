# Generated by Django 5.1.1 on 2024-11-14 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0018_alter_noticia_arquivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediador',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='polo',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='polo',
            name='mediador',
        ),
        migrations.CreateModel(
            name='CursoPolo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cead.curso')),
                ('polo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cead.polo')),
            ],
        ),
    ]