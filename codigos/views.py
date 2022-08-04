from Ordens.models import Ordens
from django.shortcuts import render, redirect, get_object_or_404
from codigos.forms import CodigosForm
from codigos.models.codigos import ModeloCodigos

# Create your views here.

def deleta_codigo(request, elemento_id, ordem_id):
    ordem = get_object_or_404(Ordens, pk=ordem_id)
    plano_objeto = ordem.plano
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola':
        codigo = get_object_or_404(ModeloCodigos, pk=elemento_id)
        codigo.delete()
        
        ordem.codigos_inseridos -= 1
        ordem.ordem_rowspan -= 1
        ordem.save()
        
        return redirect('entra_na_ordem_mensagem', ordem_id=ordem_id, mensagem='Deletou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def abre_codigo(request, ordem_id, codigo_id='',abre_codigo=''):
    instancia_ordem = get_object_or_404(Ordens, pk=ordem_id)
    plano_objeto = instancia_ordem.plano
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola':
        if abre_codigo:
            controle = True
            abre_novo_codigo = True
            edita_codigo = False
            ordem2 = Ordens.objects.filter(pk=ordem_id)
            form = CodigosForm()
            codigo = ModeloCodigos.objects.order_by('identificacao').filter(ordem=instancia_ordem)

            dados_a_exibir = {

                'chave_ordens' : instancia_ordem,
                'chave_ordens2' : ordem2,
                'chave_codigos' : codigo,
                'form_codigos' : form,
                'contexto_extra': controle,
                'chave_abre_novo_codigo': abre_novo_codigo,
                'chave_abre_edita_codigo': edita_codigo,
            }
            return render(request, 'ordem.html', dados_a_exibir)

        else:

            print('ABRIU MODAL EDICAO CODIGO')
            controle = True
            abre_novo_codigo = False
            edita_codigo = True
            instancia_ordem = get_object_or_404(Ordens, pk=ordem_id)
            instancia_codigo = get_object_or_404(ModeloCodigos, pk=codigo_id)
            ordem2 = Ordens.objects.filter(pk=ordem_id)
            edita_form_codigos = CodigosForm()
            codigo = ModeloCodigos.objects.order_by('identificacao').filter(ordem=instancia_ordem.id)
            # cria_codigo(request, instancia_ordem, controle, id_da_ordem)

            edita_form_codigos.fields['identificacao'].initial = instancia_codigo.identificacao
            edita_form_codigos.fields['especificacao'].initial = instancia_codigo.especificacao
            edita_form_codigos.fields['justificativa'].initial = instancia_codigo.justificativa
            edita_form_codigos.fields['embalagem'].initial = instancia_codigo.embalagem
            edita_form_codigos.fields['quantidade'].initial = instancia_codigo.quantidade
            edita_form_codigos.fields['preco_unitario'].initial = instancia_codigo.preco_unitario
            edita_form_codigos.fields['tipo_produto'].initial = instancia_codigo.tipo_produto
            

            dados_a_exibir = {

                'chave_ordens' : instancia_ordem,
                'chave_ordens2' : ordem2,
                'chave_codigos' : codigo,
                'chave_instancia_codigos': instancia_codigo,
                'form_codigos' : edita_form_codigos,
                'contexto_extra': controle,
                'chave_abre_novo_codigo': abre_novo_codigo,
                'chave_abre_edita_codigo': edita_codigo,
            }
            return render(request, 'ordem.html', dados_a_exibir)

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def novo_codigo(request, ordem_id, variavel): # Criação de novos codigos
    controle = False
    instancia_ordem = get_object_or_404(Ordens, pk=ordem_id)
    id_da_ordem = instancia_ordem.id
    ordem2 = Ordens.objects.filter(pk=ordem_id)
    form = CodigosForm()
    codigo = ModeloCodigos.objects.order_by('identificacao').filter(ordem=instancia_ordem)
    plano_objeto = instancia_ordem.plano
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola' and plano_objeto.tipo_fia == False:
        if request.method == 'POST':
            controle = False
            form = CodigosForm(request.POST, ordem_id=id_da_ordem)
            if form.is_valid():
                valor_identificacao = request.POST['identificacao']
                valor_maiusculo = valor_identificacao.upper()
                instancia = form.save(commit=False)
                instancia.ordem = instancia_ordem
                instancia.identificacao = valor_maiusculo
                if instancia.tipo_produto == 'Capital':
                    instancia.preco_total_capital = instancia.quantidade * instancia.preco_unitario
                    instancia.preco_total_custeio = 0
                elif instancia.tipo_produto == 'Custeio':
                    instancia.preco_total_custeio = instancia.quantidade * instancia.preco_unitario
                    instancia.preco_total_capital = 0
                instancia.save()
                
                return redirect('entra_na_ordem_mensagem', ordem_id=id_da_ordem, mensagem='Criou')
            else:
                controle = True
                abre_novo_codigo = True

                dados_a_exibir = {

                    'chave_ordens' : instancia_ordem,
                    'chave_ordens2' : ordem2,
                    'chave_codigos' : codigo,
                    'form_codigos' : form,
                    'contexto_extra': controle,
                    'chave_abre_novo_codigo': abre_novo_codigo,
                }
                return render(request, 'ordem.html', dados_a_exibir)

        dados_a_exibir = {

            'chave_ordens' : instancia_ordem,
            'chave_ordens2' : ordem2,
            'chave_codigos' : codigo,
            'form_codigos' : form,
            'contexto_extra': controle
        }
        return render(request, 'ordem.html', dados_a_exibir)

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def edita_codigo(request, ordem_id, codigo_id):
    instancia_ordem = get_object_or_404(Ordens, pk=ordem_id)
    plano_objeto = instancia_ordem.plano
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola':

        if request.method == 'POST':
            edita_codigo_form = CodigosForm(request.POST, ordem_id=ordem_id, edita_super='Sim')
            if edita_codigo_form.is_valid():
                edita_identificacao = edita_codigo_form.cleaned_data.get('identificacao')
                edita_especificacao = edita_codigo_form.cleaned_data.get('especificacao')
                edita_justificativa = edita_codigo_form.cleaned_data.get('justificativa')
                edita_embalagem = edita_codigo_form.cleaned_data.get('embalagem')
                edita_quantidade = edita_codigo_form.cleaned_data.get('quantidade')
                edita_preco_unitario = edita_codigo_form.cleaned_data.get('preco_unitario')
                edita_tipo_produto = edita_codigo_form.cleaned_data.get('tipo_produto')
                codigo = get_object_or_404(ModeloCodigos, pk=codigo_id)
                codigo.identificacao = edita_identificacao.upper()
                codigo.especificacao = edita_especificacao
                codigo.justificativa = edita_justificativa
                codigo.embalagem = edita_embalagem
                codigo.quantidade = edita_quantidade
                codigo.preco_unitario = edita_preco_unitario
                codigo.tipo_produto = edita_tipo_produto

                if codigo.tipo_produto == 'Capital':
                    codigo.preco_total_capital = codigo.quantidade * codigo.preco_unitario
                    codigo.preco_total_custeio = 0
                elif codigo.tipo_produto == 'Custeio':
                    codigo.preco_total_custeio = codigo.quantidade * codigo.preco_unitario
                    codigo.preco_total_capital = 0

                codigo.save()

            else:
                controle = True
                abre_novo_codigo = False
                edita_codigo = True
                instancia_ordem = get_object_or_404(Ordens, pk=ordem_id)
                instancia_codigo = get_object_or_404(ModeloCodigos, pk=codigo_id)
                ordem2 = Ordens.objects.filter(pk=ordem_id)
                codigo = ModeloCodigos.objects.order_by('identificacao').filter(ordem=instancia_ordem.id)

                dados_a_exibir = {

                    'chave_ordens' : instancia_ordem,
                    'chave_ordens2' : ordem2,
                    'chave_codigos' : codigo,
                    'chave_instancia_codigos': instancia_codigo,
                    'form_codigos' : edita_codigo_form,
                    'contexto_extra': controle,
                    'chave_abre_novo_codigo': abre_novo_codigo,
                    'chave_abre_edita_codigo': edita_codigo,
                }
                return render(request, 'ordem.html', dados_a_exibir)

        return redirect('entra_na_ordem_mensagem', ordem_id=ordem_id, mensagem='Editou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')