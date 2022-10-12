from Escolas.models import Escola
from logs.pesquisas import pesquisa_log_plano_escola, pesquisa_log_plano_func_sec
from usuarios.models import Classificacao, Turmas # Turmas_plano
from codigos.models.codigos import ModeloCodigos
from Ordens.models import Ordens
from Ordens.forms import OrdemForm
from plano_de_acao.forms import PlanoForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from plano_de_acao.models import Plano_de_acao
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Q
from eventlog import EventGroup
from eventlog.models import Event
from logs.logs import *

# Create your views here.

### VIEWS TESTADAS ###

def log_planos(request, **kwargs): # pagina listando todos os planos de ação possíveis de serem vistos
    valor_pesquisa = ''
    planos=''
    search=''
    checa_usuario = request.user
    tipo_usuario_logado = request.user.groups.get().name
    escola_matriz = request.user.classificacao.escola

    if tipo_usuario_logado == 'Secretaria' or tipo_usuario_logado == 'Func_sec' :
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(~Q(situacao='Em desenvolvimento'))
        
        if kwargs.get('search'):
            planos = pesquisa_log_plano_func_sec(request)
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')

    elif tipo_usuario_logado == 'Diretor_escola':
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=escola_matriz).filter(~Q(situacao='Em desenvolvimento'))

        if kwargs.get('search'):
            planos = pesquisa_log_plano_escola(request)
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')

    elif tipo_usuario_logado == 'Funcionario':
        
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(escola=escola_matriz).filter(~Q(situacao='Em desenvolvimento'))

        if kwargs.get('search'):
            planos = pesquisa_log_plano_escola(request)
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')

    paginator_planos = Paginator(planos, 10)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    if kwargs.get('search'):
        search = kwargs['search']

    dados = {
        'chave_log_planos' : page,
        'chave_var_pesquisa' : search,
        'chave_valor_pesquisa' : valor_pesquisa,
        'chave_achou_plano' : planos,
    }

    return render(request, 'log_planos_de_acao.html', dados)

def chama_log_plano(request, **kwargs):
    plano = get_object_or_404(Plano_de_acao, pk=kwargs['elemento_id'])

    log_do_plano = Event.objects.order_by('-timestamp').filter(plano_base=plano.id) # A variavel plano_base é tipo integer, portanto tenho que filtrar pelo id do plano.

    paginator_planos = Paginator(log_do_plano, 10)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    dados = {
        'instancia_plano' : plano,
        'log_plano' : page,
        'chave_existe_log' : log_do_plano,
    }

    return render(request, 'log_plano.html', dados)