from ast import arg
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from usuarios.views import *

class Testurls(SimpleTestCase):
    
    def test_cadastrar_escolas_resolve(self):
        url = reverse('cadastrar_escolas', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_de_escolas)

    def test_cadastrar_escolas_mensagem_resolve(self):
        url = reverse('cadastrar_escolas_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_de_escolas)

    def test_abre_altera_cargo_resolve(self):
        url = reverse('abre_altera_cargo', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, altera_cargo)

    def test_altera_cargo_resolve(self):
        url = reverse('altera_cargo', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, altera_cargo)
    
    def test_cadastrar_funcionarios_resolve(self):
        url = reverse('cadastrar_funcionarios', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_escola)

    def test_cadastrar_funcionarios_secretaria_resolve(self):
        url = reverse('cadastrar_funcionarios_secretaria', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_de_funcionarios_secretaria)

    def test_cadastrar_funcionarios_mensagem_resolve(self):
        url = reverse('cadastrar_funcionarios_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_escola)

    def test_cadastrar_funcionarios_secretaria_mensagem_resolve(self):
        url = reverse('cadastrar_funcionarios_secretaria_mensagem', args=[1,'slug','slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_de_funcionarios_secretaria)

    def test_deletando_funcionario_resolve(self):
        url = reverse('deletando_funcionario', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, deleta_funcionario)

    def test_cadastrando_turmas_resolve(self):
        url = reverse('cadastrando_turmas', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_turmas)

    def test_cadastrando_turmas_mensagem_resolve(self):
        url = reverse('cadastrando_turmas_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_turmas)

    def test_cadastrando_turmas_abre_form_resolve(self):
        url = reverse('cadastrando_turmas_abre_form', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_turmas)

    def test_deletando_turma_resolve(self):
        url = reverse('deletando_turma', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, deleta_turma)

    def test_fazendo_login_resolve(self):
        url = reverse('fazendo_login')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, login)

    def test_fazendo_login_mensagem_resolve(self):
        url = reverse('fazendo_login_mensagem', args=['slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, login)

    def test_dashboard_resolve(self):
        url = reverse('dashboard')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, dashboard)

    def test_fazendo_logout_resolve(self):
        url = reverse('fazendo_logout')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, logout)

    def test_pesquisa_cadastro_escolas_resolve(self):
        url = reverse('pesquisa_cadastro_escolas', args=['slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_da_secretaria)

    def test_pesquisa_cadastro_funcionarios_resolve(self):
        url = reverse('pesquisa_cadastro_funcionarios', args=[1,'slug','slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastro_de_funcionarios_secretaria)

    def test_meu_acesso_resolve(self):
        url = reverse('abre_meu_acesso', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, meu_acesso)

    def test_altera_login_resolve(self):
        url = reverse('altera_login', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, altera_login)

    def test_abre_altera_login_resolve(self):
        url = reverse('abre_altera_login', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, meu_acesso)

    def test_abre_altera_assinatura_resolve(self):
        url = reverse('abre_altera_assinatura', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, meu_acesso)

    def test_cadastra_assinatura_resolve(self):
        url = reverse('cadastra_assinatura', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, salva_assinatura)

    def test_cadastra_assinatura_teste_resolve(self):
        url = reverse('cadastra_assinatura_teste', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, salva_assinatura)

    def test_apaga_assinatura_resolve(self):
        url = reverse('apaga_assinatura', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, remove_assinatura)

    def test_altera_mail_resolve(self):
        url = reverse('altera_mail', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, altera_mail)

    def test_enviando_email_resolve(self):
        url = reverse('enviando_email')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, envia_email)

    def test_apaga_mail_resolve(self):
        url = reverse('apaga_mail', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, remove_mail)

    def test_ativacao_email_resolve(self):
        url = reverse('ativacao_email', args=['text','text'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, ativacao_email)

    def test_abre_altera_mail_resolve(self):
        url = reverse('abre_altera_mail', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, meu_acesso)
    
    def test_abre_meu_acesso_mensagem_resolve(self):
        url = reverse('abre_meu_acesso_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, meu_acesso)

    def test_profile_escola_resolve(self):
        url = reverse('profile_escola', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, profile_escola)

    