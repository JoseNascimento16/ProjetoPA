# Generated by Django 3.1.7 on 2022-08-13 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0026_auto_20220806_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacao',
            name='cargo_herdado',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
