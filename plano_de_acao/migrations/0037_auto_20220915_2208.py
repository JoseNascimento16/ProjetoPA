# Generated by Django 3.1.7 on 2022-09-16 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plano_de_acao', '0036_plano_de_acao_escola'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plano_de_acao',
            name='corretor_plano',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corretor', to=settings.AUTH_USER_MODEL),
        ),
    ]
