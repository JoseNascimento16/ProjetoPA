# Generated by Django 3.1.7 on 2021-07-17 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0042_auto_20210716_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('caixa', 'caixa'), ('unidade', 'unidade')], max_length=10),
        ),
    ]