# Generated by Django 3.1.7 on 2022-07-24 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0022_auto_20220723_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='turmas',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
