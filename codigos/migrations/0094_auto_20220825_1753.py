# Generated by Django 3.1.7 on 2022-08-25 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0093_auto_20220812_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Custeio', 'Custeio'), ('Capital', 'Capital')], max_length=10),
        ),
    ]
