# Generated by Django 3.1.7 on 2021-06-16 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0025_auto_20210616_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('caixa', 'caixa'), ('unidade', 'unidade')], max_length=10),
        ),
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Capital', 'Capital'), ('Custeio', 'Custeio')], max_length=10),
        ),
    ]
