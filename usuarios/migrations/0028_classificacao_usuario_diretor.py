# Generated by Django 3.1.7 on 2022-08-31 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0027_classificacao_cargo_herdado'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacao',
            name='usuario_diretor',
            field=models.BooleanField(default=False),
        ),
    ]
