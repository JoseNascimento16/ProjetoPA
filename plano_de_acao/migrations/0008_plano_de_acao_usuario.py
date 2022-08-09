# Generated by Django 3.1.7 on 2021-04-18 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_email'),
        ('plano_de_acao', '0007_auto_20210417_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='plano_de_acao',
            name='usuario',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuario'),
            preserve_default=False,
        ),
    ]