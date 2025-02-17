
# Generated by Django 5.1.1 on 2024-11-22 12:25

# Generated by Django 5.1.1 on 2024-11-22 11:16


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cead', '0028_merge_0026_gestorpolos_0027_remove_noticia_cead'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gestor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('email', models.EmailField(default='email@exemplo.com', max_length=100)),
                ('telefone', models.IntegerField(default='7499999999')),
                ('situacao', models.CharField(choices=[('ATIVO', 'Ativo'), ('INATIVO', 'Inativo')], default='ATIVO', max_length=10)),
                ('publicacao', models.DateField(auto_now_add=True)),
                ('edicao', models.DateField(auto_now=True)),

                ('formacao', models.TextField(max_length=255)),


            ],
        ),
        migrations.AlterField(
            model_name='gestorpolos',
            name='gestor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gestor_polos', to='cead.gestor'),
        ),
    ]
