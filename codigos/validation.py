from codigos.models.codigos import ModeloCodigos
from django.shortcuts import get_object_or_404
from .models import Ordens

def campo_tem_algum_numero(valor_identificacao, identificacao, lista_de_erros):
    if valor_identificacao:
        if any(char.isdigit() for char in valor_identificacao):
            print('Campo tem numero')
            lista_de_erros[identificacao] = 'Identificação inválida: não inclua números'

def campo_possui_mais_de_1_caractere(valor_identificacao, identificacao, lista_de_erros):
    if valor_identificacao:
        if len(valor_identificacao) > 1 :
            print('Campo possui mais de um caractere')
            lista_de_erros[identificacao] = 'Identificação inválida: Use somente 1 letra'

def campos_sao_iguais(valor_especificacao, valor_justificativa, justificativa, lista_de_erros):
    if valor_especificacao == valor_justificativa:
        lista_de_erros[justificativa] = 'Especificacao e Justificativa não podem ser iguais'
        
def nao_escolheu_field(valor, campo, lista_de_erros):
    if valor:
        if valor == '-------': 
            lista_de_erros[campo] = 'Selecione uma opção...'

def valor_minimo_1(valor_quantidade, quantidade, lista_de_erros):
    if valor_quantidade:
        if valor_quantidade < 1:
            lista_de_erros[quantidade] = 'O valor mínimo é 1'

def somente_valores_positivos(valor_preco_unitario, preco_unitario, lista_de_erros):
    if valor_preco_unitario:
        if valor_preco_unitario < 0:
            lista_de_erros[preco_unitario] = 'Não inclua valores negativos'

def valor_ja_esta_sendo_usado(valor, campo, lista_De_erros, valor_ordem_id):
    if valor:
        instancia_ordem = get_object_or_404(Ordens, pk=valor_ordem_id)
        valor_maiusculo = valor.upper()
        if ModeloCodigos.objects.filter(ordem=instancia_ordem.id).filter(identificacao=valor_maiusculo).exists():
            lista_De_erros[campo] = 'A letra ' + valor + ' já está sendo usada, escolha outra...'