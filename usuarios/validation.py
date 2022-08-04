from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import re
# from django.core import validators

# VALIDACAO DE FUNCIONARIOS

def funcionario_ja_cadastrado(valor_first_name, first_name, lista_de_erros):
    instancia_user = User.objects.filter(first_name=valor_first_name).exists()
    if instancia_user:
        lista_de_erros[first_name] = 'Usuário já está cadastrado(a)'

def funcao_nao_foi_selecionada(valor_cargo, cargo, lista_de_erros):
    if valor_cargo == '-------':
        lista_de_erros[cargo] = 'Escolha o cargo do funcionário'

def login_ja_existe(valor, campo, lista_de_erros):
    instancia_user = User.objects.filter(username=valor).exists()
    if instancia_user:
        lista_de_erros[campo] = 'Este login não está disponível, escolha outro'

def senhas_nao_sao_iguais(valor_password1, valor_password2, campo, lista_de_erros):
    if valor_password1 != valor_password2:
        lista_de_erros[campo] = 'As senhas não coincidem...'
    
def campo_none(valor, campo, lista_de_erros):
    if not valor:
        lista_de_erros[campo] = 'Preencha este campo corretamente...'

def iniciou_com_espaco_em_branco(valor, campo, lista_de_erros):
    # testando = re.search(r'^\s', valor) 
    # print(testando)
    # if testando:
    #     lista_de_erros[campo] = 'Não inclua espaços no início...'
    # if valor[0] == ' ' or valor[0] == ' ':
    #     lista_de_erros[campo] = 'Não inclua espaços no início...'
    pass

def campo_em_branco(valor, campo, lista_de_erros):
    valor.strip()
    if not valor:
        lista_de_erros[campo] = 'Preencha o campo...'

def campo_contem_espacos(valor, campo, lista_de_erros):
    if valor:
        testando = re.search('\s', valor) 
        if testando:
            lista_de_erros[campo] = 'Não inclua espaços neste campo...'

def valida_minimo_caracter_senha(valor, campo, lista_de_erros):
    if valor:
        if len(valor) < 6:
            lista_de_erros[campo] = 'A senha deve conter no mínimo 6 digitos...'

# VALIDACAO DE ESCOLAS (algumas validacoes acima também foram reaproveitadas)

def escola_ja_cadastrada(valor, campo, lista_de_erros):
    instancia_user = User.objects.filter(last_name=valor).exists()
    if instancia_user:
        lista_de_erros[campo] = 'Já existe cadastro para esta escola...'

def nome_contem_numeros(valor, campo, lista_de_erros):
    if valor:
        checa = bool(re.search(r'\d', valor) ) #checa se contém numeros no nome do diretor(a)
        if checa:
            lista_de_erros[campo] = 'Não inclua números...'
        # if any(char.isdigit() for char in valor):

