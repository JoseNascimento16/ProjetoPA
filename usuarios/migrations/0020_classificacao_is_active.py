# Generated by Django 3.1.7 on 2022-06-27 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0019_auto_20220620_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacao',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
