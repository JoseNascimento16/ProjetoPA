# Generated by Django 3.1.7 on 2022-03-09 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0016_auto_20220309_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correcoes',
            name='codigo_associado',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='correcoes',
            name='ordem_associada',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]