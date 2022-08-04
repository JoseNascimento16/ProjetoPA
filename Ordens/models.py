from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, IntegerField
from plano_de_acao.models import Plano_de_acao
from datetime import datetime


# Create your models here.

class Ordens(models.Model):
    plano = models.ForeignKey(Plano_de_acao, on_delete=models.CASCADE)
    identificacao_numerica = models.IntegerField()
    descricao_do_problema = models.TextField(max_length=500)
    prazo_execucao_inicial = models.DateField(null=True, blank=True)
    prazo_execucao_final = models.DateField(null=True, blank=True)
    resultados_esperados = models.TextField(max_length=500)
    data_de_criação = models.DateTimeField(default=datetime.now, blank=True)
    inserida = BooleanField(default=False)
    codigos_inseridos = IntegerField(default=0)
    quebra_de_linha = IntegerField(default=0)
    ordem_rowspan = IntegerField(default=0)
    possui_sugestao_correcao = BooleanField(default=False)


    def __str__(self):
        string1 = str(self.identificacao_numerica)
        string2 = self.plano.ano_referencia
        return 'Ordem: ' + string1 + '. Plano: ' + string2

class ControleOrdens(models.Model):
    todas_inseridas = BooleanField()
    comando_todas = BooleanField(default=False)
    comando_individual = BooleanField(default=False)
    var_template = IntegerField(default=0)