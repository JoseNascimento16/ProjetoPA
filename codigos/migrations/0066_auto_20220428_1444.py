# Generated by Django 3.1.7 on 2022-04-28 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0065_auto_20220322_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('caixa', 'caixa'), ('unidade', 'unidade')], max_length=10),
        ),
    ]
