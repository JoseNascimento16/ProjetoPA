# Generated by Django 3.1.7 on 2021-05-04 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='identificacao',
            field=models.CharField(max_length=1),
        ),
    ]