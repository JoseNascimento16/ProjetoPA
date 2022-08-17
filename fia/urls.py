from django.urls import path
from . import views


urlpatterns = [
    path('cria/fia',views.cria_fia, name='criando_fia'),
    path('formulario/<int:elemento_id>/inclusao/acoes',views.documento_fia, name='chamando_documento_fia'),
    path('formulario/<int:elemento_id>/inclusao/acoes/<slug:mensagem>',views.documento_fia, name='chamando_documento_fia_mensagem'),
    path('fia/<int:elemento_id>/altera/ordemprincipal',views.altera_fia, name='chama_altera_fia'),
    path('chama/<int:elemento_id>/cria/extra/fia/<slug:abreform_extra_criacao>',views.documento_fia, name='chama_cria_extra_fia'),
    path('cria/extra/fia/<int:modelo_fia_id>',views.cria_ordem_extra_fia, name='cria_extra_fia'),
    path('chama/altera/<int:elemento_id>/ordem_extra/<slug:abreform_extra_edicao>/extra_id/<int:ordem_extra_id>',views.documento_fia, name='chama_altera_extra_fia'),
    path('cria/extra/fia/<int:modelo_fia_id>/ordem_extra/<int:ordem_extra_id>',views.altera_ordem_extra_fia, name='altera_extra_fia'),
    path('extra/fia/<int:ordem_extra_id>/exclui',views.exclui_ordem_extra_fia, name='excluir_extra_fia'),
    path('plano/<int:elemento_id>/corrigir/<int:modelo_fia_id>',views.correcao_plano_fia, name='chamando_correcao_modelo_fia'),
    path('plano/<int:elemento_id>/corrigir/extra/<int:ordem_extra_id>',views.correcao_plano_fia, name='chamando_correcao_extra_fia'),
    path('plano/<int:plano_id>/cria_correcao/<int:ordem_id>/fia',views.cria_altera_correcao_fia, name='chamando_cria_altera_correcao_fia'),
    path('plano/<int:plano_id>/fia/deleta_correcao/<int:ordem_id>/slug/<slug:tipo_ordem>',views.deleta_correcao_fia, name='chamando_deleta_correcao_fia'),
    path('abre_correcao/fia/<int:elemento_id>/acao/<int:ident_numerica>/slug/<slug:abreFormFia>',views.abre_correcao_fia, name='abrindo_correcao_fia'),
    path('corrigindo/fia/<int:elemento_id>/acao/<int:ident_numerica>',views.corrige_fia, name='corrigindo_fia'),
    path('fia/<int:modelo_fia_id>/assinatura/tecnico',views.salva_assinatura_tecnico_fia, name='salvando_assinatura_tecnico'),
    path('fia/sign/<int:modelo_fia_id>/remove', views.remove_assinatura_tecnico, name='apaga_assinatura_tecnico'),
]