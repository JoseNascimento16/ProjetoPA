# Generated by Django 3.1.7 on 2022-09-30 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Escolas', '0009_escola_diretor'),
    ]

    operations = [
        migrations.AddField(
            model_name='escola',
            name='possui_tesoureiro',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='escola',
            name='quant_membro_colegiado',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
