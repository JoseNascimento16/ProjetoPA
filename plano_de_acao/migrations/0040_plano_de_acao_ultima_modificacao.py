# Generated by Django 3.1.7 on 2022-11-18 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plano_de_acao', '0039_auto_20220929_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='plano_de_acao',
            name='ultima_modificacao',
            field=models.DateField(blank=True, null=True),
        ),
    ]
