from plano_de_acao.views import *
from .models import Plano_de_acao
from django.shortcuts import get_object_or_404
from usuarios.models import Classificacao
from datetime import date

def zera_assinaturas(id_plano):
    plano = get_object_or_404(Plano_de_acao, pk=id_plano)
    plano.assinaturas = 0
    plano.save()

def inclui_assinatura(elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    plano.assinaturas += 1
    plano.save()

def atualiza_assinaturas_escola(elemento_id):
    lista = []
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    # func_que_assinam = Classificacao.objects.filter(assina_plano=True)
    
    assinaturas = plano.classificacao_set.all()
    if assinaturas:
        for item in assinaturas:
            if item.tipo_de_acesso == 'Funcionario' or item.tipo_de_acesso == 'Escola':
                lista.append(item)
        plano.assinaturas = len(lista)
    else:
        plano.assinaturas = len(lista)
        
    if not plano.tipo_fia: # plano comum
        plano.save()
    else: # Plano FIA
        modelo_fia = get_object_or_404(Modelo_fia, plano=plano)
        if modelo_fia.assinatura_tecnico:
            plano.assinaturas += 1
        plano.save()

def atualiza_assinaturas_sec(elemento_id):
    lista = []
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    # func_que_assinam = Classificacao.objects.filter(assina_plano=True)
    assinaturas = plano.classificacao_set.all()
    if assinaturas:
        for item in assinaturas:
            if item.tipo_de_acesso == 'Func_sec':
                lista.append(item)
        plano.assinaturas_sec = len(lista)
    plano.save()

def reduz_assinatura(elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    plano.assinaturas -= 1
    plano.save()

def ocorreu_alteracao(elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    if plano.situacao == 'Publicado' or plano.situacao == 'Pronto':
        plano.situacao = 'Em desenvolvimento'
        plano.save()

        zera_assinaturas(plano.id)

def plano_inteiramente_assinado(captura_plano):
    # func_que_assinam = Classificacao.objects.filter(assina_plano=True)
    if captura_plano.situacao == 'Assinado' and captura_plano.assinaturas_sec > 0 and captura_plano.assinaturas_sec == 3:
        captura_plano.situacao = 'Inteiramente assinado'
        captura_plano.data_assinaturas_suprof = date.today()
        captura_plano.save()

        nome_plano = captura_plano.ano_referencia
        log_plano_inteiramente_assinado(nome_plano, captura_plano.id)

def confere_assinaturas_muda_para_pronto(captura_plano, captura_escola):
    # Se tiver aprovado e com todas as assinaturas
    if captura_plano.situacao == 'Aprovado' and captura_plano.assinaturas > 0 and captura_plano.assinaturas == captura_escola.quant_funcionarios:
        # if request.method == 'POST':
        captura_plano.situacao = 'Pronto'
        captura_plano.data_assinaturas_escola = date.today()
        captura_plano.save()

        nome_plano = captura_plano.ano_referencia
        log_plano_pronto(nome_plano, captura_plano.id)

    # Se tiver devolvido, corrigido(publicado), permitido assinaturas e já com todas as assinaturas
    elif captura_plano.situacao == 'Publicado' and captura_plano.pre_assinatura == True and captura_plano.devolvido == True and captura_plano.assinaturas > 0 and captura_plano.assinaturas == captura_escola.quant_funcionarios:
        # if request.method == 'POST':
        
        captura_plano.situacao = 'Pronto'
        captura_plano.save()

        nome_plano = captura_plano.ano_referencia

        log_plano_aprovado_auto(nome_plano, captura_plano.id)
        log_plano_pronto(nome_plano, captura_plano.id)

def fia_confere_assinaturas_muda_para_pronto(captura_plano):
    # Se tiver aprovado e com todas as assinaturas
    if captura_plano.situacao == 'Aprovado' and captura_plano.assinaturas == 4:
        # if request.method == 'POST':
        captura_plano.situacao = 'Pronto'
        captura_plano.data_assinaturas_escola = date.today()
        captura_plano.save()

        nome_plano = captura_plano.ano_referencia
        log_plano_pronto(nome_plano, captura_plano.id)

    # Se tiver devolvido, corrigido(publicado), permitido assinaturas e já com todas as assinaturas
    elif captura_plano.situacao == 'Publicado' and captura_plano.pre_assinatura == True and captura_plano.devolvido == True and captura_plano.assinaturas == 4:
        # if request.method == 'POST':
        
        captura_plano.situacao = 'Pronto'
        captura_plano.data_assinaturas_escola = date.today()
        captura_plano.save()

        nome_plano = captura_plano.ano_referencia

        log_plano_aprovado_auto(nome_plano, captura_plano.id)
        log_plano_pronto(nome_plano, captura_plano.id)

def cria_associacao(request, captura_plano, captura_funcionario, elemento_id):
    captura_funcionario.plano_associado.add(captura_plano) #salva no banco dizendo que este usuario acabou de autorizar este plano, e portanto já assinou e não precisa mais assinar. Gera um associação many-too_many.
    atualiza_assinaturas_escola(elemento_id)
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    captura_plano.alterabilidade = 'Desativada'
    captura_plano.save()

    checa_usuario = request.user.first_name
    nome_plano = captura_plano.ano_referencia
    log_plano_assinado(nome_plano, checa_usuario, captura_plano.id)