# Generated by Django 3.1.7 on 2022-03-12 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0019_correcoes_plano_associado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plano_de_acao',
            name='pre_analise',
        ),
    ]