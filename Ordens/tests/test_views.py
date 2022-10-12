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
        self.modelo_fia = Modelo_fia.objects.create(plano=self.plano)
        self.modelo_fia.save()
        self.extra_fia = Extra_fia.objects.create(fia_matriz=self.modelo_fia, valor_numerico=1)
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

    def test_cadastra_data(self):
        # TESTE (POST)
        # USUARIO: Func_sec
        # ERRO: FORM COM DATA ERRADA
        # RENDERIZA PAGINA DE AÇÃO PLANO
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()

        data = {
            'prazo_execucao_inicial':'01/01/1001',
            'prazo_execucao_final':'01/01/1001', #data errada (igual)
        }
        kwargs = {'elemento_id':self.plano.id, 'ordem_id':self.ordem.id}
        response = self.c.post(reverse('cadastrando_datas', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acao-visualizacao.html')
        self.assertEquals(response.context['chave_erro_form_datas'], True) #variavel setada true quando ha erro no form
        # self.assertTrue(response.context['dicionario_planos'])

        # TESTE (POST)
        # USUARIO: Func_sec
        # SUCESSO: CADASTRA DATAS
        # REDIRECIONA PAGINA AÇÃO PLANO
        data = {
            'prazo_execucao_inicial':'01/01/1001',
            'prazo_execucao_final':'01/01/1002',
        }
        kwargs = {'elemento_id':self.plano.id, 'ordem_id':self.ordem.id}
        response = self.c.post(reverse('cadastrando_datas', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes')

    def test_edita_ordem(self):
        # TESTE (POST)
        # USUARIO: Diretor
        # ERRO: FORM COM IDENTIFICACAO ERRADA
        # RENDERIZA PAGINA DE AÇÃO PLANO
        data = {
            'identificacao_numerica':'99999', #erro numero maior que 100
            'descricao_do_problema':'a', 
            'resultados_esperados':'b',
        }
        kwargs = {'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.post(reverse('editando_ordem', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plano.html')
        self.assertEquals(response.context['chave_abre_modal_edicao'], True) #variavel setada true quando ha erro no form
        # self.assertTrue(response.context['dicionario_planos'])

        # TESTE (POST)
        # USUARIO: Diretor
        # SUCESSO: EDITOU ORDEM
        # REDIRECIONA PAGINA PLANO
        data = {
            'identificacao_numerica':'1', 
            'descricao_do_problema':'a', 
            'resultados_esperados':'b',
        }
        kwargs = {'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.post(reverse('editando_ordem', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/ordens/Editou')

    def test_deleta_ordem(self):
        # TESTE (GET)
        # USUARIO: Diretor
        # SUCESSO: DELETA ORDEM
        # REDIRECIONA
        kwargs = {'plano_id':self.plano.id,'elemento_id':self.ordem.id}
        response = self.c.get(reverse('deletar_ordem', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/ordens/Deletou')

    def test_cria_ordem(self):
        # TESTE (POST)
        # USUARIO: Diretor
        # ERRO: FORM - ORDEM JA EXISTE
        # RENDERIZA PAGINA DE AÇÃO PLANO
        data = {
            'identificacao_numerica':'1', #erro numero de ordem que ja existe
            'descricao_do_problema':'a', 
            'resultados_esperados':'b',
        }
        kwargs = {'plano_id':self.plano.id}
        response = self.c.post(reverse('criar_ordem', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plano.html')
        self.assertEquals(response.context['chave_abre_nova_ordem'], True) #variavel setada true quando ha erro no form
        # self.assertTrue(response.context['dicionario_planos'])

        # TESTE (POST)
        # USUARIO: Diretor
        # SUCESSO: CRIA NOVA ORDEM
        # REDIRECIONA PAGINA PLANO
        data = {
            'identificacao_numerica':'3', 
            'descricao_do_problema':'a', 
            'resultados_esperados':'b',
        }
        kwargs = {'plano_id':self.plano.id}
        response = self.c.post(reverse('criar_ordem', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/ordens/Criou')

    def test_ordem(self):
        # TESTE (GET)
        # USUARIO: Diretor
        # RENDERIZA PAGINA DA ORDEM
        kwargs = {'ordem_id':self.ordem.id}
        response = self.c.get(reverse('entra_na_ordem', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ordem.html')
        # self.assertEquals(response.context['chave_abre_nova_ordem'], True) #variavel setada true quando ha erro no form
        # self.assertTrue(response.context['dicionario_planos'])

        # TESTE (GET)
        # USUARIO: Diretor
        # MENSAGEM
        # RENDERIZA PAGINA DA ORDEM 
        kwargs = {'ordem_id':self.ordem.id,'mensagem':'Criou'}
        response = self.c.get(reverse('entra_na_ordem_mensagem', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ordem.html')
