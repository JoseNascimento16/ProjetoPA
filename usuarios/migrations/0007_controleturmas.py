# Generated by Django 3.1.7 on 2021-06-16 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_turmas'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControleTurmas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('todas_turmas_inseridas', models.BooleanField(default=False)),
                ('comando_turmas_todas', models.BooleanField(default=False)),
                ('comando_turmas_individual', models.BooleanField(default=False)),
            ],
        ),
    ]
