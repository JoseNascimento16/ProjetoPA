# Generated by Django 3.1.7 on 2022-09-09 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0029_classificacao_usuario_coordenador'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacao',
            name='email_ativado',
            field=models.BooleanField(default=False),
        ),
    ]
