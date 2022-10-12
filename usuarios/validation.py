from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import re
from Escolas.models import Escola

from usuarios.models import Classificacao
# from django.core import validators

# VALIDACAO DE FUNCIONARIOS

def funcionario_ja_cadastrado(valor_first_name, first_name, lista_de_erros):
    instancia_user = User.objects.filter(first_name=valor_first_name).exists()
    if instancia_user:
        lista_de_erros[first_name] = 'Usuário já está cadastrado(a)'

def funcao_nao_foi_selecionada(valor_cargo, cargo, lista_de_erros):
    if valor_cargo == '-------':
        lista_de_erros[cargo] = 'Escolha o cargo do funcionário'

def ja_existe_diretor(valor_cargo, cargo, lista_de_erros):
    if valor_cargo == 'Diretor':
        lista_func_sec = Classificacao.objects.filter(tipo_de_acesso='Func_sec').filter(usuario_diretor=True)
        if lista_func_sec:
            lista_de_erros[cargo] = 'Já existe um diretor da SUPROT cadastrado no sistema...'
        
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
    instancia_escola = Escola.objects.filter(nome=valor).exists()
    if instancia_escola:
        lista_de_erros[campo] = 'Já existe cadastro para esta escola...'

def chega_disponibilidade_do_cargo(valor_cargo, campo, escola, lista_de_erros):
    if valor_cargo:
        if valor_cargo == 'Tesoureiro(a)' and escola.possui_tesoureiro:
            lista_de_erros[campo] = 'Só pode existir 1 tesoureiro(a) cadastrado(a)...'
        if valor_cargo == 'Membro do colegiado' and escola.quant_membro_colegiado == 3:
            lista_de_erros[campo] = 'Limite máximo. Já existem 3 "membros do colegiado" cadastrados...'

def nome_contem_numeros(valor, campo, lista_de_erros):
    if valor:
        checa = bool(re.search(r'\d', valor) ) #checa se contém numeros no nome do diretor(a)
        if checa:
            lista_de_erros[campo] = 'Não inclua números...'
        # if any(char.isdigit() for char in valor):

def sem_sobrenome(valor, campo, lista_de_erros):
    if valor:
        lista = list(valor.split(" "))
        if len(lista) < 2:
            lista_de_erros[campo] = 'Insira ao menos um sobrenome...'

def email_ja_cadastrado(valor, user_id, campo, lista_de_erros):
    usuario = get_object_or_404(User, pk=user_id)
    usuarios = User.objects.filter(email=valor) # Só 1 objeto deve obrigatoriamente ser encontrado
    for item in usuarios:
        if usuario.email == item.email:
            pass # Permite (modo alteração)
        elif usuarios:
            lista_de_erros[campo] = 'Indisponível! Cadastre outro endereço de e-mail...'
        
def email_ja_cadastrado2(valor, campo, lista_de_erros):
    if valor:
        usuarios = User.objects.filter(email=valor) # Só 1 objeto deve obrigatoriamente ser encontrado
        if usuarios:
            lista_de_erros[campo] = 'Indisponível! Já existe usuário com este endereço de e-mail...'
