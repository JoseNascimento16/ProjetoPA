# Generated by Django 3.1.7 on 2021-06-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0021_auto_20210616_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('caixa', 'caixa'), ('unidade', 'unidade')], max_length=10),
        ),
    ]
