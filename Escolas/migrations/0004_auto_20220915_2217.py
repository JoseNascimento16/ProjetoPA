# Generated by Django 3.1.7 on 2022-09-16 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Escolas', '0003_escola_diretor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escola',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
