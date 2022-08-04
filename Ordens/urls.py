from django.urls import path
from . import views


urlpatterns = [
    path('ordem/<int:ordem_id>',views.ordem, name='entra_na_ordem'),
    path('ordem/<int:ordem_id>/<slug:mensagem>',views.ordem, name='entra_na_ordem_mensagem'),
    path('cria/ordem_plano/<int:plano_id>',views.cria_ordem, name='criar_ordem'),
    path('edita/plano/<int:plano_id>/ordem/<int:ordem_id>',views.edita_ordem, name='editando_ordem'),
    path('cadastra_datas/<int:elemento_id>/ordem_data/<int:ordem_id>', views.cadastra_data, name='cadastrando_datas'),
    path('plano/<int:plano_id>/deleta_ordem/<int:elemento_id>',views.deleta_ordem, name='deletar_ordem'),
]