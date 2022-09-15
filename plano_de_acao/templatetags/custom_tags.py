from sys import api_version
from django import template
from django.shortcuts import get_object_or_404
from fia.models import Modelo_fia
from plano_de_acao.models import Plano_de_acao
from usuarios.models import Classificacao


register = template.Library()

@register.simple_tag
def tag_any(a,b):
    if any(item.user == a for item in b):
        return a
    return False

@register.simple_tag
def tag_any2(funcionarios,b):
    for funcionario in funcionarios:
        if any(item.user.last_name == 'Tesoureiro(a)' for item in b):
            if funcionario.user.last_name == 'Tesoureiro(a)':
                return funcionario
    return False

@register.simple_tag
def tag_any3(funcionario,b):
    if any(item.user == funcionario.user for item in b):
        if funcionario.user.last_name == 'Membro do colegiado':
            return funcionario
    return False

@register.simple_tag
def tag_membro(membro,b):
    if any(item.user.first_name == membro.first_name for item in b):
        return membro
    return False

@register.simple_tag
def tag_len_alto_cargo(classificacoes):
    lista_alto_cargo=[]
    for item in classificacoes:
        if item.tipo_de_acesso == 'Func_sec' and item.assina_plano and item.is_active:
            lista_alto_cargo.append(item)
    tamanho = len(lista_alto_cargo)
    return tamanho

@register.simple_tag
def tag_len_suprof(assinaturas):
    lista_assinaturas_suprof=[]
    for item in assinaturas:
        if item.tipo_de_acesso == 'Func_sec':
            lista_assinaturas_suprof.append(item)
    tamanho = len(lista_assinaturas_suprof)
    return tamanho

@register.simple_tag
def tag_assinaturas_suprof(counter,b):
    lista_assinaturas_suprof=[]
    for item in b:
        if item.tipo_de_acesso == 'Func_sec':
            lista_assinaturas_suprof.append(item)
    
    for item in lista_assinaturas_suprof:
        return lista_assinaturas_suprof[counter]

@register.simple_tag
def tag_assinaturas_suprof_fia(assinaturas):
    lista_assinaturas_suprof=[]
    for item in assinaturas:
        if item.tipo_de_acesso == 'Func_sec':
            lista_assinaturas_suprof.append(item)
    
    return lista_assinaturas_suprof

@register.simple_tag
def tag_len_funcionarios(classificacoes, escola, objeto_plano_elemento):
    if objeto_plano_elemento.tipo_fia:
        tamanho = 4
        return tamanho
    else:
        lista_funcionarios=[]
        for item in classificacoes:
            if item.tipo_de_acesso == 'Funcionario' and item.matriz == escola:
                lista_funcionarios.append(item)
            elif item.tipo_de_acesso == 'Escola' and item.user.last_name == escola:
                lista_funcionarios.append(item)
        tamanho = len(lista_funcionarios)
        return tamanho

@register.simple_tag
def tag_len_assinaturas(assinaturas, objeto_plano):
    lista_assinaturas=[]
    for item in assinaturas:
        if item.tipo_de_acesso == 'Funcionario' or item.tipo_de_acesso == 'Escola':
            lista_assinaturas.append(item)
    tamanho = len(lista_assinaturas)
    if objeto_plano.tipo_fia:
        modelo_fia = get_object_or_404(Modelo_fia, plano=objeto_plano)
        if modelo_fia.assinatura_tecnico:
            tamanho += 1
    return tamanho

@register.simple_tag
def tag_loop1(numero):
    lista_elementos=[]
    for elemento in range(numero):
        lista_elementos.append(elemento)
    return lista_elementos

@register.simple_tag
def tag_first_last_names(valor):
    lista_elementos = list(valor.split(" "))
    return lista_elementos

@register.simple_tag
def tag_verifica_membro_colegiado(objeto_plano, user):
    modelo_fia = get_object_or_404(Modelo_fia, plano=objeto_plano)
    if modelo_fia.membro_colegiado_1 and user.first_name == modelo_fia.membro_colegiado_1.first_name:
        return True
    elif modelo_fia.membro_colegiado_2 and user.first_name == modelo_fia.membro_colegiado_2.first_name:
        return True
    else:
        return False

@register.simple_tag
def tag_verifica_diretor(objeto_escola):
    from usuarios.alteracoes import identifica_diretor
    diretor = identifica_diretor(objeto_escola.id)
    
    return diretor