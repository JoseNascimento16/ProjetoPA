from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from Escolas.models import Escola
from Ordens.models import Ordens
from codigos.models.codigos import ModeloCodigos
from fia.models import Extra_fia, Modelo_fia
from plano_de_acao.models import Correcoes, Plano_de_acao
from usuarios.models import Classificacao, Turmas
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from PIL import Image



class TestViews(TestCase):
    def setUp(self):
        #create permissions group
        self.group = Group(name='Diretor_escola')
        self.group.save()
        self.c = Client()
        self.user = User.objects.create_user(first_name='test' ,username="test", email="test@test.com", password="test")
        self.user.groups.add(self.group)
        self.escola = Escola.objects.create(nome='escola_teste')
        self.escola.save()
        self.classificacao = Classificacao.objects.create(user=self.user, escola=self.escola)
        self.classificacao.save()
        self.plano = Plano_de_acao.objects.create(escola=self.escola, ano_referencia='nome_qualquer', alterabilidade='Escola', situacao='Em desenvolvimento')
        self.plano.save()
        self.plano2 = Plano_de_acao.objects.create(escola=self.escola, ano_referencia='nome_qualquer2')
        self.plano2.save()
        self.ordem = Ordens.objects.create(plano=self.plano, identificacao_numerica=1, data_de_criação=timezone.now())
        self.ordem.save()
        self.codigo = ModeloCodigos.objects.create(ordem=self.ordem, identificacao='A', quantidade=1)
        self.codigo.save()
        self.modelo_fia = Modelo_fia.objects.create(plano=self.plano, valor_total_item=0)
        self.modelo_fia.save()
        self.extra_fia = Extra_fia.objects.create(fia_matriz=self.modelo_fia, valor_numerico=2, quantidade=0, valor_total_item=0, preco_unitario_item=0)
        self.extra_fia.save()
        self.user.save()
        self.c.login(username='test', password='test')
        # self.factory = RequestFactory()
        

    # def tearDown(self):
    #     self.user.delete()
    #     self.group.delete()
    #     self.classificacao.delete()
    #     self.escola.delete()

##################################################################################################

    def test_edita_codigo(self):
        # TESTE (POST)
        # FORM INVALIDO
        data = {
            'identificacao':'AB',# erro, possui mais de uma letra
            'especificacao':'a',
            'justificativa':'b',
            'embalagem':'unidade',
            'quantidade':1,
            'preco_unitario':1,
            'tipo_produto':'Capital',
        }
        kwargs = {'ordem_id':self.ordem.id, 'codigo_id':self.codigo.id}
        response = self.c.post(reverse('editando_codigo', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ordem.html')
        self.assertEquals(response.context['chave_abre_edita_codigo'], True)

        # TESTE (POST)
        # FORM VALIDO
        data = {
            'identificacao':'A',
            'especificacao':'a',
            'justificativa':'b',
            'embalagem':'unidade',
            'quantidade':1,
            'preco_unitario':1,
            'tipo_produto':'Capital',
        }
        kwargs = {'ordem_id':self.ordem.id, 'codigo_id':self.codigo.id}
        response = self.c.post(reverse('editando_codigo', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/ordem/'+str(self.ordem.id)+'/Editou')

    def test_novo_codigo(self):
        # TESTE (POST)
        # FORM INVALIDO
        data = {
            'identificacao':'AB',# erro, possui mais de uma letra
            'especificacao':'a',
            'justificativa':'b',
            'embalagem':'unidade',
            'quantidade':1,
            'preco_unitario':1,
            'tipo_produto':'Capital',
        }
        kwargs = {'ordem_id':self.ordem.id, 'variavel':'sim'}
        response = self.c.post(reverse('novo_codigo', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ordem.html')
        self.assertEquals(response.context['chave_abre_novo_codigo'], True)

        # TESTE (POST)
        # FORM VALIDO
        data = {
            'identificacao':'B',
            'especificacao':'a',
            'justificativa':'b',
            'embalagem':'unidade',
            'quantidade':1,
            'preco_unitario':1,
            'tipo_produto':'Capital',
        }
        kwargs = {'ordem_id':self.ordem.id, 'variavel':'sim'}
        response = self.c.post(reverse('novo_codigo', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/ordem/'+str(self.ordem.id)+'/Criou')

    def test_abre_codigo(self):
        # TESTE (GET)
        # ABRE EDIÇÃO CODIGO
        kwargs = {'ordem_id':self.ordem.id, 'codigo_id':self.codigo.id}
        response = self.c.get(reverse('abre_edicao_codigo', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ordem.html')
        self.assertEquals(response.context['chave_abre_edita_codigo'], True)

        # TESTE (GET)
        # ABRE CRIAÇÃO CODIGO
        kwargs = {'ordem_id':self.ordem.id, 'abre_codigo':'sim'}
        response = self.c.get(reverse('abre_criacao_codigo', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ordem.html')
        self.assertEquals(response.context['chave_abre_novo_codigo'], True)

    def test_deleta_codigo(self):
        # TESTE (GET)
        # DELETA CODIGO
        # REDUZ NUMERO DE CODIGOS INSERIDOS DA ORDEM
        # REDUZ ROWSPAN DA ORDEM
        self.codigo.inserido = True
        self.codigo.save
        self.codigo2 = ModeloCodigos.objects.create(ordem=self.ordem, identificacao='B', quantidade=1, inserido=True)
        self.codigo3 = ModeloCodigos.objects.create(ordem=self.ordem, identificacao='C', quantidade=1, inserido=True)
        self.ordem.codigos_inseridos = 3
        self.ordem.ordem_rowspan = 3
        self.ordem.save()
        kwargs = {'ordem_id':self.ordem.id, 'elemento_id':self.codigo.id}
        response = self.c.get(reverse('deletar_codigo', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/ordem/'+str(self.ordem.id)+'/Deletou')