from ast import arg
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from usuarios.views import *

class Testurls(SimpleTestCase):
    
    def test_cadastrar_escolas_resolve(self):
        url = reverse('cadastrar_escolas', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_secretaria)

    def test_cadastrar_escolas_mensagem_resolve(self):
        url = reverse('cadastrar_escolas_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_secretaria)

    def test_cadastrar_funcionarios_resolve(self):
        url = reverse('cadastrar_funcionarios', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_escola)

    def test_cadastrar_funcionarios_secretaria_resolve(self):
        url = reverse('cadastrar_funcionarios_secretaria', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_secretaria)

    def test_cadastrar_funcionarios_secretaria_mensagem_resolve(self):
        url = reverse('cadastrar_funcionarios_secretaria_mensagem', args=[1,'slug','slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_secretaria)

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
        url = reverse('pesquisa_cadastro_escolas', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_secretaria)

    def test_pesquisa_cadastro_funcionarios_resolve(self):
        url = reverse('pesquisa_cadastro_funcionarios', args=[1,'slug','slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cadastros_secretaria)

    def test_meu_acesso_resolve(self):
        url = reverse('abre_meu_acesso', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, meu_acesso)

    def test_abre_altera_nome_resolve(self):
        url = reverse('abre_altera_nome', args=[1,'slug'])
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

    def test_apaga_assinatura_resolve(self):
        url = reverse('apaga_assinatura', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, remove_assinatura)

    