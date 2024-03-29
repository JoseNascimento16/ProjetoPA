from django.db import models
from django.contrib.auth.models import User

from plano_de_acao.models import Plano_de_acao

# Create your models here.

class Modelo_fia(models.Model):
    plano = models.ForeignKey(Plano_de_acao, on_delete=models.CASCADE)
    nome_caixa_escolar = models.CharField(max_length=100, blank=True)
    ano_exercicio = models.IntegerField(blank=True, null=True)
    valor_numerico = models.IntegerField(default=1, blank=True)
    discriminacao = models.CharField(max_length=900, blank=True)
    quantidade = models.IntegerField(default=0, blank=True)
    preco_unitario_item = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, max_length=50, null=True)
    valor_total_anterior = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    valor_total_atual = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True, blank=True)
    valor_total_item = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    valor_total_fia = models.DecimalField(max_digits=14, decimal_places=2, max_length=50, null=True)
    justificativa = models.CharField(max_length=900, blank=True)
    possui_sugestao_correcao = models.BooleanField(default=False)
    membro_colegiado_1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='membro1')
    membro_colegiado_2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='membro2')
    tecnico_responsavel = models.CharField(max_length=100, blank=True)
    assinatura_tecnico = models.ImageField(upload_to='SetupPrincipal/img/signs', blank=True, null=True, verbose_name='Assinatura')
    quebra_de_linha = models.IntegerField(default=0)

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
    quebra_de_linha = models.IntegerField(default=0)