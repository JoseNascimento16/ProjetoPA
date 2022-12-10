from django.conf import settings
from django.core.mail import send_mail
from plano_de_acao.views import *
from .models import Correcoes, Plano_de_acao
from django.shortcuts import get_object_or_404
from usuarios.models import Classificacao
from fia.models import Modelo_fia
from datetime import date
from Escolas.models import Escola
from logs.logs import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def define_planos_coordenador(request):
    planos1 = Plano_de_acao.objects.filter(corretor_plano=request.user).exclude(situacao='Em desenvolvimento').exclude(situacao='Publicado').exclude(situacao='Necessita correção').exclude(situacao='Aprovado').exclude(situacao='Pronto').exclude(situacao='Finalizado')
    planos2 = Plano_de_acao.objects.filter(corretor_plano=None).exclude(situacao='Em desenvolvimento').exclude(situacao='Publicado').exclude(situacao='Necessita correção').exclude(situacao='Aprovado').exclude(situacao='Pronto').exclude(situacao='Finalizado')
    planos3 = planos1.union(planos2)
    planos4 = Plano_de_acao.objects.filter(Q(situacao='Assinado') | Q(situacao='Inteiramente assinado')).filter(assinatura_coordenador=False)
    planos5 = planos3.union(planos4)
    planos_assinados = request.user.classificacao.plano_associado.filter(Q(situacao='Assinado') | Q(situacao='Inteiramente assinado'))
    planos = planos5.union(planos_assinados).order_by('-data_de_criação')
    
    return planos

def define_planos_corretor(request):
    planos1 = Plano_de_acao.objects.filter(corretor_plano=request.user).exclude(alterabilidade='Escola').exclude(situacao='Finalizado')
    planos2 = Plano_de_acao.objects.filter(corretor_plano=None).filter(situacao='Pendente')
    planos = planos1.union(planos2).order_by('-data_de_criação')
    
    return planos

def zera_assinaturas(id_plano):
    plano = get_object_or_404(Plano_de_acao, pk=id_plano)
    plano.assinaturas = 0
    plano.save()

def checa_se_pode_assinar_func_sec(request, captura_plano):
    cargo = request.user.classificacao.cargo_herdado
    if captura_plano.corretor_plano == request.user and not captura_plano.assinatura_corretor:
        return True
    elif cargo == 'Coordenador' and captura_plano.corretor_plano != request.user and not captura_plano.assinatura_coordenador:
        return True
    elif cargo == 'Diretor SUPROT' and not captura_plano.assinatura_diretor:
        return True
    return False

def inclui_assinatura(elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    plano.assinaturas += 1
    plano.save()

def atualiza_assinaturas_escola(elemento_id):
    lista = []
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    
    assinaturas = plano.classificacao_set.all()
    if assinaturas:
        for item in assinaturas:
            if item.user.groups.filter(name='Funcionario').exists() or item.user.groups.filter(name='Diretor_escola').exists():
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
            if item.user.groups.filter(name='Func_sec').exists():
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
    if captura_plano.situacao == 'Assinado' and captura_plano.assinatura_corretor and captura_plano.assinatura_coordenador and captura_plano.assinatura_diretor:
        captura_plano.situacao = 'Inteiramente assinado'
        captura_plano.data_assinaturas_suprof = date.today()
        captura_plano.save()

        nome_plano = captura_plano.ano_referencia
        log_plano_inteiramente_assinado(nome_plano, captura_plano.id)

def confere_assinaturas_muda_para_pronto(request, captura_plano, captura_escola):
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

        log_plano_pronto(nome_plano, captura_plano.id)

def fia_confere_assinaturas_muda_para_pronto(request, captura_plano):
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

def define_matriz(request):
    entidade_escola = request.user.classificacao.escola
    return entidade_escola

def mostra_alerta_laranja(objeto_matriz):
    ######################
    # checa se a escola possui planos com correções
    #  mostra alerta laranja
    planos_com_correcao = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=objeto_matriz)
    if any(plano.correcoes_a_fazer > 0 and plano.situacao == 'Necessita correção' for plano in planos_com_correcao):
        return True
    else:
        return False

def gera_lista_planos_assinados(planos, checa_usuario):
    ######################
    # Gera lista de planos que o usuário logado atual já assinou
    lista_planos_assinados=[]
    for plano in planos:
            funcionario_associado = Classificacao.objects.filter(plano_associado=plano)#DE TODOS OS FUNCIONARIOS ASSOCIADOS A ESTE PLANO
            for funcionario in funcionario_associado:
                if funcionario.user_id == checa_usuario.id: #SE QUALQUER FUNCIONARIO ASSOCIADO A ESTE PLANO, TIVER O MESMO ID DO USUARIO ATUAL
                    # Adiciono à lista para que o HTML possa decidir qual botão mostrar
                    lista_planos_assinados.append(plano.ano_referencia)

    return lista_planos_assinados

def atualiza_quant_correcoes_plano(plano):
    ######################
    # Atualiza a quantidade de correções em um plano
    correcoes_no_plano = Correcoes.objects.filter(plano_associado=plano)
    plano.correcoes_a_fazer = len(correcoes_no_plano)
    plano.save()

    return len(correcoes_no_plano)

def calcula_soma_capital(codigos_iteravel):
    # SOMA OS VALORES DE TODOS PRODUTOS DO TIPO CAPITAL
    soma_capital = 0
    for elemento in codigos_iteravel:
        if elemento.preco_total_capital:
            soma_capital = soma_capital + elemento.preco_total_capital
    return soma_capital

def calcula_soma_custeio(codigos_iteravel):
    # SOMA OS VALORES DE TODOS PRODUTOS DO TIPO CUSTEIO
    soma_custeio = 0
    for elemento in codigos_iteravel:
        if elemento.preco_total_custeio:
            soma_custeio = soma_custeio + elemento.preco_total_custeio
    return soma_custeio

def normaliza_rowspan(ordens_iteravel):
    # Redundância para garantir que os valores de rowspan, codigos_inseridos (ordem) e inserido(codigo) não saiam do padrão por qualquer motivo que seja
    # Recebe todas as ordens de um plano especifico
    for ordem_OBJ in ordens_iteravel:
        if ordem_OBJ.codigos_inseridos < 0 or ordem_OBJ.ordem_rowspan < 0 or ordem_OBJ.codigos_inseridos != ordem_OBJ.ordem_rowspan:
            ordem_OBJ.codigos_inseridos = 0
            ordem_OBJ.ordem_rowspan = 0
            ordem_OBJ.save()
            codigos_dessa_ordem = ModeloCodigos.objects.order_by('identificacao').filter(ordem=ordem_OBJ)
            for codigo in codigos_dessa_ordem:
                codigo.inserido = False
                codigo.save()

def ordem_atualiza_rowspan_e_codigos_inseridos(ordem_objeto):
    # Atualiza a quantidade de codigos inseridos em uma ordem
    # Atualiza a rowspan = quantidade de codigos inseridos
    quant_codigos = ModeloCodigos.objects.filter(ordem=ordem_objeto).filter(inserido=True)
    ordem_objeto.codigos_inseridos = len(quant_codigos)
    ordem_objeto.ordem_rowspan = len(quant_codigos)
    ordem_objeto.save()

def define_destinatarios(plano):
    lista_destinatarios = []
    if not plano.tipo_fia:
        classificacoes = Classificacao.objects.filter(escola=plano.escola).filter(is_active=True)
        for item in classificacoes:
            usuario = item.user
            lista_destinatarios.append(usuario)
    elif plano.tipo_fia:
        modelo_fia = get_object_or_404(Modelo_fia, plano=plano)
        lista_destinatarios.append(modelo_fia.membro_colegiado_1)
        lista_destinatarios.append(modelo_fia.membro_colegiado_2)
        lista_destinatarios.append(plano.escola.diretor)

    return lista_destinatarios

def envia_email_plano_aprovado(request, plano):
    # ENVIA UM EMAIL INFORMANDO ÀS PARTES INTERESSADAS QUE O PLANO FOI APROVADO

    lista_destinatarios = define_destinatarios(plano)
    # print(lista_destinatarios)

    site_atual = get_current_site(request)
    for usuario in lista_destinatarios:
        contexto = {
            'first_name' : usuario.first_name,
            'plano' : plano.ano_referencia,
            'domain' : site_atual,
        }

        subject = 'SIPA - Plano aprovado'
        message = render_to_string('authentication/plano-aprovado.txt', contexto)
        remetente = settings.EMAIL_HOST_USER
        destinatario = usuario.email

        send_mail(subject, message, remetente, [destinatario], fail_silently=False)

def envia_email_plano_finalizado(request, plano):
    # ENVIA UM EMAIL INFORMANDO ÀS PARTES INTERESSADAS QUE O PLANO FOI FINALIZADO
    
    lista_destinatarios = define_destinatarios(plano)
    # print(lista_destinatarios)

    site_atual = get_current_site(request)
    for usuario in lista_destinatarios:
        contexto = {
            'first_name' : usuario.first_name,
            'plano' : plano.ano_referencia,
            'domain' : site_atual,
        }

        subject = 'SIPA - Plano finalizado'
        message = render_to_string('authentication/plano-finalizado.txt', contexto)
        remetente = settings.EMAIL_HOST_USER
        destinatario = usuario.email

        send_mail(subject, message, remetente, [destinatario], fail_silently=False)

def envia_email_plano_devolvido(request, plano):
    # ENVIA UM EMAIL INFORMANDO ÀS PARTES INTERESSADAS QUE O PLANO FOI DEVOLVIDO
    
    lista_destinatarios = define_destinatarios(plano)
    # print(lista_destinatarios)

    site_atual = get_current_site(request)
    for usuario in lista_destinatarios:
        contexto = {
            'first_name' : usuario.first_name,
            'plano' : plano.ano_referencia,
            'domain' : site_atual,
        }

        subject = 'SIPA - Plano devolvido'
        message = render_to_string('authentication/plano-devolvido.txt', contexto)
        remetente = settings.EMAIL_HOST_USER
        destinatario = usuario.email

        send_mail(subject, message, remetente, [destinatario], fail_silently=False)