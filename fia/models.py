from django.db import models

from plano_de_acao.models import Plano_de_acao

# Create your models here.

class Modelo_fia(models.Model):
    plano = models.ForeignKey(Plano_de_acao, on_delete=models.CASCADE)
    nome_caixa_escolar = models.CharField(max_length=100, blank=True)
    ano_exercicio = models.IntegerField(blank=True, null=True)
    valor_numerico = models.IntegerField(default=1, blank=True)
    discriminacao = models.CharField(max_length=900, blank=True)
    quantidade = models.IntegerField(default=0, blank=True)
    preco_unitario_item = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    valor_total_anterior = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    valor_total_atual = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True, blank=True)
    valor_total_item = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    valor_total_fia = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    justificativa = models.CharField(max_length=900, blank=True)
    possui_sugestao_correcao = models.BooleanField(default=False)

    def __str__(self):
        return self.plano.ano_referencia

class Extra_fia(models.Model):
    fia_matriz = models.ForeignKey(Modelo_fia, on_delete=models.CASCADE)
    valor_numerico = models.IntegerField(default=0, blank=True)
    discriminacao = models.CharField(max_length=900, blank=True)
    quantidade = models.IntegerField(default=0, blank=True)
    preco_unitario_item = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    valor_total_item = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    justificativa = models.CharField(max_length=900, blank=True)
    possui_sugestao_correcao = models.BooleanField(default=False)