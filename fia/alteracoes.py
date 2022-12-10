from plano_de_acao.models import Correcoes, Plano_de_acao
from .models import Extra_fia, Modelo_fia
from django.shortcuts import get_object_or_404
from fia.forms import ModeloFiaForm
from usuarios.models import Classificacao
from django import forms

def atualiza_valor_total_fia(var_total_item, pk_fia):
    valor_final_fia = 0
    modelo_fia = get_object_or_404(Modelo_fia, pk=pk_fia)
    ordens_extras = Extra_fia.objects.filter(fia_matriz=modelo_fia)
    if ordens_extras:
        for item in ordens_extras:
            valor_final_fia += item.valor_total_item
        valor_final_fia += var_total_item
    else:
        valor_final_fia = var_total_item

    modelo_fia.valor_total_fia = valor_final_fia
    modelo_fia.save()

def atualiza_total_correcoes(plano_id):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    correcoes_do_plano = Correcoes.objects.filter(plano_associado=plano_objeto)
    plano_objeto.correcoes_a_fazer = len(correcoes_do_plano)
    plano_objeto.save()

def salva_form_modelo_fia(form_modelo_fia, modelo_fia):
    var_cx_escolar = form_modelo_fia.cleaned_data.get('nome_caixa_escolar')
    var_ano_exercicio = form_modelo_fia.cleaned_data.get('ano_exercicio')
    var_discriminacao = form_modelo_fia.cleaned_data.get('discriminacao')
    var_preco_unitario_item = form_modelo_fia.cleaned_data.get('preco_unitario_item')
    var_justificativa = form_modelo_fia.cleaned_data.get('justificativa')
    modelo_fia.nome_caixa_escolar = var_cx_escolar
    modelo_fia.ano_exercicio = var_ano_exercicio
    modelo_fia.discriminacao = var_discriminacao
    modelo_fia.quantidade = 1
    modelo_fia.preco_unitario_item = var_preco_unitario_item
    modelo_fia.justificativa = var_justificativa

    var_total_item = 1 * var_preco_unitario_item
    modelo_fia.valor_total_item = var_total_item

    modelo_fia.save()

    return modelo_fia.valor_total_item

def salva_form_extra_fia(form_extra_fia, extra_fia):
    # var_valor_numerico = form_extra_fia.cleaned_data.get('valor_numerico')
    var_discriminacao = form_extra_fia.cleaned_data.get('discriminacao')
    var_quantidade = form_extra_fia.cleaned_data.get('quantidade')
    var_preco_unitario_item = form_extra_fia.cleaned_data.get('preco_unitario_item')
    var_justificativa = form_extra_fia.cleaned_data.get('justificativa')
    var_valor_total_item = var_quantidade * var_preco_unitario_item
    
    # extra_fia.valor_numerico=var_valor_numerico
    extra_fia.discriminacao=var_discriminacao
    extra_fia.quantidade=var_quantidade
    extra_fia.preco_unitario_item=var_preco_unitario_item
    extra_fia.valor_total_item=var_valor_total_item
    extra_fia.justificativa=var_justificativa
    
    extra_fia.save()

def remove_assinatura_membro(plano_objeto, membro):
    from plano_de_acao.alteracoes import atualiza_assinaturas_escola
    assinaturas = plano_objeto.classificacao_set.all()
    for item in assinaturas:
        if item.user == membro:
            item.plano_associado.remove(plano_objeto)

            atualiza_assinaturas_escola(plano_objeto.id)


def checa_grupo_de_autorizacao(modelo_fia):
    # Checa se um plano fia já tem todos os membros definidos
    if modelo_fia.membro_colegiado_1 and modelo_fia.membro_colegiado_2 and modelo_fia.tecnico_responsavel:
        return True
    return False

def checa_se_pode_assinar_escola_fia(request, modelo_fia):
    # Checa se o funcionário faz parte do grupo de autorização cadastrado
    # Escola: 1 Diretor, 1 técnico, 2 membros do colegiado
    # SUPROT: 1 Corretor do plano, 1 coordenador, 1 Diretor suprot
    lista_de_autorizados = []
    lista_de_autorizados.append(modelo_fia.membro_colegiado_1)
    lista_de_autorizados.append(modelo_fia.membro_colegiado_2)
    lista_de_autorizados.append(modelo_fia.plano.escola.diretor)
    if any(request.user == usuario for usuario in lista_de_autorizados):
        return True
    return False

def renderiza_form_fia(plano_objeto, modelo_fia_objeto):
    membro1=''
    membro2=''
    ModeloFiaForm.base_fields['membro1'] = forms.ModelChoiceField(
        queryset=Classificacao.objects.order_by('-user').filter(escola=plano_objeto.escola).filter(tipo_de_acesso='Funcionario').filter(cargo_herdado='Membro do colegiado'),
        empty_label="------------",
        label='Colegiado escolar 1:',
        required=False,
        widget=forms.Select)
    ModeloFiaForm.base_fields['membro2'] = forms.ModelChoiceField(
        queryset=Classificacao.objects.order_by('-user').filter(escola=plano_objeto.escola).filter(tipo_de_acesso='Funcionario').filter(cargo_herdado='Membro do colegiado'),
        empty_label="------------",
        label='Colegiado escolar 2:',
        required=False,
        widget=forms.Select)

    # form_fia = ModeloFiaForm()
    
    if modelo_fia_objeto.membro_colegiado_1:
        membro1 = modelo_fia_objeto.membro_colegiado_1.id
    if modelo_fia_objeto.membro_colegiado_2:
        membro2 = modelo_fia_objeto.membro_colegiado_2.id

    form_fia = ModeloFiaForm(initial={
        'nome_caixa_escolar': modelo_fia_objeto.nome_caixa_escolar,
        'ano_exercicio': modelo_fia_objeto.ano_exercicio,
        'discriminacao': modelo_fia_objeto.discriminacao,
        'preco_unitario_item': modelo_fia_objeto.preco_unitario_item,
        'justificativa': modelo_fia_objeto.justificativa,
        'membro1': membro1,
        'membro2': membro2,
        'tecnico_responsavel': modelo_fia_objeto.tecnico_responsavel,
        })
    form_fia.fields['membro1'].required = False
    form_fia.fields['membro2'].required = False

    return form_fia