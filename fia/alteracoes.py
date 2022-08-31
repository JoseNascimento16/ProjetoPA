from plano_de_acao.models import Correcoes, Plano_de_acao
from .models import Extra_fia, Modelo_fia
from django.shortcuts import get_object_or_404

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

# Checa se um plano fia já tem todos os membros definidos
def checa_grupo_de_autorizacao(modelo_fia):
    if modelo_fia.membro_colegiado_1 and modelo_fia.membro_colegiado_2 and modelo_fia.tecnico_responsavel:
        return True
    else:
        return False
