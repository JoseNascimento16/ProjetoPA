# Generated by Django 3.1.7 on 2022-08-06 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0025_auto_20220806_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classificacao',
            name='assinatura',
            field=models.ImageField(blank=True, null=True, upload_to='SetupPrincipal/img/signs', verbose_name='Assinatura'),
        ),
    ]
