# Generated by Django 3.1.7 on 2022-05-05 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0023_plano_de_acao_assinaturas_sec'),
    ]

    operations = [
        migrations.AddField(
            model_name='plano_de_acao',
            name='pre_assinatura',
            field=models.BooleanField(default=False),
        ),
    ]
