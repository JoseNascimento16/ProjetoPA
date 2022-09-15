from base64 import b64decode, urlsafe_b64decode
from multiprocessing import context
from django.core.files.base import ContentFile
import base64
import io
from PIL import Image
from tkinter import Image
from django.dispatch import Signal
from plano_de_acao.alteracoes import atualiza_assinaturas_escola
from usuarios.alteracoes import envia_email_ativacao
from usuarios.models import Classificacao, Turmas, Usuario
from usuarios.forms import FuncionariosForm, TurmasForm, EscolasForms, FuncionariosSecretariaForm, AlteraCargoForm, FormAlteraNome, FormAlteraMail
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from plano_de_acao.models import Plano_de_acao
from usuarios.pesquisas import pesquisa_escolas_cadastradas, pesquisa_funcionarios_cadastrados
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django import forms
from .utils import generate_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from.decorators import usuario_nao_autenticado



# Create your views here.

@login_required
def cadastros_secretaria(request, user_id, mensagem='', cad_funcionarios='', search='', retorno_altera_cargo=''): # Pagina de cadastros quando o usuario é da Secretaria
    from .forms_campos import campo_cargo_func_sec
    usuario = get_object_or_404(User, pk=user_id)
    tipo_usuario = usuario.classificacao.tipo_de_acesso
    controle_form_cadastro_escolas = False
    controle_form_cadastro_funcionarios = False
    form_escolas = EscolasForms()
  
    checa_usuario = request.user
    tipo_usuario_logado = checa_usuario.classificacao.tipo_de_acesso

    if tipo_usuario == 'Secretaria' or tipo_usuario == 'Func_sec':
        
        if not cad_funcionarios: # Cadastro de escolas
            var_pesquisa_escola = False

            if mensagem == 'Criou':
                messages.success(request, 'Escola cadastrada com sucesso!')
            if mensagem == 'Deletou':
                messages.success(request, 'Escola excluída com sucesso!')

            if not search:
                if request.method == 'POST':
                    form_escolas = EscolasForms(request.POST)
                    if form_escolas.is_valid():
                        last_form = form_escolas.cleaned_data.get('last_name')
                        muni_form = form_escolas.cleaned_data.get('municipio')
                        codigo_form = form_escolas.cleaned_data.get('codigo_escola')
                        nte_form = form_escolas.cleaned_data.get('nte')
                        first_form = form_escolas.cleaned_data.get('first_name')
                        user_form = form_escolas.cleaned_data.get('username')
                        pass_form = form_escolas.cleaned_data.get('password')
                        pass_form2 = form_escolas.cleaned_data.get('password2')

                        user = User.objects.create_user(
                        username=user_form,
                        first_name=first_form,
                        last_name=last_form,
                        email='',
                        password=pass_form2)
                        user.save()

                        usuario_cadastrado = User.objects.get(username=user_form)
                        classificacao = Classificacao.objects.create(
                        user=usuario_cadastrado,
                        tipo_de_acesso='Escola',
                        municipio=muni_form,
                        codigo_escola=codigo_form,
                        nte=nte_form, quant_funcionarios=1
                        )
                        classificacao.save()

                        # PODE-SE FAZER ISSO VIA SIGNALS

                        return redirect('cadastrar_escolas_mensagem', user_id=user_id, mensagem='Criou') #id da secretaria
                    else:
                        controle_form_cadastro_escolas = True

            escolas_cadastradas = Classificacao.objects.filter(tipo_de_acesso='Escola').filter(is_active=True)

            if search:
                escolas_cadastradas = pesquisa_escolas_cadastradas(request)
                var_pesquisa_escola = True

            dados_a_exibir = {
                'chave_tipo_usuario' : tipo_usuario_logado,
                'escolas_a_exibir': escolas_cadastradas,
                'contexto_extra': controle_form_cadastro_escolas,
                'chave_form_cadastro_escolas': form_escolas,
                'contexto_extra_form_escolas': controle_form_cadastro_escolas,
                'chave_var_pesquisa_escola' : var_pesquisa_escola,
            }
            return render(request, 'cadastros-secretaria.html', dados_a_exibir)

        elif cad_funcionarios: # Cadastro de funcionarios
            if request.user.classificacao.usuario_diretor or request.user.classificacao.usuario_coordenador or tipo_usuario == 'Secretaria':
                form_funcionarios = ''
                funcionarios_cadastrados = ''
                var_pesquisa_func = False
                

                # funcionarios_cadastrados = Classificacao.objects.filter(tipo_de_acesso='Func_sec')
                
                if mensagem == 'Criou':
                    messages.success(request, 'Funcionário cadastrado com sucesso!')
                if mensagem == 'Deletou':
                    messages.success(request, 'Funcionário excluído com sucesso!')
                if mensagem == 'Sucesso':
                    messages.success(request, 'Alteração efetuada com sucesso!')
                if mensagem == 'Erro':
                    messages.error(request, 'Erro! Você não pode alterar o seu próprio status!')
                
                if not search:

                    form = campo_cargo_func_sec(request, tipo_usuario)

                    form_funcionarios = form

                    if request.method == 'POST':
                        form_funcionarios = FuncionariosSecretariaForm(request.POST)
                        if form_funcionarios.is_valid():
                            instancia_form = form_funcionarios.save(commit=False)
                            cargo1 = form_funcionarios.cleaned_data.get('cargo')
                            # var_assina = form_funcionarios.cleaned_data.get('assina')
                            
                            user = User.objects.create_user(
                                username=instancia_form.username,
                                first_name=instancia_form.first_name,
                                last_name=cargo1,
                                email='',
                                password=instancia_form.password)
                            # user.save()
                            
                            nome = form_funcionarios.cleaned_data.get('username')
                            usuario_objeto = get_object_or_404(User, username=nome) # Usuario recem criado

                            if tipo_usuario == 'Func_sec':
                                classif_user_atual=get_object_or_404(Classificacao, user_id=user_id)
                                matriz_last_name = classif_user_atual.matriz

                            else:
                                matriz_objeto = get_object_or_404(User, pk=user_id)
                                matriz_last_name = matriz_objeto.last_name

                            if cargo1 == 'Corretor (Técnico)':
                                classificacao = Classificacao.objects.create(user=usuario_objeto, tipo_de_acesso='Func_sec', assina_plano=False, matriz=matriz_last_name)
                            if cargo1 == 'Coordenador':
                                classificacao = Classificacao.objects.create(user=usuario_objeto, tipo_de_acesso='Func_sec', assina_plano=False, usuario_coordenador=True, matriz=matriz_last_name)
                            if cargo1 == 'Diretor':
                                classificacao = Classificacao.objects.create(user=usuario_objeto, tipo_de_acesso='Func_sec', assina_plano=True, usuario_diretor=True, matriz=matriz_last_name)
                            # Um signal pre_save é gerado
                            classificacao.save()

                            classificacao_da_matriz = get_object_or_404(Classificacao, tipo_de_acesso='Secretaria')
                            quant_func_secs = Classificacao.objects.filter(tipo_de_acesso='Func_sec')
                            classificacao_da_matriz.quant_funcionarios = len(quant_func_secs)
                            classificacao_da_matriz.save()


                            print('formulario valido, SALVOU!!!')

                            return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=user_id, mensagem='Criou', cad_funcionarios='Sim')

                        else:
                            print('formulario INVALIDO!!!')
                            controle_form_cadastro_funcionarios = True
            else:
                return redirect('dashboard')

            funcionarios_cadastrados = Classificacao.objects.order_by('-user__last_name').filter(tipo_de_acesso='Func_sec').filter(is_active=True)
            

            if search:
                print('PESQUISA FUNCIONÁRIOS CADASTRADOS')
                funcionarios_cadastrados = pesquisa_funcionarios_cadastrados(request)
                var_pesquisa_func = True

            dados_a_exibir = {

                'chave_form_cadastro_funcionarios' : form_funcionarios,
                'funcionarios_a_exibir' : funcionarios_cadastrados,
                'contexto_extra_form_funcionarios': controle_form_cadastro_funcionarios,
                'chave_tipo_usuario' : tipo_usuario_logado,
                'chave_cad_funcionarios' : cad_funcionarios,
                'chave_var_pesquisa_func' : var_pesquisa_func,
            }

            if not retorno_altera_cargo:
                return render(request, 'cadastros-secretaria.html', dados_a_exibir)
            else:
                return dados_a_exibir

    return redirect('dashboard')

@login_required
def cadastros_escola(request, user_id, mensagem=''):
    usuario = get_object_or_404(User, pk=user_id)
    tipo_usuario = usuario.classificacao.tipo_de_acesso
    controle_form_cadastro_funcionarios = False

    checa_usuario = request.user
    tipo_usuario_logado = checa_usuario.classificacao.tipo_de_acesso

    if mensagem == 'Criou':
        messages.success(request, 'Funcionário cadastrado com sucesso!')
    if mensagem == 'Deletou':
        messages.success(request, 'Funcionário excluído com sucesso!')

    if tipo_usuario == 'Escola':
        # controle = False
        form_funcionarios = FuncionariosForm(initial={'cargo': '-------'})

        if request.method == 'POST':
            form_funcionarios = FuncionariosForm(request.POST)
            if form_funcionarios.is_valid():
                instancia_form = form_funcionarios.save(commit=False)
                cargo1 = form_funcionarios.cleaned_data.get('cargo')
                
                #cria objeto usuario
                User.objects.create_user(
                    username=instancia_form.username,
                    first_name=instancia_form.first_name,
                    last_name=cargo1,
                    email='',
                    password=instancia_form.password)
                
                nome = form_funcionarios.cleaned_data.get('username')
                usuario_objeto = get_object_or_404(User, username=nome)

                matriz_objeto = get_object_or_404(User, pk=user_id)
                matriz_last_name = matriz_objeto.last_name

                #Cria objeto classificacao
                Classificacao.objects.create(user=usuario_objeto, tipo_de_acesso='Funcionario', cargo_herdado=cargo1, matriz=matriz_last_name, quant_funcionarios=0)
                
                # Atualiza quant. funcionarios da matriz
                classificacao_da_matriz = get_object_or_404(Classificacao, user_id=user_id)
                quant_funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=matriz_last_name).filter(is_active=True)
                classificacao_da_matriz.quant_funcionarios = len(quant_funcionarios)
                classificacao_da_matriz.save()

                print('formulario valido, SALVOU!!!')

                return redirect('cadastrar_funcionarios_mensagem', user_id=user_id, mensagem='Criou')

            else:
                print('formulario INVALIDO!!!')
                controle_form_cadastro_funcionarios = True

        funcionarios_cadastrados = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=usuario.last_name).filter(is_active=True)
        
        dados_a_exibir = {

            'chave_form_cadastro_funcionarios' : form_funcionarios,
            'funcionarios_a_exibir' : funcionarios_cadastrados,
            'contexto_extra_form_funcionarios': controle_form_cadastro_funcionarios,
            'chave_tipo_usuario' : tipo_usuario_logado,
        }

        return render(request, 'cadastros.html', dados_a_exibir)

    return redirect('dashboard')

def deleta_funcionario(request, elemento_id):
    from plano_de_acao.alteracoes import reduz_assinatura

    usuario_logado = request.user
    tipo_usuario = usuario_logado.classificacao.tipo_de_acesso

    # planos = Plano_de_acao.objects.filter(usuario=escola)
    if tipo_usuario == 'Escola':

        planos = Plano_de_acao.objects.filter(usuario=usuario_logado)

        funcionario_classificacao = get_object_or_404(Classificacao, pk=elemento_id)
        funcionario_id = funcionario_classificacao.user.id
        funcionario_objeto = get_object_or_404(User, pk=funcionario_id)
        funcionario_objeto.is_active = False
        funcionario_objeto.email = ''
        funcionario_classificacao.is_active = False
        funcionario_classificacao.email_ativado = False
        if funcionario_classificacao.assinatura:
            funcionario_classificacao.assinatura.delete()
        funcionario_objeto.save()
        funcionario_classificacao.save()

        id_do_usuario = request.user.id
        classificacao_da_matriz = get_object_or_404(Classificacao, user_id=id_do_usuario)
        quantidade_funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(matriz=request.user.last_name).filter(is_active=True)
        classificacao_da_matriz.quant_funcionarios = len(quantidade_funcionarios)
        classificacao_da_matriz.save()
        
        # Remove assinaturas e atualiza
        for plano in planos:
            if plano.situacao != 'Finalizado':
                funcionario_classificacao.plano_associado.remove(plano) # Remove qualquer associação com planos que este usuario tiver
                atualiza_assinaturas_escola(plano.id)

        # funcionario_objeto.delete()

        return redirect('cadastrar_funcionarios_mensagem', user_id=usuario_logado.id, mensagem='Deletou')
    
    if tipo_usuario == 'Secretaria' or tipo_usuario == 'Func_sec' and usuario_logado.classificacao.usuario_diretor == True:
        # planos = Plano_de_acao.objects.filter(usuario=escola)

        # Desativa classificação Func_sec,escolas,funcionarios (inativação)
        objeto_classificacao = get_object_or_404(Classificacao, pk=elemento_id)
        objeto_classificacao.is_active = False
        objeto_classificacao.email_ativado = False
        objeto_classificacao.assina_plano = False
        objeto_classificacao.usuario_diretor = False
        objeto_classificacao.usuario_coordenador = False
        if objeto_classificacao.assinatura:
            objeto_classificacao.assinatura.delete()
        objeto_classificacao.save()

        # exclusão de Func_sec,escolas,funcionarios (inativação)
        funcionario_id = objeto_classificacao.user.id
        usuario_objeto = get_object_or_404(User, pk=funcionario_id)
        usuario_objeto.is_active = False
        usuario_objeto.email = ''
        usuario_objeto.save()

        # atualiza quant_func da matriz
        if objeto_classificacao.tipo_de_acesso == 'Func_sec':
            classificacao_da_matriz = get_object_or_404(Classificacao, tipo_de_acesso='Secretaria')
            quant_func_secs = Classificacao.objects.filter(tipo_de_acesso='Func_sec').filter(is_active=True)
            classificacao_da_matriz.quant_funcionarios = len(quant_func_secs)
            classificacao_da_matriz.save()

        # Exclui(desativa) também todos os funcionários da escola e suas classificações (inativação)
        if objeto_classificacao.tipo_de_acesso == 'Escola':
            funcionarios_da_escola = Classificacao.objects.filter(matriz=usuario_objeto.last_name)
            for item in funcionarios_da_escola:
                item.is_active = False
                item.email_ativado = False
                item.assina_plano = False
                item.usuario_diretor = False
                item.usuario_coordenador = False
                if item.assinatura:
                    item.assinatura.delete()
                item.save()
                funcionario_objeto = get_object_or_404(User, first_name=item.user.first_name )
                funcionario_objeto.is_active = False
                funcionario_objeto.email = ''
                funcionario_objeto.save()

        id_do_usuario = request.user.id
        return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=usuario_logado.id, mensagem='Deletou', cad_funcionarios='Sim')

    else:
        return redirect('dashboard')        

def altera_cargo(request, elemento_id, edita=''):
    checa_usuario = request.user
    tipo_usuario_logado = checa_usuario.classificacao.tipo_de_acesso
    if tipo_usuario_logado == 'Secretaria' or checa_usuario.classificacao.usuario_diretor:
        if not edita:
            altera_cargo = True
            form = AlteraCargoForm()

            contexto = cadastros_secretaria(request, user_id=checa_usuario.id, cad_funcionarios=True, retorno_altera_cargo=True)
            contexto['chave_form_altera_cargo'] = form
            contexto['chave_altera_cargo'] = altera_cargo
            contexto['chave_elemento_id'] = elemento_id
            return render(request, 'cadastros-secretaria.html', contexto)

        else:
            usuario = request.user.id
            form = AlteraCargoForm(request.POST)
            classificacao_func = get_object_or_404(Classificacao, pk=elemento_id)
            if classificacao_func == request.user.classificacao:
                return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=request.user.id, cad_funcionarios='sim', mensagem='Erro')
            if request.method == 'POST':
                if form.is_valid():
                    valor_campo = form.cleaned_data.get('campo')
                    if valor_campo == 'Coordenador':
                        print('entrou coordenador')
                        classificacao_func.assina_plano = False
                        classificacao_func.usuario_coordenador = True
                        classificacao_func.user.last_name = 'Coordenador'
                        classificacao_func.save()
                        classificacao_func.user.save()
                    else:
                        print('entrou corretor')
                        classificacao_func.assina_plano = False
                        classificacao_func.usuario_coordenador = False
                        classificacao_func.user.last_name = 'Corretor (Técnico)'
                        classificacao_func.save()
                        classificacao_func.user.save()

                    # GERAR LOG

                    return redirect('cadastrar_funcionarios_secretaria_mensagem', user_id=request.user.id, cad_funcionarios='sim', mensagem='Sucesso')

    return redirect('dashboard')   

@login_required
def cadastro_turmas(request, user_id, abre_form='', mensagem=''):
    controle_turmas = False
    checa_usuario = request.user
    tipo_usuario = checa_usuario.classificacao.tipo_de_acesso
    if tipo_usuario == 'Escola':

        if abre_form:
            controle_turmas = True

        form_turmas = TurmasForm()
        usuario = get_object_or_404(User, pk=user_id)
        
        if mensagem == 'Criou':
            messages.success(request, 'Turma criada com sucesso!')
        elif mensagem == 'Deletou':
            messages.success(request, 'Turma excluída com sucesso!')

        if request.method == 'POST':
            form_turmas = TurmasForm(request.POST)
            if form_turmas.is_valid():
                nome1 = form_turmas.cleaned_data.get('nome')
                qt_aluno = form_turmas.cleaned_data.get('quantidade_alunos')
                turma = Turmas.objects.create(
                    user = usuario,
                    nome = nome1,
                    quantidade_alunos = qt_aluno
                )
                turma.save()
                
                return redirect('cadastrando_turmas_mensagem', user_id=user_id, mensagem='Criou')
            else:
                controle_turmas = True

        turmas_cadastradas = Turmas.objects.order_by('nome').filter(user=usuario).filter(is_active=True)
        
        turmas_a_exibir = {
            'chave_user_id' : usuario,
            'chave_form_cadastro_turmas' : form_turmas,
            'chave_turmas_cadastradas' : turmas_cadastradas,
            'contexto_extra_turmas' : controle_turmas,
            'chave_tipo_usuario' : tipo_usuario,
        }
        
        return render(request, 'cadastro_turmas.html', turmas_a_exibir)

    return redirect('dashboard')

def deleta_turma(request, turma_id):
    tipo_usuario = request.user.classificacao.tipo_de_acesso
    turma_objeto = get_object_or_404(Turmas, id=turma_id)
    if tipo_usuario == 'Escola' and turma_objeto.user == request.user:
        if turma_objeto.plano_associado.exists():
            print('ACHOU PLANO, TORNOU INATIVA')
            turma_objeto.is_active = False
            turma_objeto.save()
        else:
            turma_objeto.delete()
            print('NÃO ACHOU NADA, APAGOU')

        id_do_usuario = request.user.id
        return redirect('cadastrando_turmas_mensagem', user_id=id_do_usuario, mensagem='Deletou')

    return redirect('dashboard')

@usuario_nao_autenticado
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

@login_required
def dashboard(request):
    # if request.user.is_authenticated:
    return render(request, 'dashboard.html')
    # else:
    #     print('Você está deslogado, faça o login novamente')
    #     return redirect('fazendo_logout')

def meu_acesso(request, user_id, mensagem='', altera='', altera_erro='', form_erro='', mail=''):
    abre_modal = False
    abre_modal_sign = False
    abre_modal_mail = False
    form = ''
    form2 = ''
    usuario = request.user.classificacao.tipo_de_acesso

    if mensagem == 'success':
            messages.success(request, 'Alteração efetuada com sucesso!')
    elif mensagem == 'sent_activation':
            messages.warning(request, 'Verifique sua caixa de entrada para confirmar o seu e-mail!')
    elif mensagem == 'activation_success':
            messages.success(request, 'E-mail ativado com sucesso!')
    elif mensagem == 'mail_removed':
            messages.success(request, 'E-mail removido com sucesso!')

    if altera == 'alt_name':
        abre_modal = True
        if not altera_erro:
            form = FormAlteraNome()
        else:
            form = form_erro

    elif altera == 'alt_sign':
        abre_modal_sign = True

    elif altera == 'chng_mail':
        abre_modal_mail = True
        if not altera_erro:
            form2 = FormAlteraMail()
            form2 = FormAlteraMail(prefix='qualquer') 
            form2.fields['email'].initial = request.user.email
        else:
            form2 = form_erro
        
    else:
        form = ''
    contexto = {
        'chave_tipo_usuario' : usuario,
        'chave_abre_altera_nome':abre_modal,
        'chave_abre_altera_assinatura':abre_modal_sign,
        'chave_abre_altera_mail' : abre_modal_mail,
        'chave_form_altera_nome':form,
        'chave_form_altera_mail':form2,
    }

    return render(request, 'profile.html', contexto)

def altera_nome(request, user_id):
    if request.method == 'POST':
        form = FormAlteraNome(request.POST)
        usuario = get_object_or_404(User, pk=user_id)
        if form.is_valid():
            valor = form.cleaned_data.get('first_name')
            print(type(valor))
            usuario.first_name = valor
            usuario.save()
            return meu_acesso(request, user_id)
        else:
            return meu_acesso(request, user_id, altera='alt_name', altera_erro='sim', form_erro=form)
    
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
    
@login_required
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
            return meu_acesso(request, user_id, altera='chng_mail', altera_erro='sim', form_erro=form)

def ativacao_email(request, uidb64, token):
    try:
        uid_b64 = urlsafe_base64_decode(uidb64) # Converte URLBASE64 para BASE64
        uid_bytes = base64.b64decode(uid_b64) # Converte BASE64 para BYTES
        uid = int(force_str(uid_bytes)) # Converte BYTES para STR, e de STR para INT
        usuario = get_object_or_404(User, pk=uid)
    except Exception as e:
        usuario = None

    if usuario and generate_token.check_token(usuario, token):
        classificacao = get_object_or_404(Classificacao, user=usuario)
        classificacao.email_ativado = True
        classificacao.save()

        if request.user.is_authenticated:
            return redirect('abre_meu_acesso_mensagem', mensagem='activation_success', user_id=uid)
        else:
            return render(request, 'authentication/authentication_success.html')

    return render(request, 'authentication/authentication_failed.html')

def envia_email(request):
    contexto = {
        'nome' : request.user.first_name
    }
    subject = 'Assunto do email'
    message = render_to_string('teste-email.txt', contexto)
    remetente = settings.EMAIL_HOST_USER
    destinatario = request.user.email

    try:
        send_mail(subject, message, remetente, [destinatario], fail_silently=False)

        # print('enviou email!')
        return redirect('abre_meu_acesso', user_id=request.user.id)
        
    except BadHeaderError:
	    return HttpResponse('Invalid header found.')

def salva_assinatura(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    classificacao = get_object_or_404(Classificacao, user=usuario)
    if request.method == 'POST':
        form = request.POST
        print(form)
        imagem = request.POST['canvasData']
        format, imgstr = imagem.split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr)) 
        file_name = "'mysign." + ext
        classificacao.assinatura.save(file_name, data, save=True) 
        
        return redirect('abre_meu_acesso', user_id=user_id)

    return redirect('dashboard')

def remove_assinatura(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    classificacao = get_object_or_404(Classificacao, user=usuario)
    if request.method == 'POST':
        classificacao.assinatura.delete()
        classificacao.save()
        
        return redirect('abre_meu_acesso', user_id=user_id)

    return redirect('dashboard')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('fazendo_login')




