from ast import arg
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Ordens.views import *

class Testurls(SimpleTestCase):
    
    def test_entra_na_ordem_resolve(self):
        url = reverse('entra_na_ordem', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, ordem)

    def test_entra_na_ordem_mensagem_resolve(self):
        url = reverse('entra_na_ordem_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, ordem)

    def test_criar_ordem_resolve(self):
        url = reverse('criar_ordem', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cria_ordem)

    def test_editando_ordem_resolve(self):
        url = reverse('editando_ordem', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, edita_ordem)

    def test_deletar_ordem_resolve(self):
        url = reverse('deletar_ordem', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, deleta_ordem)

    