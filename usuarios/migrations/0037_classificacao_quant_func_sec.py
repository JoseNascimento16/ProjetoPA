# Generated by Django 3.1.7 on 2022-09-16 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0036_auto_20220915_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacao',
            name='quant_func_sec',
            field=models.IntegerField(default=0),
        ),
    ]