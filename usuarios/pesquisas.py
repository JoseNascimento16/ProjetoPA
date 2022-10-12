from msilib.schema import Class
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from plano_de_acao.models import Plano_de_acao
from usuarios.models import Classificacao
from Escolas.models import Escola

def pesquisa_escolas_cadastradas(request):
    lista_escolas_pesquisa = []
    
    if request.method == 'POST':
        valor_pesquisa = request.POST['campo']
        if valor_pesquisa == '' or valor_pesquisa.startswith(' '):
            pass
        else:
            escolas = Escola.objects.filter(nome__icontains=valor_pesquisa).filter(is_active=True)
            municipios = Escola.objects.filter(municipio__icontains=valor_pesquisa).filter(is_active=True)
            diretores = User.objects.filter(first_name__icontains=valor_pesquisa).filter(is_active=True)
            
            if escolas.exists():
                for escola in escolas:
                    lista_escolas_pesquisa.append(escola)

            elif municipios.exists():
                for escola in municipios:
                    lista_escolas_pesquisa.append(escola)

            elif diretores.exists():
                for diretor in diretores:
                    if diretor.classificacao.diretor_escolar:
                        escola = get_object_or_404(Escola, diretor=diretor)
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
            cargos = User.objects.filter(last_name__icontains=valor_pesquisa).filter(is_active=True)
            
            if funcionarios.exists():
                for elemento in funcionarios:
                    if elemento.groups.filter(name='Func_sec').exists():
                        funcionarios_cadastrados = Classificacao.objects.filter(user=elemento)
                        for funcionario in funcionarios_cadastrados:
                            lista_func_pesquisa.append(funcionario)
            
            elif cargos.exists():
                for elemento in cargos:
                    if elemento.groups.filter(name='Func_sec').exists():
                        funcionarios_cadastrados = Classificacao.objects.filter(user=elemento)
                        for funcionario in funcionarios_cadastrados:
                            lista_func_pesquisa.append(funcionario)
            
    else:
        pass

    return lista_func_pesquisa