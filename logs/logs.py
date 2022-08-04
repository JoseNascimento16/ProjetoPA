from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from plano_de_acao.models import Plano_de_acao
from plano_de_acao.views import *
from eventlog import EventGroup
from eventlog.models import Event

def log_plano_publicado(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi publicado.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_assinado(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi assinado.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_assinado_sec(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi assinado por um funcionário da Secretaria.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_enviado(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi enviado à Secretaria.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_re_enviado(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi corrigido e re-enviado à Secretaria.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_devolvido(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi devolvido à escola para correções.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_correcoes_concluidas(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Correções no plano "' + nome_plano + '" foram concluídas.', initiator=checa_usuario, plano_base=id_plano)

def log_pre_assinatura_permitida(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Assinaturas no plano "' + nome_plano + '" já foram permitidas.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_concluido(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi concluído e enviado à SUPROT.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_aprovado(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi aprovado pela Secretaria.', initiator=checa_usuario, plano_base=id_plano)

def log_plano_aprovado_auto(nome_plano, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" aprovado automaticamente (já assinado).', initiator='Sistema', plano_base=id_plano)

def log_plano_pronto(nome_plano, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" está pronto para ser concluído.', initiator='Sistema', plano_base=id_plano)

def log_plano_inteiramente_assinado(nome_plano, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" recebeu a ultima assinatura da Secretaria.', initiator='Sistema', plano_base=id_plano)

def log_plano_finalizado(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi finalizado (completo)!!', initiator=checa_usuario, plano_base=id_plano)

def log_plano_resetado(nome_plano, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "' + nome_plano + '" foi resetado (assinaturas removidas).', initiator=checa_usuario, plano_base=id_plano)

def log_nome_plano_alterado(nome_antigo, edita_ano_referencia, checa_usuario, id_plano):
    e = EventGroup()
    e.info('Plano "'+ nome_antigo +'" alterado para: "' + edita_ano_referencia + '"', initiator=checa_usuario, plano_base=id_plano)

def log_atribuiu_corretor(checa_corretor, checa_usuario, id_plano):
    e = EventGroup()
    e.info('"' + checa_corretor + '" se tornou o(a) corretor(a) do plano.', initiator=checa_usuario, plano_base=id_plano)

def log_alterou_corretor(checa_corretor, checa_usuario, id_plano):
    e = EventGroup()
    e.info('"' + checa_corretor + '" se tornou o(a) novo(a) corretor(a) do plano.', initiator=checa_usuario, plano_base=id_plano)

def log_removeu_corretor(checa_corretor, checa_usuario, id_plano):
    e = EventGroup()
    e.info('"' + checa_corretor + '" foi removido(a) como corretor(a) do plano.', initiator=checa_usuario, plano_base=id_plano)