# Generated by Django 3.1.7 on 2022-09-16 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Escolas', '0007_escola_diretor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='escola',
            name='diretor',
        ),
    ]
