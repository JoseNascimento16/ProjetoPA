# Generated by Django 3.1.7 on 2021-06-16 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0010_plano_de_acao_situacao'),
        ('usuarios', '0009_auto_20210616_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='turmas',
            name='plano_associado',
            field=models.ManyToManyField(to='plano_de_acao.Plano_de_acao'),
        ),
    ]