# Generated by Django 3.1.7 on 2022-10-25 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0124_auto_20221017_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('unidade', 'unidade'), ('caixa', 'caixa')], max_length=10),
        ),
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Capital', 'Capital'), ('Custeio', 'Custeio')], max_length=10),
        ),
    ]
