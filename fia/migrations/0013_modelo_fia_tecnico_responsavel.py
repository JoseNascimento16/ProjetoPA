# Generated by Django 3.1.7 on 2022-08-16 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fia', '0012_auto_20220812_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelo_fia',
            name='tecnico_responsavel',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
