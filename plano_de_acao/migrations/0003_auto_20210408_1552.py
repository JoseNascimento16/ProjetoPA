# Generated by Django 3.1.7 on 2021-04-08 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0002_auto_20210408_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plano_de_acao',
            name='ano_referencia',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='plano_de_acao',
            name='descricao_plano',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='plano_de_acao',
            name='resultados_esperados',
            field=models.TextField(max_length=300),
        ),
    ]
