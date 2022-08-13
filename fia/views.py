from webbrowser import get
from django.shortcuts import get_object_or_404, redirect, render
from django import forms
from fia.forms import ModeloFiaForm, OrdemExtraForm
from fia.models import Modelo_fia, Extra_fia
import plano_de_acao
from plano_de_acao.forms import Correcao_FiaForm, FiaForm
from django.contrib.auth.models import User
from plano_de_acao.models import Correcoes, Plano_de_acao
from django.db.models import Q
from django.contrib import messages
from plano_de_acao.views import pagina_correcoes
from usuarios.models import Classificacao, Turmas # Turmas_plano

# Create your views here.

def cria_fia(request): #CRIA UM PLANO TIPO FIA
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola':
        controle_form_fia = False
        form_fia = FiaForm()
        usuario_ativo = get_object_or_404(User, pk=request.user.id)
        if request.method == 'POST':
            form_fia = FiaForm(request.POST)
            if form_fia.is_valid():
                print('SALVOU FIA!!!!')
                ano_form = form_fia.cleaned_data.get('ano_referencia')
                plano = Plano_de_acao.objects.create(
                    ano_referencia = ano_form,
                    usuario = usuario_ativo,
                    tipo_fia = True
                )
                plano.save() # GERA SIGNAL DE CRIAÇÃO DE MODELO_FIA

                return redirect('pagina_planos_de_acao_mensagem', mensagem='Criou')
            else:
                controle_form_fia = True
                print('FORM PLANO INVALIDO')
                id = request.user.id

                planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=id).filter(~Q(situacao='Concluido'))

                dados = {
                'chave_planos' : planos,
                'chave_form_fia' : form_fia,
                'contexto_extra_fia' : controle_form_fia
                }

                return render(request, 'planos_de_acao.html', dados)

    return redirect('pagina_planos_de_acao')

def documento_fia(request, elemento_id, mensagem='', reabreform_modelo_fia='', abreform_extra_criacao='', abreform_extra_edicao='', reabreform_extra='', ordem_extra_id='', abre_correcao=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    # modelo_fia_objeto = get_object_or_404(Modelo_fia, plano=plano_objeto)
    modelo_fia_query = Modelo_fia.objects.filter(plano=plano_objeto)
    if modelo_fia_query.exists():
        for item in modelo_fia_query:
            modelo_fia_objeto = get_object_or_404(Modelo_fia, plano=item.plano)
    else: #FORÇA A CRIAÇÃO DE UM MODELO_FIA PARA ESTE PLANO CASO NÃO EXISTA POR ALGUM MOTIVO
        plano_objeto.forca_criacao_modelo_fia = True
        plano_objeto.save() #GERA UM SIGNALS PARA CRIAÇÃO DO MODELO_FIA
        modelo_fia_objeto = get_object_or_404(Modelo_fia, plano=plano_objeto)

    ordens_extras = Extra_fia.objects.order_by('valor_numerico').filter(fia_matriz=modelo_fia_objeto)
    modo_edicao = False
    var_plano_pre_aprovado = False
    ordem_extra_objeto = ''
    lista_ordens_fia = []
    lista_ordens_com_correcao = []
    form_extra_fia = OrdemExtraForm()
    tipo_usuario = request.user.classificacao.tipo_de_acesso

    ModeloFiaForm.base_fields['membro1'] = forms.ModelChoiceField(
        queryset=Classificacao.objects.order_by('-user').filter(matriz=plano_objeto.usuario.last_name).filter(tipo_de_acesso='Funcionario').filter(cargo_herdado='Membro do colegiado'),
        empty_label="------------",
        label='Colegiado escolar 1:',
        required=False,
        widget=forms.Select)
    ModeloFiaForm.base_fields['membro2'] = forms.ModelChoiceField(
        queryset=Classificacao.objects.order_by('-user').filter(matriz=plano_objeto.usuario.last_name).filter(tipo_de_acesso='Funcionario').filter(cargo_herdado='Membro do colegiado'),
        empty_label="------------",
        label='Colegiado escolar 2:',
        required=False,
        widget=forms.Select)

    form_fia = ModeloFiaForm()
    
    form_fia.fields['nome_caixa_escolar'].initial = modelo_fia_objeto.nome_caixa_escolar
    form_fia.fields['ano_exercicio'].initial = modelo_fia_objeto.ano_exercicio
    form_fia.fields['discriminacao'].initial = modelo_fia_objeto.discriminacao
    # form_fia.fields['quantidade'].initial = modelo_fia_objeto.quantidade
    if modelo_fia_objeto.preco_unitario_item == 0:
        form_fia.fields['preco_unitario_item'].initial = ''
    else:
        form_fia.fields['preco_unitario_item'].initial = modelo_fia_objeto.preco_unitario_item
    form_fia.fields['justificativa'].initial = modelo_fia_objeto.justificativa
    form_fia.fields['membro1'].required = False
    form_fia.fields['membro2'].required = False

    form_extra_fia.fields['valor_numerico'].initial = ''
    form_extra_fia.fields['quantidade'].initial = ''

    if ordem_extra_id:
        modo_edicao = True
        ordem_extra_objeto = get_object_or_404(Extra_fia, pk=ordem_extra_id)
        form_extra_fia.fields['valor_numerico'].initial = ordem_extra_objeto.valor_numerico
        form_extra_fia.fields['discriminacao'].initial = ordem_extra_objeto.discriminacao
        form_extra_fia.fields['quantidade'].initial = ordem_extra_objeto.quantidade
        form_extra_fia.fields['preco_unitario_item'].initial = ordem_extra_objeto.preco_unitario_item
        form_extra_fia.fields['justificativa'].initial = ordem_extra_objeto.justificativa

    if mensagem == 'Sucesso':
        messages.success(request, 'Sucesso!')
    elif mensagem == 'sucesso2':
        messages.success(request, 'Alteração efetuada com sucesso!')
    elif mensagem == 'criou':
        messages.success(request, 'Sugestão de correção criada com sucesso!')
    elif mensagem == 'criou_extra':
        messages.success(request, 'Ordem extra criada com sucesso!')
    elif mensagem == 'editou':
        messages.success(request, 'Sugestão de correção alterada com sucesso!')
    elif mensagem == 'excluiu_extra':
        messages.success(request, 'Ordem excluída com sucesso!')
    elif mensagem == 'excluiu_sugestao':
        messages.success(request, 'Sugestão de correção excluída com sucesso!')
    elif mensagem == 'not_allowed':
        messages.error(request, 'Acesso negado, esta alteração não pode ser efetuada no momento!')
    elif mensagem == 'nao_corretor':
        messages.error(request, 'Você não é o corretor responsável por este plano!!')
        
    turmas_iteravel = Turmas.objects.order_by('nome').filter(user=plano_objeto.usuario)
    turmas_associadas_iteravel = Turmas.objects.order_by('nome').filter(user=plano_objeto.usuario).filter(plano_associado=plano_objeto)
    
    if modelo_fia_objeto.possui_sugestao_correcao:
        lista_ordens_com_correcao.append(modelo_fia_objeto.valor_numerico)
    for ordem in ordens_extras:
        if ordem.possui_sugestao_correcao:
            lista_ordens_com_correcao.append(ordem.valor_numerico)

    lista_ordens_fia.append(modelo_fia_objeto.valor_numerico)
    for ordem in ordens_extras:
        lista_ordens_fia.append(ordem.valor_numerico)

    if plano_objeto.situacao == 'Publicado' and plano_objeto.devolvido == True and plano_objeto.correcoes_a_fazer == 0 and plano_objeto.pre_assinatura == True:
        var_plano_pre_aprovado = True
    elif plano_objeto.situacao == 'Aprovado':
        var_plano_pre_aprovado = True

    dados = {
        'chave_planos':plano_objeto,
        'chave_turmas' : turmas_iteravel,
        'chave_turmas_associadas' : turmas_associadas_iteravel,
        'chave_tipo_usuario' : tipo_usuario,
        'chave_modelo_fia' : modelo_fia_objeto,
        'chave_form_modelo_fia' : form_fia,
        'chave_ordens_extra' : ordens_extras,
        'chave_form_extra_fia' : form_extra_fia,
        'chave_modo_edicao' : modo_edicao,
        'chave_ordem_extra_objeto' : ordem_extra_objeto,
        'chave_abre_form_extra_criacao' : abreform_extra_criacao,
        'chave_abre_form_extra_edicao' : abreform_extra_edicao,
        'chave_lista_todas_ordens' : lista_ordens_fia,
        'chave_ordens_com_correcao' : lista_ordens_com_correcao,
        'plano_aprovado' : var_plano_pre_aprovado,
    }

    if reabreform_modelo_fia or reabreform_extra or abre_correcao:
        return dados
    else:
        return render(request, 'fia-visualizacao.html', dados)

def altera_fia(request, elemento_id):
    from fia.alteracoes import atualiza_valor_total_fia
    modelo_fia = get_object_or_404(Modelo_fia, pk=elemento_id)
    form_fia = ModeloFiaForm()
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and modelo_fia.plano.alterabilidade == 'Escola':
        if request.method == 'POST':
            form_fia = ModeloFiaForm(request.POST, modelo_fia_super=modelo_fia)
            if form_fia.is_valid():
                var_cx_escolar = form_fia.cleaned_data.get('nome_caixa_escolar')
                var_ano_exercicio = form_fia.cleaned_data.get('ano_exercicio')
                var_discriminacao = form_fia.cleaned_data.get('discriminacao')
                # var_quantidade = form_fia.cleaned_data.get('quantidade')
                var_preco_unitario_item = form_fia.cleaned_data.get('preco_unitario_item')
                var_justificativa = form_fia.cleaned_data.get('justificativa')
                var_membro1 = form_fia.cleaned_data.get('membro1')
                var_membro2 = form_fia.cleaned_data.get('membro2')
                modelo_fia.nome_caixa_escolar = var_cx_escolar
                modelo_fia.ano_exercicio = var_ano_exercicio
                modelo_fia.discriminacao = var_discriminacao
                modelo_fia.quantidade = 1
                modelo_fia.preco_unitario_item = var_preco_unitario_item
                modelo_fia.justificativa = var_justificativa
                if var_membro1:
                    objeto1 = get_object_or_404(User, first_name=var_membro1)
                    modelo_fia.membro_colegiado_1 = objeto1
                else:
                    modelo_fia.membro_colegiado_1 = None
                if var_membro2:
                    objeto2 = get_object_or_404(User, first_name=var_membro2)
                    modelo_fia.membro_colegiado_2 = objeto2
                else:
                    modelo_fia.membro_colegiado_2 = None

                var_total_item = 1 * var_preco_unitario_item
                modelo_fia.valor_total_item = var_total_item

                modelo_fia.save()

                atualiza_valor_total_fia(var_total_item, elemento_id)
                
                return redirect('chamando_documento_fia_mensagem', elemento_id=modelo_fia.plano.id, mensagem='sucesso2')
            else:
                print('invalido')
                id_plano_fia = modelo_fia.plano.id #id do plano_fia
                contexto = documento_fia(request, elemento_id=id_plano_fia, reabreform_modelo_fia='sim')
                contexto['chave_form_modelo_fia'] = form_fia
                contexto['contexto_extra_modelo_fia'] = True

                return render(request, 'fia-visualizacao.html', contexto)

    return redirect('chamando_documento_fia_mensagem', elemento_id=modelo_fia.plano.id, mensagem='not_allowed')

def cria_ordem_extra_fia(request, modelo_fia_id):
    from fia.alteracoes import atualiza_valor_total_fia
    modelo_fia = get_object_or_404(Modelo_fia, pk=modelo_fia_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and modelo_fia.plano.alterabilidade == 'Escola':
        if request.method == 'POST':
            form_extra_fia = OrdemExtraForm(request.POST, modelo_fia_id=modelo_fia.id)
            if form_extra_fia.is_valid():
                var_valor_numerico = form_extra_fia.cleaned_data.get('valor_numerico')
                var_discriminacao = form_extra_fia.cleaned_data.get('discriminacao')
                var_quantidade = form_extra_fia.cleaned_data.get('quantidade')
                var_preco_unitario_item = form_extra_fia.cleaned_data.get('preco_unitario_item')
                var_justificativa = form_extra_fia.cleaned_data.get('justificativa')
                var_valor_total_item = var_quantidade * var_preco_unitario_item
                ordem_extra = Extra_fia.objects.create(
                    fia_matriz=modelo_fia,
                    valor_numerico=var_valor_numerico,
                    discriminacao=var_discriminacao,
                    quantidade=var_quantidade,
                    preco_unitario_item=var_preco_unitario_item,
                    valor_total_item=var_valor_total_item,
                    justificativa=var_justificativa
                )
                ordem_extra.save()

                atualiza_valor_total_fia(modelo_fia.valor_total_item, modelo_fia.id)
                
                return redirect('chamando_documento_fia_mensagem', elemento_id=modelo_fia.plano.id, mensagem='criou_extra')
            else:
                id_plano_fia = modelo_fia.plano.id #id do plano_fia
                contexto = documento_fia(request, elemento_id=id_plano_fia, reabreform_extra='sim')
                contexto['chave_form_extra_fia'] = form_extra_fia
                contexto['contexto_extra_ordem_fia'] = True

                return render(request, 'fia-visualizacao.html', contexto)

    return redirect('chamando_documento_fia_mensagem', elemento_id=modelo_fia.plano.id, mensagem='not_allowed')

def altera_ordem_extra_fia(request, modelo_fia_id, ordem_extra_id):
    from fia.alteracoes import atualiza_valor_total_fia
    modelo_fia = get_object_or_404(Modelo_fia, pk=modelo_fia_id)
    ordem_extra_objeto = get_object_or_404(Extra_fia, pk=ordem_extra_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola' and modelo_fia.plano.alterabilidade == 'Escola':
        if request.method == 'POST':
            form_extra_fia = OrdemExtraForm(request.POST, modelo_fia_id=modelo_fia.id, id_ordem_extra=ordem_extra_objeto.id, altera_ordem=True)
            if form_extra_fia.is_valid():
                var_valor_numerico = form_extra_fia.cleaned_data.get('valor_numerico')
                var_discriminacao = form_extra_fia.cleaned_data.get('discriminacao')
                var_quantidade = form_extra_fia.cleaned_data.get('quantidade')
                var_preco_unitario_item = form_extra_fia.cleaned_data.get('preco_unitario_item')
                var_justificativa = form_extra_fia.cleaned_data.get('justificativa')
                var_valor_total_item = var_quantidade * var_preco_unitario_item
                
                ordem_extra_objeto.valor_numerico=var_valor_numerico
                ordem_extra_objeto.discriminacao=var_discriminacao
                ordem_extra_objeto.quantidade=var_quantidade
                ordem_extra_objeto.preco_unitario_item=var_preco_unitario_item
                ordem_extra_objeto.valor_total_item=var_valor_total_item
                ordem_extra_objeto.justificativa=var_justificativa
                
                ordem_extra_objeto.save()

                atualiza_valor_total_fia(modelo_fia.valor_total_item, modelo_fia.id)
                
                return redirect('chamando_documento_fia_mensagem', elemento_id=modelo_fia.plano.id, mensagem='sucesso2')
            else:
                id_plano_fia = modelo_fia.plano.id #id do plano_fia
                contexto = documento_fia(request, elemento_id=id_plano_fia, reabreform_extra='sim')
                contexto['chave_form_extra_fia'] = form_extra_fia
                contexto['contexto_extra_ordem_fia'] = True

                return render(request, 'fia-visualizacao.html', contexto)
    
    return redirect('chamando_documento_fia_mensagem', elemento_id=modelo_fia.plano.id, mensagem='not_allowed')

def exclui_ordem_extra_fia(request, ordem_extra_id):
    from fia.alteracoes import atualiza_valor_total_fia
    ordem_extra = get_object_or_404(Extra_fia, pk=ordem_extra_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    plano_objeto = get_object_or_404(Plano_de_acao, pk=ordem_extra.fia_matriz.plano.id)
    if tipo_usuario == 'Escola' and plano_objeto.alterabilidade == 'Escola':
        if request.method == 'POST':
            ordem_extra.delete()

            atualiza_valor_total_fia(ordem_extra.fia_matriz.valor_total_item, ordem_extra.fia_matriz.id)

            return redirect('chamando_documento_fia_mensagem', elemento_id=ordem_extra.fia_matriz.plano.id, mensagem='excluiu_extra')

    return redirect('chamando_documento_fia_mensagem', elemento_id=ordem_extra.fia_matriz.plano.id, mensagem='not_allowed')

def correcao_plano_fia(request, elemento_id, modelo_fia_id='', ordem_extra_id=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    form_correcao_fia = Correcao_FiaForm()
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria':
        if plano_objeto.corretor_plano == request.user: # se usuario atual for o corretor
            if modelo_fia_id:
                modelo_fia_corrigir = get_object_or_404(Modelo_fia, pk=modelo_fia_id)
                ordem_a_corrigir = modelo_fia_corrigir
                form_correcao_fia.fields['ordem_associada'].initial = str(modelo_fia_corrigir.valor_numerico)
                form_correcao_fia.fields['ordem_associada'].disabled = True
                if modelo_fia_corrigir.possui_sugestao_correcao:
                    correcao_fia_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=modelo_fia_corrigir.valor_numerico)
                    for item in correcao_fia_iteravel:
                        form_correcao_fia.fields['sugestao'].initial = item.sugestao
            elif ordem_extra_id:
                extra_fia_corrigir = get_object_or_404(Extra_fia, pk=ordem_extra_id)
                ordem_a_corrigir = extra_fia_corrigir
                form_correcao_fia.fields['ordem_associada'].initial = str(extra_fia_corrigir.valor_numerico)
                form_correcao_fia.fields['ordem_associada'].disabled = True
                if extra_fia_corrigir.possui_sugestao_correcao:
                    correcao_fia_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=extra_fia_corrigir.valor_numerico)
                    for item in correcao_fia_iteravel:
                        form_correcao_fia.fields['sugestao'].initial = item.sugestao

            form_correcao_fia.fields['plano_nome'].initial = plano_objeto.ano_referencia
            form_correcao_fia.fields['plano_nome'].disabled = True
            form_correcao_fia.fields['documento_associado'].initial = 'FIA - Formulário de Inclusão de Ações'
            form_correcao_fia.fields['documento_associado'].disabled = True

            contexto_extra_corrigir = True
            
            contexto = documento_fia(request, elemento_id=elemento_id, abre_correcao=True)
            contexto['chave_ordem_fia_a_corrigir'] = ordem_a_corrigir
            contexto['chave_contexto_corrigir_fia'] = contexto_extra_corrigir
            contexto['chave_form_correcao_fia'] = form_correcao_fia
            return render(request, 'fia-visualizacao.html', contexto)

        else:
            return redirect('chamando_documento_fia_mensagem', elemento_id=elemento_id, mensagem='nao_corretor')
    
    return redirect('dashboard')

def cria_altera_correcao_fia(request, plano_id, ordem_id):
    from fia.alteracoes import atualiza_total_correcoes
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria' and plano_objeto.corretor_plano == request.user:
        if request.method == 'POST':
            form_correcao_fia_preenchido = Correcao_FiaForm(request.POST)
            if form_correcao_fia_preenchido.is_valid():
                campo_numero = form_correcao_fia_preenchido.cleaned_data.get('ordem_associada')
                if campo_numero == 1: # É MODELO_FIA
                    objeto_a_corrigir = get_object_or_404(Modelo_fia, pk=ordem_id)
                else: # É EXTRA_FIA
                    objeto_a_corrigir = get_object_or_404(Extra_fia, pk=ordem_id)
                
                # CRIA NOVA CORREÇÃO
                if not objeto_a_corrigir.possui_sugestao_correcao:  
                    instancia = form_correcao_fia_preenchido.save(commit=False)
                    instancia.plano_associado = plano_objeto
                    instancia.ordem_associada = objeto_a_corrigir.valor_numerico
                    instancia.save()

                    atualiza_total_correcoes(plano_id)

                    objeto_a_corrigir.possui_sugestao_correcao = True
                    objeto_a_corrigir.save()

                    mensagem_var = 'criou'

                # ALTERA CORREÇÃO EXISTENTE
                else:
                    correcao_fia_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=objeto_a_corrigir.valor_numerico)
                    for item in correcao_fia_iteravel:
                        item.sugestao = form_correcao_fia_preenchido.cleaned_data.get('sugestao')
                        item.save()

                    mensagem_var = 'editou'

                return redirect('chamando_documento_fia_mensagem', elemento_id=plano_id, mensagem=mensagem_var)
    else:
        return redirect('dashboard')

def deleta_correcao_fia(request, plano_id, ordem_id, tipo_ordem=''):
    from fia.alteracoes import atualiza_total_correcoes
    plano_objeto = get_object_or_404(Plano_de_acao, pk=plano_id)
    if tipo_ordem == 'modelo_fia':
        objeto_a_exlcuir = get_object_or_404(Modelo_fia, pk=ordem_id)
    elif tipo_ordem == 'extra_fia':
        objeto_a_exlcuir = get_object_or_404(Extra_fia, pk=ordem_id)

    tipo_usuario = request.user.classificacao.tipo_de_acesso
    if tipo_usuario == 'Func_sec' and plano_objeto.alterabilidade == 'Secretaria' and plano_objeto.corretor_plano == request.user:
        if request.method == 'POST':
            correcao_fia_iteravel = Correcoes.objects.filter(plano_associado=plano_objeto).filter(ordem_associada=objeto_a_exlcuir.valor_numerico)
            for item in correcao_fia_iteravel:
                item.delete()

            atualiza_total_correcoes(plano_id)

            objeto_a_exlcuir.possui_sugestao_correcao = False
            objeto_a_exlcuir.save()

            return redirect('chamando_documento_fia_mensagem', elemento_id=plano_id, mensagem='excluiu_sugestao')
        
    else:
        return redirect('dashboard')

def abre_correcao_fia(request, elemento_id, ident_numerica='', abreFormFia=''):
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    modelo_fia = get_object_or_404(Modelo_fia, plano=plano_objeto)

    if abreFormFia:
        correcao_de_fia_objeto = get_object_or_404(Correcoes, plano_associado=plano_objeto, ordem_associada=ident_numerica)
        correcao_de_ordem_especifica = Correcoes.objects.order_by('ordem_associada').filter(plano_associado=plano_objeto).filter(documento_associado = 'FIA - Formulário de Inclusão de Ações').filter(ordem_associada=ident_numerica)

        if ident_numerica == 1:
            objeto_corrigindo = get_object_or_404(Modelo_fia, plano=plano_objeto)
            corrigindo_modelo_fia = True
            form_fia = ModeloFiaForm()
            form_fia.fields['nome_caixa_escolar'].initial = objeto_corrigindo.nome_caixa_escolar
            form_fia.fields['ano_exercicio'].initial = objeto_corrigindo.ano_exercicio
            form_fia.fields['discriminacao'].initial = objeto_corrigindo.discriminacao
            if objeto_corrigindo.preco_unitario_item == 0:
                form_fia.fields['preco_unitario_item'].initial = ''
            else:
                form_fia.fields['preco_unitario_item'].initial = objeto_corrigindo.preco_unitario_item
            form_fia.fields['justificativa'].initial = objeto_corrigindo.justificativa

            contexto = pagina_correcoes(request, elemento_id, retorna_contexto_fia='sim')
            contexto['chave_corrigindo_modelo_fia'] = corrigindo_modelo_fia
            contexto['chave_especifica_objeto'] = correcao_de_fia_objeto
            contexto['chave_correcao_ordem_especifica'] = correcao_de_ordem_especifica
            contexto['chave_do_form'] = form_fia
            return render(request, 'correcoes.html', contexto)

        else:
            objeto_corrigindo = get_object_or_404(Extra_fia, fia_matriz=modelo_fia, valor_numerico=ident_numerica)
            corrigindo_extra_fia = True
            form_extra_fia = OrdemExtraForm()
            form_extra_fia.fields['valor_numerico'].initial = objeto_corrigindo.valor_numerico
            form_extra_fia.fields['valor_numerico'].disabled = True
            form_extra_fia.fields['discriminacao'].initial = objeto_corrigindo.discriminacao
            form_extra_fia.fields['quantidade'].initial = objeto_corrigindo.quantidade
            form_extra_fia.fields['preco_unitario_item'].initial = objeto_corrigindo.preco_unitario_item
            form_extra_fia.fields['justificativa'].initial = objeto_corrigindo.justificativa

            contexto = pagina_correcoes(request, elemento_id, retorna_contexto_fia='sim')
            contexto['chave_corrigindo_extra_fia'] = corrigindo_extra_fia
            contexto['chave_especifica_objeto'] = correcao_de_fia_objeto
            contexto['chave_correcao_ordem_especifica'] = correcao_de_ordem_especifica
            contexto['chave_do_form'] = form_extra_fia
            return render(request, 'correcoes.html', contexto)
    
    return redirect('dashboard')
        
def corrige_fia(request, elemento_id, ident_numerica):
    from fia.alteracoes import salva_form_modelo_fia, salva_form_extra_fia, atualiza_valor_total_fia, atualiza_total_correcoes
    plano_objeto = get_object_or_404(Plano_de_acao, pk=elemento_id)
    modelo_fia = get_object_or_404(Modelo_fia, plano=plano_objeto)

    if ident_numerica == 1:
        form_modelo_fia = ModeloFiaForm(request.POST)
        if form_modelo_fia.is_valid():
            var_total_item = salva_form_modelo_fia(form_modelo_fia, modelo_fia)
            atualiza_valor_total_fia(var_total_item, modelo_fia.id)
                
            # Tira o indicativo de que a ordem possui sugestão de correção
            modelo_fia.possui_sugestao_correcao = False
            modelo_fia.save()

            # Remove o objeto 'correcao' uma vez que ele acabou de ser corrigido.
            correcao_de_ordem_especifica = get_object_or_404(Correcoes, plano_associado=plano_objeto, ordem_associada=ident_numerica)
            correcao_de_ordem_especifica.delete()

            # Atualiza a quantidade de correções neste plano
            atualiza_total_correcoes(elemento_id)

            return redirect('pagina_correcoes_mensagem', elemento_id=elemento_id, mensagem='Sucesso')
        else:
            contexto = abre_correcao_fia(request, elemento_id, ident_numerica, abreFormFia='sim')
            contexto['chave_do_form'] = form_modelo_fia
            return render(request, 'correcoes.html', contexto)

    else:
        extra_fia = get_object_or_404(Extra_fia, fia_matriz=modelo_fia, valor_numerico=ident_numerica)
        form_extra_fia = OrdemExtraForm(request.POST, modelo_fia_id=modelo_fia.id, id_ordem_extra=extra_fia.id, altera_ordem=True)
        if form_extra_fia.is_valid():
            print('oi teste')
            var_total_item = salva_form_extra_fia(form_extra_fia, extra_fia)
            
            atualiza_valor_total_fia(modelo_fia.valor_total_item, modelo_fia.id)

            # Tira o indicativo de que a ordem possui sugestão de correção
            extra_fia.possui_sugestao_correcao = False
            extra_fia.save()

            # Remove o objeto 'correcao' uma vez que ele acabou de ser corrigido.
            correcao_de_ordem_especifica = get_object_or_404(Correcoes, plano_associado=plano_objeto, ordem_associada=ident_numerica)
            correcao_de_ordem_especifica.delete()

            # Atualiza a quantidade de correções neste plano
            atualiza_total_correcoes(elemento_id)

            return redirect('pagina_correcoes_mensagem', elemento_id=elemento_id, mensagem='Sucesso')

        else:
            print('invalido')
            contexto = abre_correcao_fia(request, elemento_id, ident_numerica, abreFormFia='sim')
            contexto['chave_do_form'] = form_extra_fia
            return render(request, 'correcoes.html', contexto)