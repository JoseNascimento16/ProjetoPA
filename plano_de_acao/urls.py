from django.urls import path
from . import views

urlpatterns = [
    
    path('acao/gerapdf/<int:plano_id>',views.gera_pdf, name='gera_pdf_acao'),

    # URLS + VIEWS TESTADAS
    path('planos_de_acao/main',views.planos_de_acao, name='pagina_planos_de_acao'),
    path('planos_de_acao/<int:elemento_id>/<slug:edita_plano>',views.planos_de_acao, name='abrindo_edicao_plano'),
    path('planos_de_acao/atribui/<int:elemento_id>/<slug:atribui>',views.planos_de_acao, name='abrindo_atribui_corretor'),
    path('planos_de_acao/<int:elemento_id>/alt_corretor/<slug:alt_corretor>',views.planos_de_acao, name='abrindo_altera_corretor'),
    path('plano/<int:elemento_id>/modal/<slug:devolve>',views.planos_de_acao, name='abre_modal_devolve'),
    path('planos_de_acao/<slug:search>/pesquisa',views.planos_de_acao, name='pagina_planos_de_acao_pesquisa'),
    path('planos_de_acao/<slug:mensagem>/msg',views.planos_de_acao, name='pagina_planos_de_acao_mensagem'),
    path('planos_de_acao/necessitando_correcao/<slug:variavel>',views.planos_a_serem_corrigidos, name='pagina_planos_a_serem_corrigidos'),
    path('planos_de_acao/altera/<int:elemento_id>/alt_corretor',views.altera_corretor, name='altera_corretor'),
    path('planos_de_acao/finalizados',views.planos_finalizados, name='pagina_planos_finalizados'),

    path('plano/<int:plano_id>/ordens',views.plano, name='chamando_1_plano'),
    path('plano/<int:plano_id>/ordens/<slug:mensagem>',views.plano, name='chamando_1_plano_mensagem'),
    path('plano/<int:plano_id>/cria/<slug:gera_ordem>',views.plano, name='nova_ordem'),
    path('plano/<int:plano_id>/ordem/<int:ordem_id>',views.abre_edicao_ordem, name='abrindo_edicao_ordem'),

    path('correcoes/<int:elemento_id>',views.pagina_correcoes, name='pagina_correcoes'),
    path('correcoes/<int:elemento_id>/<slug:mensagem>',views.pagina_correcoes, name='pagina_correcoes_mensagem'),
    path('corrigindo/<int:elemento_id>/acao/<int:ident_numerica>/slug/<slug:abreForm>',views.pagina_correcoes, name='abrindo_correcao_acao'),
    path('corrigindo/<int:elemento_id>/acao/<int:ident_numerica>/slug/<slug:codigo_ident>/codigo/<slug:abreFormDespesa>',views.pagina_correcoes, name='abrindo_correcao_despesa'),
    path('conclui_sugestao/correcao/plano<int:elemento_id>/<slug:documento>',views.concluir_sugestao, name='chamando_concluir_sugestao'),

    path('plano/<int:elemento_id>/acoes',views.acao_plano, name='chamando_acao_plano'),
    path('plano/<int:elemento_id>/acoes/<int:ordem_id>',views.acao_plano, name='chamando_acao_plano_datas'),
    path('plano/<int:elemento_id>/acoes/<slug:mensagem>',views.acao_plano, name='chamando_acao_plano_mensagem'),
    path('plano/<int:elemento_id>/acoes/<slug:mensagem>/q/<slug:q_linha>',views.acao_plano, name='chamando_acao_plano_mensagem_q_linha'),
    path('modif_all/plano/<int:plano_id>/acoes',views.acao_plano_adiciona_ordem, name='chamando_acao_plano_modifica_todas'),
    path('plano/<int:plano_id>/acoes/modifica_ordem/<int:elemento_id>',views.acao_plano_adiciona_ordem, name='chamando_acao_plano_adiciona'),
    path('acoes/plano/<int:plano_id>/ordem/<int:ordem_id>/codigo/<int:codigo_id>',views.acao_plano_modifica_codigo, name='chamando_acao_plano_adiciona_codigo'),
    path('plano/<int:elemento_id>/acoes/corrigir_ordem/<int:ordem_id>',views.acao_plano_correcao, name='chamando_correcao_acao_plano'),
    path('corrige/<int:plano_id>/ordem/<int:ordem_id>',views.corrigindo_acao, name='chama_corrige_ordem'),
    path('plano/<int:plano_id>/acoes/cria_correcao/<int:ordem_id>',views.cria_altera_correcao_acao, name='chamando_cria_altera_correcao_acao'),
    path('plano/<int:plano_id>/acoes/deleta_correcao/<int:ordem_id>',views.deleta_correcao_acao, name='chamando_deleta_correcao_acao'),

    path('plano/<int:elemento_id>/despesas',views.despesa_plano, name='chamando_despesa_plano'),
    path('plano/<int:elemento_id>/despesas/<slug:mensagem>/q/<slug:q_linha>',views.despesa_plano, name='chamando_despesa_mensagem_q_linha'),
    path('plano/<int:elemento_id>/despesas/<slug:mensagem>',views.despesa_plano, name='chamando_despesa_plano_mensagem'),
    path('plano/<int:elemento_id>/corrigir/despesas/<int:ordem_id>/<int:codigo_id>',views.despesa_plano_correcao, name='chamando_correcao_despesa_plano'),
    path('plano/<int:plano_id>/despesas/<int:ordem_id>/cria_correcao/<int:codigo_id>',views.cria_altera_correcao_despesa, name='chamando_cria_altera_correcao_despesa'),
    path('corrige/<int:plano_id>/ordem/<int:ordem_assoc>/codigo/<slug:codigo_ident>',views.corrigindo_despesas, name='chama_corrige_despesa'),
    path('plano/<int:plano_id>/despesas/deleta_correcao/<int:ordem_id>/<int:codigo_id>',views.deleta_correcao_despesa, name='chamando_deleta_correcao_despesa'),

    path('cria/plano',views.cria_plano, name='criar_plano'),
    path('editar/plano/<int:plano_id>',views.edita_plano, name='editar_plano'),
    path('publica/<int:elemento_id>',views.publica_plano, name='publicar_plano'),
    path('envia/<int:elemento_id>',views.envia_plano, name='enviar_plano'),
    path('devolve/<int:elemento_id>',views.devolve_plano, name='devolver_plano'),
    path('conclui/<int:elemento_id>',views.conclui_plano, name='concluir_plano'),
    path('autoriza/<int:elemento_id>',views.autoriza_plano, name='autorizar_plano'),
    path('autoriza/sec/<int:elemento_id>',views.autoriza_plano_func_sec, name='autorizar_plano_sec'),
    path('finaliza/<int:elemento_id>',views.finaliza_plano, name='finalizar_plano'),
    path('reset/<int:elemento_id>',views.reseta_plano, name='resetar_plano'),
    path('<int:elemento_id>',views.deleta_plano, name='deletar_plano'),
    path('plano/<int:elemento_id>/atrib_cor',views.atribui_corretor, name='chamando_atribui_corretor'),
    path('aprova/<int:elemento_id>',views.aprova_plano, name='aprovar_plano'),
    path('plano/<int:plano_id>/modifica_turma/<int:turma_id>',views.adiciona_remove_turma, name='adicionando_removendo_turma'),

    path('plano/<int:plano_id>/quebra_linha', views.quebra_de_linha, name='insere_quebra_de_linha'),
]