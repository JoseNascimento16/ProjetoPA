from django.db import models
from django.db.models.deletion import CASCADE
from django.forms.fields import Field
from Ordens.models import Ordens
from datetime import datetime
from django.utils import timezone

class ModeloCodigos(models.Model):

    ordem = models.ForeignKey(Ordens, on_delete=models.CASCADE)
    identificacao = models.CharField(max_length=2)
    especificacao = models.CharField(max_length=500)
    justificativa = models.CharField(max_length=500)
    embalagem = models.CharField(max_length=10, choices={('unidade','unidade'),('caixa','caixa')})
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    preco_total_capital = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    preco_total_custeio = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    tipo_produto = models.CharField(max_length=10, choices={('Capital','Capital'),('Custeio','Custeio')})
    # preco_total = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    data_de_criação = models.DateTimeField(default=timezone.now, blank=True)
    inserido = models.BooleanField(default=False)
    possui_sugestao_correcao = models.BooleanField(default=False)
    quebra_de_linha = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.identificacao

    # def clean_ordem(self):
    #     if self.instance and self.instance.pk:
    #         return self.instance.ordem
    #     else:
    #         return self.cleaned_data['ordem']

    