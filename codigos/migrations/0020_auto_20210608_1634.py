# Generated by Django 3.1.7 on 2021-06-08 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codigos', '0019_auto_20210608_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelocodigos',
            name='preco_total',
        ),
        migrations.AddField(
            model_name='modelocodigos',
            name='preco_total_capital',
            field=models.DecimalField(decimal_places=2, max_digits=14, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='modelocodigos',
            name='preco_total_custeio',
            field=models.DecimalField(decimal_places=2, max_digits=14, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='modelocodigos',
            name='embalagem',
            field=models.CharField(choices=[('caixa', 'caixa'), ('unidade', 'unidade')], max_length=10),
        ),
        migrations.AlterField(
            model_name='modelocodigos',
            name='tipo_produto',
            field=models.CharField(choices=[('Custeio', 'Custeio'), ('Capital', 'Capital')], max_length=10),
        ),
    ]
