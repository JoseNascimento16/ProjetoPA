# Generated by Django 3.1.7 on 2022-07-19 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0081_auto_20220719_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Capital', 'Capital'), ('Custeio', 'Custeio')], max_length=10),
        ),
    ]
