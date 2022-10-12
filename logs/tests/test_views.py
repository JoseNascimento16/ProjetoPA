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
from eventlog.models import Event

class TestViews(TestCase):
    def setUp(self):
        #create permissions group
        self.group = Group(name='Diretor_escola')
        self.group.save()
        self.c = Client()
        self.user = User.objects.create_user(first_name='nome_usuario' ,username="test", email="test@test.com", password="test")
        self.user.groups.add(self.group)
        self.user2 = User.objects.create_user(first_name='nome_user2' ,username="test2", email="test2@test.com", password="test2")
        self.user2.groups.add(self.group)
        self.escola = Escola.objects.create(nome='escola_teste')
        self.escola.save()
        self.classificacao = Classificacao.objects.create(user=self.user, escola=self.escola)
        self.classificacao.save()
        self.classificacao2 = Classificacao.objects.create(user=self.user2, escola=self.escola)
        self.classificacao2.save()
        self.plano = Plano_de_acao.objects.create(escola=self.escola, ano_referencia='nome_qualquer', alterabilidade='Escola', situacao='Publicado')
        self.plano.save()
        self.plano2 = Plano_de_acao.objects.create(escola=self.escola, ano_referencia='nome_qualquer2')
        self.plano2.save()
        self.user.save()
        self.user2.save()
        self.c.login(username='test', password='test')
        # self.factory = RequestFactory()
        

    # def tearDown(self):
    #     self.user.delete()
    #     self.group.delete()
    #     self.classificacao.delete()
    #     self.escola.delete()

##################################################################################################

    def test_chama_log_plano(self):
        # TESTE (GET)
        # NÃO EXISTE LOG AINDA
        kwargs = {'elemento_id':self.plano.id}
        response = self.c.get(reverse('chamando_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_plano.html')
        self.assertFalse(response.context['chave_existe_log'])

        # TESTE (GET)
        # EXISTE LOG
        self.log = Event.objects.create(plano_base=self.plano.id, group=True, initiator=self.user.first_name)
        
        kwargs = {'elemento_id':self.plano.id}
        response = self.c.get(reverse('chamando_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_plano.html')
        self.assertTrue(response.context['chave_existe_log'])

    def test_log_planos(self):
        # TESTE (GET)
        # TESTE SE ACHA PLANOS QUE JA EXISTEM
        # USUARIO: Func_sec, Diretor_escola e Funcionario
        self.group.name = 'Func_sec'
        self.group.save()
        
        response = self.c.get(reverse('chamando_log_planos'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        self.group.name = 'Diretor_escola'
        self.group.save()
        
        response = self.c.get(reverse('chamando_log_planos'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        self.group.name = 'Funcionario'
        self.group.save()
        
        response = self.c.get(reverse('chamando_log_planos'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        # TESTE (POST)
        # HOUVE PESQUISA
        # TESTE SE ACHA PLANOS QUE BATEM COM A PESQUISA
        # USUARIO: Func_sec
        self.log = Event.objects.create(plano_base=self.plano.id, group=True, initiator=self.user.first_name)
        self.group.name = 'Func_sec'
        self.group.save()
        
        data = {'campo':'nome_qualquer'} #acha pelo nome do plano
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        data = {'campo':'escola_teste'} #acha pelo nome da escola
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        self.group2 = Group(name='Diretor_escola')
        self.group2.save()
        self.user2.groups.remove(self.group) # 'Func_sec'
        self.user2.groups.add(self.group2) # 'Diretor_escola'
        self.user2.save()
        data = {'campo':'nome_user2'} #acha pelo nome do diretor
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        self.plano.corretor_plano = self.user
        self.plano.save()
        data = {'campo':'nome_usuario'} #acha pelo nome do corretor
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        data = {'campo':'Publicado'} #acha pela situação do plano
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        # TESTE (POST)
        # HOUVE PESQUISA
        # TESTE SE ACHA PLANOS QUE BATEM COM A PESQUISA
        # USUARIO: Diretor_escola ou Funcionario
        self.user.groups.remove(self.group)
        self.user.groups.add(self.group2)
        self.user.save()
        
        data = {'campo':'nome_qualquer'} #acha pelo nome do plano
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        data = {'campo':'Publicado'} #acha pela situação do plano
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        data = {'campo':'escola_teste'} #acha pelo nome da escola
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])

        self.plano.corretor_plano = self.user2
        self.plano.save()
        self.user2.groups.remove(self.group2) # 'Diretor_escola'
        self.user2.groups.add(self.group) # 'Func_sec'
        self.user2.save()
        data = {'campo':'nome_user2'} #acha pelo nome do corretor
        kwargs = {'search':'sim'}
        response = self.c.post(reverse('pagina_log_planos_de_acao_pesquisa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_planos_de_acao.html')
        self.assertTrue(response.context['chave_achou_plano'])