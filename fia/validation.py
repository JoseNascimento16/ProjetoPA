from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from fia.models import Extra_fia, Modelo_fia
from plano_de_acao.models import Plano_de_acao

def valor_minimo_2_extra(valor, campo, lista_de_erros):
    if valor or valor == 0:
        if valor < 2:
            lista_de_erros[campo] = 'O valor mínimo é 2...'
        
def valor_minimo_1_extra(valor, campo, lista_de_erros):
    if valor or valor == 0:
        if valor < 1:
            lista_de_erros[campo] = 'O valor mínimo é 1...'

def numero_ja_esta_sendo_usado_extra(valor, campo, lista_De_erros, valor_modelo_fia):
    if valor:
        instancia_modelo_fia = get_object_or_404(Modelo_fia, pk=valor_modelo_fia)
        if Extra_fia.objects.filter(fia_matriz=instancia_modelo_fia).filter(valor_numerico=valor).exists():
            lista_De_erros[campo] = 'Este número já está sendo usado, escolha outro...'

# PERMITE QUE NUMERO USADO SEJA IGUAL AO DA ORDEM A SER ALTERADA SOMENTE
def numero_ja_esta_sendo_usado_extra2(valor, campo, lista_De_erros, valor_modelo_fia, id_ordem_extra):
    if valor:
        instancia_modelo_fia = get_object_or_404(Modelo_fia, pk=valor_modelo_fia)
        instancia_ordem_extra = get_object_or_404(Extra_fia, pk=id_ordem_extra)
        ordens_extras = Extra_fia.objects.filter(fia_matriz=instancia_modelo_fia).filter(valor_numerico=valor)
        if ordens_extras.exists(): #checar se queryset vazio existe nessa validação!!
            for item in ordens_extras:
                if item.valor_numerico == instancia_ordem_extra.valor_numerico:
                    pass
                else:
                    lista_De_erros[campo] = 'Este número já está sendo usado, escolha outro...'

def somente_valores_positivos_extra(valor, campo, lista_de_erros):
    if valor:
        if valor < 0:
            lista_de_erros[campo] = 'Não inclua valores negativos'