# Generated by Django 3.1.7 on 2022-03-10 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordens', '0017_controleordens_var_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordens',
            name='possui_sugestao_correcao',
            field=models.BooleanField(default=False),
        ),
    ]