# Generated by Django 3.1.7 on 2021-05-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0017_auto_20210519_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='quantidade',
            field=models.IntegerField(max_length=5),
        ),
    ]
