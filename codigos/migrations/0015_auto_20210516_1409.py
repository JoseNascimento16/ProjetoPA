# Generated by Django 3.1.7 on 2021-05-16 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0014_auto_20210515_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('caixa', 'caixa'), ('unidade', 'unidade')], max_length=10),
        ),
    ]
