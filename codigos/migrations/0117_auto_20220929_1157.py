# Generated by Django 3.1.7 on 2022-09-29 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0116_auto_20220918_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('unidade', 'unidade'), ('caixa', 'caixa')], max_length=10),
        ),
    ]