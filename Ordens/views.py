from codigos.models import codigos
from codigos.models.codigos import ModeloCodigos
from plano_de_acao.models import Plano_de_acao
from plano_de_acao.views import acao_plano
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ordens
from codigos.forms import CodigosForm
from Ordens.forms import OrdemForm, Edita_Ordem_Form, Cadastra_datas_Ordem_Form
from plano_de_acao.views import plano
from django.utils import timezone

# Create your views here.



##### VIEWS TESTADAS #####
def ordem(request, ordem_id, mensagem=''): # Acesso aos códigos de uma ordem
    instancia_ordem = get_object_or_404(Ordens, pk=ordem_id)
    tipo_usuario = request.user.groups.get().name
    plano_objeto = instancia_ordem.plano
    
    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola' and plano_objeto.tipo_fia == False:
        if mensagem == 'Criou':
            messages.success(request, 'Código criado com sucesso!')
        elif mensagem == 'Deletou':
            messages.success(request, 'Código excluído com sucesso!')
        elif mensagem == 'Editou':
            messages.success(request, 'Código alterado com sucesso!')

        controle = False
        
        ordem2 = Ordens.objects.filter(pk=ordem_id)
        form = CodigosForm()
        codigo = ModeloCodigos.objects.order_by('identificacao').filter(ordem=instancia_ordem)

        dados_a_exibir = {

            'chave_ordens' : instancia_ordem,
            'chave_ordens2' : ordem2,
            'chave_codigos' : codigo,
            'form_codigos' : form,
            'contexto_extra': controle,
            'chave_tipo_usuario' : tipo_usuario,
        }
        return render(request, 'ordem.html', dados_a_exibir)
    else:
        return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def cria_ordem(request, **kwargs):
    abre_nova_ordem = False
    form_ordem = OrdemForm()
    instancia_plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Diretor_escola' and instancia_plano.alterabilidade == 'Escola' and instancia_plano.tipo_fia == False:
        if request.method == 'POST':
            form_ordem = OrdemForm(request.POST, plano_id_super=kwargs['plano_id'])
            if form_ordem.is_valid():
                ident_form = form_ordem.cleaned_data.get('identificacao_numerica')
                descr_form = form_ordem.cleaned_data.get('descricao_do_problema')
                # inic_form = form_ordem.cleaned_data.get('prazo_execucao_inicial')
                # fin_form = form_ordem.cleaned_data.get('prazo_execucao_final')
                result_form = form_ordem.cleaned_data.get('resultados_esperados')
                ordem = Ordens.objects.create(
                    plano = instancia_plano,
                    identificacao_numerica = ident_form,
                    descricao_do_problema = descr_form,
                    # prazo_execucao_inicial = None,
                    # prazo_execucao_final = None,
                    resultados_esperados = result_form,
                    data_de_criação = timezone.now()
                ) #nao precisei cadastrar os outros campos que existem no modelo de ordens, pois eles tem valor default que são preenchidos automaticamente quando uma ordem é criada.
                ordem.save()
                return redirect('chamando_1_plano_mensagem', plano_id=kwargs['plano_id'], mensagem='Criou')
            else:
                contexto = plano(request, plano_id=kwargs['plano_id'], contx_cria_ordem=True)
                contexto['chave_form_ordem'] = form_ordem
                contexto['chave_abre_nova_ordem'] = True
                return render(request, 'plano.html', contexto)

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def deleta_ordem(request, **kwargs):
    instancia_plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Diretor_escola' and instancia_plano.alterabilidade == 'Escola' and instancia_plano.tipo_fia == False:
        ordem = get_object_or_404(Ordens, pk=kwargs['elemento_id'])
        ordem.delete()
        
        return redirect('chamando_1_plano_mensagem', plano_id=kwargs['plano_id'], mensagem='Deletou')
    
    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def edita_ordem(request, **kwargs):
    instancia_plano = get_object_or_404(Plano_de_acao, pk=kwargs['plano_id'])
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Diretor_escola' and instancia_plano.alterabilidade == 'Escola':
        edita_ordem_form = OrdemForm()
        if request.method == 'POST':
            edita_ordem_form = OrdemForm(request.POST, plano_id_super=kwargs['plano_id'], ordem_id_super=kwargs['ordem_id'])
            if edita_ordem_form.is_valid():
                edita_identificacao_numerica = edita_ordem_form.cleaned_data.get('identificacao_numerica')
                edita_descricao_do_problema = edita_ordem_form.cleaned_data.get('descricao_do_problema')
                # edita_prazo_execucao_inicial = edita_ordem_form.cleaned_data.get('prazo_execucao_inicial')
                # edita_prazo_execucao_final = edita_ordem_form.cleaned_data.get('prazo_execucao_final')
                edita_resultados_esperados = edita_ordem_form.cleaned_data.get('resultados_esperados')
                ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
                ordem.identificacao_numerica = edita_identificacao_numerica
                ordem.descricao_do_problema = edita_descricao_do_problema
                # ordem.prazo_execucao_inicial = edita_prazo_execucao_inicial
                # ordem.prazo_execucao_final = edita_prazo_execucao_final
                ordem.resultados_esperados = edita_resultados_esperados
                ordem.save()
                return redirect('chamando_1_plano_mensagem', plano_id=kwargs['plano_id'], mensagem='Editou')

            else:
                ordem_objeto = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
                contexto = plano(request, plano_id=kwargs['plano_id'], contx_edita_ordem=True)
                contexto['chave_form_ordem'] = edita_ordem_form
                contexto['chave_ordens'] = ordem_objeto
                contexto['chave_abre_modal_edicao'] = True
                contexto['chave_insere_form_edita_ordem'] = True
                return render(request, 'plano.html', contexto)

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def cadastra_data(request, elemento_id, ordem_id, **kwargs):
    objeto_plano = get_object_or_404(Plano_de_acao, pk=elemento_id)
    ordem = get_object_or_404(Ordens, pk=ordem_id)
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Func_sec' and objeto_plano.alterabilidade == 'Secretaria':
        if request.method == 'POST':
            cadastra_datas_form = Cadastra_datas_Ordem_Form(request.POST)
            
            if cadastra_datas_form.is_valid():
                edita_prazo_execucao_inicial = cadastra_datas_form.cleaned_data.get('prazo_execucao_inicial')
                edita_prazo_execucao_final = cadastra_datas_form.cleaned_data.get('prazo_execucao_final')
                ordem.prazo_execucao_inicial = edita_prazo_execucao_inicial
                ordem.prazo_execucao_final = edita_prazo_execucao_final
                ordem.save()
                return redirect('chamando_acao_plano', elemento_id=elemento_id)

            else:
                erro_form_datas = True
                chama_acao_plano = acao_plano(request, elemento_id=elemento_id, ordem_id=ordem_id, contx_ordem=True) #contexto puxado da funcao acao_plano nas views de plano_de_acao
                chama_acao_plano['chave_form_datas'] = cadastra_datas_form
                chama_acao_plano['chave_erro_form_datas'] = erro_form_datas
                return render(request, 'acao-visualizacao.html', chama_acao_plano)

    return redirect('chamando_acao_plano_mensagem', elemento_id=elemento_id, mensagem='Acesso_negado')