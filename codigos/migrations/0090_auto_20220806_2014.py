# Generated by Django 3.1.7 on 2022-08-06 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0089_auto_20220728_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Capital', 'Capital'), ('Custeio', 'Custeio')], max_length=10),
        ),
    ]
