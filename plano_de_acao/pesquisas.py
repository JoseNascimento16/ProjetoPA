from string import whitespace
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from Escolas.models import Escola
from plano_de_acao.models import Plano_de_acao

# Funções que definem quais planos serão mostrados em caso de uma pesquisa.

def pesquisa_func_sec(request):
    lista_planos_pesquisa = []
    
    if request.method == 'POST':
        valor_pesquisa = request.POST['campo']
    else:
        valor_pesquisa = request.GET.get('q','')

    if valor_pesquisa == '' or valor_pesquisa.startswith(' '):
        pass
    else:
        escolas = Escola.objects.filter(nome__icontains=valor_pesquisa)
        nome_planos = Plano_de_acao.objects.filter(ano_referencia__icontains=valor_pesquisa).exclude(situacao='Em desenvolvimento')
        diretores_ou_corretores = User.objects.filter(first_name__icontains=valor_pesquisa)
        situacoes = Plano_de_acao.objects.filter(situacao__icontains=valor_pesquisa).exclude(situacao='Em desenvolvimento')
        
        if nome_planos.exists():
            for plano in nome_planos:
                lista_planos_pesquisa.append(plano)

        elif escolas.exists():
            for elemento in escolas:
                planos_pesquisa = Plano_de_acao.objects.filter(escola=elemento).exclude(situacao='Em desenvolvimento')
                for plano in planos_pesquisa:
                    lista_planos_pesquisa.append(plano)

        elif diretores_ou_corretores.exists():
            for elemento in diretores_ou_corretores:
                if elemento.groups.get().name == 'Diretor_escola':
                    planos_pesquisa = Plano_de_acao.objects.filter(escola=elemento.escola).exclude(situacao='Em desenvolvimento')
                    for plano in planos_pesquisa:
                        lista_planos_pesquisa.append(plano)
                elif elemento.groups.get().name == 'Func_sec':
                    planos_pesquisa = Plano_de_acao.objects.filter(corretor_plano=elemento).exclude(situacao='Em desenvolvimento')
                    for plano in planos_pesquisa:
                        lista_planos_pesquisa.append(plano)

        elif situacoes.exists():
            for plano in situacoes:
                lista_planos_pesquisa.append(plano)
            
    # else:
    #     return redirect('pagina_planos_de_acao')

    return lista_planos_pesquisa

def pesquisa_escola(request):
    lista_planos_pesquisa = []
    objeto_escola = request.user.classificacao.escola

    if request.method == 'POST':
        valor_pesquisa = request.POST['campo']
    else:
        valor_pesquisa = request.GET.get('q','')

    if valor_pesquisa == '' or valor_pesquisa.startswith(' '):
        pass
    else:
        nome_planos = Plano_de_acao.objects.filter(escola=objeto_escola).filter(ano_referencia__icontains=valor_pesquisa)
        situacoes = Plano_de_acao.objects.filter(escola=objeto_escola).filter(situacao__icontains=valor_pesquisa)
        escola = Escola.objects.filter(nome__icontains=valor_pesquisa)
        corretores = User.objects.filter(first_name__icontains=valor_pesquisa)
        
        if nome_planos.exists():
            for plano in nome_planos:
                lista_planos_pesquisa.append(plano)

        elif situacoes.exists():
            for plano in situacoes:
                lista_planos_pesquisa.append(plano)

        elif escola.exists():
            for elemento in escola:
                planos_pesquisa = Plano_de_acao.objects.filter(escola=objeto_escola)
                for plano in planos_pesquisa:
                    lista_planos_pesquisa.append(plano)
                    
        elif corretores.exists():
            for elemento in corretores:
                if elemento.groups.get().name == 'Func_sec':
                    planos_pesquisa = Plano_de_acao.objects.filter(escola=objeto_escola).filter(corretor_plano=elemento)
                    for plano in planos_pesquisa:
                        lista_planos_pesquisa.append(plano)
            

    return lista_planos_pesquisa