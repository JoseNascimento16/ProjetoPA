# Generated by Django 3.1.7 on 2022-09-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0111_auto_20220916_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('unidade', 'unidade'), ('caixa', 'caixa')], max_length=10),
        ),
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Custeio', 'Custeio'), ('Capital', 'Capital')], max_length=10),
        ),
    ]