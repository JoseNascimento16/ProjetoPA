from django.urls import path
from . import views


urlpatterns = [

    
    ### URLS + VIEWS TESTADAS ###
    path('ordem/<int:ordem_id>',views.ordem, name='entra_na_ordem'),
    path('ordem/<int:ordem_id>/<slug:mensagem>',views.ordem, name='entra_na_ordem_mensagem'),
    path('cria/ordem_plano/<int:plano_id>',views.cria_ordem, name='criar_ordem'),
    path('editando/ordem/<int:plano_id>/ordem/<int:ordem_id>',views.edita_ordem, name='editando_ordem'),
    path('plano/<int:plano_id>/deleta_ordem/<int:elemento_id>',views.deleta_ordem, name='deletar_ordem'),
    path('cadastra_datas/<int:elemento_id>/ordem_data/<int:ordem_id>', views.cadastra_data, name='cadastrando_datas'),
]