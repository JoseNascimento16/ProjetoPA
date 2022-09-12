from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .utils import generate_token
import base64


def envia_email_ativacao(request, user, var_email):
    site_atual = get_current_site(request)
    forcebytes_uid = force_bytes(user.id) # Converte INT para BYTES
    bytes_to_b64  = base64.b64encode(forcebytes_uid) # Converte BYTES para BASE64
    uidb64_urlsafe = urlsafe_base64_encode(bytes_to_b64 ) # Converte BASE64 para URLSAFE_BASE64

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