# Generated by Django 4.1.4 on 2022-12-16 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0128_alter_modelocodigos_tipo_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('unidade', 'unidade'), ('caixa', 'caixa')], max_length=10),
        ),
        migrations.AlterField(
            model_name='modelocodigos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
