# Generated by Django 3.1.7 on 2021-05-12 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_classificacao_municipio'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacao',
            name='matriz',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
