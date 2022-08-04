from ast import arg
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from codigos.views import *

class Testurls(SimpleTestCase):
    
    def test_deletar_codigo_resolve(self):
        url = reverse('deletar_codigo', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, deleta_codigo)

    def test_abre_criacao_codigo_resolve(self):
        url = reverse('abre_criacao_codigo', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, abre_codigo)

    def test_abre_edicao_codigo_codigo_resolve(self):
        url = reverse('abre_edicao_codigo', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, abre_codigo)

    def test_novo_codigo_codigo_resolve(self):
        url = reverse('novo_codigo', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, novo_codigo)

    def test_editando_codigo_resolve(self):
        url = reverse('editando_codigo', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, edita_codigo)

    