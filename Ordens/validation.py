from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from plano_de_acao.models import Plano_de_acao
from Ordens.models import Ordens

def numero_ja_esta_sendo_usado(valor, campo, lista_De_erros, valor_plano_id):
    if valor:
        instancia_plano = get_object_or_404(Plano_de_acao, pk=valor_plano_id)
        if Ordens.objects.filter(plano=instancia_plano.id).filter(identificacao_numerica=valor).exists():
            lista_De_erros[campo] = 'A ordem ' + str(valor) + ' já existe, defina outro número...'

def permite_manter_mesmo_numero_de_ordem(valor, campo, lista_De_erros, valor_plano_id, valor_ordem_id):
    if valor:
        instancia_plano = get_object_or_404(Plano_de_acao, pk=valor_plano_id)
        instancia_ordem = get_object_or_404(Ordens, pk=valor_ordem_id)
        if valor != instancia_ordem.identificacao_numerica:
            if Ordens.objects.filter(plano=instancia_plano.id).filter(identificacao_numerica=valor).exists():
                lista_De_erros[campo] = 'A ordem ' + str(valor) + ' já existe, defina outro número...'

def numero_menor_que_1(valor, campo, lista_de_erros):
    if valor or valor == 0:
        if valor < 1:
            lista_de_erros[campo] = 'Somente números acima de 1...'

def numero_maior_que_100(valor, campo, lista_de_erros):
    if valor:
        if valor > 100:
            lista_de_erros[campo] = 'O valor máximo é 100...'            

def data_final_antes_da_inicial(valor1, valor2, campo, lista_de_erros):
    if valor1 and valor2 :
        if valor2 < valor1:
            lista_de_erros[campo] = 'O prazo final não pode ser anterior ao prazo inicial...'

def data_final_igual_inicial(valor1, valor2, campo, lista_de_erros):
    if valor1 and valor2 :
        if valor2 == valor1:
            lista_de_erros[campo] = 'O prazo final tem que ser posterior ao prazo inicial...'