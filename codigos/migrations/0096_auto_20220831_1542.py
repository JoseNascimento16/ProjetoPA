# Generated by Django 3.1.7 on 2022-08-31 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0095_modelocodigos_quebra_de_linha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Capital', 'Capital'), ('Custeio', 'Custeio')], max_length=10),
        ),
    ]