# Generated by Django 4.1.4 on 2022-12-15 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0127_auto_20221118_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Custeio', 'Custeio'), ('Capital', 'Capital')], max_length=10),
        ),
    ]
