# Generated by Django 4.1.4 on 2022-12-16 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0043_classificacao_login_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classificacao',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='turmas',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
