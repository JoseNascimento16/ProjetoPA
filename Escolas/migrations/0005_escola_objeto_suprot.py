# Generated by Django 3.1.7 on 2022-09-16 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Escolas', '0004_auto_20220915_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='escola',
            name='objeto_suprot',
            field=models.BooleanField(default=False),
        ),
    ]