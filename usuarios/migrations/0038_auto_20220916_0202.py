# Generated by Django 3.1.7 on 2022-09-16 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0037_classificacao_quant_func_sec'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classificacao',
            name='quant_func_sec',
        ),
        migrations.RemoveField(
            model_name='turmas',
            name='user',
        ),
    ]
