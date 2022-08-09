from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
  
urlpatterns = [
    path('cadastro_secretaria/<int:user_id>',views.cadastros_secretaria, name='cadastrar_escolas'),
    path('cadastro_secretaria/<int:user_id>/<slug:mensagem>',views.cadastros_secretaria, name='cadastrar_escolas_mensagem'),
    path('cadastros_escolas/<int:user_id>',views.cadastros_escola, name='cadastrar_funcionarios'),
    path('cadastros_secretaria/<int:user_id>/<slug:cad_funcionarios>',views.cadastros_secretaria, name='cadastrar_funcionarios_secretaria'),
    path('cadastros_secretaria/<int:user_id>/<slug:cad_funcionarios>/<slug:mensagem>',views.cadastros_secretaria, name='cadastrar_funcionarios_secretaria_mensagem'),
    path('cadastro_secretaria/search/<int:user_id>/<slug:search>',views.cadastros_secretaria, name='pesquisa_cadastro_escolas'),
    path('cadastro_secretaria/search/<int:user_id>/<slug:cad_funcionarios>/<slug:search>',views.cadastros_secretaria, name='pesquisa_cadastro_funcionarios'),
    path('altera_cargo/<int:elemento_id>',views.altera_cargo, name='abre_altera_cargo'),
    path('altera_cargo/edita/<int:elemento_id>/<slug:edita>',views.altera_cargo, name='altera_cargo'),

    path('cadastros_escolas/<int:user_id>/<slug:mensagem>/<slug:cad_funcionarios>',views.cadastros_secretaria, name='cadastrar_funcionarios_secretaria_mensagem'),
    # path('cadastro_funcionarios/del/<int:user_id>/<slug:mensagem>/<slug:cad_funcionarios>',views.cadastro_escolas, name='cadastrar_funcionarios_secretaria_mensagem'),
    
    path('cadastros_escolas/<int:user_id>/<slug:mensagem>',views.cadastros_escola, name='cadastrar_funcionarios_mensagem'),
    path('excluir_funcionario/<int:elemento_id>',views.deleta_funcionario, name='deletando_funcionario'),
    path('cadastro_turmas/<int:user_id>',views.cadastro_turmas, name='cadastrando_turmas'),
    path('cadastro_turmas/<int:user_id>/<slug:mensagem>',views.cadastro_turmas, name='cadastrando_turmas_mensagem'),
    path('cadastro_turmas/<int:user_id>/<slug:abre_form>/form',views.cadastro_turmas, name='cadastrando_turmas_abre_form'),
    path('apaga_turma/<int:turma_id>',views.deleta_turma, name='deletando_turma'),
    path('',views.login, name='fazendo_login'),
    path('login/index/<slug:mensagem>',views.login, name='fazendo_login_mensagem'),
    path('profile/<int:user_id>', views.meu_acesso, name='abre_meu_acesso'),
    path('profile/change/<int:user_id>/<slug:altera>', views.meu_acesso, name='abre_altera_nome'),
    path('profile/change/<int:user_id>/sign/<slug:altera>', views.meu_acesso, name='abre_altera_assinatura'),
    path('profile/<int:user_id>/sign/cadastro', views.salva_assinatura, name='cadastra_assinatura'),
    path('profile/sign/remove<int:user_id>', views.remove_assinatura, name='apaga_assinatura'),
    path('profile/altera/<int:user_id>', views.altera_nome, name='altera_nome'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('index/',views.logout, name='fazendo_logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)