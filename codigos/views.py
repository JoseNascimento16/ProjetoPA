from Ordens.models import Ordens
from django.shortcuts import render, redirect, get_object_or_404
from codigos.forms import CodigosForm
from codigos.models.codigos import ModeloCodigos

# Create your views here.

### VIEWS TESTADAS ###

def deleta_codigo(request, **kwargs):
    from plano_de_acao.alteracoes import ordem_atualiza_rowspan_e_codigos_inseridos
    ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
    plano_objeto = ordem.plano
    tipo_usuario = request.user.groups.get().name
    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola':
        codigo = get_object_or_404(ModeloCodigos, pk=kwargs['elemento_id'])
        codigo.delete()
        
        ordem_atualiza_rowspan_e_codigos_inseridos(ordem)
        
        return redirect('entra_na_ordem_mensagem', ordem_id=kwargs['ordem_id'], mensagem='Deletou')

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def abre_codigo(request, **kwargs):
    edita_codigo = False
    abre_novo_codigo = False
    controle = True
    instancia_codigo = ''
    instancia_ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
    ordem2 = Ordens.objects.filter(pk=kwargs['ordem_id'])
    codigo = ModeloCodigos.objects.order_by('identificacao').filter(ordem=instancia_ordem)
    plano_objeto = instancia_ordem.plano
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola':

        if kwargs.get('abre_codigo'):
            abre_novo_codigo = True
            form = CodigosForm()

        elif kwargs.get('codigo_id'):
            edita_codigo = True
            instancia_ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
            instancia_codigo = get_object_or_404(ModeloCodigos, pk=kwargs['codigo_id'])
            
            form = CodigosForm()
            form.fields['identificacao'].initial = instancia_codigo.identificacao
            form.fields['especificacao'].initial = instancia_codigo.especificacao
            form.fields['justificativa'].initial = instancia_codigo.justificativa
            form.fields['embalagem'].initial = instancia_codigo.embalagem
            form.fields['quantidade'].initial = instancia_codigo.quantidade
            form.fields['preco_unitario'].initial = instancia_codigo.preco_unitario
            form.fields['tipo_produto'].initial = instancia_codigo.tipo_produto
            

        dados_a_exibir = {

            'chave_ordens' : instancia_ordem,
            'chave_ordens2' : ordem2,
            'chave_codigos' : codigo,
            'chave_instancia_codigos': instancia_codigo,
            'form_codigos' : form,
            'contexto_extra': controle,
            'chave_abre_novo_codigo': abre_novo_codigo,
            'chave_abre_edita_codigo': edita_codigo,
        }
        return render(request, 'ordem.html', dados_a_exibir)

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def novo_codigo(request, **kwargs): # Criação de novos codigos
    controle = False
    abre_novo_codigo = False
    instancia_ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
    id_da_ordem = instancia_ordem.id
    ordem2 = Ordens.objects.filter(pk=kwargs['ordem_id'])
    form = CodigosForm()
    codigo = ModeloCodigos.objects.order_by('identificacao').filter(ordem=instancia_ordem)
    plano_objeto = instancia_ordem.plano
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola' and plano_objeto.tipo_fia == False:
        if request.method == 'POST':
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

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')

def edita_codigo(request, **kwargs):
    instancia_ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
    plano_objeto = instancia_ordem.plano
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola' and plano_objeto.alterabilidade == 'Escola':
        if request.method == 'POST':
            edita_codigo_form = CodigosForm(request.POST, ordem_id=kwargs['ordem_id'], edita_super='Sim')
            if edita_codigo_form.is_valid():
                edita_identificacao = edita_codigo_form.cleaned_data.get('identificacao')
                edita_especificacao = edita_codigo_form.cleaned_data.get('especificacao')
                edita_justificativa = edita_codigo_form.cleaned_data.get('justificativa')
                edita_embalagem = edita_codigo_form.cleaned_data.get('embalagem')
                edita_quantidade = edita_codigo_form.cleaned_data.get('quantidade')
                edita_preco_unitario = edita_codigo_form.cleaned_data.get('preco_unitario')
                edita_tipo_produto = edita_codigo_form.cleaned_data.get('tipo_produto')
                codigo = get_object_or_404(ModeloCodigos, pk=kwargs['codigo_id'])
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

                return redirect('entra_na_ordem_mensagem', ordem_id=kwargs['ordem_id'], mensagem='Editou')

            else:
                # print(edita_codigo_form.errors)
                controle = True
                abre_novo_codigo = False
                edita_codigo = True
                instancia_ordem = get_object_or_404(Ordens, pk=kwargs['ordem_id'])
                instancia_codigo = get_object_or_404(ModeloCodigos, pk=kwargs['codigo_id'])
                ordem2 = Ordens.objects.filter(pk=kwargs['ordem_id'])
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

    return redirect('pagina_planos_de_acao_mensagem', mensagem='Acesso_negado')