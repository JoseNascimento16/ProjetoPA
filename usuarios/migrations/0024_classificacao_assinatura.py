# Generated by Django 3.1.7 on 2022-08-04 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0023_turmas_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacao',
            name='assinatura',
            field=models.ImageField(blank=True, null=True, upload_to='static/img/assinaturas', verbose_name='Assinatura'),
        ),
    ]