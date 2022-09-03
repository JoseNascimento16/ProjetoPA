from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from fia.models import Extra_fia, Modelo_fia
from usuarios.models import Classificacao, Turmas # Turmas_plano
from codigos.models.codigos import ModeloCodigos
from Ordens.models import Ordens, ControleOrdens
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

@login_required
def planos_de_acao(request, elemento_id='', atribui='', alt_corretor='', mensagem='', search='', devolve='', edita_plano='', falha_novo_plano=''): # pagina listando todos os planos de ação possíveis de serem vistos
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
    lista_planos_pesquisa = []


    if mensagem == 'Sucesso':
        messages.success(request, 'Sucesso!')
    elif mensagem == 'Criou':
        messages.success(request, 'Plano criado com sucesso!')
    elif mensagem == 'Deletou':
        messages.success(request, 'Plano excluído com sucesso!')
    elif mensagem == 'Editou':
        messages.success(request, 'Plano alterado com sucesso!')
    elif mensagem == 'Publicou':
        messages.success(request, 'Plano publicado com sucesso!')
    elif mensagem == 'Enviou':
        messages.success(request, 'Plano enviado à SUPROT com sucesso!')
    elif mensagem == 'Devolveu':
        messages.success(request, 'Plano devolvido à escola com sucesso!')
    elif mensagem == 'Concluiu':
        messages.success(request, 'Plano enviado à SUPROT com sucesso!')
    elif mensagem == 'Aprovou':
        messages.success(request, 'Plano aprovado com sucesso!')
    elif mensagem == 'Assinado':
        messages.success(request, 'Plano assinado com sucesso!')
    elif mensagem == 'Finalizado':
        messages.success(request, 'Plano finalizado com sucesso!')
    elif mensagem == 'Atribuiu':
        messages.success(request, 'Sucesso! Você agora é o corretor responsável por este plano!')
    elif mensagem == 'Alterou':
        messages.success(request, 'Alteração efetuada com sucesso!')
    elif mensagem == 'Sem_funcionarios':
        messages.error(request, 'Para publicar um plano um tesoureiro ou membro do colegiado deve ser cadastrado!')
    elif mensagem == 'Acesso_negado':
        messages.error(request, 'Acesso negado!')
    elif mensagem == 'Acesso_negado_situacao':
        messages.error(request, 'A situação atual do plano não permite esta alteração!')
    elif mensagem == 'Acesso_negado_situacao2':
        messages.error(request, 'A situação atual do plano não permite este acesso. Favor verificar a legenda!')
    elif mensagem == 'Sem_ordem':
        messages.error(request, 'Para enviar, é preciso ter ao menos 1 "Ordem" cadastrada e inserida no documento: Ações !')
    elif mensagem == 'Sem_codigo':
        messages.error(request, 'Para enviar, todas as ordens do plano precisam ter ao menos 1 "Código" cadastrado e inserido no documento: Ações !')
    elif mensagem == 'Ja_possui':
        messages.error(request, 'Acesso negado, já existe um responsável por este plano!')
    elif mensagem == 'preenchimento':
        messages.error(request, 'Para enviar, preencha as informações faltantes no documento FIA!')
    elif mensagem == 'grupo_incompleto':
        messages.error(request, 'Os membros para autorização do documento ainda não foram totalmente definidos...')
    elif mensagem == 'reset_corretor':
        messages.error(request, 'Somente o "corretor" deste plano pode efetuar esta ação...')

    id = request.user.id
    checa_usuario = request.user
    entidade_matriz = checa_usuario.classificacao.matriz
    # entidade_escola = get_object_or_404(User, last_name=escola_matriz)

    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso

    # checa se a escola possui planos com correções, mostra alerta laranja
    if checa_usuario.classificacao.tipo_de_acesso == 'Escola':
        entidade_escola_nome = get_object_or_404(User, id=id)
        planos_com_correcao = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=entidade_escola_nome)
        for plano in planos_com_correcao:
            if plano.correcoes_a_fazer > 0 and plano.situacao == 'Necessita correção':
                planos_possuem_correcao = True

    if checa_usuario.classificacao.tipo_de_acesso == 'Secretaria' or checa_usuario.classificacao.tipo_de_acesso == 'Func_sec':
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').exclude(situacao='Em desenvolvimento').exclude(situacao='Publicado').exclude(situacao='Necessita correção').exclude(situacao='Aprovado').exclude(situacao='Pronto').exclude(situacao='Finalizado')
        
        if checa_usuario.classificacao.tipo_de_acesso == 'Func_sec':

            if search: #Se for efetuada uma pesquisa por planos

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
                    planos1 = Plano_de_acao.objects.filter(corretor_plano=checa_usuario).exclude(situacao='Em desenvolvimento').exclude(situacao='Publicado').exclude(situacao='Necessita correção').exclude(situacao='Aprovado').exclude(situacao='Pronto').exclude(situacao='Finalizado')
                    planos2 = Plano_de_acao.objects.filter(corretor_plano=None).exclude(situacao='Em desenvolvimento').exclude(situacao='Publicado').exclude(situacao='Necessita correção').exclude(situacao='Aprovado').exclude(situacao='Pronto').exclude(situacao='Finalizado')
                    planos3 = planos1.union(planos2)
                    planos4 = Plano_de_acao.objects.filter(Q(situacao='Assinado') | Q(situacao='Inteiramente assinado')).filter(assinatura_coordenador=False)
                    planos5 = planos3.union(planos4)
                    planos_assinados = checa_usuario.classificacao.plano_associado.filter(Q(situacao='Assinado') | Q(situacao='Inteiramente assinado'))
                    planos = planos5.union(planos_assinados).order_by('-data_de_criação')
                
                else:
                    planos1 = Plano_de_acao.objects.filter(corretor_plano=checa_usuario).exclude(alterabilidade='Escola').exclude(situacao='Finalizado')
                    planos2 = Plano_de_acao.objects.filter(corretor_plano=None).filter(situacao='Pendente')
                    planos = planos1.union(planos2).order_by('-data_de_criação')

            # transforma em "Inteiramente assinado" o plano caso já tenha todas as assinaturas necessárias
            from .alteracoes import plano_inteiramente_assinado
            for item in planos:
                if item.situacao == 'Assinado':
                    captura_plano = get_object_or_404(Plano_de_acao, pk=item.id)
                    plano_inteiramente_assinado(captura_plano)

            objeto_matriz = get_object_or_404(User, last_name=entidade_matriz)
            # if entidade_matriz != 'Secretaria da educação':
            if objeto_matriz.classificacao.tipo_de_acesso == 'Secretaria': # Se for funcionário da secretaria
                for plano in planos:# ESTOU NO PLANO
                    funcionario_associado = Classificacao.objects.filter(plano_associado=plano)#DE TODOS OS FUNCIONARIOS ASSOCIADOS A ESTE PLANO
                    for funcionario in funcionario_associado:
                        if funcionario.user_id == checa_usuario.id: #SE QUALQUER FUNCIONARIO ASSOCIADO A ESTE PLANO, TIVER O MESMO ID DO USUARIO ATUAL
                            # Adiciono à lista para que o HTML possa decidir qual botão mostrar
                            lista_planos_assinados.append(plano.ano_referencia)

        elif checa_usuario.classificacao.tipo_de_acesso == 'Secretaria':
            if search: #Se for efetuada uma pesquisa por planos

                planos = pesquisa_func_sec(request)
                var_pesquisa = True
                if request.method == 'POST':
                    valor_pesquisa = request.POST['campo']
                else:
                    valor_pesquisa = request.GET.get('q','')

        # Se plano estiver pra ser devolvido com correções, manda formulário para permitir marcar checkbox de pré assinatura
        if any(plano.situacao == 'Pendente' and plano.pre_analise_acao and plano.pre_analise_despesa and plano.correcoes_a_fazer > 0 for plano in planos):
            form_pre_assinatura = PreAssinaturaForm()
                               
    elif checa_usuario.classificacao.tipo_de_acesso == 'Escola':

        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=id).filter(~Q(situacao='Pendente')).filter(~Q(situacao='Concluido')).filter(~Q(situacao='Necessita correção')).filter(~Q(situacao='Corrigido pela escola')).filter(~Q(situacao='Finalizado')).filter(~Q(situacao='Assinado')).filter(~Q(situacao='Inteiramente assinado'))
        
        if search: #Se for efetuada uma pesquisa por planos   
            planos = pesquisa_escola(request)
            var_pesquisa = True
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')

        for plano in planos:# ESTOU NO PLANO
                funcionario_associado = Classificacao.objects.filter(plano_associado=plano)#DE TODOS OS FUNCIONARIOS ASSOCIADOS A ESTE PLANO
                for funcionario in funcionario_associado:
                    if funcionario.user_id == checa_usuario.id: #SE QUALQUER FUNCIONARIO ASSOCIADO A ESTE PLANO, TIVER O MESMO ID DO USUARIO ATUAL
                        # Adiciono à lista para que o HTML possa decidir qual botão mostrar
                        lista_planos_assinados.append(plano.ano_referencia)

    elif checa_usuario.classificacao.tipo_de_acesso == 'Funcionario':
        objeto_matriz = get_object_or_404(User, last_name=entidade_matriz)
        # if entidade_matriz != 'Secretaria da educação':
        if objeto_matriz.classificacao.tipo_de_acesso == 'Escola': # Se for funcionário de escolas
            planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=objeto_matriz).filter(~Q(situacao='Finalizado'))
            for plano in planos:# ESTOU NO PLANO
                funcionario_associado = Classificacao.objects.filter(plano_associado=plano)#DE TODOS OS FUNCIONARIOS ASSOCIADOS A ESTE PLANO
                for funcionario in funcionario_associado:
                    if funcionario.user_id == checa_usuario.id: #SE QUALQUER FUNCIONARIO ASSOCIADO A ESTE PLANO, TIVER O MESMO ID DO USUARIO ATUAL
                        # Adiciono à lista para que o HTML possa decidir qual botão mostrar
                        lista_planos_assinados.append(plano.ano_referencia)

        elif objeto_matriz.classificacao.tipo_de_acesso == 'Secretaria' or objeto_matriz.classificacao.tipo_de_acesso == 'Func_sec': # Se for funcionario da secretaria
            planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(situacao='Finalizado')

    if atribui: # abre modal de confirmação de atribuição de corretor para o plano
        confirma_corrige = True
        plano_atribui = get_object_or_404(Plano_de_acao, pk=elemento_id)

    if alt_corretor: # abre modal para alteração do corretor do plano
        altera_corretor = True
        plano_altera_corretor = get_object_or_404(Plano_de_acao, pk=elemento_id)
        corretor_form = AlteraCorretorForm()
        corretor_form.fields['campo'].initial = plano_altera_corretor.corretor_plano

    if devolve: # abre modal para devolução de planos com correções
        confirma_devolve = True
        plano_devolver = get_object_or_404(Plano_de_acao, pk=elemento_id)

    

    paginator_planos = Paginator(planos, 10)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)
    
    classificacoes = Classificacao.objects.all()

    if edita_plano:
        print('ENTROU EDICAO NOME PLANO')
        plano_selecionado = get_object_or_404(Plano_de_acao, pk=elemento_id)
        plano_selecionado2 = Plano_de_acao.objects.filter(pk=elemento_id)

        edita_plano_form.fields['ano_referencia'].initial = plano_selecionado.ano_referencia

        dados = {
            'chave_planos' : page,
            'chave_form_planos' : form_plano,
            'chave_form_fia' : form_fia,
            'chave_edita_plano_form' : edita_plano_form,
            'contexto_edicao_plano' : plano_selecionado,
            'chave_contexto_edicao_plano' : plano_selecionado2,
            'chave_tipo_usuario' : tipo_usuario,
            'chave_planos_com_correcao' : planos_possuem_correcao,
            'chave_planos_assinados' : lista_planos_assinados,
            'chave_pre_assinatura' : form_pre_assinatura,
            'chave_classificacoes' : classificacoes,
        }
        return render(request, 'planos_de_acao.html', dados)
    else:
        dados = {
            'chave_planos' : page,
            'chave_form_planos' : form_plano,
            'chave_form_fia' : form_fia,
            'chave_edita_plano_form' : edita_plano_form,
            'chave_tipo_usuario' : tipo_usuario,
            'chave_planos_com_correcao' : planos_possuem_correcao,
            'chave_planos_assinados' : lista_planos_assinados,
            'chave_pre_assinatura' : form_pre_assinatura,
            'chave_confirma_corrige' : confirma_corrige,
            'chave_plano_atribui' : plano_atribui,
            'chave_plano_altera_corretor' : plano_altera_corretor,
            'chave_altera_corretor' : altera_corretor,
            'chave_corretor_form' : corretor_form,
            'chave_var_pesquisa' : var_pesquisa,
            'chave_valor_pesquisa' : valor_pesquisa,
            'chave_classificacoes' : classificacoes,
            'chave_confirma_devolve' : confirma_devolve,
            'chave_plano_devolver' : plano_devolver,
        }

    if falha_novo_plano:
        return dados
    else:
        return render(request, 'planos_de_acao.html', dados)

def pesquisa_plano(request):
    print('testeeesese')
    if request.method == 'POST':
        valor_pesquisa = request.POST['campo']
        print(valor_pesquisa)
        if valor_pesquisa != '':
            return redirect('pagina_planos_de_acao_pesquisa', search=valor_pesquisa)
        else:
            return redirect('pagina_planos_de_acao')
    else:
        print('ELSE')
        return redirect('pagina_planos_de_acao')

def planos_finalizados(request): # pagina dos planos já aprovados
    # print('entrou def planos concluidos')
    id = request.user.id
    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso

    if checa_usuario.classificacao.tipo_de_acesso == 'Secretaria' or checa_usuario.classificacao.tipo_de_acesso == 'Func_sec':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(situacao='Finalizado')
    elif checa_usuario.classificacao.tipo_de_acesso == 'Escola':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=id).filter(situacao='Finalizado')
    elif checa_usuario.classificacao.tipo_de_acesso == 'Funcionario':
        matriz_usuario_atual = checa_usuario.classificacao.matriz
        escola = get_object_or_404(User, last_name=matriz_usuario_atual)
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=escola).filter(situacao='Finalizado')

    paginator_planos = Paginator(planos, 2)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    dados = {
        'chave_planos' : page,
        'chave_tipo_usuario': tipo_usuario
    }

    return render(request, 'planos_de_acao.html', dados)

def planos_a_serem_corrigidos(request, variavel=''): # pagina dos planos já aprovados
    id = request.user.id
    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso
    pagina_correcoes = True

    if checa_usuario.classificacao.tipo_de_acesso == 'Secretaria' or checa_usuario.classificacao.tipo_de_acesso == 'Func_sec':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(situacao ='Necessita correção')
    elif checa_usuario.classificacao.tipo_de_acesso == 'Escola':
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=id).filter(situacao='Necessita correção')
    elif checa_usuario.classificacao.tipo_de_acesso == 'Funcionario':
        matriz_usuario_atual = checa_usuario.classificacao.matriz
        escola = get_object_or_404(User, last_name=matriz_usuario_atual)
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=escola).filter(situacao='Necessita correção')

    paginator_planos = Paginator(planos, 2)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    dados = {
        'chave_planos' : page,
        'chave_tipo_usuario' : tipo_usuario,
        'chave_pagina_correcoes' : pagina_correcoes,
    }

    return render(request, 'planos_de_acao.html', dados)

def plano(request, plano_id, gera_ordem='', ordem_id='', edita_ordem='', mensagem=''):# acesso às ordens de um plano
    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola' and plano_objeto.tipo_fia == False:
        print('ENTROU EM UM PLANO')

        if mensagem == 'Criou':
            messages.success(request, 'Ordem criada com sucesso!')
        elif mensagem == 'Deletou':
            messages.success(request, 'Ordem excluída com sucesso!')
        elif mensagem == 'Editou':
            messages.success(request, 'Ordem alterada com sucesso!')

        ordem = False
        form_ordem = False

        plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
        plano2 = Plano_de_acao.objects.filter(pk=plano_id)
        ordem2 = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_id)

        if gera_ordem == 'gera':
            abre_nova_ordem = True
            form_ordem = OrdemForm()
        else:
            abre_nova_ordem = False

        plano_a_exibir = {
            'chave_planos' : plano_objeto,
            'chave_planos2' : plano2,
            'chave_ordens' : ordem,
            'chave_ordens2' : ordem2,
            'chave_tipo_usuario' : tipo_usuario,

            'chave_form_ordem' : form_ordem,
            'chave_abre_nova_ordem' : abre_nova_ordem,

        }

        return render(request, 'plano.html', plano_a_exibir)
    else:
        if tipo_usuario == 'Escola':
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao2')
        else:
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def abre_edicao_ordem(request, plano_id, ordem_id=''): #elemento_id é o id do plano
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    plano = get_object_or_404(Plano_de_acao, pk=plano_id)
    if tipo_usuario == 'Escola' and plano.alterabilidade == 'Escola':
        plano = get_object_or_404(Plano_de_acao, pk=plano_id)
        ordem = get_object_or_404(Ordens, pk=ordem_id)
        plano2 = Plano_de_acao.objects.filter(pk=plano_id)
        ordem2 = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_id)

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
    else:
        return redirect('dashboard')

def acao_plano(request, elemento_id, mensagem='', pdf='', ordem_id='', contx_ordem='', q_linha=''): # visualização acao principal
    
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    # ordem_objeto = get_object_or_404(Ordens, pk=38) # acho que esta inutilizado
    plano_iteravel = Plano_de_acao.objects.filter(pk=elemento_id)
    ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto.id)
    codigos_iteravel=[]
    ordens_sem_codigo=[]
    ordens_lista=[]
    ordens_lista2=[]
    membros_colegiado=[]
    quant_de_membros = 0
    var_template = get_object_or_404(ControleOrdens, pk=1)
    funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.usuario.last_name)
    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso
    situacao_plano = plano_objeto.situacao
    contexto_abre_form_datas = False
    var_reset = False
    apos_print = False
    quebra_linha = False
    var_plano_pre_aprovado = False
    ordem_data = ''
    form_datas = Cadastra_datas_Ordem_Form()

    for item in funcionarios:
        if item.user.last_name == 'Membro do colegiado':
            membros_colegiado.append(item)
    
    if mensagem == 'Criou':
        messages.success(request, 'Sugestão de correção criada com sucesso!')
    elif mensagem == 'Deletou':
        messages.success(request, 'Sugestão de correção excluída com sucesso!')
    elif mensagem == 'Editou':
        messages.success(request, 'Sugestão de correção alterada com sucesso!')
    elif mensagem == 'Sucesso':
        messages.success(request, 'Sucesso!')
    elif mensagem == 'Sucesso2':
        if request.method == 'GET' and 'postprint' not in request.GET:
            messages.success(request, 'Alteração efetuada com sucesso!')
    elif mensagem == 'Datas':
        messages.error(request, 'Para concluir é necessário definir as datas de todos os "prazos de execução"!')
    elif mensagem == 'Nao_corretor':
        messages.error(request, 'Você não é o corretor responsável por este plano')
    elif mensagem == 'Erro':
        messages.error(request, 'Ocorreu algum erro!')
    elif mensagem == 'Acesso_negado':
        messages.error(request, 'Acesso negado!')

    # Redundância para garantir que os valores de rowspan, codigos_inseridos (ordem) e inserido(codigo) não saiam do padrão por qualquer motivo que seja
    for ordem_OBJ in ordens_iteravel:
        if ordem_OBJ.codigos_inseridos < 0 or ordem_OBJ.ordem_rowspan < 0 or ordem_OBJ.codigos_inseridos != ordem_OBJ.ordem_rowspan:
            print('CONSERTOU')
            ordem_OBJ.codigos_inseridos = 0
            ordem_OBJ.ordem_rowspan = 0
            ordem_OBJ.save()
            codigos_dessa_ordem = ModeloCodigos.objects.order_by('identificacao').filter(ordem=ordem_OBJ)
            for codigo in codigos_dessa_ordem:
                codigo.inserido = False
                codigo.save()


    for elemento in ordens_iteravel: # Todas as ordens deste plano
        codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
        # print(codigos_varredura)
        if not codigos_varredura: # Se a ordem nao possuir codigos, manda essa informação pro contexto
            ordens_sem_codigo.append(elemento)
        for items in codigos_varredura:
            codigos_iteravel.append(items) # Lista com todos os 'OBJETOS codigo' de todas as ordens deste plano

    # print(codigos_iteravel)

    for elemento in ordens_iteravel:
        ordens_lista.append(elemento.identificacao_numerica)
    # print(ordens_lista) #LISTA COM NUMERO DAS ORDENS DESSE PLANO

    for pessoas in funcionarios:
        if pessoas.user.last_name == 'Membro do colegiado':
            quant_de_membros += 1

    quant_de_membros_mais = quant_de_membros + 1

    todas_ordens = get_object_or_404(ControleOrdens, pk=1)

    #Coloca o numero de todas as ordens deste plano em uma lista para ser passada pro jquery
    ordens_com_sugestao = Ordens.objects.filter(plano=plano_objeto).filter(possui_sugestao_correcao=True)
    for itens in ordens_com_sugestao:
        ordens_lista2.append(itens.identificacao_numerica)
    # print(ordens_lista2)

    if plano_objeto.pre_analise_acao:
        sugestoes_plano_concluidas = 1
    else:
        sugestoes_plano_concluidas = 0

    if plano_objeto.devolvido:
        var_devolvido = 1
    else:
        var_devolvido = 0

    if ordem_id: # Abre formulario para cadastro de datas
        if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
            ordem_data = get_object_or_404(Ordens, pk=ordem_id)
            contexto_abre_form_datas = True
            form_datas = Cadastra_datas_Ordem_Form()
            if ordem_data.prazo_execucao_inicial != '':
                form_datas.fields['prazo_execucao_inicial'].initial = ordem_data.prazo_execucao_inicial
            if ordem_data.prazo_execucao_final != '':
                form_datas.fields['prazo_execucao_final'].initial = ordem_data.prazo_execucao_final
        else: # se usuario atual nao for o corretor
            return redirect('chamando_acao_plano_mensagem', elemento_id=elemento_id, mensagem='Nao_corretor')

    if plano_objeto.situacao == 'Assinado':
        var_reset = True

    if request.method == 'GET' and 'postprint' in request.GET:
        apos_print = request.GET.get('postprint','')

    if q_linha:
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
        'chave_todas_ordens' : todas_ordens,
        'chave_codigos' : codigos_iteravel,
        'vartemplate' : var_template,
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
        'chave_reset_plano' : var_reset,
        'chave_q_linha' : quebra_linha,
        'chave_apos_print' : apos_print,
        'plano_aprovado' : var_plano_pre_aprovado,
        'pagina_acoes' : True,
    }

    if pdf: # A FUNÇÃO 'gera_pdf' CHAMA ESTE CONTEXTO PARA RENDERIZAR O PDF
        contexto_pdf = plano_a_exibir
        return contexto_pdf

    if contx_ordem: # A FUNÇÃO 'cadastra_data' DA VIEWS DE ORDENS CHAMA ESTE CONTEXTO PARA RENDERIZAR ESTA PAGINA
        contexto_ordem = plano_a_exibir
        print('chamou contexto novo')
        return contexto_ordem

    return render(request, 'acao-visualizacao.html', plano_a_exibir)

def acao_plano_correcao(request, elemento_id, ordem_id):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
        ordem_a_corrigir = get_object_or_404(Ordens, pk=ordem_id)
        contexto_extra_corrigir = True
        var_reset = False

        form_correcao_acao = Correcao_acaoForm()

        # plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)
        correcao_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=None)
        plano_iteravel = Plano_de_acao.objects.filter(pk=elemento_id)
        ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto.id)
        codigos_iteravel=[]
        ordens_lista=[]
        ordens_lista2=[]
        membros_colegiado=[]
        quant_de_membros = 0
        var_template = get_object_or_404(ControleOrdens, pk=1)
        funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.usuario.last_name)
        checa_usuario = request.user
        tipo_usuario = checa_usuario.classificacao.tipo_de_acesso
        situacao_plano = plano_objeto.situacao

        for item in funcionarios:
            if item.user.last_name == 'Membro do colegiado':
                membros_colegiado.append(item)

        for elemento in ordens_iteravel:
            codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
            # print(codigos_varredura)
            for items in codigos_varredura:
                codigos_iteravel.append(items)

        for elemento in ordens_iteravel:
            ordens_lista.append(elemento.identificacao_numerica)
        # print(ordens_lista) #LISTA COM NUMERO DAS ORDENS DESSE PLANO

        for pessoas in funcionarios:
            if pessoas.user.last_name == 'Membro do colegiado':
                quant_de_membros += 1

        quant_de_membros_mais = quant_de_membros + 1

        todas_ordens = get_object_or_404(ControleOrdens, pk=1)

        #Coloca o numero de todas as ordens deste plano em uma lista para ser passada pro jquery
        ordens_com_sugestao = Ordens.objects.filter(plano=plano_objeto).filter(possui_sugestao_correcao=True)
        for itens in ordens_com_sugestao:
            ordens_lista2.append(itens.identificacao_numerica)
        # print(ordens_lista2)

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
            'chave_todas_ordens' : todas_ordens,
            'chave_codigos' : codigos_iteravel,
            'vartemplate' : var_template,
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
    else:
        return redirect('chamando_acao_plano_mensagem', elemento_id=elemento_id, mensagem='Nao_corretor')

def cria_altera_correcao_acao(request, plano_id, ordem_id=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)
        form_correcao_acao_preenchido = Correcao_acaoForm()
        if request.method == 'POST':
            form_correcao_acao_preenchido = Correcao_acaoForm(request.POST)
            if form_correcao_acao_preenchido.is_valid():
                # CRIA NOVA CORREÇÃO
                if not ordem_objeto.possui_sugestao_correcao:
                    instancia = form_correcao_acao_preenchido.save(commit=False)
                    instancia.plano_associado = plano_objeto
                    instancia.save()

                    plano_objeto.correcoes_a_fazer += 1
                    plano_objeto.save()

                    ordem_objeto.possui_sugestao_correcao = True
                    ordem_objeto.save()

                    mensagem_var = 'Criou'
                    # print('criou nova correcao')
                # ALTERA CORREÇÃO EXISTENTE
                else:
                    correcao_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica)
                    for item in correcao_iteravel:
                        item.sugestao = form_correcao_acao_preenchido.cleaned_data.get('sugestao')
                        item.save()

                        mensagem_var = 'Editou'
                    # print('alterou correcao')
            else:
                print(form_correcao_acao_preenchido.errors)

        return redirect('chamando_acao_plano_mensagem', elemento_id=plano_id, mensagem=mensagem_var)

    return redirect('chamando_acao_plano', elemento_id=plano_id)

def deleta_correcao_acao(request, plano_id, ordem_id=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)
        if request.method == 'POST':
            correcao_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica)
            for item in correcao_iteravel:
                item.delete()

            plano_objeto.correcoes_a_fazer -= 1
            plano_objeto.save()

            ordem_objeto.possui_sugestao_correcao = False
            ordem_objeto.save()
            # print('apagou correcao')

        return redirect('chamando_acao_plano_mensagem', elemento_id=plano_id, mensagem='Deletou')

    return redirect('chamando_acao_plano', elemento_id=plano_id)

def acao_plano_adiciona_ordem(request, plano_id, elemento_id=''):
    print('entrou adiciona ordem')
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola':
        ordens_iteravel = Ordens.objects.filter(plano=plano_id)
        todas_ordens = get_object_or_404(ControleOrdens, pk=1)

        if elemento_id: #Se receber id de ordem, modifica esta ordem
            ordem_a_modificarOBJ = get_object_or_404(Ordens, pk=elemento_id)
            ordem_a_modificarITR = Ordens.objects.filter(pk=elemento_id)
            if not ordem_a_modificarOBJ.inserida: #Se não estiver inserida
                ordem_a_modificarOBJ.inserida = True
                todas_ordens.comando_todas = False
                todas_ordens.comando_individual = True
                ordem_a_modificarOBJ.save()
                todas_ordens.save()
                print('ADICIONOU ORDEM = ' + str(elemento_id))
            else: #Se estiver inserida
                ordem_a_modificarOBJ.inserida = False
                todas_ordens.comando_todas = False
                todas_ordens.comando_individual = True
                ordem_a_modificarOBJ.save()
                todas_ordens.save()
                print('REMOVEU ORDEM = ' + str(elemento_id))
        else: #Se não receber id de ordem, altera todas

            if not todas_ordens.todas_inseridas:
                todas_ordens.todas_inseridas = True
                todas_ordens.comando_todas = True
                todas_ordens.comando_individual = False
                todas_ordens.save()
                for elemento in ordens_iteravel:
                    elemento.inserida = True
                    elemento.save()
                print('ADICIONOU TODAS AS ORDENS')
            else:
                todas_ordens.todas_inseridas = False
                todas_ordens.comando_todas = True
                todas_ordens.comando_individual = False
                todas_ordens.save()
                for elemento in ordens_iteravel:
                    elemento.inserida = False
                    elemento.save()
                print('REMOVEU TODAS AS ORDENS')

        plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
        plano_iteravel = Plano_de_acao.objects.filter(pk=plano_id)

        # ADICIONOU ORDEM

        return redirect('chamando_acao_plano', elemento_id=plano_id)
    
    return redirect('dashboard')

def acao_plano_modifica_codigo(request, plano_id, ordem_id, codigo_id):
    codigo_OBJ = get_object_or_404(ModeloCodigos, pk=codigo_id)
    ordem_OBJ = get_object_or_404(Ordens, pk=ordem_id)

    # ALTERANDO ESTADO
    if not codigo_OBJ.inserido:
        codigo_OBJ.inserido = True
        codigo_OBJ.save()
        ordem_OBJ.codigos_inseridos += 1
        ordem_OBJ.ordem_rowspan += 1
        ordem_OBJ.save()

    else:
        codigo_OBJ.inserido = False
        codigo_OBJ.save()
        ordem_OBJ.codigos_inseridos -= 1
        ordem_OBJ.ordem_rowspan -= 1
        ordem_OBJ.save()

    return redirect('chamando_acao_plano', elemento_id=plano_id)

def despesa_plano(request, elemento_id, mensagem='', q_linha=''): # Visualização principal

    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    ordem_objeto = get_object_or_404(Ordens, pk=20)
    plano_iteravel = Plano_de_acao.objects.filter(pk=elemento_id)
    ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto.id)
    codigos_iteravel=[]
    codigos_lista=[]
    codigos_lista2=[]
    membros_colegiado=[]
    turmas_iteravel = Turmas.objects.order_by('nome').filter(user=plano_objeto.usuario)
    turmas_associadas_iteravel = Turmas.objects.order_by('nome').filter(user=plano_objeto.usuario).filter(plano_associado=plano_objeto)
    quant_de_membros = 0
    soma_capital = 0
    soma_custeio = 0
    quebra_linha = False
    apos_print = False
    var_template = get_object_or_404(ControleOrdens, pk=1)
    funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.usuario.last_name)
    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso
    # lista_turmas_no_menu = []
    situacao_plano = plano_objeto.situacao

    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso

    for item in funcionarios:
        if item.user.last_name == 'Membro do colegiado':
            membros_colegiado.append(item)

    if mensagem == 'Criou':
        messages.success(request, 'Sugestão de correção criada com sucesso!')
    elif mensagem == 'Sucesso':
        messages.success(request, 'Alteração realizada com sucesso!')
    elif mensagem == 'Sucesso2':
        if request.method == 'GET' and 'postprint' not in request.GET:
            messages.success(request, 'Alteração efetuada com sucesso!')
    elif mensagem == 'Deletou':
        messages.success(request, 'Sugestão de correção excluída com sucesso!')
    elif mensagem == 'Editou':
        messages.success(request, 'Sugestão de correção alterada com sucesso!')
    elif mensagem == 'Nao_corretor':
        messages.error(request, 'Você não é o corretor responsável por este plano!')
    elif mensagem == 'Acesso_negado':
        messages.error(request, 'Acesso_negado!')
    elif mensagem == 'Acesso_negado_situacao':
        messages.error(request, 'Acesso_negado, a situação atual do plano não permite esta alteração!')

    for elemento in ordens_iteravel:
        codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
        for items in codigos_varredura:
            codigos_iteravel.append(items)
    # print(codigos_iteravel)

    for pessoas in funcionarios:
        if pessoas.user.last_name == 'Membro do colegiado':
            quant_de_membros += 1

    for elemento in codigos_iteravel:
        if elemento.preco_total_capital: #checagem para não tentar somar com valores nulos
            soma_capital = soma_capital + elemento.preco_total_capital
        # print(soma_capital)

    for elemento in codigos_iteravel:
        if elemento.preco_total_custeio: #checagem para não tentar somar com valores nulos
            soma_custeio = soma_custeio + elemento.preco_total_custeio
        # print(soma_custeio)

    soma_total = soma_capital + soma_custeio
    quant_de_membros_mais = quant_de_membros + 1

    todas_ordens = get_object_or_404(ControleOrdens, pk=1)

    #Coloca as ordens e seus respectivos códigos em uma lista para serem passados pro jquery
    for elemento in ordens_iteravel:
        codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
        for items in codigos_varredura:
            codigos_lista.append(str(elemento.identificacao_numerica) + items.identificacao)
            if items.possui_sugestao_correcao:
                codigos_lista2.append(str(elemento.identificacao_numerica) + items.identificacao)

    if request.method == 'GET' and 'postprint' in request.GET:
        apos_print = request.GET.get('postprint','')

    if q_linha:
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
        'chave_ordens' : ordem_objeto,
        'chave_ordens2' : ordens_iteravel,
        'chave_todas_ordens' : todas_ordens,
        'chave_codigos' : codigos_iteravel,
        'chave_turmas' : turmas_iteravel,
        'chave_turmas_associadas' : turmas_associadas_iteravel,
        # 'chave_lista_turmas' : lista_turmas_no_menu,
        'vartemplate' : var_template,
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

def despesa_plano_correcao(request, elemento_id, ordem_id, codigo_id):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
        codigo_objeto_corrigir = get_object_or_404(ModeloCodigos, pk=codigo_id)
        contexto_extra_corrigir = True

        form_correcao_despesa = Correcao_despesaForm()

        # plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)

        plano_iteravel = Plano_de_acao.objects.filter(pk=elemento_id)
        ordens_iteravel = Ordens.objects.order_by('identificacao_numerica').filter(plano=plano_objeto.id)
        correcao_depesas_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=codigo_objeto_corrigir.identificacao)
        codigos_iteravel=[]
        codigos_lista=[]
        codigos_lista2=[]
        turmas_iteravel = Turmas.objects.order_by('nome').filter(user=plano_objeto.usuario)
        turmas_associadas_iteravel = Turmas.objects.order_by('nome').filter(user=plano_objeto.usuario).filter(plano_associado=plano_objeto)
        quant_de_membros = 0
        soma_capital = 0
        soma_custeio = 0
        var_template = get_object_or_404(ControleOrdens, pk=1)
        funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=plano_objeto.usuario.last_name)
        checa_usuario = request.user
        tipo_usuario = checa_usuario.classificacao.tipo_de_acesso
        # lista_turmas_no_menu = []
        situacao_plano = plano_objeto.situacao

        checa_usuario = request.user
        tipo_usuario = checa_usuario.classificacao.tipo_de_acesso

        for elemento in ordens_iteravel:
            codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
            # print(codigos_varredura)
            for items in codigos_varredura:
                codigos_iteravel.append(items)

        for pessoas in funcionarios:
            if pessoas.user.last_name == 'Membro do colegiado':
                quant_de_membros += 1

        for elemento in codigos_iteravel:
            if elemento.preco_total_capital: #checagem para não tentar somar com valores nulos
                soma_capital = soma_capital + elemento.preco_total_capital
            # print(soma_capital)

        for elemento in codigos_iteravel:
            if elemento.preco_total_custeio: #checagem para não tentar somar com valores nulos
                soma_custeio = soma_custeio + elemento.preco_total_custeio
            # print(soma_custeio)

        soma_total = soma_capital + soma_custeio
        quant_de_membros_mais = quant_de_membros + 1

        todas_ordens = get_object_or_404(ControleOrdens, pk=1)

        #Coloca as ordens e seus respectivos códigos em uma lista para serem passados pro jquery
        for elemento in ordens_iteravel:
            codigos_varredura = ModeloCodigos.objects.order_by('identificacao').filter(ordem=elemento)
            for items in codigos_varredura:
                codigos_lista.append(str(elemento.identificacao_numerica) + items.identificacao)
                if items.possui_sugestao_correcao:
                    codigos_lista2.append(str(elemento.identificacao_numerica) + items.identificacao)
        # print(codigos_lista) #resultado por ex:['1G', '1U', '1Y', '3A', '3B', '3C']
        # print(codigos_lista2) #resultado por ex:['1G', '3A']



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
            'chave_todas_ordens' : todas_ordens,
            'chave_codigos' : codigos_iteravel,
            'chave_turmas' : turmas_iteravel,
            'chave_turmas_associadas' : turmas_associadas_iteravel,
            # 'chave_lista_turmas' : lista_turmas_no_menu,
            'vartemplate' : var_template,
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
        return redirect('chamando_despesa_plano_mensagem', elemento_id=elemento_id, mensagem='Nao_corretor')

def cria_altera_correcao_despesa(request, plano_id, ordem_id='', codigo_id=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)
        codigo_objeto_corrigir = get_object_or_404(ModeloCodigos, pk=codigo_id)
        form_correcao_despesa_preenchido = Correcao_despesaForm()
        if request.method == 'POST':
            form_correcao_despesa_preenchido = Correcao_despesaForm(request.POST)
            if form_correcao_despesa_preenchido.is_valid():
                # CRIA NOVA CORREÇÃO
                if not codigo_objeto_corrigir.possui_sugestao_correcao:
                    instancia = form_correcao_despesa_preenchido.save(commit=False)
                    instancia.plano_associado = plano_objeto
                    instancia.ordem_associada = ordem_objeto.identificacao_numerica
                    instancia.codigo_associado = codigo_objeto_corrigir.identificacao
                    instancia.save()

                    plano_objeto.correcoes_a_fazer += 1
                    plano_objeto.save()

                    codigo_objeto_corrigir.possui_sugestao_correcao = True
                    codigo_objeto_corrigir.save()

                    mensagem_var = 'Criou'
                    # print('criou nova correcao despesa')
                # ALTERA CORREÇÃO EXISTENTE
                else:
                    correcao_depesas_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=codigo_objeto_corrigir.identificacao)
                    for item in correcao_depesas_iteravel:
                        item.sugestao = form_correcao_despesa_preenchido.cleaned_data.get('sugestao')
                        item.save()

                        mensagem_var = 'Editou'
                    # print('alterou correcao despesa')
            else:
                print(form_correcao_despesa_preenchido.errors)

        return redirect('chamando_despesa_plano_mensagem', elemento_id=plano_id, mensagem=mensagem_var)

    return redirect('chamando_despesa_plano', elemento_id=plano_id)

def deleta_correcao_despesa(request, plano_id, ordem_id='', codigo_id=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)
        codigo_objeto_corrigir = get_object_or_404(ModeloCodigos, pk=codigo_id)
        if request.method == 'POST':
            correcao_depesas_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=ordem_objeto.identificacao_numerica).filter(codigo_associado=codigo_objeto_corrigir.identificacao)
            for item in correcao_depesas_iteravel:
                item.delete()

            plano_objeto.correcoes_a_fazer -= 1
            plano_objeto.save()

            codigo_objeto_corrigir.possui_sugestao_correcao = False
            codigo_objeto_corrigir.save()
            # print('apagou correcao')

        return redirect('chamando_despesa_plano_mensagem', elemento_id=plano_id, mensagem='Deletou')

    return redirect('chamando_despesa_plano', elemento_id=plano_id)

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

def pagina_correcoes(request, elemento_id, ident_numerica='', abreForm='', codigo_ident='', abreFormDespesa='', retorna_contexto_fia='', mensagem=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    correcoes_no_plano = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto)
    if not plano_objeto.tipo_fia:
        correcoes_de_ordens = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto).filter(documento_associado = '1 - Identificação das ações')
    else:
        correcoes_de_ordens = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto).filter(documento_associado = 'FIA - Formulário de Inclusão de Ações')
    correcoes_de_codigos = Correcoes.objects.order_by('codigo_associado').filter(plano_associado=plano_objeto).filter(documento_associado = '2 - Detalhamento das Despesas')

    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso

    if mensagem == 'Sucesso':
        messages.success(request, 'Correção efetuada com sucesso!')

    if (plano_objeto.devolvido == True) and (plano_objeto.correcoes_a_fazer == 0):
        plano_objeto.situacao = 'Publicado'
        plano_objeto.save()

        nome_usuario = checa_usuario.first_name
        nome_plano = plano_objeto.ano_referencia
        log_plano_correcoes_concluidas(nome_plano, nome_usuario, plano_objeto.id)

    if abreForm:
        print('abriu form acao ou FIA')
        contexto_corrigindo = True
        ordem_objeto = get_object_or_404(Ordens, plano=plano_objeto, identificacao_numerica = ident_numerica)
        correcao_de_ordem_especifica = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto).filter(documento_associado = '1 - Identificação das ações').filter(ordem_associada=ident_numerica)


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

        # print(list_forms)


        if abreForm == 'form_ordem_invalido': # este valor vem da função 'corrigindo acao' que chama esta função pra renderizar o form com os erros
            contexto = {
            'chave_plano': plano_objeto,
            'chave_ordem': ordem_objeto,
            'chave_correcoes_ordens': correcoes_de_ordens,
            'chave_correcao_ordem_especifica': correcao_de_ordem_especifica,
            'chave_correcoes_codigos': correcoes_de_codigos,
            'chave_contexto_corrigindo_acao' : contexto_corrigindo,
            'chave_form_codigos' : list_forms,
            'chave_tipo_usuario' : tipo_usuario,
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
        }
            return render(request, 'correcoes.html', contexto)

    elif abreFormDespesa:
        print('abriu form despesa')
        contexto_corrigindo_despesa = True
        ordem_objeto = get_object_or_404(Ordens, plano=plano_objeto, identificacao_numerica = ident_numerica)
        codigo_objeto = get_object_or_404(ModeloCodigos, ordem=ordem_objeto, identificacao = codigo_ident)
        correcao_de_codigo_especifico = get_object_or_404(Correcoes, plano_associado=plano_objeto, ordem_associada=ident_numerica, codigo_associado=codigo_ident)


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

        if abreFormDespesa == 'form_despesa_invalido':
            contexto = {
                'chave_plano': plano_objeto,
                'chave_ordem': ordem_objeto,
                'chave_codigo': codigo_objeto,
                'chave_correcoes_ordens': correcoes_de_ordens,
                'chave_correcoes_codigos': correcoes_de_codigos,
                'chave_correcao_codigo_especifico': correcao_de_codigo_especifico,
                'chave_contexto_corrigindo_despesa' : contexto_corrigindo_despesa,
                'chave_tipo_usuario' : tipo_usuario,
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
            }
            return render(request, 'correcoes.html', contexto)

    else:

        contexto = {
            'chave_plano': plano_objeto,
            'chave_correcoes_ordens': correcoes_de_ordens,
            'chave_correcoes_codigos': correcoes_de_codigos,
            'chave_tipo_usuario' : tipo_usuario,
        }

        if retorna_contexto_fia:
            return contexto
        else:
            return render(request, 'correcoes.html', contexto)

def corrigindo_acao(request, plano_id, ordem_id):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola':
        ordem_objeto = get_object_or_404(Ordens, pk=ordem_id)
        codigos_da_ordem_inseridos = ModeloCodigos.objects.order_by('identificacao').filter(ordem=ordem_objeto).filter(inserido=True)

        # form de ordem
        if request.method == 'POST':
            firstform = Edita_Ordem_Form(request.POST, plano_id_super=plano_id, correcao_super='form_correcao')
            if firstform.is_valid():
                print('valido')
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

                # Reduz em 1 a quantidade de correções neste plano
                plano_objeto.correcoes_a_fazer -= 1
                plano_objeto.save()

                # Remove o objeto 'correcao' uma vez que ela acabou de ser corrigida.
                correcao_remover = Correcoes.objects.filter(plano_associado=plano_objeto).filter(documento_associado = '1 - Identificação das ações').filter(ordem_associada = ordem_objeto.identificacao_numerica)
                for objeto in correcao_remover:
                    objeto.delete()

                # Salva as informações nos forms de codigos, nos seus respectivos objetos
                for modelo in codigos_da_ordem_inseridos:
                    secondform = Mini_form_Codigos(request.POST, prefix=modelo.identificacao)
                    if secondform.is_valid():
                        print('validos')
                        valor_especificacao = secondform.cleaned_data.get('especificacao')
                        modelo.especificacao = valor_especificacao
                        modelo.save()

                    else:
                        # sempre será valido
                        pass

            else:
                contexto = pagina_correcoes(request, plano_id, ordem_objeto.identificacao_numerica, 'form_ordem_invalido')
                form_com_erro = Edita_Ordem_Form(request.POST, plano_id_super=plano_id, correcao_super='form_correcao')
                form_com_erro.fields['identificacao_numerica'].initial = ordem_objeto.identificacao_numerica
                form_com_erro.fields['identificacao_numerica'].disabled = True
                contexto['chave_form_ordem'] = form_com_erro
                return render(request, 'correcoes.html', contexto)

        return redirect('pagina_correcoes_mensagem', elemento_id=plano_id, mensagem='Sucesso')

    return redirect('dashboard')

def corrigindo_despesas(request, plano_id, ordem_assoc, codigo_ident):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola':
        ordem_objeto = get_object_or_404(Ordens, plano=plano_objeto, identificacao_numerica=ordem_assoc)
        codigo_objeto = get_object_or_404(ModeloCodigos, ordem=ordem_objeto, identificacao=codigo_ident)

        if request.method == 'POST':
            form_codigo = CodigosForm(request.POST, correcao_super='form_correcao')
            if form_codigo.is_valid():
                print('FORM CODIGO VALIDO!!!!!')
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

                # Reduz em 1 a quantidade de correções neste plano
                plano_objeto.correcoes_a_fazer -= 1
                plano_objeto.save()

                # Remove o objeto 'correcao' uma vez que ele acabou de ser corrigido.
                correcao_de_codigo_especifico = get_object_or_404(Correcoes, plano_associado=plano_objeto, ordem_associada=ordem_assoc, codigo_associado=codigo_ident)
                correcao_de_codigo_especifico.delete()

            else:
                print('FORM CODIGO INVALIDOOO')
                print(form_codigo.errors)
                contexto = pagina_correcoes(request, plano_id, ordem_objeto.identificacao_numerica, False, codigo_objeto.identificacao, 'form_despesa_invalido')
                form_com_erro = CodigosForm(request.POST, correcao_super='form_correcao')
                form_com_erro.fields['identificacao'].initial = str(ordem_objeto.identificacao_numerica) + codigo_objeto.identificacao
                form_com_erro.fields['identificacao'].label = 'Código: '
                form_com_erro.fields['identificacao'].disabled = True
                contexto['chave_form_codigo'] = form_com_erro
                return render(request, 'correcoes.html', contexto)

        return redirect('pagina_correcoes', elemento_id=plano_id)

    return redirect('dashboard')

def cria_plano(request):
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola':
        controle_form_plano = False
        form_plano = PlanoForm()
        usuario_ativo = get_object_or_404(User, pk=request.user.id)
        if request.method == 'POST':
            form_plano = PlanoForm(request.POST)
            if form_plano.is_valid():
                print('SALVOU PLANO!!!!')
                ano_form = form_plano.cleaned_data.get('ano_referencia')
                plano = Plano_de_acao.objects.create(
                    ano_referencia = ano_form,
                    usuario = usuario_ativo,
                )
                plano.save()
                return redirect('pagina_planos_de_acao_mensagem', mensagem='Criou')
            else:
                controle_form_plano = True
                print('FORM PLANO INVALIDO')
                id = request.user.id

                contexto = planos_de_acao(request, falha_novo_plano=True)
                contexto['chave_form_planos'] = form_plano
                contexto['contexto_extra_plano'] = controle_form_plano
                return render(request, 'planos_de_acao.html', contexto)

                planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=id).filter(~Q(situacao='Concluido'))

                dados = {
                'chave_planos' : planos,
                'chave_form_planos' : form_plano,
                'contexto_extra_plano' : controle_form_plano
                }

                return render(request, 'planos_de_acao.html', dados)

    return redirect('pagina_planos_de_acao')

def edita_plano(request, plano_id):
    plano = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano.alterabilidade == 'Escola':
        form_plano = PlanoForm()
        # form_plano.fields['ano_referencia'].initial = plano
        edita_plano_form = Edita_planoForm()
        # edita_plano_form.fields['ano_referencia'].initial = plano
        if request.method == 'POST':
            edita_plano_form = Edita_planoForm(request.POST)
            if edita_plano_form.is_valid():
                print('EDITOU PLANO!!!!')
                edita_ano_referencia = edita_plano_form.cleaned_data.get('ano_referencia')
                plano = get_object_or_404(Plano_de_acao, pk=plano_id)
                nome_antigo = plano.ano_referencia
                if plano.situacao != 'Em desenvolvimento':
                    checa_usuario = request.user
                    log_nome_plano_alterado(nome_antigo, edita_ano_referencia, checa_usuario, plano.id)
                plano.ano_referencia = edita_ano_referencia
                plano.save()

            else:

                controle_form_edita_plano = True
                print('FORM EDITA PLANO INVALIDO')

                checa_usuario = request.user
                id = request.user.id
                if checa_usuario.classificacao.tipo_de_acesso == 'Escola':
                    planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=id).filter(~Q(situacao='Concluido'))

                plano_selecionado = get_object_or_404(Plano_de_acao, pk=plano_id)
                plano_selecionado2 = Plano_de_acao.objects.filter(pk=plano_id)

                dados = {
                'chave_planos' : planos,
                'chave_form_planos' : form_plano,
                'chave_edita_plano_form' : edita_plano_form,
                'contexto_extra_edita_plano' : controle_form_edita_plano,
                'contexto_edicao_plano' : plano_selecionado,
                'chave_contexto_edicao_plano' : plano_selecionado2,

                }

                # return redirect('pagina_planos_de_acao_argumento', extra=controle_form_plano)
                return render(request, 'planos_de_acao.html', dados)

        return redirect('pagina_planos_de_acao_mensagem', mensagem='Editou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao')

def deleta_plano(request, elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola':
        existem_turmas_associadas = Turmas.objects.filter(plano_associado=plano)
        if existem_turmas_associadas:
            for turmas in existem_turmas_associadas:
                turmas.plano_associado.remove(plano)# Desassocia as turmas associadas a este plano.
        plano.delete()

        return redirect('pagina_planos_de_acao_mensagem', mensagem='Deletou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def publica_plano(request, elemento_id):
    from .alteracoes import atualiza_assinaturas_escola
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and captura_plano.alterabilidade == 'Escola':
        checa_usuario = request.user.last_name
        quantidade_funcionarios = get_object_or_404(Classificacao, user_id=request.user.id)
        if quantidade_funcionarios.quant_funcionarios >= 1:
            if request.method == 'POST':
                captura_plano.situacao = 'Publicado'
                captura_plano.save()
                mensagem_var = 'Publicou'

                nome_plano = captura_plano.ano_referencia
                log_plano_publicado(nome_plano, checa_usuario, captura_plano.id)

                atualiza_assinaturas_escola(captura_plano.id)
        else:
            mensagem_var = 'Sem_funcionarios'

        return redirect('pagina_planos_de_acao_mensagem', mensagem=mensagem_var)

    return redirect('pagina_planos_de_acao_mensagem', mensagem="Acesso_negado")

def autoriza_plano(request, elemento_id): #ASSINATURA
    from .alteracoes import cria_associacao, confere_assinaturas_muda_para_pronto, fia_confere_assinaturas_muda_para_pronto
    from fia.alteracoes import checa_grupo_de_autorizacao
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' or tipo_usuario == 'Funcionario':
        if captura_plano.alterabilidade == 'Desativada' or captura_plano.pre_assinatura == True:
            escola_id = captura_plano.usuario_id
            captura_escola = get_object_or_404(Classificacao, user_id=escola_id)

            captura_funcionario = get_object_or_404(Classificacao, user_id=request.user.id)
            funcionario_associado = Classificacao.objects.filter(plano_associado=captura_plano)#DE TODOS FUNCIONARIOS ASSOCIADOS A ESTE PLANO

            if any(funcionario.user_id == request.user.id for funcionario in funcionario_associado ): #se qualquer funcionario associado a ESTE PLANO tiver o mesmo ID do ATUAL. Significa que este usuário já autorizou!!
                print('Achou funcionario associado com ID igual ao atual, NADA ACONTECE')
                pass

            else: # Significa que este usuário ainda não autorizou este plano, e portanto, criamos a autorização!!
                print('Nao existe funcionario com ID igual ao atual associado a este plano, CRIANDO AUTORIZAÇÃO!!')

                # PLANO COMUM
                if not captura_plano.tipo_fia:
                    cria_associacao(request, captura_plano, captura_funcionario, elemento_id)

                # PLANO FIA
                elif captura_plano.tipo_fia:
                    modelo_fia = get_object_or_404(Modelo_fia, plano=captura_plano)
                    pode_assinar = checa_grupo_de_autorizacao(modelo_fia)
                    if pode_assinar:
                        cria_associacao(request, captura_plano, captura_funcionario, elemento_id)
                    else:
                        return redirect('pagina_planos_de_acao_mensagem', mensagem='grupo_incompleto')

            # PLANO COMUM
            if not captura_plano.tipo_fia:
                captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
                confere_assinaturas_muda_para_pronto(captura_plano, captura_escola)
                
            # PLANO FIA
            elif captura_plano.tipo_fia:
                captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
                fia_confere_assinaturas_muda_para_pronto(captura_plano)

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Assinado')
    
    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def autoriza_plano_func_sec(request, elemento_id): #ASSINATURA FUNC_SEC
    from .alteracoes import plano_inteiramente_assinado,atualiza_assinaturas_sec
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and captura_plano.alterabilidade == 'Desativada':
        escola_id = captura_plano.usuario_id
        captura_escola = get_object_or_404(Classificacao, user_id=escola_id)

        captura_funcionario = get_object_or_404(Classificacao, user_id=request.user.id)
        funcionario_associado = Classificacao.objects.filter(plano_associado=captura_plano)#DE TODOS FUNCIONARIOS ASSOCIADOS A ESTE PLANO

        if any(funcionario.user_id == request.user.id for funcionario in funcionario_associado ): #se qualquer funcionario associado a ESTE PLANO tiver o mesmo ID do ATUAL. Significa que este usuário já autorizou!!
            print('Achou funcionario associado com ID igual ao atual, NADA ACONTECE')
            pass

        else: # Significa que este usuário ainda não autorizou este plano, e portanto, criamos a autorização!!
            print('Nao existe funcionario com ID igual ao atual associado a este plano, CRIANDO AUTORIZAÇÃO!!')

            captura_funcionario.plano_associado.add(captura_plano) #salva no banco dizendo que este usuario acabou de autorizar este plano, e portanto já assinou e não precisa mais assinar. Gera um associação many-too_many.
            
            # Seta as variaveis booleanas do modelo de plano que dizem quem dos 3 acabou de assinar
            if captura_funcionario.usuario_diretor:
                captura_plano.assinatura_diretor = True
            elif captura_plano.corretor_plano == request.user:
                captura_plano.assinatura_corretor = True
            elif captura_funcionario.usuario_coordenador:
                captura_plano.assinatura_coordenador = True
            captura_plano.save()

            atualiza_assinaturas_sec(elemento_id)
            captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)

            checa_usuario = request.user.first_name
            nome_plano = captura_plano.ano_referencia
            log_plano_assinado_sec(nome_plano, checa_usuario, captura_plano.id)

            # transforma em "Inteiramente assinado" o plano caso tenha todas as assinaturas necessárias
            plano_inteiramente_assinado(captura_plano)
            
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Assinado')

        return redirect('pagina_planos_de_acao')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def envia_plano(request, elemento_id):
    if request.method == 'POST':
        captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)

        if not captura_plano.tipo_fia:
            contem_ordens = Ordens.objects.filter(plano=captura_plano) # todas as ordens do plano
            if contem_ordens: # Se plano contem ordens

                if any( elemento.inserida for elemento in contem_ordens ):# Se houver alguma ordem inserida

                    for elemento in contem_ordens:
                        if elemento.inserida:# para todas as ordens inseridas
                            contem_codigos = ModeloCodigos.objects.filter(ordem=elemento)

                            if contem_codigos:# Se  ordem inserida tiver códigos

                                if any(codigo.inserido for codigo in contem_codigos):# Se algum codigo inserido

                                    print('ACHOU ALGUM CODIGO INSERIDO!!')
                                    # PODE ENVIAR

                                else:
                                    print('NAO TEM CODIGO INSERIDO EM UMA ORDEM INSERIDA')
                                    return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_codigo')
                            else:
                                print('TEM ORDEM, MAS NAO TEM CODIGO')
                                return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_codigo')
                else:
                    print('NÃO TEM ORDEM INSERIDA!')
                    return redirect('pagina_planos_de_acao_mensagem', mensagem='Sem_ordem')
            else:
                print('NÃO TEM ORDEM!')
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

def devolve_plano(request, elemento_id):
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
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

                    if valor_pre_assinatura == True:
                        log_pre_assinatura_permitida(nome_plano, checa_usuario, captura_plano.id)

        return redirect('pagina_planos_de_acao_mensagem', mensagem='Devolveu')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def conclui_plano(request, elemento_id):
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and captura_plano.alterabilidade == 'Desativada':
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

def finaliza_plano(request, elemento_id):
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and captura_plano.alterabilidade == 'Desativada':
        if request.method == 'POST':
            checa_usuario = request.user.first_name
            captura_plano.situacao = 'Finalizado'
            captura_plano.save()

            nome_plano = captura_plano.ano_referencia
            log_plano_finalizado(nome_plano, checa_usuario, captura_plano.id)

        return redirect('pagina_planos_de_acao_mensagem', mensagem='Finalizado')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def reseta_plano(request, elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec':
        if request.method == 'POST':
            checa_usuario = request.user
            nome_usuario = checa_usuario.first_name
            if plano.situacao == 'Assinado':
                if checa_usuario.classificacao.tipo_de_acesso == 'Secretaria' or checa_usuario.classificacao.tipo_de_acesso == 'Func_sec':
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
                        plano.save()

                        log_plano_resetado(plano.ano_referencia, nome_usuario, elemento_id)

                        if not plano.tipo_fia:
                            return redirect('chamando_acao_plano_mensagem', elemento_id=elemento_id, mensagem='Sucesso')
                        else:
                            return redirect('chamando_documento_fia_mensagem', elemento_id=elemento_id, mensagem='sucesso2')
                    else:
                        return redirect('pagina_planos_de_acao_mensagem', mensagem='reset_corretor')

    return redirect('chamando_acao_plano_mensagem', elemento_id=elemento_id, mensagem='Acesso_negado')

def concluir_sugestao(request, elemento_id, documento=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    
    if request.method == 'POST':
        plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
        ordens_iteravel = Ordens.objects.filter(plano=plano_objeto)
        if documento == 'acao':
            if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
                for ordem in ordens_iteravel:
                    if ordem.inserida:
                        if ordem.prazo_execucao_inicial == None or ordem.prazo_execucao_final == None:
                            print('erro concluir')
                            return redirect('chamando_acao_plano_mensagem', elemento_id=elemento_id, mensagem='Datas')
            
                plano_objeto.pre_analise_acao = True
                plano_objeto.save()

                return redirect('pagina_planos_de_acao_mensagem', mensagem='Sucesso')
            else:
                return redirect('chamando_acao_plano_mensagem', elemento_id=elemento_id, mensagem='Nao_corretor')

        elif documento == 'despesa':
            if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
                plano_objeto.pre_analise_despesa = True
                plano_objeto.save()

                return redirect('pagina_planos_de_acao_mensagem', mensagem='Sucesso')
            else:
                return redirect('chamando_despesa_plano_mensagem', elemento_id=elemento_id, mensagem='Nao_corretor')
        
        elif documento == 'fia':
            if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
                plano_objeto.pre_analise_fia = True
                plano_objeto.save()

                return redirect('pagina_planos_de_acao_mensagem', mensagem='Sucesso')
            else:
                return redirect('chamando_despesa_plano_mensagem', elemento_id=elemento_id, mensagem='Nao_corretor')

    return redirect('pagina_planos_de_acao')
    
def atribui_corretor(request, elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano.alterabilidade == 'Secretaria':
        if plano.corretor_plano == None:
            id1 = request.user.id
            usuario = get_object_or_404(User, pk=id1)
            plano.corretor_plano = usuario
            print(plano.corretor_plano)
            plano.save()

            checa_corretor = request.user.first_name
            checa_usuario = request.user.first_name
            plano_id = plano.id
            log_atribuiu_corretor(checa_corretor, checa_usuario, plano_id)

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Atribuiu')
        else:
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Ja_possui')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao')
        
def altera_corretor(request, elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec':
        if plano.alterabilidade == 'Desativada':
            return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado_situacao')
        else:
            if request.method == 'POST':
                plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
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

                checa_usuario = request.user.first_name
                plano_id = plano.id
                if corretor == None:
                    checa_corretor = corretor_antigo.first_name
                    log_removeu_corretor(checa_corretor, checa_usuario, plano_id)
                else:
                    checa_corretor = corretor_objeto.first_name
                    log_alterou_corretor(checa_corretor, checa_usuario, plano_id)
        
        return redirect('pagina_planos_de_acao_mensagem', mensagem='Alterou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def quebra_de_linha(request, plano_id):
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

        return redirect('chamando_acao_plano_mensagem_q_linha', elemento_id=plano_id, mensagem=var_mensagem, q_linha='q_linha')
    
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

        return redirect('chamando_despesa_mensagem_q_linha', elemento_id=plano_id, mensagem=var_mensagem, q_linha='q_linha')

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

        return redirect('chamando_documento_fia_mensagem_q_linha', elemento_id=plano_id, mensagem=var_mensagem, q_linha='q_linha')

    elif 'extra_fiaid' in request.GET:
        extra_fiaid = int(request.GET.get('extra_fiaid',''))
        valor_quebra_de_linha = int(request.GET.get('valor',''))
        extra_fia_objeto = get_object_or_404(Extra_fia, pk=extra_fiaid)
        extra_fia_objeto.quebra_de_linha = valor_quebra_de_linha
        extra_fia_objeto.save()
        if request.method == 'GET ' and 'postprint' in request.GET:
            var_mensagem = 'insere' # Não deve mostrar mensagem alguma
        else:
            var_mensagem = 'Sucesso3'

        return redirect('chamando_documento_fia_mensagem_q_linha', elemento_id=plano_id, mensagem=var_mensagem, q_linha='q_linha')

def teste(request):
    pass

# AQUI É ONDE PARTE DAS INFORMAÇÕES DOS PLANOS SERÃO SALVAS PERMANENTEMENTE, SEM A OPÇÃO DE SEREM ALTERADAS!!
def aprova_plano(request, elemento_id):
    captura_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
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

            return redirect('pagina_planos_de_acao_mensagem', mensagem='Aprovou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def adiciona_remove_turma(request, plano_id, turma_id):
    captura_plano = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and captura_plano.alterabilidade == 'Escola':

        if turma_id: # Turma selecionada
            turma_selecionada  = get_object_or_404(Turmas, pk=turma_id)
            turmas_associadas = Turmas.objects.filter(plano_associado=captura_plano).filter(user=captura_plano.usuario)

            if turmas_associadas: # Se existem turmas associadas a este plano
                if any(turma == turma_selecionada for turma in turmas_associadas): #Se alguma turma associada for a selecionada
                    turma_selecionada.plano_associado.remove(captura_plano) # Remove associação do plano à turma selecionada
                else:
                    turma_selecionada.plano_associado.add(captura_plano) # Cria associação desta turma com o plano
            else: # Se nenhuma das turmas associadas for a turma selecionada
                turma_selecionada.plano_associado.add(captura_plano) # Cria associação desta turma com o plano
                        
        if not captura_plano.tipo_fia:
            return redirect('chamando_despesa_plano_mensagem', elemento_id=plano_id, mensagem='Sucesso')
        else:
            return redirect('chamando_documento_fia_mensagem', elemento_id=plano_id, mensagem='Sucesso')
    if not captura_plano.tipo_fia:
        return redirect('chamando_despesa_plano_mensagem', elemento_id=plano_id, mensagem='Acesso_negado_situacao')
    else:
        return redirect('chamando_documento_fia_mensagem', elemento_id=plano_id, mensagem='not_allowed')