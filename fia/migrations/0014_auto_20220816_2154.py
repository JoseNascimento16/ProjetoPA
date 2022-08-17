# Generated by Django 3.1.7 on 2022-08-17 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0031_plano_de_acao_pre_analise_fia'),
        ('fia', '0013_modelo_fia_tecnico_responsavel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelo_fia',
            name='plano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plano_de_acao.plano_de_acao'),
        ),
    ]
