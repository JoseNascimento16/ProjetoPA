# Generated by Django 3.1.7 on 2021-05-17 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordens', '0016_auto_20210516_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='controleordens',
            name='var_template',
            field=models.IntegerField(default=0),
        ),
    ]
