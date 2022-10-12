from django.urls import path
from . import views
# from plano_de_acao import views

urlpatterns = [
    
    ### URLS + VIEWS TESTADAS ###
    path('log_planos',views.log_planos, name='chamando_log_planos'),
    path('log_plano/<int:elemento_id>',views.chama_log_plano, name='chamando_plano'),
    path('log_planos/pesquisa/<slug:search>',views.log_planos, name='pagina_log_planos_de_acao_pesquisa'),
]