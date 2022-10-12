from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from plano_de_acao.models import Plano_de_acao

def plano_ja_existe(valor, campo, escola, lista_de_erros):
    instancia_plano = Plano_de_acao.objects.filter(ano_referencia=valor).filter(escola=escola).exists()
    if instancia_plano:
        lista_de_erros[campo] = 'Já existe um plano com este nome, escolha outro...'

def plano_ja_existe2(valor, campo, escola, lista_de_erros):
    instancia_plano = Plano_de_acao.objects.filter(ano_referencia=valor).filter(escola=escola).exists()
    if instancia_plano:
        lista_de_erros[campo] = 'Este nome já está sendo utilizado, defina outro...'

def inicia_com_FIA(valor, campo, lista_de_erros):
    if valor.startswith('FIA'):
        lista_de_erros[campo] = 'Não inicie nomes de planos com a identificação FIA...'



