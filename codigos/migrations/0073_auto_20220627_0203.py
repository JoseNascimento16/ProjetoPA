# Generated by Django 3.1.7 on 2022-06-27 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0072_auto_20220620_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Custeio', 'Custeio'), ('Capital', 'Capital')], max_length=10),
        ),
    ]
