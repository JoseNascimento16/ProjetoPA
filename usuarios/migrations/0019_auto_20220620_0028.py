# Generated by Django 3.1.7 on 2022-06-20 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0025_auto_20220513_1412'),
        ('usuarios', '0018_auto_20220620_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classificacao',
            name='plano_associado',
            field=models.ManyToManyField(blank=True, to='plano_de_acao.Plano_de_acao'),
        ),
    ]