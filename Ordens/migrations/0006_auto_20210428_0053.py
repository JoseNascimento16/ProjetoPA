# Generated by Django 3.1.7 on 2021-04-28 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ordens', '0005_auto_20210427_2209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordens',
            old_name='Identificacao_numerica',
            new_name='identificacao_numerica',
        ),
    ]