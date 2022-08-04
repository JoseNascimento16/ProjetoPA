from logs.pesquisas import pesquisa_log_plano_escola, pesquisa_log_plano_func_sec
from usuarios.models import Classificacao, Turmas # Turmas_plano
from codigos.models.codigos import ModeloCodigos
from Ordens.models import Ordens, ControleOrdens
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

@login_required
def log_planos(request, search=''): # pagina listando todos os planos de ação possíveis de serem vistos
    valor_pesquisa = ''
    id = request.user.id
    checa_usuario = request.user
    escola_matriz = checa_usuario.classificacao.matriz
    # entidade_escola = get_object_or_404(User, last_name=escola_matriz)

    if checa_usuario.classificacao.tipo_de_acesso == 'Secretaria' or checa_usuario.classificacao.tipo_de_acesso == 'Func_sec' :
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(~Q(situacao='Em desenvolvimento'))

        if search:
            planos = pesquisa_log_plano_func_sec(request)
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')

    elif checa_usuario.classificacao.tipo_de_acesso == 'Escola':
        
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=id).filter(~Q(situacao='Em desenvolvimento'))

        if search:
            planos = pesquisa_log_plano_escola(request)
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')

    elif checa_usuario.classificacao.tipo_de_acesso == 'Funcionario':
        
        entidade_escola = get_object_or_404(User, last_name=escola_matriz)
        planos = Plano_de_acao.objects.order_by('-data_de_criação').filter(usuario=entidade_escola).filter(~Q(situacao='Em desenvolvimento'))

        if search:
            planos = pesquisa_log_plano_escola(request)
            if request.method == 'POST':
                valor_pesquisa = request.POST['campo']
            else:
                valor_pesquisa = request.GET.get('q','')

    paginator_planos = Paginator(planos, 10)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    dados = {
        'chave_log_planos' : page,
        'chave_var_pesquisa' : search,
        'chave_valor_pesquisa' : valor_pesquisa,
    }

    return render(request, 'log_planos_de_acao.html', dados)

@login_required
def chama_log_plano(request, elemento_id):
    plano = get_object_or_404(Plano_de_acao, pk=elemento_id)

    log_do_plano = Event.objects.order_by('-timestamp').filter(plano_base=plano.id) # A variavel plano_base é tipo integer, portanto tenho que filtrar pelo id do plano.

    paginator_planos = Paginator(log_do_plano, 10)
    page_number = request.GET.get('page')
    page = paginator_planos.get_page(page_number)

    dados = {
        'instancia_plano' : plano,
        'log_plano' : page
    }

    return render(request, 'log_plano.html', dados)