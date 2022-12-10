from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from usuarios.models import Classificacao
from Escolas.models import Escola
from django.shortcuts import get_object_or_404
from .utils import generate_token
import base64


def identifica_diretor(escola_id):
    # FUNÇÃO QUE CAPTURA O DIRETOR ATUAL DA ESCOLA
    # SE HOUVER
    diretor=''
    escola = get_object_or_404(Escola, pk=escola_id)
    if escola.diretor:
        diretor = escola.diretor    
    return diretor

def converteINT_b64_urlsafe(user_id):
    forcebytes_uid = force_bytes(user_id) # Converte INT para BYTES
    bytes_to_b64  = base64.b64encode(forcebytes_uid) # Converte BYTES para BASE64
    uidb64_urlsafe = urlsafe_base64_encode(bytes_to_b64 ) # Converte BASE64 para URLSAFE_BASE64

    return uidb64_urlsafe

def envia_email_ativacao(request, user, var_email):
    # ENVIA UM EMAIL PARA ATIVAÇÃO DE EMAIL
    site_atual = get_current_site(request)

    uidb64_urlsafe = converteINT_b64_urlsafe(user.id)

    contexto = {
        'user' : user.first_name,
        'domain' : site_atual,
        'uid' : uidb64_urlsafe,
        'token' : generate_token.make_token(user)
    }

    subject = 'SIPA - Ativação do seu e-mail'
    message = render_to_string('authentication/email-ativacao.txt', contexto)
    remetente = settings.EMAIL_HOST_USER
    destinatario = var_email

    send_mail(subject, message, remetente, [destinatario], fail_silently=False)

def atualiza_quant_funcionarios_da_escola(escola):
    quantidade_funcionarios = Classificacao.objects.filter(escola=escola).filter(is_active=True)
    escola.quant_funcionarios = len(quantidade_funcionarios)
    escola.save()

def retorna_quant_funcionarios_da_escola(escola):
    quantidade_funcionarios = Classificacao.objects.filter(tipo_de_acesso='Funcionario').filter(escola=escola).filter(is_active=True)
    return len(quantidade_funcionarios)

def checa_se_possui_tesoureiro_e_atualiza(escola):
    escola = get_object_or_404(Escola, pk=escola.id)
    tesoureiro = Classificacao.objects.filter(escola=escola).filter(cargo_herdado='Tesoureiro(a)').filter(is_active=True)
    if tesoureiro.exists():
        escola.possui_tesoureiro = True
    else:
        escola.possui_tesoureiro = False

    return escola.possui_tesoureiro

def checa_membros_colegiado_e_atualiza(escola):
    escola = get_object_or_404(Escola, pk=escola.id)
    quant_membros = Classificacao.objects.filter(escola=escola).filter(cargo_herdado='Membro do colegiado').filter(is_active=True)
    return len(quant_membros)

def atualiza_cargos_da_matriz_cadastro(cargo, escola):
    if cargo == 'Membro do colegiado':
        funcionarios_membros = Classificacao.objects.filter(cargo_herdado='Membro do colegiado').filter(is_active=True)
        escola.quant_membro_colegiado = len(funcionarios_membros)
        escola.save()
    elif cargo == 'Tesoureiro(a)':
        escola.possui_tesoureiro = True
        escola.save()

def atualiza_cargos_da_matriz_exclusao(funcionario_classificacao, escola):
    if funcionario_classificacao.cargo_herdado == 'Membro do colegiado':
        # PODEM HAVER MAIS DE UM MEMBRO DO COLEGIADO
        funcionarios_membros = Classificacao.objects.filter(cargo_herdado='Membro do colegiado').filter(is_active=True)
        escola.quant_membro_colegiado = len(funcionarios_membros)
        escola.save()
    elif funcionario_classificacao.cargo_herdado == 'Tesoureiro(a)':
        # SO PODE HAVER 1 TESOUREIRO
        escola.possui_tesoureiro = False
        escola.save()

def checa_usuario_unico(nome_usuario):
    # Checa se nome de usuario criado ja existe
    nome_de_usuario = User.objects.filter(username=nome_usuario)
    if nome_de_usuario.exists():
        return True
    else:
        return False

def envia_email_new_user(request, novo_usuario, password):
    # ENVIA UM EMAIL INFORMANDO USUARIO E SENHA DO USUARIO RECEM CRIADO
    site_atual = get_current_site(request)

    contexto = {
        'first_name' : novo_usuario.first_name,
        'user' : novo_usuario.username,
        'password' : password,
        'domain' : site_atual,
    }

    subject = 'SIPA - Usuário cadastrado'
    message = render_to_string('authentication/novo-usuario.txt', contexto)
    remetente = settings.EMAIL_HOST_USER
    destinatario = novo_usuario.email

    send_mail(subject, message, remetente, [destinatario], fail_silently=False)