# Generated by Django 3.1.7 on 2022-09-16 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Escolas', '0001_initial'),
        ('plano_de_acao', '0035_remove_plano_de_acao_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='plano_de_acao',
            name='escola',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Criador', to='Escolas.escola'),
        ),
    ]
