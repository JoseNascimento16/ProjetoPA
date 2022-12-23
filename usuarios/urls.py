from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
  
urlpatterns = [
    
    

    # URLS + VIEWS TESTADAS
    path('escola/cadastros',views.cadastros_da_secretaria, name='chama_cadastros_secretaria'),
    path('escola/cadastros/<slug:mensagem>',views.cadastros_da_secretaria, name='chama_cadastros_secretaria_mensagem'),
    path('escola/<int:escola_id>/cadastro_diretor/<cadastro_diretor>',views.cadastros_da_secretaria, name='chama_cadastrar_diretor'),
    path('cadastro_escolas/search/<slug:search>',views.cadastros_da_secretaria, name='pesquisa_cadastro_escolas'),
    path('cadastro/diretor/<int:escola_id>',views.cadastro_diretor_escola, name='cadastrar_diretor'),
    path('cadastro_escolas/<int:user_id>',views.cadastro_de_escolas, name='cadastrar_escolas'),
    path('cadastro_escolas/<int:user_id>/<slug:mensagem>',views.cadastro_de_escolas, name='cadastrar_escolas_mensagem'),
    path('cadastros_secretaria/<int:user_id>/<slug:cad_funcionarios>',views.cadastro_de_funcionarios_secretaria, name='cadastrar_funcionarios_secretaria'),
    path('cadastros_secretaria/<int:user_id>/<slug:cad_funcionarios>/<slug:mensagem>',views.cadastro_de_funcionarios_secretaria, name='cadastrar_funcionarios_secretaria_mensagem'),    
    path('cadastro_secretaria/search/<int:user_id>/<slug:cad_funcionarios>/<slug:search>',views.cadastro_de_funcionarios_secretaria, name='pesquisa_cadastro_funcionarios'),
    path('cadastro_funcionarios_escola/<int:user_id>',views.cadastros_escola, name='cadastrar_funcionarios'),
    path('cadastro_funcionarios_escola/<int:user_id>/<slug:mensagem>',views.cadastros_escola, name='cadastrar_funcionarios_mensagem'),
    path('escola/remocao/diretor/<int:user_id>',views.solicita_remocao, name='solicitar_remocao'),
    path('escola/cancela/remocao/diretor/<int:user_id>',views.cancela_remocao_diretor, name='cancelar_remocao'),
    path('excluir_funcionario/<int:elemento_id>',views.deleta_funcionario, name='deletando_funcionario'),
    path('altera_cargo/<int:elemento_id>',views.altera_cargo, name='abre_altera_cargo'),
    path('altera_cargo/edita/<int:elemento_id>/<slug:edita>',views.altera_cargo, name='altera_cargo'),
    path('cadastro_turmas/<int:user_id>',views.cadastro_turmas, name='cadastrando_turmas'),
    path('cadastro_turmas/<int:user_id>/<slug:mensagem>',views.cadastro_turmas, name='cadastrando_turmas_mensagem'),
    path('cadastro_turmas/<int:user_id>/<slug:abre_form>/form',views.cadastro_turmas, name='cadastrando_turmas_abre_form'),
    path('apaga_turma/<int:turma_id>',views.deleta_turma, name='deletando_turma'),
    path('profile/<int:user_id>', views.meu_acesso, name='abre_meu_acesso'),
    path('profile/change/<int:user_id>/<slug:altera>', views.meu_acesso, name='abre_altera_login'),
    path('profile/change/<int:user_id>/sign/<slug:altera>', views.meu_acesso, name='abre_altera_assinatura'),
    path('profile/change/<int:user_id>/mail/<slug:altera>', views.meu_acesso, name='abre_altera_mail'),
    path('profile/<int:user_id>/msg/<slug:mensagem>', views.meu_acesso, name='abre_meu_acesso_mensagem'),
    path('profile/altera/<int:user_id>', views.altera_login, name='altera_login'),
    path('profile/escola/<int:escola_id>', views.profile_escola, name='profile_escola'),
    path('profile/altera_email/<int:user_id>', views.altera_mail, name='altera_mail'),
    path('mail/<uidb64>/activation/<token>', views.ativacao_email, name='ativacao_email'),
    path('profile/remove_mail/<int:user_id>', views.remove_mail, name='apaga_mail'),
    path('profile/<int:user_id>/sign/cadastro', views.salva_assinatura, name='cadastra_assinatura'),
    path('profile/sign/remove<int:user_id>', views.remove_assinatura, name='apaga_assinatura'),
    path('',views.login, name='fazendo_login'),
    path('login/index/<slug:mensagem>',views.login, name='fazendo_login_mensagem'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('logout/',views.logout, name='fazendo_logout'),
    ############################
    
    path('envia_mail/teste', views.envia_email, name='enviando_email'),
    ############################

    # CLASS BASED URLs
        # Página de reset password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='authentication/reset_password.html'), name='reset_password'),
        # Página de mensagem de reset enviado
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/reset_password_sent.html'), name='password_reset_done'),
        # Link que o usuário irá receber para resetar a senha
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/reset_password_confirm.html'), name='password_reset_confirm'),
        # Página de mensagem de sucesso que a senha foi trocada
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/reset_password_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)