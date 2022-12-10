from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from Escolas.models import Escola
from fia.models import Extra_fia, Modelo_fia
from usuarios.models import Classificacao, Turmas # Turmas_plano
from codigos.models.codigos import ModeloCodigos
from Ordens.models import Ordens
from Ordens.forms import Edita_Ordem_Form, OrdemForm, Cadastra_datas_Ordem_Form
from codigos.forms import Mini_form_Codigos, CodigosForm
from plano_de_acao.forms import FiaForm, PlanoForm, Edita_planoForm, Correcoes, Correcao_acaoForm, Correcao_despesaForm, PreAssinaturaForm, AlteraCorretorForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plano_de_acao
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, time
from django.db.models import Q
from eventlog import EventGroup
from eventlog.models import Event
from logs.logs import *
from .alteracoes import *
from .pesquisas import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import json


# Create your views here.


##### VIEWS TESTADAS #####

def planos_de_acao(request, **kwargs):
    # pagina listando todos os planos de ação possíveis de serem vistos
    from .alteracoes import define_matriz, mostra_alerta_laranja, gera_lista_planos_assinados, define_planos_coordenador, define_planos_corretor
    from usuarios.alteracoes import atualiza_quant_funcionarios_da_escola, checa_se_possui_tesoureiro_e_atualiza, checa_membros_colegiado_e_atualiza
    form_plano = PlanoForm()
    form_fia = FiaForm()
    edita_plano_form = Edita_planoForm()
    form_pre_assinatura = None
    planos_possuem_correcao = False
    confirma_corrige = False
    altera_corretor = False
    var_pesquisa = False
    confirma_devolve = False
    plano_devolver=''
    corretor_form = ''
    plano_atribui = ''
    plano_altera_corretor = ''
    plano_selecionado = ''
    plano_selecionado2 = ''
    valor_pesquisa = ''
    lista_planos_assinados = []
    checa_usuario = request.user
    tipo_usuario = request.user.groups.get().name
    classificacoes = Classificacao.objects.all()
    objeto_matriz = define_matriz(request)

    if kwargs.get('mensagem') == 'Sucesso':
        messages.success(request, 'Sucesso!')
    elif kwargs.get('mensagem') == 'Criou':
        messages.success(request, 'Plano criado com sucesso!')
    elif kwargs.get('mensagem') == 'Deletou':
        messages.success(request, 'Plano excluído com sucesso!')
    elif kwargs.get('mensagem') == 'Editou':
        messages.success(request, 'Plano alterado com sucesso!')
    elif kwargs.get('mensagem') == 'Publicou':
        messages.success(request, 'Plano publicado com sucesso!')
    elif kwargs.get('mensagem') == 'Enviou':
        messages.success(request, 'Plano enviado à SUPROT com sucesso!')
    elif kwargs.get('mensagem') == 'Devolveu':
        messages.success(request, 'Plano devolvido à escola com sucesso!')
    elif kwargs.get('mensagem') == 'Concluiu':
        messages.success(request, 'Plano enviado à SUPROT com sucesso!')
    elif kwargs.get('mensagem') == 'Aprovou':
        messages.success(request, 'Plano aprovado com sucesso!')
    elif kwargs.get('mensagem') == 'Assinado':
        messages.success(request, 'Plano assinado com sucesso!')
    elif kwargs.get('mensagem') == 'Ja_assinado':
        messages.warning(request, 'Você já assinou este plano!')
    elif kwargs.get('mensagem') == 'Finalizado':
        messages.success(request, 'Plano finalizado com sucesso!')
    elif kwargs.get('mensagem') == 'Atribuiu':
        messages.success(request, 'Sucesso! Você agora é o corretor responsável por este plano!')
    elif kwargs.get('mensagem') == 'Alterou':
        messages.success(request, 'Alteração efetuada com sucesso!')
    elif kwargs.get('mensagem') == 'Sem_funcionarios':
        messages.error(request, 'Para enviar um plano, no mínimo um tesoureiro e um membro do colegiado devem ser cadastrados!')
    elif kwargs.get('mensagem') == 'Arquivado':
        messages.error(request, 'Planos arquivados não podem ser excluídos!')
    elif kwargs.get('mensagem') == 'Acesso_negado':
        messages.error(request, 'Acesso negado!')
    elif kwargs.get('mensagem') == 'Acesso_negado_situacao':
        messages.error(request, 'A situação atual do plano não permite esta alteração!')
    elif kwargs.get('mensagem') == 'Acesso_negado_situacao2':
        messages.error(request, 'A situação atual do plano não permite este acesso. Favor verificar a legenda!')
    elif kwargs.get('mensagem') == 'Sem_ordem':
        messages.error(request, 'Para enviar, é preciso ter ao menos 1 "Ordem" cadastrada e inserida no documento: Ações !')
    elif kwargs.get('mensagem') == 'Sem_codigo':
        messages.error(request, 'Para enviar, todas as ordens do plano precisam ter ao menos 1 "Código" cadastrado e inserido no documento: Ações !')
    elif kwargs.get('mensagem') == 'Ja_possui':
        messages.error(request, 'Acesso negado, já existe um responsável por este plano!')
    elif kwargs.get('mensagem') == 'preenchimento':
        messages.error(request, 'Para enviar, preencha as informações faltantes no documento FIA!')
    elif kwargs.get('mensagem') == 'grupo_incompleto':
        messages.error(request, 'Os membros para autorização do documento ainda não foram totalmente definidos...')
    elif kwargs.get('mensagem') == 'reset_corretor':
        messages.error(request, 'Somente o "corretor" deste plano pode efetuar esta ação...')
    elif kwargs.get('mensagem') == 'no_sign':
        messages.error(request, 'Você não foi cadastrado como membro assinante para este plano...')
    elif kwargs.get('mensagem') == 'no_sign_funcsec':
        messages.error(request, 'Indisponível, talvez este plano já tenha todas as assinaturas...')

    if tipo_usuario == 'Secretaria' or tipo_usuario == 'Func_sec':
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').exclude(situacao='Em desenvolvimento').exclude(situacao='Publicado').exclude(situacao='Necessita correção').exclude(situacao='Aprovado').exclude(situacao='Pronto').exclude(situacao='Finalizado')
        
        if tipo_usuario == 'Func_sec':

            if kwargs.get('search'): #Se for efetuada uma pesquisa por planos

                planos = pesquisa_func_sec(request)
                var_pesquisa = True
                if request.method == 'POST':
                    valor_pesquisa = request.POST['campo']
                else:
                    valor_pesquisa = request.GET.get('q','')

            else:
                if checa_usuario.classificacao.usuario_diretor:
                    planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(Q(situacao='Assinado') | Q(situacao='Inteiramente assinado'))
                    
                elif checa_usuario.classificacao.usuario_coordenador:
                    planos = define_planos_coordenador(request)
                else:
                    planos = define_planos_corretor(request)

            # transforma em "Inteiramente assinado" o plano caso já tenha todas as assinaturas necessárias
            from .alteracoes import plano_inteiramente_assinado
            for item in planos:
                if item.situacao == 'Assinado':
                    plano_inteiramente_assinado(item)

            # Cria lista de planos assinados para Func_sec
            if objeto_matriz.objeto_suprot == True: # Se for funcionário da secretaria
                for plano in planos:# ESTOU NO PLANO
                    funcionario_associado = Classificacao.objects.filter(plano_associado=plano)#DE TODOS OS FUNCIONARIOS ASSOCIADOS A ESTE PLANO
                    for funcionario in funcionario_associado:
                        if funcionario.user_id == checa_usuario.id: #SE QUALQUER FUNCIONARIO ASSOCIADO A ESTE PLANO, TIVER O MESMO ID DO USUARIO ATUAL
                            # Adiciono à lista para que o HTML possa decidir qual botão mostrar
                            lista_planos_assinados.append(plano.ano_referencia)

        elif tipo_usuario == 'Secretaria':
            if kwargs.get('search'): #Se for efetuada uma pesquisa por planos

                planos = pesquisa_func_sec(request)
                var_pesquisa = True
                if request.method == 'POST':
                    valor_pesquisa = request.POST['campo']
                else:
                    valor_pesquisa = request.GET.get('q','')

        # Se plano estiver pra ser devolvido com correções, manda formulário para permitir marcar checkbox de pré assinatura
        if any(plano.pre_analise_acao and plano.pre_analise_despesa and plano.correcoes_a_fazer > 0 for plano in planos):
            form_pre_assinatura = PreAssinaturaForm()
                               
    elif tipo_usuario == 'Diretor_escola':
        escola = request.user.classificacao.escola
        escola.possui_tesoureiro = checa_se_possui_tesoureiro_e_atualiza(escola)
        escola.quant_membro_colegiado = checa_membros_colegiado_e_atualiza(escola)
        atualiza_quant_funcionarios_da_escola(escola)
        escola.save()
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=objeto_matriz).filter(~Q(situacao='Pendente')).filter(~Q(situacao='Concluido')).filter(~Q(situacao='Necessita correção')).filter(~Q(situacao='Corrigido pela escola')).filter(~Q(situacao='Finalizado')).filter(~Q(situacao='Assinado')).filter(~Q(situacao='Inteiramente assinado'))

        ######################
        #Se for efetuada uma pesquisa por planos   
        if kwargs.get('search'): 
            planos = pesquisa_escola(request)
            var_pesquisa = True
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')
        ######################

        lista_planos_assinados = gera_lista_planos_assinados(planos, checa_usuario)

        planos_possuem_correcao = mostra_alerta_laranja(objeto_matriz)

    elif tipo_usuario == 'Funcionario':
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=objeto_matriz).filter(~Q(situacao='Pendente')).filter(~Q(situacao='Concluido')).filter(~Q(situacao='Necessita correção')).filter(~Q(situacao='Corrigido pela escola')).filter(~Q(situacao='Finalizado')).filter(~Q(situacao='Assinado')).filter(~Q(situacao='Inteiramente assinado'))
        
        lista_planos_assinados = gera_lista_planos_assinados(planos, checa_usuario)

    ##########################################################################
    # abre modal de confirmação de atribuição de corretor para o plano
    if kwargs.get('atribui'): 
        confirma_corrige = True
        plano_atribui = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])

    # abre modal para alteração do corretor do plano
    if kwargs.get('alt_corretor'): 
        altera_corretor = True
        plano_altera_corretor = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
        corretor_form = AlteraCorretorForm()
        corretor_form.fields['campo'].initial = plano_altera_corretor.corretor_plano

    # abre modal para devolução de planos com correções
    if kwargs.get('devolve'): 
        confirma_devolve = True
        plano_devolver = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id']) 
    ##########################################################################

    # Configura paginator
    paginator_planos = Paginator(planos, 10)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)
    ##########################################################################
    
    if kwargs.get('edita_plano'):
        plano_selecionado = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
        plano_selecionado2 = Plano_de_acao.objects.filter(pk=kwargs['elemento_id'])

        edita_plano_form.fields['ano_referencia'].initial = plano_selecionado.ano_referencia

    dados = {
        'chave_planos' : page,
        'dicionario_planos' : planos,
        'chave_form_planos' : form_plano,
        'chave_form_fia' : form_fia,
        'chave_tipo_usuario' : tipo_usuario,
        'chave_planos_com_correcao' : planos_possuem_correcao,
        'chave_planos_assinados' : lista_planos_assinados,
        'chave_pre_assinatura' : form_pre_assinatura,
        'chave_classificacoes' : classificacoes,
        'chave_edita_plano_form' : edita_plano_form,
        'contexto_edicao_plano' : plano_selecionado,
        'chave_contexto_edicao_plano' : plano_selecionado2,
        'chave_confirma_corrige' : confirma_corrige,
        'chave_plano_atribui' : plano_atribui,
        'chave_plano_altera_corretor' : plano_altera_corretor,
        'chave_altera_corretor' : altera_corretor,
        'chave_corretor_form' : corretor_form,
        'chave_var_pesquisa' : var_pesquisa,
        'chave_valor_pesquisa' : valor_pesquisa,
        'chave_confirma_devolve' : confirma_devolve,
        'chave_plano_devolver' : plano_devolver,
    }

    # Retorna o contexto para a função "cria_plano" que o chamou
    if kwargs.get('falha_novo_plano'):
        return dados
    else:
        return render(request, 'planos_de_acao.html', dados)

def planos_finalizados(request): # pagina dos planos já finalizados
    tipo_usuario = request.user.groups.get().name
    escola = request.user.classificacao.escola
    planos_finalizados = True

    if tipo_usuario == 'Secretaria' or tipo_usuario == 'Func_sec':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(situacao='Finalizado')
    elif tipo_usuario == 'Diretor_escola':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=escola).filter(situacao='Finalizado')
    elif tipo_usuario == 'Funcionario':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=escola).filter(situacao='Finalizado')

    paginator_planos = Paginator(planos, 2)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    dados = {
        'chave_planos' : page,
        'chave_tipo_usuario': tipo_usuario,
        'chave_planos_finalizados' : planos_finalizados
    }

    return render(request, 'planos_de_acao.html', dados)

def planos_a_serem_corrigidos(request,**kwargs): # pagina dos planos já aprovados
    tipo_usuario = request.user.groups.get().name
    pagina_correcoes = True
    escola = request.user.classificacao.escola

    if tipo_usuario == 'Secretaria' or tipo_usuario == 'Func_sec':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(situacao ='Necessita correção')
    elif tipo_usuario == 'Diretor_escola':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=escola).filter(situacao='Necessita correção')
    elif tipo_usuario == 'Funcionario':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=escola).filter(situacao='Necessita correção')

    paginator_planos = Paginator(planos, 2)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    dados = {
        'chave_planos' : page,
        'chave_tipo_usuario' : tipo_usuario,
        'chave_pagina_correcoes' : pagina_correcoes,
    }

    return render(request, 'planos_de_acao.html', dados)

def plano(request, **kwargs):# acesso às ordens de um plano
    checa_usuario = request.user
    tipo_usuario = request.user.groups.get().name
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])

    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola' and plano_objeto.tipo_fia == False:

        if kwargs.get('mensagem') == 'Criou':
            messages.success(request, 'Ordem criada com sucesso!')
        elif kwargs.get('mensagem') == 'Deletou':
            messages.success(request, 'Ordem excluída com sucesso!')
        elif kwargs.get('mensagem') == 'Editou':
            messages.success(request, 'Ordem alterada com sucesso!')

        abre_nova_ordem = False
        ordem = False
        form_ordem = False
        plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
        plano2 = Plano_de_acao.objects.filter(pk=kwargs['plano_id'])
        ordem2 = Ordens.objects.order_by('identificacao_numerica').filter(plano=kwargs['plano_id'])

        if kwargs.get('gera_ordem'):
            abre_nova_ordem = True
            form_ordem = OrdemForm()
            
        plano_a_exibir = {
            'chave_planos' : plano_objeto,
            'chave_planos2' : plano2,
            'chave_ordens' : ordem,
            'chave_ordens2' : ordem2,
            'chave_tipo_usuario' : tipo_usuario,
            'chave_form_ordem' : form_ordem,
            'chave_abre_nova_ordem' : abre_nova_ordem,
        }

        if kwargs.get('contx_edita_ordem') or kwargs.get('contx_cria_ordem'):
            return plano_a_exibir
            
        return render(request, 'plano.html', plano_a_exibir)

    else:
        if tipo_usuario == 'Diretor_escola':
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao2')
        else:
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def abre_edicao_ordem(request, **kwargs): #elemento_id é o id do plano
    tipo_usuario = request.user.groups.get().name
    plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])

    if tipo_usuario == 'Diretor_escola' and plano.alterabilidade == 'Escola':
        plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
        ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        plano2 = Plano_de_acao.objects.filter(pk=kwargs['plano_id'])
        ordem2 = Ordens.objects.order_by('identificacao_numerica').filter(plano=kwargs['plano_id'])

        edita_ordem_existente = True

        form_ordem = OrdemForm()
        form_ordem.fields['identificacao_numerica'].initial = ordem.identificacao_numerica
        form_ordem.fields['descricao_do_problema'].initial = ordem.descricao_do_problema
        # form_ordem.fields['prazo_execucao_inicial'].initial = ordem.prazo_execucao_inicial
        # form_ordem.fields['prazo_execucao_final'].initial = ordem.prazo_execucao_final
        form_ordem.fields['resultados_esperados'].initial = ordem.resultados_esperados

        plano_a_exibir = {
            'chave_planos' : plano,
            'chave_planos2' : plano2,
            'chave_ordens2' : ordem2,
            'chave_ordens' : ordem,
            'chave_form_ordem' : form_ordem,
            'chave_edita_ordem_existente' : edita_ordem_existente,
        }

        return render(request, 'plano.html', plano_a_exibir)
    
    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao2')

def acao_plano(request, **kwargs): # visualização acao principal
    
    from .alteracoes import normaliza_rowspan
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    plano_iteravel = Plano_de_acao.objects.filter(pk=kwargs['elemento_id'])
    ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto)
    codigos_iteravel=[]
    ordens_sem_codigo=[]
    ordens_lista=[]
    ordens_lista2=[]
    membros_colegiado=[]
    quant_de_membros = 0
    funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome)
    checa_usuario = request.user
    tipo_usuario = request.user.groups.get().name
    situacao_plano = plano_objeto.situacao
    contexto_abre_form_datas = False
    var_reset = False
    apos_print = False
    quebra_linha = False
    var_plano_pre_aprovado = False
    ordem_data = ''
    form_datas = Cadastra_datas_Ordem_Form()
    erro_form_datas = False

    for item in funcionarios:
        if item.user.last_name == 'Membro do colegiado':
            membros_colegiado.append(item)
    
    if kwargs.get('mensagem') == 'Criou':
        messages.success(request, 'Sugestão de correção criada com sucesso!')
    elif kwargs.get('mensagem') == 'Deletou':
        messages.success(request, 'Sugestão de correção excluída com sucesso!')
    elif kwargs.get('mensagem') == 'Editou':
        messages.success(request, 'Sugestão de correção alterada com sucesso!')
    elif kwargs.get('mensagem') == 'Sucesso':
        messages.success(request, 'Sucesso!')
    elif kwargs.get('mensagem') == 'Sucesso2':
        if request.method == 'GET' and 'postprint' not in request.GET:
            messages.success(request, 'Alteração efetuada com sucesso!')
    elif kwargs.get('mensagem') == 'Datas':
        messages.error(request, 'Para concluir é necessário definir as datas de todos os "prazos de execução"!')
    elif kwargs.get('mensagem') == 'Nao_corretor':
        messages.error(request, 'Você não é o corretor responsável por este plano')
    elif kwargs.get('mensagem') == 'Erro':
        messages.error(request, 'Ocorreu algum erro!')
    elif kwargs.get('mensagem') == 'Acesso_negado':
        messages.error(request, 'Acesso negado!')
    elif kwargs.get('mensagem') == 'Acesso_negado_situacao':
        messages.error(request, 'A situação do plano não permite que ele seja modificado no momento...!')

    # Redundância para garantir que os valores de rowspan, codigos_inseridos (ordem) e inserido(codigo) não saiam do padrão por qualquer motivo que seja
    normaliza_rowspan(ordens_iteravel)
    ##########################################

    # Todas as ordens deste plano
    for elemento in ordens_iteravel: 
        codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
        if not codigos_varredura: # Se a ordem nao possuir codigos, manda essa informação pro contexto
            ordens_sem_codigo.append(elemento)
        for items in codigos_varredura:
            codigos_iteravel.append(items) # Lista com todos os 'OBJETOS codigo' de todas as ordens deste plano
    ##########################################

    #LISTA COM NUMERO DAS ORDENS DESSE PLANO
    for elemento in ordens_iteravel:
        ordens_lista.append(elemento.identificacao_numerica)
    ##########################################

    quant_de_membros = len(Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome).filter(cargo_herdado='Membro do colegiado'))
    quant_de_membros_mais = quant_de_membros + 1
    
    #Coloca o numero de todas as ordens deste plano em uma lista para ser passada pro jquery
    ordens_com_sugestao = Ordens.objects.filter(plano=plano_objeto).filter(possui_sugestao_correcao=True)
    for itens in ordens_com_sugestao:
        ordens_lista2.append(itens.identificacao_numerica)
    ##########################################

    if plano_objeto.pre_analise_acao:
        sugestoes_plano_concluidas = 1
    else:
        sugestoes_plano_concluidas = 0

    if plano_objeto.devolvido:
        var_devolvido = 1
    else:
        var_devolvido = 0
    
    # Abre formulario para cadastro de datas
    if kwargs.get('ordem_id') and not kwargs.get('contx_ordem'): 
        if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
            ordem_data = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
            contexto_abre_form_datas = True
            form_datas = Cadastra_datas_Ordem_Form()
            if ordem_data.prazo_execucao_inicial != '':
                form_datas.fields['prazo_execucao_inicial'].initial = ordem_data.prazo_execucao_inicial
            if ordem_data.prazo_execucao_final != '':
                form_datas.fields['prazo_execucao_final'].initial = ordem_data.prazo_execucao_final
        else: # se usuario atual nao for o corretor
            return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Nao_corretor')
    ##########################################
    
    if plano_objeto.situacao == 'Assinado':
        var_reset = True

    if request.method == 'GET' and 'postprint' in request.GET:
        apos_print = request.GET.get('postprint','')

    if kwargs.get('q_linha'):
        quebra_linha = True

    if plano_objeto.situacao == 'Publicado' and plano_objeto.devolvido == True and plano_objeto.correcoes_a_fazer == 0 and plano_objeto.pre_assinatura == True:
        var_plano_pre_aprovado = True
    elif plano_objeto.situacao == 'Aprovado':
        var_plano_pre_aprovado = True
    
    plano_a_exibir = {
        'chave_planos' : plano_objeto,
        'chave_planos2' : plano_iteravel,
        # 'chave_ordens' : ordem_objeto,
        'chave_ordens2' : ordens_iteravel,
        'chave_ordens_sem_codigo' : ordens_sem_codigo,
        'chave_codigos' : codigos_iteravel,
        # 'vartemplate' : var_template,
        'chave_funcionarios' : funcionarios,
        'chave_membros_colegiado' : membros_colegiado,
        'varmembros' : quant_de_membros_mais,
        'chave_lista_ordens' : ordens_lista,
        'chave2_lista_ordens' : ordens_lista2,
        'chave_sugestoes_acoes_concluidas' : sugestoes_plano_concluidas,
        'chave_devolvido' : var_devolvido,
        'chave_tipo_usuario' : tipo_usuario,
        'chave_situacao_plano' : situacao_plano,
        'chave_ordem_data' : ordem_data,
        'chave_contexto_abre_form_datas' : contexto_abre_form_datas,
        'chave_form_datas' : form_datas,
        'chave_erro_form_datas': erro_form_datas,
        'chave_reset_plano' : var_reset,
        'chave_q_linha' : quebra_linha,
        'chave_apos_print' : apos_print,
        'plano_aprovado' : var_plano_pre_aprovado,
        'pagina_acoes' : True,
    }

    if kwargs.get('pdf'): # A FUNÇÃO 'gera_pdf' CHAMA ESTE CONTEXTO PARA RENDERIZAR O PDF
        contexto_pdf = plano_a_exibir
        return contexto_pdf

    if kwargs.get('contx_ordem'): # A FUNÇÃO 'cadastra_data' DA VIEWS DE ORDENS CHAMA ESTE CONTEXTO PARA RENDERIZAR ESTA PAGINA
        return plano_a_exibir

    return render(request, 'acao-visualizacao.html', plano_a_exibir)

def acao_plano_correcao(request, **kwargs):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
        ordem_a_corrigir = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        contexto_extra_corrigir = True
        var_reset = False
        ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        correcao_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=None)
        plano_iteravel = Plano_de_acao.objects.filter(pk=kwargs['elemento_id'])
        ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto.id)
        codigos_iteravel=[]
        ordens_lista=[]
        ordens_lista2=[]
        quant_de_membros = 0
        funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome)
        checa_usuario = request.user
        tipo_usuario = request.user.groups.get().name
        situacao_plano = plano_objeto.situacao
        membros_colegiado = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome).filter(cargo_herdado='Membro do colegiado')
        
        # LISTA TODOS OS CODIGOS DE UMA ORDEM ESPECIFICA
        for elemento in ordens_iteravel:
            codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
            for items in codigos_varredura:
                codigos_iteravel.append(items)
        ##########################################################################

        quant_de_membros = len(Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome).filter(cargo_herdado='Membro do colegiado'))
        quant_de_membros_mais = quant_de_membros + 1

        #LISTA COM NUMERO DAS ORDENS DESSE PLANO
        for elemento in ordens_iteravel:
            ordens_lista.append(elemento.identificacao_numerica)
        ##############################

        ##########################################################################
        #Coloca a indentificação numérica das ordens em uma lista para serem passados pro jquery
        ordens_com_sugestao = Ordens.objects.filter(plano=plano_objeto).filter(possui_sugestao_correcao=True)
        for itens in ordens_com_sugestao:
            ordens_lista2.append(itens.identificacao_numerica)
        ##########################################################################

        # INSTANCIA O FORM E SETA VALORES INICIAIS
        form_correcao_acao = Correcao_acaoForm()
        form_correcao_acao.fields['plano_nome'].initial = plano_objeto.ano_referencia
        form_correcao_acao.fields['plano_nome'].disabled = True
        form_correcao_acao.fields['documento_associado'].initial = '1 - Identificação das ações'
        form_correcao_acao.fields['documento_associado'].disabled = True
        form_correcao_acao.fields['ordem_associada'].initial = ordem_objeto.identificacao_numerica
        form_correcao_acao.fields['ordem_associada'].disabled = True
        if ordem_objeto.possui_sugestao_correcao:
            for item in correcao_iteravel:
                form_correcao_acao.fields['sugestao'].initial = item.sugestao

        if plano_objeto.pre_analise_acao:
            sugestoes_acoes_plano_concluidas = 1
        else:
            sugestoes_acoes_plano_concluidas = 0

        if plano_objeto.devolvido:
            var_devolvido = 1
        else:
            var_devolvido = 0

        if plano_objeto.situacao == 'Assinado':
            var_reset = True

        plano_a_exibir = {
            'chave_planos' : plano_objeto,
            'chave_planos2' : plano_iteravel,
            'chave_ordens' : ordem_objeto,
            'chave_ordens2' : ordens_iteravel,
            'chave_codigos' : codigos_iteravel,
            # 'vartemplate' : var_template,
            'chave_funcionarios' : funcionarios,
            'chave_membros_colegiado' : membros_colegiado,
            'varmembros' : quant_de_membros_mais,
            'chave_lista_ordens' : ordens_lista,
            'chave2_lista_ordens' : ordens_lista2,
            'chave_ordem_corrigir' : ordem_a_corrigir,
            'chave_contexto_extra_corrigir' : contexto_extra_corrigir,
            'chave_form_correcao_acao' : form_correcao_acao,
            'chave_sugestoes_acoes_concluidas' : sugestoes_acoes_plano_concluidas,
            'chave_devolvido' : var_devolvido,
            'chave_tipo_usuario' : tipo_usuario,
            'chave_situacao_plano' : situacao_plano,
            'chave_reset_plano' : var_reset
        }

        return render(request, 'acao-visualizacao.html', plano_a_exibir)
        
    return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Nao_corretor')

def cria_altera_correcao_acao(request, **kwargs):
    from .alteracoes import atualiza_quant_correcoes_plano
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        form_correcao_acao_preenchido = Correcao_acaoForm()
        if request.method == 'POST':
            form_correcao_acao_preenchido = Correcao_acaoForm(request.POST)
            if form_correcao_acao_preenchido.is_valid():
                # CRIA NOVA CORREÇÃO
                # print(plano_objeto.correcoes_a_fazer)
                if not ordem_objeto.possui_sugestao_correcao:
                    instancia = form_correcao_acao_preenchido.save(commit=False)
                    instancia.plano_associado = plano_objeto
                    instancia.save()

                    atualiza_quant_correcoes_plano(plano_objeto)

                    ordem_objeto.possui_sugestao_correcao = True
                    ordem_objeto.save()

                    mensagem_var = 'Criou'
                    # print('criou nova correcao')
                
                else:
                    # ALTERA CORREÇÃO EXISTENTE
                    correcao_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(documento_associado = '1 - Identificação das ações')
                    for item in correcao_iteravel:
                        item.sugestao = form_correcao_acao_preenchido.cleaned_data.get('sugestao')
                        item.save()

                        mensagem_var = 'Editou'
                    # print('alterou correcao')
            else:
                pass

        return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem=mensagem_var)

    return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem='Acesso_negado_situacao')

def deleta_correcao_acao(request, **kwargs):
    from .alteracoes import atualiza_quant_correcoes_plano
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        if request.method == 'POST':
            # print(plano_objeto.correcoes_a_fazer)
            correcao_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(documento_associado = '1 - Identificação das ações')
            for item in correcao_iteravel:
                item.delete()

            atualiza_quant_correcoes_plano(plano_objeto)

            ordem_objeto.possui_sugestao_correcao = False
            ordem_objeto.save()

            return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem='Deletou')

    return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem='Acesso_negado_situacao')

def acao_plano_adiciona_ordem(request, **kwargs):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola':
        ordens_iteravel = Ordens.objects.filter(plano=kwargs['plano_id'])

        if kwargs.get('elemento_id'): #Se receber id de ordem, modifica esta ordem
            ordem_a_modificarOBJ = get_object_or_404(Ordens, pk=kwargs['elemento_id'])
            if not ordem_a_modificarOBJ.inserida: #Se não estiver inserida
                ordem_a_modificarOBJ.inserida = True
                plano_objeto.comando_todas = False
                plano_objeto.comando_individual = True
                ordem_a_modificarOBJ.save()
                plano_objeto.save()
                # print('ADICIONOU ORDEM = ' + str(elemento_id))
            else: #Se estiver inserida
                ordem_a_modificarOBJ.inserida = False
                plano_objeto.comando_todas = False
                plano_objeto.comando_individual = True
                ordem_a_modificarOBJ.save()
                plano_objeto.save()
                # print('REMOVEU ORDEM = ' + str(elemento_id))
                
        else: #Se não receber id de ordem, altera todas

            if not plano_objeto.todas_inseridas:
                plano_objeto.todas_inseridas = True
                plano_objeto.comando_todas = True
                plano_objeto.comando_individual = False
                plano_objeto.save()
                for elemento in ordens_iteravel:
                    elemento.inserida = True
                    elemento.save()
                # print('ADICIONOU TODAS AS ORDENS')
            else:
                plano_objeto.todas_inseridas = False
                plano_objeto.comando_todas = True
                plano_objeto.comando_individual = False
                plano_objeto.save()
                for elemento in ordens_iteravel:
                    elemento.inserida = False
                    elemento.save()
                # print('REMOVEU TODAS AS ORDENS')

        return redirect('chamando_acao_plano', elemento_id=kwargs['plano_id'])
    
    return redirect('dashboard')

def acao_plano_modifica_codigo(request, **kwargs):
    codigo_OBJ = get_object_or_404(ModeloCodigos, pk=kwargs['codigo_id'])
    ordem_OBJ = get_object_or_404(Ordens, pk=kwargs['ordem_id'])

    # ALTERANDO ESTADO
    if not codigo_OBJ.inserido:
        codigo_OBJ.inserido = True
        codigo_OBJ.save()
        codigos_inseridos = ModeloCodigos.objects.filter(ordem=ordem_OBJ).filter(inserido=True)
        ordem_OBJ.codigos_inseridos = len(codigos_inseridos)
        ordem_OBJ.ordem_rowspan = len(codigos_inseridos)
        ordem_OBJ.save()

    else:
        codigo_OBJ.inserido = False
        codigo_OBJ.save()
        codigos_inseridos = ModeloCodigos.objects.filter(ordem=ordem_OBJ).filter(inserido=True)
        ordem_OBJ.codigos_inseridos = len(codigos_inseridos)
        ordem_OBJ.ordem_rowspan = len(codigos_inseridos)
        ordem_OBJ.save()

    return redirect('chamando_acao_plano', elemento_id=kwargs['plano_id'])

def despesa_plano(request, **kwargs): # Visualização principal
    from .alteracoes import calcula_soma_capital, calcula_soma_custeio
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    # ordem_objeto = get_object_or_404(Ordens, pk=20)
    plano_iteravel = Plano_de_acao.objects.filter(pk=kwargs['elemento_id'])
    ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto.id)
    codigos_iteravel=[]
    codigos_lista=[]
    codigos_lista2=[]
    membros_colegiado=[]
    turmas_iteravel = Turmas.objects.order_by('nome').filter(escola=plano_objeto.escola)
    turmas_associadas_iteravel = Turmas.objects.order_by('nome').filter(escola=plano_objeto.escola).filter(plano_associado=plano_objeto)
    quant_de_membros = 0
    soma_capital = 0
    soma_custeio = 0
    quebra_linha = False
    apos_print = False
    funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome)
    checa_usuario = request.user
    tipo_usuario = request.user.groups.get().name
    # lista_turmas_no_menu = []
    situacao_plano = plano_objeto.situacao

    if kwargs.get('mensagem') == 'Criou':
        messages.success(request, 'Sugestão de correção criada com sucesso!')
    elif kwargs.get('mensagem') == 'Sucesso':
        messages.success(request, 'Alteração realizada com sucesso!')
    elif kwargs.get('mensagem') == 'Sucesso2':
        if request.method == 'GET' and 'postprint' not in request.GET:
            messages.success(request, 'Alteração efetuada com sucesso!')
    elif kwargs.get('mensagem') == 'Deletou':
        messages.success(request, 'Sugestão de correção excluída com sucesso!')
    elif kwargs.get('mensagem') == 'Editou':
        messages.success(request, 'Sugestão de correção alterada com sucesso!')
    elif kwargs.get('mensagem') == 'Nao_corretor':
        messages.error(request, 'Você não é o corretor responsável por este plano!')
    elif kwargs.get('mensagem') == 'Acesso_negado':
        messages.error(request, 'Acesso_negado!')
    elif kwargs.get('mensagem') == 'Acesso_negado_situacao':
        messages.error(request, 'Acesso_negado, a situação atual do plano não permite esta alteração!')

    # LISTA TODOS OS CODIGOS DE UMA ORDEM ESPECIFICA
    for elemento in ordens_iteravel:
        codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
        for items in codigos_varredura:
            codigos_iteravel.append(items)

    quant_de_membros = len(Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome).filter(cargo_herdado='Membro do colegiado'))
    quant_de_membros_mais = quant_de_membros + 1

    for item in funcionarios:
        if item.user.last_name == 'Membro do colegiado':
            membros_colegiado.append(item)

    # SOMA OS VALORES DE TODOS PRODUTOS DO TIPO CAPITAL
    soma_capital = calcula_soma_capital(codigos_iteravel)
    # SOMA OS VALORES DE TODOS PRODUTOS DO TIPO CUSTEIO
    soma_custeio = calcula_soma_custeio(codigos_iteravel)
    # SOMA VALORES TOTAIS DE CAPITAL + CUSTEIO
    soma_total = soma_capital + soma_custeio

    ##########################################################################
    #Coloca as ordens e seus respectivos códigos em uma lista para serem passados pro jquery
    for elemento in ordens_iteravel:
        codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
        for items in codigos_varredura:
            codigos_lista.append(str(elemento.identificacao_numerica) + items.identificacao)
            if items.possui_sugestao_correcao:
                codigos_lista2.append(str(elemento.identificacao_numerica) + items.identificacao)
    # print(codigos_lista) #resultado por ex:['1G', '1U', '1Y', '3A', '3B', '3C']
    # print(codigos_lista2) #resultado por ex:['1G', '3A']
    ##########################################################################

    if request.method == 'GET' and 'postprint' in request.GET:
        apos_print = request.GET.get('postprint','')

    if kwargs.get('q_linha'):
        quebra_linha = True

    if plano_objeto.pre_analise_despesa:
        sugestoes_despesas_plano_concluidas = 1
    else:
        sugestoes_despesas_plano_concluidas = 0

    if plano_objeto.devolvido:
        var_devolvido = 1
    else:
        var_devolvido = 0

    plano_a_exibir = {
        'chave_planos' : plano_objeto,
        'chave_planos2' : plano_iteravel,
        # 'chave_ordens' : ordem_objeto,
        'chave_ordens2' : ordens_iteravel,
        'chave_codigos' : codigos_iteravel,
        'chave_turmas' : turmas_iteravel,
        'chave_turmas_associadas' : turmas_associadas_iteravel,
        # 'chave_lista_turmas' : lista_turmas_no_menu,
        # 'vartemplate' : var_template,
        'chave_funcionarios' : funcionarios,
        'chave_membros_colegiado' : membros_colegiado,
        'varmembros' : quant_de_membros_mais,
        'var_capital' : soma_capital,
        'var_custeio' : soma_custeio,
        'var_total' : soma_total,
        'chave_lista_codigos' : codigos_lista,
        'chave_lista2_codigos' : codigos_lista2,
        'chave_sugestoes_despesas_concluidas' : sugestoes_despesas_plano_concluidas,
        'chave_devolvido': var_devolvido,
        'chave_tipo_usuario': tipo_usuario,
        'chave_situacao_plano' : situacao_plano,
        'chave_q_linha' : quebra_linha,
        'chave_apos_print' : apos_print,
        'pagina_despesas' : True
    }

    return render(request, 'despesas-visualizacao.html', plano_a_exibir)

def despesa_plano_correcao(request, **kwargs):
    from .alteracoes import calcula_soma_capital, calcula_soma_custeio
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])

    if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
        codigo_objeto_corrigir = get_object_or_404(ModeloCodigos, pk=kwargs['codigo_id'])
        contexto_extra_corrigir = True
        ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        plano_iteravel = Plano_de_acao.objects.filter(pk=kwargs['elemento_id'])
        ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto.id)
        correcao_depesas_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=codigo_objeto_corrigir.identificacao)
        codigos_iteravel=[]
        codigos_lista=[]
        codigos_lista2=[]
        turmas_iteravel = Turmas.objects.order_by('nome').filter(escola=plano_objeto.escola)
        turmas_associadas_iteravel = Turmas.objects.order_by('nome').filter(escola=plano_objeto.escola).filter(plano_associado=plano_objeto)
        quant_de_membros = 0
        soma_capital = 0
        soma_custeio = 0
        funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome)
        checa_usuario = request.user
        tipo_usuario = request.user.groups.get().name
        # lista_turmas_no_menu = []
        situacao_plano = plano_objeto.situacao

        # LISTA TODOS OS CODIGOS DE UMA ORDEM ESPECIFICA
        for elemento in ordens_iteravel:
            codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
            for items in codigos_varredura:
                codigos_iteravel.append(items)

        quant_de_membros = len(Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.escola.nome).filter(cargo_herdado='Membro do colegiado'))
        quant_de_membros_mais = quant_de_membros + 1

        # SOMA OS VALORES DE TODOS PRODUTOS DO TIPO CAPITAL
        soma_capital = calcula_soma_capital(codigos_iteravel)
        # SOMA OS VALORES DE TODOS PRODUTOS DO TIPO CUSTEIO
        soma_custeio = calcula_soma_custeio(codigos_iteravel)
        # SOMA VALORES TOTAIS DE CAPITAL + CUSTEIO
        soma_total = soma_capital + soma_custeio

        ##########################################################################
        #Coloca as ordens e seus respectivos códigos em uma lista para serem passados pro jquery
        for elemento in ordens_iteravel:
            codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
            for items in codigos_varredura:
                codigos_lista.append(str(elemento.identificacao_numerica) + items.identificacao)
                if items.possui_sugestao_correcao:
                    codigos_lista2.append(str(elemento.identificacao_numerica) + items.identificacao)
        # print(codigos_lista) #resultado por ex:['1G', '1U', '1Y', '3A', '3B', '3C']
        # print(codigos_lista2) #resultado por ex:['1G', '3A']
        ##########################################################################

        # INSTANCIA O FORM E SETA VALORES INICIAIS
        form_correcao_despesa = Correcao_despesaForm()
        form_correcao_despesa.fields['plano_nome'].initial = plano_objeto.ano_referencia
        form_correcao_despesa.fields['plano_nome'].disabled = True
        form_correcao_despesa.fields['documento_associado'].initial = '2 - Detalhamento das Despesas'
        form_correcao_despesa.fields['documento_associado'].disabled = True
        form_correcao_despesa.fields['codigo_associado'].initial = str(ordem_objeto.identificacao_numerica) + codigo_objeto_corrigir.identificacao
        form_correcao_despesa.fields['codigo_associado'].disabled = True
        if codigo_objeto_corrigir.possui_sugestao_correcao:
            for item in correcao_depesas_iteravel:
                form_correcao_despesa.fields['sugestao'].initial = item.sugestao

        if plano_objeto.pre_analise_despesa:
            sugestoes_despesas_plano_concluidas = 1
        else:
            sugestoes_despesas_plano_concluidas = 0

        if plano_objeto.devolvido:
            var_devolvido = 1
        else:
            var_devolvido = 0

        plano_a_exibir = {
            'chave_planos' : plano_objeto,
            'chave_planos2' : plano_iteravel,
            'chave_ordens' : ordem_objeto,
            'chave_ordens2' : ordens_iteravel,
            'chave_codigos' : codigos_iteravel,
            'chave_turmas' : turmas_iteravel,
            'chave_turmas_associadas' : turmas_associadas_iteravel,
            # 'chave_lista_turmas' : lista_turmas_no_menu,
            # 'vartemplate' : var_template,
            'chave_funcionarios' : funcionarios,
            'varmembros' : quant_de_membros_mais,
            'var_capital' : soma_capital,
            'var_custeio' : soma_custeio,
            'var_total' : soma_total,
            'chave_lista_codigos' : codigos_lista,
            'chave_lista2_codigos' : codigos_lista2,
            'chave_form_correcao_despesa' : form_correcao_despesa,
            'chave_contexto_extra_corrigir_despesas' : contexto_extra_corrigir,
            'chave_codigo_corrigir' : codigo_objeto_corrigir,
            'chave_sugestoes_despesas_concluidas' : sugestoes_despesas_plano_concluidas,
            'chave_devolvido': var_devolvido,
            'chave_tipo_usuario': tipo_usuario,
            'chave_situacao_plano' : situacao_plano,
        }

        return render(request, 'despesas-visualizacao.html', plano_a_exibir)
    else:
        return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Nao_corretor')

def cria_altera_correcao_despesa(request, **kwargs):
    from .alteracoes import atualiza_quant_correcoes_plano
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        codigo_objeto_corrigir = get_object_or_404(ModeloCodigos, pk=kwargs['codigo_id'])
        form_correcao_despesa_preenchido = Correcao_despesaForm()
        if request.method == 'POST':
            form_correcao_despesa_preenchido = Correcao_despesaForm(request.POST)
            if form_correcao_despesa_preenchido.is_valid():
                # CRIA NOVA CORREÇÃO
                # print(plano_objeto.correcoes_a_fazer)
                if not codigo_objeto_corrigir.possui_sugestao_correcao:
                    instancia = form_correcao_despesa_preenchido.save(commit=False)
                    instancia.plano_associado = plano_objeto
                    instancia.ordem_associada = ordem_objeto.identificacao_numerica
                    instancia.codigo_associado = codigo_objeto_corrigir.identificacao
                    instancia.save()

                    # Atualiza a quantidade de correções em um plano
                    atualiza_quant_correcoes_plano(plano_objeto)

                    codigo_objeto_corrigir.possui_sugestao_correcao = True
                    codigo_objeto_corrigir.save()

                    mensagem_var = 'Criou'
                    # print('criou nova correcao despesa')
                
                else:
                    correcao_depesas_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=codigo_objeto_corrigir.identificacao).filter(documento_associado='2 - Detalhamento das Despesas')
                    for item in correcao_depesas_iteravel:
                        item.sugestao = form_correcao_despesa_preenchido.cleaned_data.get('sugestao')
                        item.save()

                        mensagem_var = 'Editou'
                    # print('alterou correcao despesa')
            else:
                # Não da erro porque os campos já são pré preenchidos com as informações corretas
                pass

        return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem=mensagem_var)

    return redirect('chamando_despesa_plano', elemento_id=kwargs['plano_id'])

def deleta_correcao_despesa(request, **kwargs):
    from .alteracoes import atualiza_quant_correcoes_plano
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        codigo_objeto_corrigir = get_object_or_404(ModeloCodigos, pk=kwargs['codigo_id'])
        if request.method == 'POST':
            # print(plano_objeto.correcoes_a_fazer)
            correcao_depesas_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=codigo_objeto_corrigir.identificacao).filter(documento_associado='2 - Detalhamento das Despesas')
            for item in correcao_depesas_iteravel:
                item.delete()
            
            # Atualiza a quantidade de correções neste plano
            atualiza_quant_correcoes_plano(plano_objeto)

            codigo_objeto_corrigir.possui_sugestao_correcao = False
            codigo_objeto_corrigir.save()
            

        return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem='Deletou')

    return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem='Acesso_negado_situacao')

def pagina_correcoes(request, **kwargs):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    correcoes_concluidas = False
    
    if not plano_objeto.tipo_fia:
        correcoes_de_ordens = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto).filter(documento_associado = '1 - Identificação das ações')
    else:
        correcoes_de_ordens = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto).filter(documento_associado = 'FIA - Formulário de Inclusão de Ações')

    correcoes_de_codigos = Correcoes.objects.order_by('codigo_associado').filter(plano_associado=plano_objeto).filter(documento_associado = '2 - Detalhamento das Despesas')

    checa_usuario = request.user
    tipo_usuario = request.user.groups.get().name

    if kwargs.get('mensagem') == 'Sucesso':
        messages.success(request, 'Correção efetuada com sucesso!')

    ##########################################
    # Retorna situacao do plano para 'Publicado' quando acabarem as correções
    if (plano_objeto.devolvido == True) and (plano_objeto.correcoes_a_fazer == 0):
        plano_objeto.situacao = 'Publicado'
        plano_objeto.save()
        correcoes_concluidas = True
    
        nome_usuario = checa_usuario.first_name
        nome_plano = plano_objeto.ano_referencia
        log_plano_correcoes_concluidas(nome_plano, nome_usuario, plano_objeto.id)
    ##########################################
    
    if kwargs.get('abreForm'):
        contexto_corrigindo = True
        ordem_objeto = get_object_or_404(Ordens, plano=plano_objeto, identificacao_numerica = kwargs['ident_numerica'])
        correcao_de_ordem_especifica = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto).filter(documento_associado = '1 - Identificação das ações').filter(ordem_associada=kwargs['ident_numerica'])


        edita_form_ordem = Edita_Ordem_Form()
        edita_form_ordem.fields['identificacao_numerica'].initial = ordem_objeto.identificacao_numerica
        edita_form_ordem.fields['identificacao_numerica'].disabled = True
        edita_form_ordem.fields['descricao_do_problema'].initial = ordem_objeto.descricao_do_problema
        # edita_form_ordem.fields['prazo_execucao_inicial'].initial = ordem_objeto.prazo_execucao_inicial
        # edita_form_ordem.fields['prazo_execucao_final'].initial = ordem_objeto.prazo_execucao_final
        edita_form_ordem.fields['resultados_esperados'].initial = ordem_objeto.resultados_esperados

        list_forms = list()
        codigos_da_ordem_inseridos = ModeloCodigos.objects.order_by('identificacao').filter(ordem=ordem_objeto).filter(inserido=True)

        for modelo in codigos_da_ordem_inseridos:
            form_codigos = Mini_form_Codigos(prefix=modelo.identificacao)
            form_codigos.fields['identificacao'].label = 'Código: ' + str(ordem_objeto.identificacao_numerica) + modelo.identificacao
            form_codigos.fields['identificacao'].initial = modelo.identificacao
            form_codigos.fields['especificacao'].initial = modelo.especificacao
            list_forms.append(form_codigos)


        if kwargs.get('abreForm') == 'form_ordem_invalido': # este valor vem da função 'corrigindo acao' que chama esta função pra renderizar o form com os erros
            contexto = {
            'chave_plano': plano_objeto,
            'chave_ordem': ordem_objeto,
            'chave_correcoes_ordens': correcoes_de_ordens,
            'chave_correcao_ordem_especifica': correcao_de_ordem_especifica,
            'chave_correcoes_codigos': correcoes_de_codigos,
            'chave_contexto_corrigindo_acao' : contexto_corrigindo,
            'chave_form_codigos' : list_forms,
            'chave_tipo_usuario' : tipo_usuario,
            'chave_correcoes_concluidas' : correcoes_concluidas,
        }
            return contexto
        else:
            contexto = {
            'chave_plano': plano_objeto,
            'chave_ordem': ordem_objeto,
            'chave_correcoes_ordens': correcoes_de_ordens,
            'chave_correcao_ordem_especifica': correcao_de_ordem_especifica,
            'chave_correcoes_codigos': correcoes_de_codigos,
            'chave_contexto_corrigindo_acao' : contexto_corrigindo,
            'chave_form_ordem' : edita_form_ordem,
            'chave_form_codigos' : list_forms,
            'chave_tipo_usuario' : tipo_usuario,
            'chave_correcoes_concluidas' : correcoes_concluidas,
        }
            return render(request, 'correcoes.html', contexto)
    
    elif kwargs.get('abreFormDespesa'):
        contexto_corrigindo_despesa = True
        ordem_objeto = get_object_or_404(Ordens, plano=plano_objeto, identificacao_numerica = kwargs['ident_numerica'])
        codigo_objeto = get_object_or_404(ModeloCodigos, ordem=ordem_objeto, identificacao = kwargs['codigo_ident'])
        correcao_de_codigo_especifico = get_object_or_404(Correcoes, plano_associado=plano_objeto, ordem_associada=kwargs['ident_numerica'], codigo_associado=kwargs['codigo_ident'])

        edita_form_codigo = CodigosForm()
        edita_form_codigo.fields['identificacao'].initial = str(ordem_objeto.identificacao_numerica) + codigo_objeto.identificacao
        edita_form_codigo.fields['identificacao'].label = 'Código: '
        edita_form_codigo.fields['identificacao'].disabled = True
        edita_form_codigo.fields['especificacao'].initial = codigo_objeto.especificacao
        edita_form_codigo.fields['justificativa'].initial = codigo_objeto.justificativa
        edita_form_codigo.fields['embalagem'].initial = codigo_objeto.embalagem
        edita_form_codigo.fields['quantidade'].initial = codigo_objeto.quantidade
        edita_form_codigo.fields['preco_unitario'].initial = codigo_objeto.preco_unitario
        edita_form_codigo.fields['tipo_produto'].initial = codigo_objeto.tipo_produto

        if kwargs.get('abreFormDespesa') == 'form_despesa_invalido':
            contexto = {
                'chave_plano': plano_objeto,
                'chave_ordem': ordem_objeto,
                'chave_codigo': codigo_objeto,
                'chave_correcoes_ordens': correcoes_de_ordens,
                'chave_correcoes_codigos': correcoes_de_codigos,
                'chave_correcao_codigo_especifico': correcao_de_codigo_especifico,
                'chave_contexto_corrigindo_despesa' : contexto_corrigindo_despesa,
                'chave_tipo_usuario' : tipo_usuario,
                'chave_correcoes_concluidas' : correcoes_concluidas,
            }
            return contexto
        else:
            contexto = {
                'chave_plano': plano_objeto,
                'chave_ordem': ordem_objeto,
                'chave_codigo': codigo_objeto,
                'chave_correcoes_ordens': correcoes_de_ordens,
                'chave_correcoes_codigos': correcoes_de_codigos,
                'chave_correcao_codigo_especifico': correcao_de_codigo_especifico,
                'chave_contexto_corrigindo_despesa' : contexto_corrigindo_despesa,
                'chave_form_codigo' : edita_form_codigo,
                'chave_tipo_usuario' : tipo_usuario,
                'chave_correcoes_concluidas' : correcoes_concluidas,
            }
            return render(request, 'correcoes.html', contexto)

    else:
        contexto = {
            'chave_plano': plano_objeto,
            'chave_correcoes_ordens': correcoes_de_ordens,
            'chave_correcoes_codigos': correcoes_de_codigos,
            'chave_tipo_usuario' : tipo_usuario,
            'chave_correcoes_concluidas' : correcoes_concluidas,
        }

        if kwargs.get('retorna_contexto_fia'):
            return contexto
        else:
            return render(request, 'correcoes.html', contexto)

def corrigindo_acao(request, **kwargs):
    from .alteracoes import atualiza_quant_correcoes_plano, envia_email_plano_aprovado
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola':
        ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
        codigos_da_ordem_inseridos = ModeloCodigos.objects.order_by('identificacao').filter(ordem=ordem_objeto).filter(inserido=True)

        # form de ordem
        if request.method == 'POST':
            firstform = Edita_Ordem_Form(request.POST, plano_id_super=kwargs['plano_id'], correcao_super='form_correcao')
            if firstform.is_valid():
                edita_identificacao_numerica = firstform.cleaned_data.get('identificacao_numerica')
                edita_descricao_do_problema = firstform.cleaned_data.get('descricao_do_problema')
                # edita_prazo_execucao_inicial = firstform.cleaned_data.get('prazo_execucao_inicial')
                # edita_prazo_execucao_final = firstform.cleaned_data.get('prazo_execucao_final')
                edita_resultados_esperados = firstform.cleaned_data.get('resultados_esperados')

                ordem_objeto.identificacao_numerica = edita_identificacao_numerica
                ordem_objeto.descricao_do_problema = edita_descricao_do_problema
                # ordem_objeto.prazo_execucao_inicial = edita_prazo_execucao_inicial
                # ordem_objeto.prazo_execucao_final = edita_prazo_execucao_final
                ordem_objeto.resultados_esperados = edita_resultados_esperados

                # Tira o indicativo de que a ordem possui sugestão de correção
                ordem_objeto.possui_sugestao_correcao = False
                ordem_objeto.save()

                # Remove o objeto 'correcao' uma vez que ela acabou de ser corrigida.
                correcao_remover = Correcoes.objects.filter(plano_associado=plano_objeto).filter(documento_associado = '1 - Identificação das ações').filter(ordem_associada = ordem_objeto.identificacao_numerica)
                for objeto in correcao_remover:
                    objeto.delete()

                # Atualiza a quantidade de correções neste plano
                quant = atualiza_quant_correcoes_plano(plano_objeto)

                # Pré aprova o plano caso as condições sejam satisfeitas
                if quant == 0 and plano_objeto.pre_assinatura and plano_objeto.devolvido:
                    log_plano_aprovado_auto(plano_objeto.ano_referencia, plano_objeto.id)
                    envia_email_plano_aprovado(request, plano_objeto)

                # Salva as informações nos forms de codigos, nos seus respectivos objetos
                for modelo in codigos_da_ordem_inseridos:
                    secondform = Mini_form_Codigos(request.POST, prefix=modelo.identificacao)
                    if secondform.is_valid():
                        valor_especificacao = secondform.cleaned_data.get('especificacao')
                        modelo.especificacao = valor_especificacao
                        modelo.save()

                    else:
                        # sempre será valido
                        pass

                return redirect('pagina_correcoes_mensagem', elemento_id=kwargs['plano_id'], mensagem='Sucesso')

            else:
                contexto = pagina_correcoes(request, elemento_id=kwargs['plano_id'], ident_numerica=ordem_objeto.identificacao_numerica, abreForm='form_ordem_invalido')
                form_com_erro = Edita_Ordem_Form(request.POST, plano_id_super=kwargs['plano_id'], correcao_super='form_correcao')
                form_com_erro.fields['identificacao_numerica'].initial = ordem_objeto.identificacao_numerica
                form_com_erro.fields['identificacao_numerica'].disabled = True
                contexto['chave_form_ordem'] = form_com_erro

                return render(request, 'correcoes.html', contexto)
    print('redirecionou dashboard')
    return redirect('dashboard')

def corrigindo_despesas(request, **kwargs):
    from .alteracoes import atualiza_quant_correcoes_plano, envia_email_plano_aprovado
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola':
        ordem_objeto = get_object_or_404(Ordens, plano=plano_objeto, identificacao_numerica=kwargs['ordem_assoc'])
        codigo_objeto = get_object_or_404(ModeloCodigos, ordem=ordem_objeto, identificacao=kwargs['codigo_ident'])

        if request.method == 'POST':
            form_codigo = CodigosForm(request.POST, correcao_super='form_correcao')
            if form_codigo.is_valid():
                # edita_identificacao = form_codigo.cleaned_data.get('identificacao')
                edita_especificacao = form_codigo.cleaned_data.get('especificacao')
                edita_justificativa = form_codigo.cleaned_data.get('justificativa')
                edita_embalagem = form_codigo.cleaned_data.get('embalagem')
                edita_quantidade = form_codigo.cleaned_data.get('quantidade')
                edita_preco_unitario = form_codigo.cleaned_data.get('preco_unitario')
                edita_tipo_produto = form_codigo.cleaned_data.get('tipo_produto')

                # codigo_objeto.identificacao = edita_identificacao
                codigo_objeto.especificacao = edita_especificacao
                codigo_objeto.justificativa = edita_justificativa
                codigo_objeto.embalagem = edita_embalagem
                codigo_objeto.quantidade = edita_quantidade
                codigo_objeto.preco_unitario = edita_preco_unitario
                codigo_objeto.tipo_produto = edita_tipo_produto

                # Tira o indicativo de que o codigo possui sugestão de correção
                codigo_objeto.possui_sugestao_correcao = False
                codigo_objeto.save()

                # Remove o objeto 'correcao' uma vez que ele acabou de ser corrigido.
                correcao_de_codigo_especifico = get_object_or_404(Correcoes, plano_associado=plano_objeto, ordem_associada=kwargs['ordem_assoc'], codigo_associado=kwargs['codigo_ident'])
                correcao_de_codigo_especifico.delete()

                # Atualiza a quantidade de correções neste plano
                quant = atualiza_quant_correcoes_plano(plano_objeto)

                # Pré aprova o plano caso as condições sejam satisfeitas
                if quant == 0 and plano_objeto.pre_assinatura and plano_objeto.devolvido:
                    log_plano_aprovado_auto(plano_objeto.ano_referencia, plano_objeto.id)
                    envia_email_plano_aprovado(request, plano_objeto)

                # print('SUCESSO')
                return redirect('pagina_correcoes_mensagem', elemento_id=kwargs['plano_id'], mensagem='Sucesso')

            else:
                contexto = pagina_correcoes(request, elemento_id=kwargs['plano_id'], ident_numerica=ordem_objeto.identificacao_numerica, codigo_ident=codigo_objeto.identificacao, abreFormDespesa='form_despesa_invalido')
                form_com_erro = CodigosForm(request.POST, correcao_super='form_correcao')
                form_com_erro.fields['identificacao'].initial = str(ordem_objeto.identificacao_numerica) + codigo_objeto.identificacao
                form_com_erro.fields['identificacao'].label = 'Código: '
                form_com_erro.fields['identificacao'].disabled = True
                contexto['chave_form_codigo'] = form_com_erro

                # print('FORM CODIGO INVALIDOOO')
                return render(request, 'correcoes.html', contexto)

    return redirect('dashboard')

def cria_plano(request):
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola':
        controle_form_plano = False
        form_plano = PlanoForm()
        escola = request.user.classificacao.escola
        if request.method == 'POST':
            form_plano = PlanoForm(request.POST, escola_super=escola)
            if form_plano.is_valid():
                ano_form = form_plano.cleaned_data.get('ano_referencia')
                plano = Plano_de_acao.objects.create(
                    ano_referencia = ano_form,
                    escola = request.user.classificacao.escola,
                )
                # print('SALVOU PLANO!!!!')
                plano.save()
                return redirect('pagina_planos_de_acao_mensagem', mensagem='Criou')
            else:
                controle_form_plano = True

                contexto = planos_de_acao(request, falha_novo_plano=True)
                contexto['chave_form_planos'] = form_plano
                contexto['contexto_extra_plano'] = controle_form_plano
                # print('FORM PLANO INVALIDO')
                return render(request, 'planos_de_acao.html', contexto)

    return redirect('pagina_planos_de_acao')

def edita_plano(request, **kwargs):
    plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and plano.alterabilidade == 'Escola':
        form_plano = PlanoForm()
        # form_plano.fields['ano_referencia'].initial = plano
        edita_plano_form = Edita_planoForm()
        # edita_plano_form.fields['ano_referencia'].initial = plano
        if request.method == 'POST':
            edita_plano_form = Edita_planoForm(request.POST, escola_super=plano.escola)
            if edita_plano_form.is_valid():
                edita_ano_referencia = edita_plano_form.cleaned_data.get('ano_referencia')
                plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
                nome_antigo = plano.ano_referencia
                if plano.situacao != 'Em desenvolvimento':
                    checa_usuario = request.user
                    log_nome_plano_alterado(nome_antigo, edita_ano_referencia, checa_usuario, plano.id)
                plano.ano_referencia = edita_ano_referencia
                plano.save()

                # print('sucesso editou')
                return redirect('pagina_planos_de_acao_mensagem', mensagem='Editou')

            else:
                controle_form_edita_plano = True

                checa_usuario = request.user
                tipo_usuario = request.user.groups.get().name
                if tipo_usuario == 'Diretor_escola':
                    planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=plano.escola).filter(~Q(situacao='Concluido'))

                plano_selecionado = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
                plano_selecionado2 = Plano_de_acao.objects.filter(pk=kwargs['plano_id'])

                dados = {
                'chave_planos' : planos,
                'chave_form_planos' : form_plano,
                'chave_edita_plano_form' : edita_plano_form,
                'contexto_extra_edita_plano' : controle_form_edita_plano,
                'contexto_edicao_plano' : plano_selecionado,
                'chave_contexto_edicao_plano' : plano_selecionado2,

                }

                # print('render form erro')
                return render(request, 'planos_de_acao.html', dados)

        return redirect('dashboard') # Caso url seja chamada por um GET
    # print('acesso negado situacao')
    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao')

def deleta_plano(request, **kwargs):
    plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Diretor_escola':
        if not plano.situacao == 'Finalizado':
            existem_turmas_associadas = Turmas.objects.filter(plano_associado=plano)
            if existem_turmas_associadas:
                for turmas in existem_turmas_associadas:
                    turmas.plano_associado.remove(plano)# Desassocia as turmas associadas a este plano.

            plano.delete()

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Deletou')
        else:
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Arquivado')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def publica_plano(request, **kwargs):
    from .alteracoes import atualiza_assinaturas_escola
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name
    
    if tipo_usuario == 'Diretor_escola' and captura_plano.alterabilidade == 'Escola':
        checa_usuario = request.user.last_name
        if request.method == 'POST':
            captura_plano.situacao = 'Publicado'
            captura_plano.save()
            mensagem_var = 'Publicou'

            nome_plano = captura_plano.ano_referencia
            log_plano_publicado(nome_plano, checa_usuario, captura_plano.id)

            atualiza_assinaturas_escola(captura_plano.id)

        return redirect('pagina_planos_de_acao_mensagem', mensagem=mensagem_var)

    return redirect('pagina_planos_de_acao_mensagem', mensagem="Acesso_negado")

def autoriza_plano(request, **kwargs): #ASSINATURA
    from .alteracoes import cria_associacao, confere_assinaturas_muda_para_pronto, fia_confere_assinaturas_muda_para_pronto
    from fia.alteracoes import checa_grupo_de_autorizacao, checa_se_pode_assinar_escola_fia
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' or tipo_usuario == 'Funcionario':
        if captura_plano.alterabilidade == 'Desativada' or captura_plano.pre_assinatura == True:
            captura_escola = captura_plano.escola

            captura_funcionario = get_object_or_404(Classificacao, user_id=request.user.id)
            funcionario_associado = Classificacao.objects.filter(plano_associado=captura_plano)#DE TODOS FUNCIONARIOS ASSOCIADOS A ESTE PLANO

            if any(funcionario.user_id == request.user.id for funcionario in funcionario_associado ): #se qualquer funcionario associado a ESTE PLANO tiver o mesmo ID do ATUAL. Significa que este usuário já autorizou!!
                # print('Achou funcionario associado com ID igual ao atual, NADA ACONTECE')
                return redirect('pagina_planos_de_acao_mensagem', mensagem='Ja_assinado')

            else: # Significa que este usuário ainda não autorizou este plano, e portanto, criamos a autorização!!
                
                # PLANO COMUM
                if not captura_plano.tipo_fia:
                    # print('Nao existe funcionario com ID igual ao atual associado a este plano, CRIANDO AUTORIZAÇÃO!!')
                    cria_associacao(request, captura_plano, captura_funcionario, kwargs['elemento_id'])

                # PLANO FIA
                elif captura_plano.tipo_fia:
                    modelo_fia = get_object_or_404(Modelo_fia, plano=captura_plano)
                    grupo_completo = checa_grupo_de_autorizacao(modelo_fia)
                    pode_assinar = checa_se_pode_assinar_escola_fia(request, modelo_fia)
                    if grupo_completo:
                        if pode_assinar:
                            # print('Nao existe funcionario com ID igual ao atual associado a este plano, CRIANDO AUTORIZAÇÃO!!')
                            cria_associacao(request, captura_plano, captura_funcionario, kwargs['elemento_id'])
                        else:
                            return redirect('pagina_planos_de_acao_mensagem', mensagem='no_sign')
                    else:
                        return redirect('pagina_planos_de_acao_mensagem', mensagem='grupo_incompleto')

            # PLANO COMUM
            if not captura_plano.tipo_fia:
                confere_assinaturas_muda_para_pronto(request, captura_plano, captura_escola)
                
            # PLANO FIA
            elif captura_plano.tipo_fia:
                fia_confere_assinaturas_muda_para_pronto(request, captura_plano)

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Assinado')
    
    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def autoriza_plano_func_sec(request, **kwargs): #ASSINATURA FUNC_SEC
    from .alteracoes import plano_inteiramente_assinado,atualiza_assinaturas_sec, checa_se_pode_assinar_func_sec
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Func_sec' and captura_plano.alterabilidade == 'Desativada':
        escola_id = captura_plano.escola.id
        captura_escola = get_object_or_404(Escola, pk=escola_id)

        captura_funcionario = get_object_or_404(Classificacao, user_id=request.user.id)
        funcionario_associado = Classificacao.objects.filter(plano_associado=captura_plano)#DE TODOS FUNCIONARIOS ASSOCIADOS A ESTE PLANO

        if any(funcionario.user_id == request.user.id for funcionario in funcionario_associado ): #se qualquer funcionario associado a ESTE PLANO tiver o mesmo ID do ATUAL. Significa que este usuário já autorizou!!
            # print('Achou funcionario associado com ID igual ao atual, NADA ACONTECE')
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Ja_assinado')

        else: # Significa que este usuário ainda não autorizou este plano, e portanto, criamos a autorização!!
            # print('Nao existe funcionario com ID igual ao atual associado a este plano, CRIANDO AUTORIZAÇÃO!!')

            pode_assinar = checa_se_pode_assinar_func_sec(request, captura_plano)
            if pode_assinar:
                captura_funcionario.plano_associado.add(captura_plano) #salva no banco dizendo que este usuario acabou de autorizar este plano, e portanto já assinou e não precisa mais assinar. Gera um associação many-too_many.
            else:
                return redirect('pagina_planos_de_acao_mensagem', mensagem='no_sign_funcsec')

            # Seta as variaveis booleanas do modelo de plano que dizem quem dos 3 acabou de assinar
            if captura_funcionario.usuario_diretor:
                captura_plano.assinatura_diretor = True
            elif captura_plano.corretor_plano == request.user:
                captura_plano.assinatura_corretor = True
            elif captura_funcionario.usuario_coordenador:
                captura_plano.assinatura_coordenador = True
            captura_plano.save()

            atualiza_assinaturas_sec(kwargs['elemento_id'])
            captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])

            checa_usuario = request.user.first_name
            nome_plano = captura_plano.ano_referencia
            log_plano_assinado_sec(nome_plano, checa_usuario, captura_plano.id)

            # transforma em "Inteiramente assinado" o plano caso tenha todas as assinaturas necessárias
            plano_inteiramente_assinado(captura_plano)
            
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Assinado')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def envia_plano(request, **kwargs):
    tipo_usuario = request.user.groups.get().name
    escola = request.user.classificacao.escola

    if tipo_usuario == 'Diretor_escola':
        if request.method == 'POST':
            captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])

            if not captura_plano.tipo_fia:
                contem_ordens = Ordens.objects.filter(plano=captura_plano) # todas as ordens do plano
                if contem_ordens: # Se plano contem ordens

                    if any( elemento.inserida for elemento in contem_ordens ):# Se houver alguma ordem inserida

                        for elemento in contem_ordens:
                            if elemento.inserida:# para todas as ordens inseridas
                                contem_codigos = ModeloCodigos.objects.filter(ordem=elemento)

                                if contem_codigos:# Se  ordem inserida tiver códigos

                                    if any(codigo.inserido for codigo in contem_codigos):# Se algum codigo inserido
                                        
                                        if escola.possui_tesoureiro and escola.quant_membro_colegiado > 0:
                                            pass
                                            # print('PASSOU POR TODAS AS CHECAGENS!!')
                                            # PODE ENVIAR
                                        else:
                                            # print('NAO TEM MINIMO DE TESOUREIRO E MEMBRO DO COLEGIADO CADASTRADOS')
                                            return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_funcionarios')
                                    else:
                                        # print('NAO TEM CODIGO INSERIDO EM UMA ORDEM INSERIDA')
                                        return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_codigo')
                                else:
                                    # print('TEM ORDEM, MAS NAO TEM CODIGO')
                                    return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_codigo')
                    else:
                        # print('NÃO TEM ORDEM INSERIDA!')
                        return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_ordem')
                else:
                    # print('NÃO TEM ORDEM!')
                    return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_ordem')
            else: # O plano é tipo fia
                modelo_fia = get_object_or_404(Modelo_fia, plano=captura_plano)
                if modelo_fia.nome_caixa_escolar == '' or modelo_fia.ano_exercicio == None or modelo_fia.discriminacao == '' or modelo_fia.preco_unitario_item == 0 or modelo_fia.justificativa == '':
                    return redirect('pagina_planos_de_acao_mensagem', mensagem='preenchimento')
        

            # SÓ ENVIA REALMENTE SE NÃO CAIR EM NENHUMA CONDIÇÃO DE ELSE ACIMA

            if (captura_plano.situacao == 'Publicado') and (not captura_plano.devolvido):
                captura_plano.situacao = 'Pendente'
                captura_plano.save()

                checa_usuario = request.user.last_name
                nome_plano = captura_plano.ano_referencia
                log_plano_enviado(nome_plano, checa_usuario, captura_plano.id)

            else:
                captura_plano.situacao = 'Corrigido pela escola'
                captura_plano.devolvido = False
                captura_plano.save()

                checa_usuario = request.user.last_name
                nome_plano = captura_plano.ano_referencia
                log_plano_re_enviado(nome_plano, checa_usuario, captura_plano.id)

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Enviou')

    return redirect('dashboard')

def devolve_plano(request, **kwargs):
    from .alteracoes import envia_email_plano_devolvido
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Func_sec' and captura_plano.alterabilidade == 'Secretaria':
        if request.method == 'POST':
            form_pre_assinatura = PreAssinaturaForm(request.POST)
            if form_pre_assinatura.is_valid():
                valor_pre_assinatura = form_pre_assinatura.cleaned_data.get('pre_assinatura')

                if captura_plano.situacao == 'Pendente' or captura_plano.situacao == 'Corrigido pela escola' :
                    captura_plano.situacao = 'Necessita correção'
                    captura_plano.pre_analise_acao = False
                    captura_plano.pre_analise_despesa = False
                    if captura_plano.tipo_fia:
                        captura_plano.pre_analise_fia = False
                    captura_plano.devolvido = True
                    captura_plano.pre_assinatura = valor_pre_assinatura
                    captura_plano.save()

                    checa_usuario = request.user.first_name
                    nome_plano = captura_plano.ano_referencia
                    log_plano_devolvido(nome_plano, checa_usuario, captura_plano.id)
                    envia_email_plano_devolvido(request, captura_plano)

                    if valor_pre_assinatura == True:
                        log_pre_assinatura_permitida(nome_plano, checa_usuario, captura_plano.id)

                    return redirect('pagina_planos_de_acao_mensagem', mensagem='Devolveu')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def conclui_plano(request, **kwargs):
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and captura_plano.alterabilidade == 'Desativada':
        if request.method == 'POST':
            if captura_plano.situacao == 'Pronto':
                captura_plano.situacao = 'Assinado'
                captura_plano.pre_assinatura = False
                captura_plano.devolvido = False
                captura_plano.pre_analise_acao = False
                captura_plano.pre_analise_despesa = False
                captura_plano.save()

                checa_usuario = request.user.last_name
                nome_plano = captura_plano.ano_referencia
                log_plano_concluido(nome_plano, checa_usuario, captura_plano.id)

        return redirect('pagina_planos_de_acao_mensagem', mensagem='Concluiu')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def finaliza_plano(request,  **kwargs):
    from .alteracoes import envia_email_plano_finalizado
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Func_sec' and captura_plano.alterabilidade == 'Desativada':
        if request.method == 'POST':
            checa_usuario = request.user
            captura_plano.situacao = 'Finalizado'
            captura_plano.save()

            nome_plano = captura_plano.ano_referencia
            log_plano_finalizado(nome_plano, checa_usuario.first_name, captura_plano.id)
            envia_email_plano_finalizado(request, captura_plano)

        return redirect('pagina_planos_de_acao_mensagem', mensagem='Finalizado')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def reseta_plano(request, **kwargs):
    plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name
    checa_usuario = request.user

    if tipo_usuario == 'Func_sec':
        if request.method == 'POST':
            nome_usuario = checa_usuario.first_name
            if plano.situacao == 'Assinado':
                if tipo_usuario == 'Func_sec':
                    if plano.corretor_plano == checa_usuario:
                        funcionario_associado = Classificacao.objects.filter(plano_associado=plano)#DE TODOS OS FUNCIONARIOS ASSOCIADOS A ESTE PLANO
                        for objeto in funcionario_associado:
                            objeto.plano_associado.remove(plano) # Apaga todas as assinaturas neste plano (escolas, funcionarios, Func_sec)
                        # existem_turmas_associadas = Turmas.objects.filter(plano_associado=plano)
                        # if existem_turmas_associadas:
                        #     for turmas in existem_turmas_associadas:
                        #         turmas.plano_associado.remove(plano)# Desassocia as turmas associadas a este plano.
                        if plano.tipo_fia: 
                            modelo_fia = get_object_or_404(Modelo_fia, plano=plano)
                            modelo_fia.assinatura_tecnico.delete() # Apaga assinatura técnico
                            modelo_fia.save()
                        plano.assinaturas = 0
                        plano.assinaturas_sec = 0
                        plano.situacao = 'Pendente'
                        plano.data_assinaturas_escola = None
                        plano.data_assinaturas_suprof = None
                        plano.assinatura_corretor = False
                        plano.assinatura_coordenador = False
                        plano.assinatura_diretor = False
                        plano.alterabilidade = 'Secretaria'
                        plano.save()
    
                        log_plano_resetado(plano.ano_referencia, nome_usuario, kwargs['elemento_id'])

                        if not plano.tipo_fia:
                            return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Sucesso')
                        else:
                            return redirect('chamando_documento_fia_mensagem', elemento_id=kwargs['elemento_id'], mensagem='sucesso2')
                    else:
                        return redirect('pagina_planos_de_acao_mensagem', mensagem='reset_corretor')

    return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Acesso_negado')

def concluir_sugestao(request, **kwargs):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    
    if request.method == 'POST':
        plano_objeto = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
        ordens_iteravel = Ordens.objects.filter(plano=plano_objeto)
        if kwargs.get('documento') == 'acao':
            if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
                for ordem in ordens_iteravel:
                    if ordem.inserida:
                        if ordem.prazo_execucao_inicial == None or ordem.prazo_execucao_final == None:
                            return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Datas')
            
                plano_objeto.pre_analise_acao = True
                plano_objeto.save()

                return redirect('pagina_planos_de_acao_mensagem', mensagem='Sucesso')
            else:
                return redirect('chamando_acao_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Nao_corretor')

        elif kwargs.get('documento') == 'despesa':
            if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
                plano_objeto.pre_analise_despesa = True
                plano_objeto.save()

                return redirect('pagina_planos_de_acao_mensagem', mensagem='Sucesso')
            else:
                return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Nao_corretor')
        
        elif kwargs.get('documento') == 'fia':
            if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
                plano_objeto.pre_analise_fia = True
                plano_objeto.save()

                return redirect('pagina_planos_de_acao_mensagem', mensagem='Sucesso')
            else:
                return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['elemento_id'], mensagem='Nao_corretor')

    return redirect('pagina_planos_de_acao')

def altera_corretor(request, **kwargs):
    plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    checa_usuario = request.user.first_name
    tipo_usuario = request.user.groups.get().name
    corretor = None
    corretor_objeto = None

    if tipo_usuario == 'Func_sec':
        if plano.alterabilidade == 'Desativada':
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao')
        else:
            if request.method == 'POST':
                plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
                corretor_antigo = plano.corretor_plano
                form = AlteraCorretorForm(request.POST)
                if form.is_valid():
                    corretor = form.cleaned_data.get('campo')
                    if corretor == None:
                        plano.corretor_plano = None
                    else:
                        corretor_objeto = get_object_or_404(User, first_name=corretor)
                        plano.corretor_plano = corretor_objeto
                    plano.save()

                if corretor == None and corretor_antigo:
                    checa_corretor = corretor_antigo.first_name
                    log_removeu_corretor(checa_corretor, checa_usuario, plano.id)
                elif corretor and corretor_antigo:
                    checa_corretor = corretor_objeto.first_name
                    log_alterou_corretor(checa_corretor, checa_usuario, plano.id)
            
        return redirect('pagina_planos_de_acao_mensagem', mensagem='Alterou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def quebra_de_linha(request, **kwargs):
    if 'ordemid' in request.GET:
        ordem_id = int(request.GET.get('ordemid',''))
        valor_quebra_de_linha = int(request.GET.get('valor',''))
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)
        ordem_objeto.quebra_de_linha = valor_quebra_de_linha
        ordem_objeto.save()
        if request.method == 'GET ' and 'postprint' in request.GET:
            var_mensagem = 'insere' # Não deve mostrar mensagem alguma
        else:
            var_mensagem = 'Sucesso2'

        return redirect('chamando_acao_plano_mensagem_q_linha', elemento_id=kwargs['plano_id'], mensagem=var_mensagem, q_linha='q_linha')
    
    elif 'codigoid' in request.GET:
        codigo_id = int(request.GET.get('codigoid',''))
        valor_quebra_de_linha = int(request.GET.get('valor',''))
        codigo_objeto = get_object_or_404(ModeloCodigos, pk=codigo_id)
        codigo_objeto.quebra_de_linha = valor_quebra_de_linha
        codigo_objeto.save()
        if request.method == 'GET ' and 'postprint' in request.GET:
            var_mensagem = 'insere' # Não deve mostrar mensagem alguma
        else:
            var_mensagem = 'Sucesso2'

        return redirect('chamando_despesa_mensagem_q_linha', elemento_id=kwargs['plano_id'], mensagem=var_mensagem, q_linha='q_linha')

    elif 'modelo_fiaid' in request.GET:
        modelo_fiaid = int(request.GET.get('modelo_fiaid',''))
        valor_quebra_de_linha = int(request.GET.get('valor',''))
        modelo_fia_objeto = get_object_or_404(Modelo_fia, pk=modelo_fiaid)
        modelo_fia_objeto.quebra_de_linha = valor_quebra_de_linha
        modelo_fia_objeto.save()
        if request.method == 'GET ' and 'postprint' in request.GET:
            var_mensagem = 'insere' # Não deve mostrar mensagem alguma
        else:
            var_mensagem = 'Sucesso3'

        return redirect('chamando_documento_fia_mensagem_q_linha', elemento_id=kwargs['plano_id'], mensagem=var_mensagem, q_linha='q_linha')

    elif 'extra_fiaid' in request.GET:
        extra_fiaid = int(request.GET.get('extra_fiaid',''))
        valor_quebra_de_linha = int(request.GET.get('valor',''))
        extra_fia_objeto = get_object_or_404(Extra_fia, pk=extra_fiaid)
        extra_fia_objeto.quebra_de_linha = valor_quebra_de_linha
        extra_fia_objeto.save()
        if request.method == 'GET' and 'postprint' in request.GET:
            var_mensagem = 'insere' # Não deve mostrar mensagem alguma
        else:
            var_mensagem = 'Sucesso3'

        return redirect('chamando_documento_fia_mensagem_q_linha', elemento_id=kwargs['plano_id'], mensagem=var_mensagem, q_linha='q_linha')

    return redirect('dashboard')

def atribui_corretor(request, **kwargs):
    plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Func_sec' and plano.alterabilidade == 'Secretaria':
        if plano.corretor_plano == None:
            id1 = request.user.id
            usuario = get_object_or_404(User, pk=id1)
            plano.corretor_plano = usuario
            plano.save()

            checa_corretor = request.user.first_name
            checa_usuario = request.user.first_name
            plano_id = plano.id
            log_atribuiu_corretor(checa_corretor, checa_usuario, plano_id)

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Atribuiu')
        else:
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Ja_possui')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao')

def aprova_plano(request, **kwargs):
    from .alteracoes import envia_email_plano_aprovado
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Func_sec':
        if request.method == 'POST':
            captura_plano.situacao = 'Aprovado'

            if captura_plano.tipo_fia:
                captura_plano.pre_analise_fia = False

            captura_plano.save()

            # gera log
            nome_plano = captura_plano.ano_referencia
            checa_usuario = request.user.first_name
            log_plano_aprovado(nome_plano,checa_usuario, captura_plano.id)
            envia_email_plano_aprovado(request, captura_plano)

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Aprovou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def adiciona_remove_turma(request, **kwargs):
    captura_plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and captura_plano.alterabilidade == 'Escola':

        if kwargs.get('turma_id'): # Turma selecionada
            turma_selecionada  = get_object_or_404(Turmas, pk=kwargs['turma_id'])
            turmas_associadas = Turmas.objects.filter(plano_associado=captura_plano).filter(escola=captura_plano.escola)

            if turmas_associadas: # Se existem turmas associadas a este plano
                if any(turma == turma_selecionada for turma in turmas_associadas): #Se alguma turma associada for a selecionada
                    turma_selecionada.plano_associado.remove(captura_plano) # Remove associação do plano à turma selecionada
                else:
                    turma_selecionada.plano_associado.add(captura_plano) # Cria associação desta turma com o plano
            else: # Se nenhuma das turmas associadas for a turma selecionada
                turma_selecionada.plano_associado.add(captura_plano) # Cria associação desta turma com o plano
                        
            if not captura_plano.tipo_fia:
                return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem='Sucesso')
            else:
                return redirect('chamando_documento_fia_mensagem', elemento_id=kwargs['plano_id'], mensagem='Sucesso')

    if not captura_plano.tipo_fia:
        return redirect('chamando_despesa_plano_mensagem', elemento_id=kwargs['plano_id'], mensagem='Acesso_negado_situacao')
    else:
        return redirect('chamando_documento_fia_mensagem', elemento_id=kwargs['plano_id'], mensagem='not_allowed')
##############################################################################






##### VIEWS NAO TESTADAS #####
def gera_pdf(request, plano_id):
    template_path = 'pdf-acao.html'
    contexto = acao_plano(request, elemento_id=plano_id,  pdf=True)
    context = contexto
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="DOCUMENTO.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def teste(request):
    pass