from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from plano_de_acao.models import Plano_de_acao
from usuarios.models import Classificacao

def pesquisa_escolas_cadastradas(request):
    lista_escolas_pesquisa = []
    
    if request.method == 'POST':
        valor_pesquisa = request.POST['campo']
        if valor_pesquisa == '' or valor_pesquisa.startswith(' '):
            pass
        else:
            escolas = User.objects.filter(last_name__icontains=valor_pesquisa).filter(is_active=True)
            municipios = Classificacao.objects.filter(municipio__icontains=valor_pesquisa)
            diretores = User.objects.filter(first_name__icontains=valor_pesquisa).filter(is_active=True)
            
            if escolas.exists():
                for elemento in escolas:
                    if elemento.classificacao.tipo_de_acesso == 'Escola':
                        escolas_cadastradas = Classificacao.objects.filter(user=elemento)
                        for escola in escolas_cadastradas:
                            lista_escolas_pesquisa.append(escola)

            elif municipios.exists():
                for municipio in municipios:
                    lista_escolas_pesquisa.append(municipio)

            elif diretores.exists():
                for diretor in diretores:
                    if diretor.classificacao.tipo_de_acesso == 'Escola':
                        escolas_cadastradas = Classificacao.objects.filter(user=diretor)
                        for escola in escolas_cadastradas:
                            lista_escolas_pesquisa.append(escola)
            
    else:
        pass

    return lista_escolas_pesquisa

def pesquisa_funcionarios_cadastrados(request):
    lista_func_pesquisa = []
    
    if request.method == 'POST':
        valor_pesquisa = request.POST['campo']
        if valor_pesquisa == '' or valor_pesquisa.startswith(' '):
            pass
        else:
            funcionarios = User.objects.filter(first_name__icontains=valor_pesquisa).filter(is_active=True)
            
            if funcionarios.exists():
                for elemento in funcionarios:
                    if elemento.classificacao.tipo_de_acesso == 'Func_sec':
                        funcionarios_cadastrados = Classificacao.objects.filter(user=elemento)
                        for funcionario in funcionarios_cadastrados:
                            lista_func_pesquisa.append(funcionario)
            
    else:
        pass

    return lista_func_pesquisa