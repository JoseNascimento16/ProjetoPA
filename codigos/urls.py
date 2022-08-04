from django.urls import path
from . import views

urlpatterns = [
    
    path('ordem/<int:ordem_id>/deleta_codigo/<int:elemento_id>',views.deleta_codigo, name='deletar_codigo'),
    path('ordem/<int:ordem_id>/cria/<slug:abre_codigo>',views.abre_codigo, name='abre_criacao_codigo'),
    path('ordem/<int:ordem_id>/abre_edicao/<int:codigo_id>',views.abre_codigo, name='abre_edicao_codigo'),
    path('ordem/<int:ordem_id>/criou_codigo/<slug:variavel>',views.novo_codigo, name='novo_codigo'),
    path('ordem/<int:ordem_id>/edita/<int:codigo_id>',views.edita_codigo, name='editando_codigo'),
    
]