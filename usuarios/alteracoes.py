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
        funcionarios_membros = Classificacao.objects.filter(cargo_herdado='Membro do colegiado').filter(is_active=True)
        escola.quant_membro_colegiado = len(funcionarios_membros)
        escola.save()
    elif funcionario_classificacao.cargo_herdado == 'Tesoureiro(a)':
        escola.possui_tesoureiro = False
        escola.save()
