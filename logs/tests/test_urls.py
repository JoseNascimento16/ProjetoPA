from ast import arg
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from logs.views import *

class Testurls(SimpleTestCase):
    
    def test_chamando_log_planos_resolve(self):
        url = reverse('chamando_log_planos')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, log_planos)

    def test_chamando_plano_resolve(self):
        url = reverse('chamando_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, chama_log_plano)

    