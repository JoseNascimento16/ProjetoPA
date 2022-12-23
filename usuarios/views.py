from base64 import b64decode, urlsafe_b64decode
from multiprocessing import context
from webbrowser import get
from django.core.files.base import ContentFile
import base64
from plano_de_acao.alteracoes import atualiza_assinaturas_escola
from usuarios.alteracoes import envia_email_ativacao, identifica_diretor, checa_usuario_unico, envia_email_new_user
from Escolas.models import Escola
from usuarios.models import Classificacao, Turmas, Usuario
from usuarios.forms import DiretorEscolaForm, FuncionariosForm, TurmasForm, EscolasForms, FuncionariosSecretariaForm, AlteraCargoForm, FormAlteraLogin, FormAlteraMail
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from plano_de_acao.models import Plano_de_acao
from usuarios.pesquisas import pesquisa_escolas_cadastradas, pesquisa_funcionarios_cadastrados
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django import forms
from .utils import generate_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from.decorators import usuario_nao_autenticado
from django.contrib.auth.base_user import BaseUserManager
from eventlog.models import Event
from django.db.models import Q
from django.core.paginator import Paginator

from datetime import date, datetime, time, timezone, timedelta

# Create your views here.




#### VIEWS TESTADAS #####

def envia_email(request):
    # contexto = {
    #     'nome' : request.user.first_name
    # }
    # subject = 'Assunto do email'
    # message = render_to_string('teste-email.txt', contexto)
    # remetente = settings.EMAIL_HOST_USER
    # destinatario = request.user.email

    # try:
    #     send_mail(subject, message, remetente, [destinatario], fail_silently=False)

    #     # print('enviou email!')
    #     return redirect('abre_meu_acesso', user_id=request.user.id)
        
    # except BadHeaderError:
	#     return HttpResponse('Invalid header found.')

    # return redirect('abre_meu_acesso', user_id=request.user.id)
    return render(request, 'teste.html')

def cadastros_da_secretaria(request, **kwargs):
    tipo_usuario_logado = request.user.groups.get().name
    controle_form_cadastro_escolas = False
    controle_form_cadastro_diretor = False
    var_pesquisa_escola = False
    form_escolas = ''
    form_diretor = ''
    escola = ''
    
    if kwargs.get('mensagem') == 'Criou_diretor':
        messages.success(request, 'Sucesso. O usuário receberá no e-mail cadastrado as credenciais de acesso!')
    if kwargs.get('mensagem') == 'Criou':
        messages.success(request, 'Escola cadastrada com sucesso!')
    if kwargs.get('mensagem') == 'Deletou':
        messages.success(request, 'Escola excluída com sucesso!')

    if tipo_usuario_logado == 'Secretaria' or tipo_usuario_logado == 'Func_sec':

        escolas_cadastradas = Escola.objects.filter(objeto_suprot=False).filter(is_active=True)
        len_escolas_a_exibir = len(escolas_cadastradas)

        if kwargs.get('search'):
            escolas_cadastradas = pesquisa_escolas_cadastradas(request)
            var_pesquisa_escola = True

        if kwargs.get('cadastro_diretor'):
            form_diretor = DiretorEscolaForm()
            controle_form_cadastro_diretor = True
            escola = get_object_or_404(Escola, id=kwargs['escola_id'])
        else:
            form_escolas = EscolasForms()

        dados_a_exibir = {
            'chave_escola' : escola,
            'chave_tipo_usuario' : tipo_usuario_logado,
            'escolas_a_exibir': escolas_cadastradas,
            'chave_len_escolas_a_exibir' : len_escolas_a_exibir,
            'chave_form_cadastro_escolas': form_escolas,
            'chave_var_pesquisa_escola' : var_pesquisa_escola,
            'chave_form_cadastro_diretor': form_diretor,
            'contexto_extra_form_diretor': controle_form_cadastro_diretor,
        }
        if kwargs.get('retorna_contexto'):
            return dados_a_exibir

        return render(request, 'cadastros-secretaria.html', dados_a_exibir)
    
    return redirect('dashboard')

def cadastro_de_escolas(request, **kwargs):#mensagem, search
    tipo_usuario_logado = request.user.groups.get().name
    controle_form_cadastro_escolas = False
    var_pesquisa_escola = False
    form_escolas = EscolasForms()

    if tipo_usuario_logado == 'Secretaria' or tipo_usuario_logado == 'Func_sec':
        if request.method == 'POST':
            form_escolas = EscolasForms(request.POST)
            if form_escolas.is_valid():
                last_form = form_escolas.cleaned_data.get('last_name')
                muni_form = form_escolas.cleaned_data.get('municipio')
                codigo_form = form_escolas.cleaned_data.get('codigo_escola')
                nte_form = form_escolas.cleaned_data.get('nte')

                escola = Escola.objects.create(
                nome=last_form,
                municipio=muni_form,
                codigo_escola=codigo_form,
                nte=nte_form)
                escola.save()

                return redirect('chama_cadastros_secretaria_mensagem', mensagem='Criou') 
            else:
                dados = cadastros_da_secretaria(request, retorna_contexto=True)
                dados['contexto_extra'] = True
                dados['contexto_extra_form_escolas'] = True
                dados['chave_escola'] = ''
                dados['chave_form_cadastro_escolas'] = form_escolas
                return render(request, 'cadastros-secretaria.html', dados)
    
    return redirect('dashboard')

def cadastro_diretor_escola(request, **kwargs):
    ja_Existe_usuario = True
    escola = get_object_or_404(Escola, id=kwargs['escola_id'])
    tipo_usuario_logado = request.user.groups.get().name
    if tipo_usuario_logado == 'Secretaria' or tipo_usuario_logado == 'Func_sec':
        if request.method == 'POST':
            form_diretor = DiretorEscolaForm(request.POST, escola_super=escola)
            if form_diretor.is_valid():
                nome = form_diretor.cleaned_data.get('first_name')
                email = form_diretor.cleaned_data.get('email')

                while ja_Existe_usuario:
                    nome_lista = list(nome.split(" "))
                    hash_1 = BaseUserManager().make_random_password(length=5)
                    nome_usuario = nome_lista[0] + '_' + hash_1
                    password = BaseUserManager().make_random_password(length=8)
                    
                    ja_Existe_usuario = checa_usuario_unico(nome_usuario)

                novo_usuario = User.objects.create_user(first_name=nome, last_name='Diretor(a)', email=email, username=nome_usuario, password=password)
                grupo_diretor = get_object_or_404(Group, name='Diretor_escola')
                novo_usuario.groups.add(grupo_diretor)
                novo_usuario.save()

                Classificacao.objects.create(user=novo_usuario, escola=escola, tipo_de_acesso='Diretor_escola', matriz=escola.nome, cargo_herdado='Diretor(a)', email_ativado=True, diretor_escolar=True)
                escola.possui_diretor = True
                escola.diretor = novo_usuario
                escola.save()

                envia_email_new_user(request, novo_usuario, password)
                
                return redirect('chama_cadastros_secretaria_mensagem', mensagem='Criou_diretor')
            else:
                dados = cadastros_da_secretaria(request, retorna_contexto=True)
                dados['chave_form_cadastro_diretor'] = form_diretor
                dados['contexto_extra_form_diretor'] = True
                dados['chave_escola'] = escola
                dados['chave_form_cadastro_escolas'] = ''
                return render(request, 'cadastros-secretaria.html', dados)

    return redirect('dashboard')

def cadastro_de_funcionarios_secretaria(request, **kwargs):
    from .forms_campos import campo_cargo_func_sec
    tipo_usuario_logado = request.user.groups.get().name
    controle_form_cadastro_funcionarios = False

    if request.user.classificacao.usuario_diretor or request.user.classificacao.usuario_coordenador or tipo_usuario_logado == 'Secretaria':
        form_funcionarios = ''
        funcionarios_cadastrados = ''
        var_pesquisa_func = False
        ja_Existe_usuario = True
        
        if kwargs.get('mensagem') == 'Criou_func':
            messages.success(request, 'Funcionário cadastrado com sucesso!')
        if kwargs.get('mensagem') == 'Deletou':
            messages.success(request, 'Funcionário excluído com sucesso!')
        if kwargs.get('mensagem') == 'Sucesso':
            messages.success(request, 'Alteração efetuada com sucesso!')
        if kwargs.get('mensagem') == 'Erro':
            messages.error(request, 'Erro! Você não pode alterar o seu próprio status!')
        
        if not kwargs.get('search'):

            form = campo_cargo_func_sec(request, tipo_usuario_logado)

            form_funcionarios = form

            if request.method == 'POST':
                objeto_matriz = request.user.classificacao.escola # Objeto 'Secretaria da educação'
                matriz_nome = request.user.classificacao.escola.nome

                form_funcionarios = FuncionariosSecretariaForm(request.POST, escola_super=objeto_matriz)
                if form_funcionarios.is_valid():
                    instancia_form = form_funcionarios.save(commit=False)
                    cargo1 = form_funcionarios.cleaned_data.get('cargo')
                    nome = instancia_form.first_name

                    while ja_Existe_usuario:
                        nome_lista = list(nome.split(" "))
                        hash_1 = BaseUserManager().make_random_password(length=5)
                        nome_usuario = nome_lista[0] + '_' + hash_1
                        password = BaseUserManager().make_random_password(length=8)
                    
                        ja_Existe_usuario = checa_usuario_unico(nome_usuario)
                    
                    usuario_criado = User.objects.create_user(
                        username=nome_usuario,
                        password=password,
                        first_name=instancia_form.first_name,
                        email=instancia_form.email,
                        last_name=cargo1,
                    )

                    grupo_func_sec = Group.objects.get(name='Func_sec')
                    if cargo1 == 'Corretor (Técnico)':
                        classificacao = Classificacao.objects.create(user=usuario_criado, tipo_de_acesso='Func_sec', assina_plano=False, matriz=matriz_nome, escola=objeto_matriz, cargo_herdado='Corretor (Técnico)')
                        usuario_criado.groups.add(grupo_func_sec)
                    elif cargo1 == 'Coordenador':
                        classificacao = Classificacao.objects.create(user=usuario_criado, tipo_de_acesso='Func_sec', assina_plano=False, usuario_coordenador=True, matriz=matriz_nome, escola=objeto_matriz, cargo_herdado='Coordenador')
                        usuario_criado.groups.add(grupo_func_sec)
                    elif cargo1 == 'Diretor SUPROT':
                        classificacao = Classificacao.objects.create(user=usuario_criado, tipo_de_acesso='Func_sec', assina_plano=True, usuario_diretor=True, matriz=matriz_nome, escola=objeto_matriz, cargo_herdado='Diretor SUPROT')
                        usuario_criado.groups.add(grupo_func_sec)
                        objeto_matriz.diretor = usuario_criado
                        objeto_matriz.possui_diretor = True

                    # Um signal pre_save é gerado
                    classificacao.save()

                    # Atualiza quant. funcionarios da matriz
                    quant_func_secs = User.objects.filter(groups__name='Func_sec')
                    objeto_matriz.quant_funcionarios = len(quant_func_secs)
                    objeto_matriz.save()

                    # Envia email com as credenciais
                    envia_email_new_user(request, usuario_criado, password)

                    return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=request.user.id, mensagem='Criou_func', cad_funcionarios='Sim')

                else:
                    controle_form_cadastro_funcionarios = True

        funcionarios_cadastrados = Classificacao.objects.order_by('-user__last_name').filter(tipo_de_acesso='Func_sec').filter(is_active=True)
        

        if kwargs.get('search'):
            funcionarios_cadastrados = pesquisa_funcionarios_cadastrados(request)
            var_pesquisa_func = True

        dados_a_exibir = {

            'chave_form_cadastro_funcionarios' : form_funcionarios,
            'funcionarios_a_exibir' : funcionarios_cadastrados,
            'contexto_extra_form_funcionarios': controle_form_cadastro_funcionarios,
            'chave_tipo_usuario' : tipo_usuario_logado,
            'chave_cad_funcionarios' : kwargs['cad_funcionarios'],
            'chave_var_pesquisa_func' : var_pesquisa_func,
        }

        if not kwargs.get('retorno_altera_cargo'):
            return render(request, 'cadastros-secretaria.html', dados_a_exibir)
        else:
            return dados_a_exibir

    return redirect('dashboard')

def cadastros_escola(request, **kwargs):
    from usuarios.alteracoes import atualiza_cargos_da_matriz_cadastro, retorna_quant_funcionarios_da_escola
    tipo_usuario_logado = request.user.groups.get().name
    escola_matriz = request.user.classificacao.escola
    controle_form_cadastro_funcionarios = False
    ja_Existe_usuario = True

    if kwargs.get('mensagem') == 'Criou':
        messages.success(request, 'Funcionário cadastrado com sucesso!')
    if kwargs.get('mensagem') == 'Deletou':
        messages.success(request, 'Funcionário excluído com sucesso!')

    if tipo_usuario_logado == 'Diretor_escola':
        # controle = False
        form_funcionarios = FuncionariosForm(initial={'cargo': '-------'})

        if request.method == 'POST':
            form_funcionarios = FuncionariosForm(request.POST, escola_super=escola_matriz)
            if form_funcionarios.is_valid():
                instancia_form = form_funcionarios.save(commit=False)
                cargo1 = form_funcionarios.cleaned_data.get('cargo')
                nome = instancia_form.first_name

                while ja_Existe_usuario:
                    nome_lista = list(nome.split(" "))
                    hash_1 = BaseUserManager().make_random_password(length=5)
                    nome_usuario = nome_lista[0] + '_' + hash_1
                    password = BaseUserManager().make_random_password(length=8)
                
                    ja_Existe_usuario = checa_usuario_unico(nome_usuario)

                #cria objeto usuario
                usuario_criado = User.objects.create_user(
                    username=nome_usuario,
                    first_name=instancia_form.first_name,
                    last_name=cargo1,
                    email=instancia_form.email,
                    password=password)

                #Cria objeto classificacao
                Classificacao.objects.create(user=usuario_criado, tipo_de_acesso='Funcionario', cargo_herdado=cargo1, matriz=escola_matriz.nome, escola=escola_matriz)
                
                # Atualiza quant. funcionarios da matriz
                quant_funcs = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(escola=escola_matriz).filter(is_active=True)
                escola_matriz.quant_funcionarios = len(quant_funcs)
                escola_matriz.save()

                # Atualiza cargos da matriz
                atualiza_cargos_da_matriz_cadastro(cargo1, escola_matriz)

                # Envia email com as credenciais
                envia_email_new_user(request, usuario_criado, password)

                return redirect('cadastrar_funcionarios_mensagem', user_id=kwargs['user_id'], mensagem='Criou')

            else:
                controle_form_cadastro_funcionarios = True

        funcionarios_cadastrados = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(escola=escola_matriz).filter(is_active=True)
        len_funcionarios_cadastrados = retorna_quant_funcionarios_da_escola(escola_matriz)
        
        dados_a_exibir = {

            'chave_form_cadastro_funcionarios' : form_funcionarios,
            'funcionarios_a_exibir' : funcionarios_cadastrados,
            'contexto_extra_form_funcionarios': controle_form_cadastro_funcionarios,
            'chave_tipo_usuario' : tipo_usuario_logado,
            'chave_len_funcionarios_cadastrados' : len_funcionarios_cadastrados
        }

        return render(request, 'cadastros.html', dados_a_exibir)

    return redirect('dashboard')

def solicita_remocao(request, **kwargs):
    # REGISTRA A SOLICITAÇÃO DE EXCLUSÃO DE UM USUARIO IMPORTANTE
    tipo_usuario_logado = request.user.groups.get().name
    usuario_alvo = get_object_or_404(User, pk=kwargs['user_id'])
    escola_id = usuario_alvo.classificacao.escola.id

    if tipo_usuario_logado == 'Func_sec':
        if request.method == 'POST':
            usuario_alvo.classificacao.marcado_para_exclusao = True
            usuario_alvo.classificacao.remocao_solicitante = request.user.first_name
            usuario_alvo.classificacao.save()
            return redirect('profile_escola', escola_id=escola_id)

    return redirect('dashboard')

def cancela_remocao_diretor(request, **kwargs):
    # CANCELA A SOLICITAÇÃO DE EXCLUSÃO DE UM USUARIO IMPORTANTE
    usuario_alvo = get_object_or_404(User, pk=kwargs['user_id'])
    escola_id = usuario_alvo.classificacao.escola.id
    
    if request.user.classificacao.usuario_diretor:
        if request.method == 'POST':
            usuario_alvo.classificacao.marcado_para_exclusao = False
            usuario_alvo.classificacao.remocao_solicitante = ''
            usuario_alvo.classificacao.save()
            
            return redirect('profile_escola', escola_id=escola_id)

    return redirect('dashboard')

def deleta_funcionario(request, **kwargs):
    from .alteracoes import atualiza_cargos_da_matriz_exclusao, atualiza_quant_funcionarios_da_escola
    ja_Existe_usuario = True
    while ja_Existe_usuario:
            random_username = BaseUserManager().make_random_password(length=15)
            ja_Existe_usuario = checa_usuario_unico(random_username)

    usuario_logado = request.user
    tipo_usuario = request.user.groups.get().name

    if tipo_usuario == 'Diretor_escola':
        
        escola = usuario_logado.classificacao.escola
        planos = Plano_de_acao.objects.filter(escola=escola)

        funcionario_classificacao = get_object_or_404(Classificacao, pk=kwargs['elemento_id'])
        funcionario_id = funcionario_classificacao.user.id
        funcionario_objeto = get_object_or_404(User, pk=funcionario_id)
        funcionario_objeto.is_active = False
        funcionario_objeto.email = ''
        funcionario_objeto.username = random_username

        funcionario_classificacao.is_active = False
        funcionario_classificacao.email_ativado = False
        if funcionario_classificacao.assinatura:
            funcionario_classificacao.assinatura.delete()

        funcionario_objeto.save()
        funcionario_classificacao.save()

        # atualiza quant_funcionarios da matriz
        atualiza_quant_funcionarios_da_escola(escola)
        
        # Atualiza os cargos da matriz
        atualiza_cargos_da_matriz_exclusao(funcionario_classificacao, escola)

        # Remove assinaturas e atualiza
        for plano in planos:
            if plano.situacao != 'Finalizado':
                funcionario_classificacao.plano_associado.remove(plano) # Remove qualquer associação com planos que este usuario tiver
                atualiza_assinaturas_escola(plano.id)

        return redirect('cadastrar_funcionarios_mensagem', user_id=usuario_logado.id, mensagem='Deletou')
    
    if tipo_usuario == 'Secretaria' or usuario_logado.classificacao.usuario_diretor or usuario_logado.classificacao.usuario_coordenador :
        
        # Captura classificação do funcionario desativado
        objeto_classificacao = get_object_or_404(Classificacao, pk=kwargs['elemento_id'])
        # Checa a matriz do funcionario desativado
        matriz = objeto_classificacao.escola

        # DESATIVA usuário (Func_sec,diretores,funcionarios)
        funcionario_id = objeto_classificacao.user.id
        usuario_objeto = get_object_or_404(User, pk=funcionario_id)
        usuario_objeto.is_active = False
        usuario_objeto.email = ''
        usuario_objeto.username = random_username
        usuario_objeto.first_name = '(desativado)' + usuario_objeto.first_name
        usuario_objeto.save()

        # Se desativou Func_sec, atualiza quant_func da Secretaria
        if objeto_classificacao.user.groups.filter(name='Func_sec').exists():
            quant_func_secs = Classificacao.objects.filter(escola=matriz).filter(is_active=True)
            matriz.quant_funcionarios = len(quant_func_secs)
            matriz.save()

        # Se usuario objeto for diretor da SUPROT
        if objeto_classificacao.usuario_diretor:
            matriz.possui_diretor = False
            matriz.diretor = None

        # Desativa classificação (Func_sec,diretores,funcionarios)
        if objeto_classificacao.assinatura:
            objeto_classificacao.assinatura.delete()
        objeto_classificacao.is_active = False
        objeto_classificacao.email_ativado = False
        objeto_classificacao.assina_plano = False
        objeto_classificacao.usuario_diretor = False
        objeto_classificacao.usuario_coordenador = False
        objeto_classificacao.diretor_escolar = False
        

        # Se desativou Diretor_escola, atualiza quant_func e outras informações da Escola
        if objeto_classificacao.user.groups.filter(name='Diretor_escola').exists():
            quant_func_escola = Classificacao.objects.filter(escola=matriz).filter(is_active=True)
            matriz.quant_funcionarios = len(quant_func_escola)

            matriz.diretor = None
            matriz.possui_diretor = False

            matriz.save()
            objeto_classificacao.save()

            return redirect('profile_escola', matriz.id)

        matriz.save()
        objeto_classificacao.save()

        return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=usuario_logado.id, mensagem='Deletou', cad_funcionarios='Sim')

    else:
        return redirect('dashboard')   

def altera_cargo(request, **kwargs):
    checa_usuario = request.user
    tipo_usuario_logado = request.user.groups.get().name
    if tipo_usuario_logado == 'Secretaria' or checa_usuario.classificacao.usuario_diretor:

        if not kwargs.get('edita'):
            altera_cargo = True
            form = AlteraCargoForm()

            contexto = cadastro_de_funcionarios_secretaria(request, user_id=checa_usuario.id, cad_funcionarios=True, retorno_altera_cargo=True)
            contexto['chave_form_altera_cargo'] = form
            contexto['chave_altera_cargo'] = altera_cargo
            contexto['chave_elemento_id'] = kwargs['elemento_id']
            return render(request, 'cadastros-secretaria.html', contexto)

        else:
            form = AlteraCargoForm(request.POST)
            classificacao_func = get_object_or_404(Classificacao, pk=kwargs['elemento_id'])
            if classificacao_func == request.user.classificacao:
                return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=request.user.id, cad_funcionarios='sim', mensagem='Erro')
            if request.method == 'POST':
                if form.is_valid():
                    valor_campo = form.cleaned_data.get('campo')
                    if valor_campo == 'Coordenador':
                        classificacao_func.assina_plano = False
                        classificacao_func.usuario_coordenador = True
                        classificacao_func.user.last_name = 'Coordenador'
                        classificacao_func.save()
                        classificacao_func.user.save()
                    else:
                        classificacao_func.assina_plano = False
                        classificacao_func.usuario_coordenador = False
                        classificacao_func.user.last_name = 'Corretor (Técnico)'
                        classificacao_func.save()
                        classificacao_func.user.save()

                    # GERAR LOG

                    return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=request.user.id, cad_funcionarios='sim', mensagem='Sucesso')

    return redirect('dashboard')   

def cadastro_turmas(request, **kwargs):
    controle_turmas = False
    tipo_usuario_logado = request.user.groups.get().name

    if kwargs.get('mensagem') == 'Criou':
        messages.success(request, 'Turma criada com sucesso!')
    elif kwargs.get('mensagem') == 'Deletou':
        messages.success(request, 'Turma excluída com sucesso!')

    if tipo_usuario_logado == 'Diretor_escola':

        form_turmas = TurmasForm()
        usuario_diretor = get_object_or_404(User, pk=kwargs['user_id'])

        if request.method == 'POST':
            form_turmas = TurmasForm(request.POST)
            if form_turmas.is_valid():
                nome1 = form_turmas.cleaned_data.get('nome')
                qt_aluno = form_turmas.cleaned_data.get('quantidade_alunos')
                turma = Turmas.objects.create(
                    escola = usuario_diretor.classificacao.escola,
                    nome = nome1,
                    quantidade_alunos = qt_aluno
                )
                turma.save()
                
                return redirect('cadastrando_turmas_mensagem', user_id=kwargs['user_id'], mensagem='Criou')
            else:
                controle_turmas = True

        turmas_cadastradas = Turmas.objects.order_by('nome').filter(escola=usuario_diretor.classificacao.escola).filter(is_active=True)
        
        if kwargs.get('abre_form'):
            controle_turmas = True

        turmas_a_exibir = {
            'chave_user_id' : usuario_diretor,
            'chave_form_cadastro_turmas' : form_turmas,
            'chave_turmas_cadastradas' : turmas_cadastradas,
            'contexto_extra_turmas' : controle_turmas,
            'chave_tipo_usuario' : tipo_usuario_logado,
        }
        
        return render(request, 'cadastro_turmas.html', turmas_a_exibir)

    return redirect('dashboard')

def deleta_turma(request, **kwargs):
    tipo_usuario = request.user.groups.get().name
    turma_objeto = get_object_or_404(Turmas, id=kwargs['turma_id'])
    if tipo_usuario == 'Diretor_escola' and turma_objeto.escola == request.user.classificacao.escola:
        if turma_objeto.plano_associado.exists():
            turma_objeto.is_active = False
            turma_objeto.save()
        else:
            turma_objeto.delete()

        id_do_usuario = request.user.id
        return redirect('cadastrando_turmas_mensagem', user_id=id_do_usuario, mensagem='Deletou')

    return redirect('dashboard')

def meu_acesso(request, **kwargs):
    abre_modal = False
    abre_modal_sign = False
    abre_modal_mail = False
    form = ''
    form2 = ''
    usuario = request.user.groups.get().name

    if kwargs.get('mensagem') == 'success':
            messages.success(request, 'Alteração efetuada com sucesso!')
    elif kwargs.get('mensagem') == 'sent_activation':
            messages.warning(request, 'Verifique sua caixa de entrada para confirmar o seu e-mail!')
    elif kwargs.get('mensagem') == 'activation_success':
            messages.success(request, 'E-mail ativado com sucesso!')
    elif kwargs.get('mensagem') == 'mail_removed':
            messages.success(request, 'E-mail removido com sucesso!')

    if kwargs.get('altera') == 'alt_login':
        abre_modal = True
        if not kwargs.get('altera_erro'):
            form = FormAlteraLogin()
        else:
            form = kwargs['form_erro']

    elif kwargs.get('altera') == 'alt_sign':
        abre_modal_sign = True

    elif kwargs.get('altera') == 'chng_mail':
        abre_modal_mail = True
        if not kwargs.get('altera_erro'):
            form2 = FormAlteraMail()
            form2 = FormAlteraMail(prefix='qualquer') 
            form2.fields['email'].initial = request.user.email
        else:
            form2 = kwargs['form_erro']
    else:
        form = ''

    contexto = {
        'chave_tipo_usuario' : usuario,
        'chave_abre_altera_login':abre_modal,
        'chave_abre_altera_assinatura':abre_modal_sign,
        'chave_abre_altera_mail' : abre_modal_mail,
        'chave_form_altera_login':form,
        'chave_form_altera_mail':form2,
    }

    return render(request, 'profile.html', contexto)

def profile_escola(request, **kwargs):
    from.alteracoes import identifica_diretor
    requisita_remocao_diretor = True
    confirma_remocao_diretor = False
    solicitante = ''
    escola = get_object_or_404(Escola, pk=kwargs['escola_id'])
    diretor = identifica_diretor(kwargs['escola_id'])

    if diretor and diretor.classificacao.marcado_para_exclusao:
        requisita_remocao_diretor = False
        confirma_remocao_diretor = True
        solicitante = diretor.classificacao.remocao_solicitante

    contexto = {
        'chave_escola' : escola,
        'chave_diretor' : diretor,
        'chave_tipo_usuario' : request.user.groups.get().name,
        'chave_requisita_remocao_diretor' : requisita_remocao_diretor,
        'chave_confirma_remocao_diretor' : confirma_remocao_diretor,
        'chave_solicitante' : solicitante,
    }
    
    return render(request, 'Profile_escola.html', contexto)

def altera_login(request, **kwargs):
    if request.method == 'POST':
        form = FormAlteraLogin(request.POST, user_super=request.user)
        usuario_logado = request.user
        if form.is_valid():
            novo_username = form.cleaned_data.get('novo_username2')
            usuario_logado.username = novo_username
            usuario_logado.save()

            usuario_logado.classificacao.login_original = False
            usuario_logado.classificacao.save()
            
            return redirect('abre_meu_acesso_mensagem', user_id=kwargs['user_id'], mensagem='success')
        else:
            return meu_acesso(request, user_id=kwargs['user_id'], altera='alt_login', altera_erro='sim', form_erro=form)
    
    return redirect('dashboard')

def remove_mail(request, user_id):
    if request.method == 'POST':
        usuario = get_object_or_404(User, pk=user_id)
        usuario.email = ''
        usuario.classificacao.email_ativado = False
        usuario.save()
        usuario.classificacao.save()

        return redirect('abre_meu_acesso_mensagem', mensagem='mail_removed', user_id=request.user.id)
    
    return redirect('dashboard')

def altera_mail(request, user_id):
    if request.method == 'POST':
        form = FormAlteraMail(request.POST, user_id_super=user_id, prefix='qualquer')
        if form.is_valid():
            var_email = form.cleaned_data.get('email')
            envia_email_ativacao(request, request.user, var_email)
            usuario = get_object_or_404(User, pk=request.user.id)
            usuario.email = var_email
            usuario.save()
            return redirect('abre_meu_acesso_mensagem', mensagem='sent_activation', user_id=request.user.id)
        else:
            return meu_acesso(request, user_id=user_id, altera='chng_mail', altera_erro='sim', form_erro=form)
            
    return redirect('dashboard')

def ativacao_email(request, *args, **kwargs):
    try:
        uid_b64 = urlsafe_base64_decode(kwargs['uidb64']) # Converte URLBASE64 para BASE64
        uid_bytes = base64.b64decode(uid_b64) # Converte BASE64 para BYTES
        uid = int(force_str(uid_bytes)) # Converte BYTES para STR, e de STR para INT
        usuario = get_object_or_404(User, pk=uid)
    except Exception as e:
        usuario = None

    if usuario and generate_token.check_token(usuario, kwargs['token']):
        classificacao = get_object_or_404(Classificacao, user=usuario)
        classificacao.email_ativado = True
        classificacao.save()

        if request.user.is_authenticated:
            return redirect('abre_meu_acesso_mensagem', mensagem='activation_success', user_id=uid)
        else:
            return render(request, 'authentication/authentication_success.html')

    return render(request, 'authentication/authentication_failed.html')

def salva_assinatura(request, **kwargs):
    usuario = get_object_or_404(User, pk=kwargs['user_id'])
    classificacao = get_object_or_404(Classificacao, user=usuario)
    if request.method == 'POST':
        imagem = request.POST['canvasData']
        format, imgstr = imagem.split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr)) 
        file_name = "'mysign." + ext
        classificacao.assinatura.save(file_name, data, save=True) 
        
        return redirect('abre_meu_acesso', user_id=kwargs['user_id'])

    return redirect('dashboard')

def remove_assinatura(request, **kwargs):
    usuario = get_object_or_404(User, pk=kwargs['user_id'])
    classificacao = get_object_or_404(Classificacao, user=usuario)
    if request.method == 'POST':
        classificacao.assinatura.delete()
        classificacao.save()
        
        return redirect('abre_meu_acesso', user_id=kwargs['user_id'])

    return redirect('dashboard')

# @usuario_nao_autenticado
def login(request, mensagem=''):
            
    if mensagem == 'Vazio':
            messages.error(request, 'Preencha os campos vazios')
    if mensagem == 'Falhou':
        messages.error(request, 'Usuário ou senha incorretos')
    
    if request.method == 'POST':
        Usuario = request.POST['username']
        Senha = request.POST['senha']

        if not Usuario.strip() or not Senha.strip() :      
            var_mensagem = 'Vazio'
            return redirect('fazendo_login_mensagem', mensagem=var_mensagem)

        if User.objects.filter(username=Usuario).exists(): 
            Nome = User.objects.filter(username=Usuario).values_list('username', flat=True).get()
            # print(Nome)
        
            user = auth.authenticate(request, username=Nome, password=Senha)

            if user is not None:
                auth.login(request, user)
                print('login realizado com sucesso')
                return redirect('dashboard')
            else:
                var_mensagem='Falhou'
                return redirect('fazendo_login_mensagem', mensagem=var_mensagem)
                
        else:
            var_mensagem='Falhou'
            return redirect('fazendo_login_mensagem', mensagem=var_mensagem)
    
    return render(request, 'index.html')

def dashboard(request):
    from plano_de_acao.alteracoes import define_planos_coordenador, define_planos_corretor
    escolas_sem_diretor=''
    marcados_exclusao=''
    planos=''
    atualizacoes=[]
    dias = 7

    grupo = request.user.groups.get().name
    cargo = request.user.classificacao.cargo_herdado

    # Por prioridade
    # Por ordem de tempo
    # Limitado a 7 dias de modificado
    if grupo == 'Func_sec':

        if cargo == 'Diretor SUPROT':
            # diretores escolares marcados para exclusão (prioridade)
            marcados_exclusao = Classificacao.objects.filter(cargo_herdado='Diretor(a)').filter(marcado_para_exclusao=True).filter(is_active=True)
            #escolas sem diretor
            escolas_sem_diretor = Escola.objects.filter(possui_diretor=False).filter(is_active=True)
            # planos assinados pela escola relevantes para o usuario
            planos = Plano_de_acao.objects.order_by('-ultima_modificacao').filter(ultima_modificacao__gte=date.today() - timedelta(days=dias)).filter(Q(situacao='Assinado') | Q(situacao='Inteiramente assinado'))
            # planos = Plano_de_acao.objects.order_by('-ultima_modificacao').filter(ultima_modificacao__gte=date.today() - timedelta(days=dias))

            for item in marcados_exclusao:
                atualizacoes.append(item)
            for item in escolas_sem_diretor:
                atualizacoes.append(item)
            for item in planos:
                atualizacoes.append(item)

        if cargo == 'Coordenador':
            #escolas sem diretor
            escolas_sem_diretor = Escola.objects.filter(possui_diretor=False).filter(is_active=True)
            planos = define_planos_coordenador(request)

            for item in escolas_sem_diretor:
                atualizacoes.append(item)
            for item in planos:
                atualizacoes.append(item)

        if cargo == 'Corretor (Técnico)':
            planos = define_planos_corretor(request)

            for item in planos:
                atualizacoes.append(item)
        
    elif grupo == 'Diretor_escola':
        matriz = request.user.classificacao.escola
        planos = Plano_de_acao.objects.order_by('-ultima_modificacao').filter(ultima_modificacao__gte=date.today() - timedelta(days=dias)).filter(escola=matriz).filter(Q(situacao='Pendente') | Q(situacao='Aprovado') | Q(situacao='Necessita correção') | Q(situacao='Finalizado'))
        for item in planos:
            atualizacoes.append(item)
    elif grupo == 'Funcionario':
        matriz = request.user.classificacao.escola
        planos = Plano_de_acao.objects.order_by('-ultima_modificacao').filter(ultima_modificacao__gte=date.today() - timedelta(days=dias)).filter(escola=matriz).filter(Q(situacao='Pendente') | Q(situacao='Aprovado') | Q(situacao='Necessita correção') | Q(situacao='Finalizado'))
        for item in planos:
            atualizacoes.append(item)

    # Configura paginator
    paginator_planos = Paginator(atualizacoes, 4)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)
    ##########################################################################    
    
    contexto = {
        'chave_atualizacoes' : page,
    }
    
    return render(request, 'dashboard.html', contexto)

def logout(request):
    auth.logout(request)
    return redirect('fazendo_login')

# def altera_nome(request, **kwargs):
#     if request.method == 'POST':
#         form = FormAlteraLogin(request.POST)
#         usuario = get_object_or_404(User, pk=kwargs['user_id'])
#         if form.is_valid():
#             valor = form.cleaned_data.get('first_name')
#             usuario.first_name = valor
#             usuario.save()
            
#             return redirect('abre_meu_acesso', user_id=kwargs['user_id'])
#         else:
#             return meu_acesso(request, user_id=kwargs['user_id'], altera='alt_login', altera_erro='sim', form_erro=form)
    
#     return redirect('dashboard')


