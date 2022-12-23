from datetime import date
from http import HTTPStatus
from urllib.parse import urlencode
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from Escolas.models import Escola
from plano_de_acao.models import Plano_de_acao
from usuarios.forms import FormAlteraMail
from usuarios.models import Classificacao, Turmas
from usuarios.views import altera_mail, envia_email
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import Group
import base64
from usuarios.alteracoes import converteINT_b64_urlsafe
from usuarios.utils import generate_token
from django.http import response, HttpRequest
from django.core.files.uploadedfile import SimpleUploadedFile


class TestViews(TestCase):
    def setUp(self):
        #create permissions group
        self.group = Group(name='My_test_group')
        self.group.save()
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.user.groups.add(self.group)
        self.escola = Escola.objects.create(nome='escola_teste')
        self.escola.save()
        self.classificacao = Classificacao.objects.create(user=self.user, escola=self.escola)
        self.classificacao.save()
        self.user.save()
        self.c.login(username='test', password='test')
        self.factory = RequestFactory()
        

    # def tearDown(self):
    #     self.user.delete()
    #     self.group.delete()
    #     self.classificacao.delete()
    #     self.escola.delete()

##################################################################################################

    def test_envia_email_200(self):
        response = self.c.get('/envia_mail/teste') # Usa o nome da URL
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teste.html')

##################################################################################################

    # def test_envia_email_funcao(self):
        
    #     response = envia_email(self.client.get('envia_mail/teste/'))

    #     self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'teste.html')

##################################################################################################

    # def test_redireciona_dashboard(self):
        
    #     response = self.c.get(reverse('enviando_email', kwargs={'variavel':'valor_qualquer'})) # Usa o nome da URL e atributos
        
    #     self.assertRedirects(response, '/dashboard')

##################################################################################################        
    
    def test_fazendo_login(self):
        self.c.logout()

        response = self.c.get(reverse('fazendo_login')) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

##################################################################################################   
    
    # FUNCIONA MAS DA CONFLITO COM O REDIRECT DO MIDDLEWARE

    # def test_fazendo_login_mensagem(self):
    #     self.c.logout()

    #     response = self.c.get(reverse('fazendo_login_mensagem', kwargs={'mensagem':'Vazio'})) # Usa o nome da URL e atributos
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')

##################################################################################################   

    def test_fazendo_logout(self):

        response = self.c.get(reverse('fazendo_logout')) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    
##################################################################################################

    def test_dashboard(self):
        self.group.name = 'Func_sec'
        self.group.save()
        self.classificacao.cargo_herdado = 'Coordenador'
        self.classificacao.save()
        plano1 = Plano_de_acao.objects.create(ano_referencia='plano1', corretor_plano=self.user, situacao='Pendente', data_de_criação=date(2022,12,23))
        plano2 = Plano_de_acao.objects.create(ano_referencia='plano2', corretor_plano=None, situacao='Pendente', data_de_criação=date(2022,12,22))
        plano3 = Plano_de_acao.objects.create(ano_referencia='plano3', corretor_plano=None, situacao='Assinado')

        response = self.c.get(reverse('dashboard')) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

##################################################################################################

    def test_remove_assinatura(self):
        
        response = self.c.post(reverse('apaga_assinatura', kwargs={'user_id':self.user.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/'+str(self.user.id))

##################################################################################################
    
    def test_salva_assinatura(self):
        imagem = SimpleUploadedFile(name='test_image.jpg', content=open('static/img/canvas_data_test.jpg', 'rb').read(), content_type='image/jpeg')
        imgTo_base64_str = base64.b64encode(imagem.read()).decode('utf-8')
        prefixo = 'data:image/jpeg;base64,'
        DataUrl = prefixo + imgTo_base64_str

        data = {'canvasData':DataUrl}
        response = self.c.post(reverse('cadastra_assinatura', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/'+str(self.user.id))

##################################################################################################

    def test_ativacao_email(self):

        uidb64_urlsafe = converteINT_b64_urlsafe(self.user.id)
        valor_token = generate_token.make_token(self.user)
        
        response = self.c.get(reverse('ativacao_email', kwargs={'uidb64':uidb64_urlsafe,'token':valor_token})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/'+str(self.user.id)+'/msg/activation_success')
    
##################################################################################################

    def test_altera_email(self):
        # TESTE POST
        # FORM COM PREFIXO, SUCESSO
        data = {
            'qualquer-email':'test@test.com'
            }
        response = self.c.post('/profile/altera_email/'+str(self.user.id), data)

        # data = {'email':'someone@email.com'}
        # response = altera_mail(self.client.post('envia_mail/teste/', data), self.user.id)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/'+str(self.user.id)+'/msg/sent_activation')

##################################################################################################

    def test_altera_email_erro_form(self):
        self.user2 = User.objects.create_user(username="test2", email="test2@test.com", password="test")
        self.user2.save()

        data = {'email':'test2@test.com'}
        response = self.c.post('/profile/altera_email/'+str(self.user.id), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

##################################################################################################

    def test_remove_mail(self):

        response = self.c.post('/profile/remove_mail/'+str(self.user.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/'+str(self.user.id)+'/msg/mail_removed')

##################################################################################################

    def test_altera_login(self):
        #FORM INVALIDO
        data = {'username':'qualquer',
                'novo_username':'nome com espaço',
                'novo_username2':'nome com espaço'  # erro, campo com espaço
                }
        response = self.c.post('/profile/altera/'+str(self.user.id), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

        #FORM VALIDO
        self.classificacao.login_original = True
        self.classificacao.save()

        data = {'username':'test','novo_username':'nomeDeUsuarioNovo','novo_username2':'nomeDeUsuarioNovo'}
        response = self.c.post('/profile/altera/'+str(self.user.id), data, follow=True)

        username_atualizado = User.objects.filter(username='nomeDeUsuarioNovo')
        self.assertTrue(username_atualizado)
        classificacao = get_object_or_404(Classificacao, user=self.user)
        self.assertFalse(classificacao.login_original)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/profile/'+str(self.user.id)+'/msg/success')
        self.assertTemplateUsed(response, 'profile.html')

##################################################################################################

    def vazio():
        # def test_altera_nome(self):

        #     #FORM VALIDO
        #     data = {'first_name':'nome qualquer'}
        #     response = self.c.post('/profile/altera/'+str(self.user.id), data, follow=True)

        #     self.assertEqual(response.status_code, 200)
        #     self.assertTemplateUsed(response, 'profile.html')

        #     #FORM INVALIDO
        #     data = {'first_name':'nome4444'}
        #     response = self.c.post('/profile/altera/'+str(self.user.id), data, follow=True)

        #     self.assertEqual(response.status_code, 200)
        #     self.assertTemplateUsed(response, 'profile.html')
        pass

##################################################################################################

    def test_profile_escola(self):
        
        response = self.c.get(reverse('profile_escola', kwargs={'escola_id':self.escola.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Profile_escola.html')

##################################################################################################

    def test_meu_acesso(self):
        
        # TESTE PADRÃO (GET)
        response = self.c.get(reverse('abre_meu_acesso', kwargs={'user_id':self.user.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

        # TESTE PADRÃO (GET)
        # KWARGS altera == 'alt_login'
        response = self.c.get(reverse('abre_altera_login', kwargs={'user_id':self.user.id, 'altera':'alt_login'})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['chave_abre_altera_login'], True) #variavel setada TRUE quando altera == 'alt_login'

        # TESTE PADRÃO (GET)
        # KWARGS altera == 'alt_sign'
        response = self.c.get(reverse('abre_altera_assinatura', kwargs={'user_id':self.user.id, 'altera':'alt_sign'})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['chave_abre_altera_assinatura'], True) #variavel setada TRUE quando altera == 'alt_sign'

        # TESTE PADRÃO (GET)
        # KWARGS altera == 'chng_mail'
        response = self.c.get(reverse('abre_altera_mail', kwargs={'user_id':self.user.id, 'altera':'chng_mail'})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['chave_abre_altera_mail'], True) #variavel setada TRUE quando altera == 'chng_mail'

##################################################################################################

    def test_deleta_turma(self):
        self.classificacao.escola = self.escola
        self.classificacao.save()
        self.group.name = 'Diretor_escola'
        self.group.save()
        turma = Turmas.objects.create(escola=self.escola, quantidade_alunos=10)

        response = self.c.get(reverse('deletando_turma', kwargs={'turma_id':turma.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastro_turmas/'+str(self.user.id)+'/Deletou')

##################################################################################################

    def test_cadastro_turmas(self):
        self.group.name = 'Diretor_escola'
        self.group.save()

        # TEST PADRÃO (GET)
        response = self.c.get(reverse('cadastrando_turmas', kwargs={'user_id':self.user.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_turmas.html')

        # TEST PADRÃO (GET)
        # abre_form = TRUE
        response = self.c.get(reverse('cadastrando_turmas_abre_form', kwargs={'user_id':self.user.id,'abre_form':True})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_turmas.html')
        self.assertEquals(response.context['contexto_extra_turmas'], True) #variavel setada TRUE quando abre_form = TRUE

        # TEST (POST)
        # TEST SUCESSO
        data = {'nome':'nome qualquer','quantidade_alunos':10}
        response = self.c.post(reverse('cadastrando_turmas', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastro_turmas/'+str(self.user.id)+'/Criou')

        # TEST (POST)
        # TEST ERRO - VALOR NEGATIVO NA QUANT ALUNOS
        data = {'nome':'nome qualquer','quantidade_alunos':-10}

        response = self.c.post(reverse('cadastrando_turmas', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_turmas.html')
        self.assertEquals(response.context['contexto_extra_turmas'], True) #variavel setada TRUE quando form da ERRO

##################################################################################################

    def test_altera_cargo(self):
        self.group.name = 'Secretaria'
        self.group.save()

        # TESTE PADRÃO (GET)
        response = self.c.get(reverse('abre_altera_cargo', kwargs={'elemento_id':self.classificacao.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['chave_altera_cargo'], True) #variavel setada TRUE quando a função função 'altera_cargo' chama a função 'cadastro_de_funcionarios_secretaria'

        #TESTE (POST)
        #TESTE EDITA SUCESSO
        self.user2 = User.objects.create_user(username="test2", email="test@test.com", password="test")
        self.classificacao2 = Classificacao.objects.create(user=self.user2)

        data = {'campo':'Coordenador'}
        response = self.c.post(reverse('altera_cargo', kwargs={'elemento_id':self.classificacao2.id,'edita':'sim'}), data) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/sim/Sucesso')

        #TESTE (POST)
        #TESTE INCOMPATIVEL - ID CLASSIFICACAO = ID USUARIO ATUAL, NÃO PODE ALTERAR PROPRIO STATUS
        data = {'campo':'Coordenador'}
        response = self.c.post(reverse('altera_cargo', kwargs={'elemento_id':self.classificacao.id,'edita':'sim'}), data) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/sim/Erro')

##################################################################################################

    def test_deleta_funcionario1(self):
        
        # TESTE USUARIO LOGADO: DIRETOR ESCOLA
        # DELETA FUNCIONARIO ESCOLA
        # VERIFICA SE DESATIVOU 1 USUÁRIO
        # VERIFICA SE REMOVEU 1 MEMBRO DO COLEGIADO DA ESCOLA
        grupos = Group.objects.all()
        self.group.name = 'Diretor_escola'
        self.group.save()
        self.user2 = User.objects.create_user(username="test2", email="test2@test.com", password="test")
        self.classificacao2 = Classificacao.objects.create(user=self.user2, tipo_de_acesso = 'Funcionario', cargo_herdado = 'Membro do colegiado', escola = self.escola)
        self.user3 = User.objects.create_user(username="test3", email="test3@test.com", password="test3")
        self.classificacao3 = Classificacao.objects.create(user=self.user3, tipo_de_acesso = 'Funcionario', cargo_herdado = 'Membro do colegiado', escola = self.escola)
        self.escola2 = Escola.objects.create(nome='escola_teste2')
        self.escola.quant_membro_colegiado = 1
        self.escola.save()
        self.user2.classificacao.escola = self.escola2
        self.user2.save()
        
        quant_membros_menos_1 = self.escola.quant_membro_colegiado - 1
        ativos_antes = len(User.objects.filter(is_active=True))

        response = self.c.get(reverse('deletando_funcionario', kwargs={'elemento_id':self.classificacao2.id}), follow=True) # Usa o nome da URL e atributos
        
        escola_pos = get_object_or_404(Escola, nome='escola_teste2')
        self.assertEqual(escola_pos.quant_membro_colegiado, quant_membros_menos_1)
        ativos_depois = len(User.objects.filter(is_active=True))
        self.assertEqual(ativos_antes, ativos_depois + 1)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/cadastro_funcionarios_escola/'+str(self.user.id)+'/Deletou')
        self.assertTemplateUsed(response, 'cadastros.html')
        self.assertEquals(response.context['chave_len_funcionarios_cadastrados'], 1)# Só existem 2 Funcionarios cadastrados no teste, como a função deleta um, sobra 1.

    def test_deleta_funcionario2(self):
        # TESTE USUARIO LOGADO: FUNC SEC
        # DELETA FUNCIONARIO SECRETARIA
        # VERIFICA SE DESATIVOU 1 USUÁRIO
        self.group.name = 'Func_sec'
        self.group.save()
        self.classificacao.usuario_diretor=True
        self.classificacao.save()
        group2 = get_object_or_404(Group, name='Func_sec')
        self.user3 = User.objects.create_user(username="test3", email="test3@test.com", password="test")
        self.escola3 = Escola.objects.create(nome='escola_teste3')
        self.classificacao3 = Classificacao.objects.create(user=self.user3, escola=self.escola3)
        self.user3.groups.add(group2)
        self.user3.save()

        ativos_antes = len(User.objects.filter(is_active=True))

        response = self.c.get(reverse('deletando_funcionario', kwargs={'elemento_id':self.classificacao3.id})) # Usa o nome da URL e atributos
        
        ativos_depois = len(User.objects.filter(is_active=True))
        self.assertEqual(ativos_antes, ativos_depois + 1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/Sim/Deletou')

    def test_deleta_funcionario3(self):
        # TESTE USUARIO LOGADO: FUNC SEC
        # DESATIVA DIRETOR ESCOLA
        # VERIFICA SE DESATIVOU 1 USUÁRIO
        # VERIFICA SE escola.diretor É REMOVIDO
        # VERIFICA SE escola.possui_diretor É REMOVIDO
        self.group.name = 'Func_sec'
        self.group.save()
        self.classificacao.usuario_diretor=True
        self.classificacao.save()
        self.group2 = Group(name='Diretor_escola')
        self.group2.save()
        self.user3 = User.objects.create_user(username="test4", email="test3@test.com", password="test")
        self.escola3 = Escola.objects.create(nome='escola_teste4')
        self.escola3.diretor = self.user3
        self.escola3.possui_diretor = True
        self.escola3.save()
        self.classificacao3 = Classificacao.objects.create(user=self.user3, escola=self.escola3)
        self.user3.groups.add(self.group2)
        self.user3.save()

        ativos_antes = len(User.objects.filter(is_active=True))

        response = self.c.get(reverse('deletando_funcionario', kwargs={'elemento_id':self.classificacao3.id})) # Usa o nome da URL e atributos
        
        ativos_depois = len(User.objects.filter(is_active=True))
        self.assertEqual(ativos_antes, ativos_depois + 1)
        escola_depois = get_object_or_404(Escola, pk=self.escola3.pk)
        self.assertEqual(escola_depois.diretor, None)
        self.assertEqual(escola_depois.possui_diretor, False)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/escola/'+str(self.escola3.id))

    def test_deleta_funcionario4(self):
        # TESTE USUARIO LOGADO: SECRETARIA
        # DESATIVA DIRETOR SUPROT
        # VERIFICA SE DESATIVOU 1 USUÁRIO
        # VERIFICA SE secretaria.diretor É REMOVIDO
        # VERIFICA SE secretaria.possui_diretor É REMOVIDO
        # VERIFICA SE classificacao.usuario_diretor É REMOVIDO
        # VERIFICA SE classificacao.is_active É REMOVIDO
        self.group.name = 'Secretaria'
        self.group.save()
        self.secretaria = Escola.objects.create(nome='Secretaria da educação')
        self.secretaria.possui_diretor = True
        self.secretaria.objeto_suprot = True
        self.secretaria.save()
        self.classificacao.tipo_de_acesso = 'Secretaria'
        self.classificacao.save()
        group2 = get_object_or_404(Group, name='Func_sec')
        self.user3 = User.objects.create_user(username="test3", email="test3@test.com", password="test")
        self.classificacao3 = Classificacao.objects.create(user=self.user3, escola=self.secretaria, usuario_diretor=True, matriz='Secretaria da educação', cargo_herdado='Diretor SUPROT', tipo_de_acesso='Func_sec')
        self.user3.groups.add(group2)
        self.user3.save()
        self.secretaria.diretor = self.user3
        self.secretaria.save()

        ativos_antes = len(User.objects.filter(is_active=True))

        response = self.c.get(reverse('deletando_funcionario', kwargs={'elemento_id':self.classificacao3.id})) # Usa o nome da URL e atributos
        
        ativos_depois = len(User.objects.filter(is_active=True))
        self.assertEqual(ativos_antes, ativos_depois + 1)
        secretaria_depois = get_object_or_404(Escola, pk=self.secretaria.pk)
        self.assertEqual(secretaria_depois.diretor, None)
        self.assertEqual(secretaria_depois.possui_diretor, False)
        classificacao_diretor = get_object_or_404(Classificacao, pk=self.classificacao3.pk)
        self.assertEqual(classificacao_diretor.usuario_diretor, False)
        self.assertEqual(classificacao_diretor.is_active, False)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/Sim/Deletou')

##################################################################################################

    def test_cadastros_da_secretaria(self):
        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE PADRÃO GET
        self.group.name = 'Func_sec'
        self.group.save()

        response = self.c.get(reverse('chama_cadastros_secretaria')) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')

        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE PADRÃO GET MENSAGEM
        response = self.c.get(reverse('chama_cadastros_secretaria_mensagem', kwargs={'mensagem':'Criou'})) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')

        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE SEARCH POR ESCOLAS

        data = {'campo':'teste'}
        response = self.c.get(reverse('pesquisa_cadastro_escolas', kwargs={'search':'sim'}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['chave_var_pesquisa_escola'], True) #variavel setada TRUE quando há uma pesquisa

        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE CADASTRO DE DIRETOR
        response = self.c.get(reverse('chama_cadastrar_diretor', kwargs={'escola_id':self.escola.id,'cadastro_diretor':True})) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['contexto_extra_form_diretor'], True) #variavel setada TRUE quando há uma pesquisa

##################################################################################################

    def test_cadastros_escola(self): # ESCOLAS CADASTRANDO FUNCIONARIOS
        # TESTE USUARIO LOGADO: DIRETOR ESCOLA
        # FORMULARIO VALIDO
        self.group.name = 'Diretor_escola'
        self.group.save()
        funcionarios_mais_um = self.escola.quant_funcionarios + 1

        data = {'first_name':'Bezerra Menezes','cargo':'Tesoureiro(a)','email':'YkREep@fres.com'}
        response = self.c.post(reverse('cadastrar_funcionarios', kwargs={'user_id':self.user.id}), data, follow=True) # Usa o nome da URL e atributos
        
        usuario_criado = User.objects.filter(first_name='Bezerra Menezes') 
        self.assertTrue(usuario_criado)
        usuario_criado2 = get_object_or_404(User, first_name='Bezerra Menezes')
        classificacao_teste = Classificacao.objects.filter(user=usuario_criado2)
        self.assertTrue(classificacao_teste)
        escola_matriz = get_object_or_404(Escola, pk=self.escola.id)
        self.assertEqual(escola_matriz.quant_funcionarios, funcionarios_mais_um)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/cadastro_funcionarios_escola/'+str(self.user.id)+'/Criou')
        self.assertTemplateUsed(response, 'cadastros.html')

        # TESTE USUARIO LOGADO: DIRETOR ESCOLA
        # FORMULARIO INVALIDO

        data = {
        'first_name':'nome qualquer',
        'cargo':'Tesoureiro(a)',
        'email':'test@test.com' # erro, ja existe
        }
        response = self.c.post(reverse('cadastrar_funcionarios', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros.html')
        self.assertEquals(response.context['contexto_extra_form_funcionarios'], True)

##################################################################################################

    def test_cadastro_de_escolas(self): # FUNC_SEC CADASTRANDO ESCOLAS
        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE (POST) - CADASTRO DE ESCOLA
        # POST SUCESSO
        self.group.name = 'Func_sec'
        self.group.save()

        data = {'last_name':'nome qualquer','municipio':'qualquer','codigo_escola':'12345','nte':'30'}
        response = self.c.post(reverse('cadastrar_escolas', kwargs={'user_id':self.user.id}), data, follow=True) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/escola/cadastros/Criou')
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['chave_len_escolas_a_exibir'], 2) # 1 escola setada no teste, e outra criada na função.

        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE (POST) - CADASTRO DE ESCOLA
        # POST ERRO
        data = {
            'last_name':'escola_teste', # erro escola ja existe
            'municipio':'qualquer',
            'codigo_escola':'12345',
            'nte':'30'}
        response = self.c.post(reverse('cadastrar_escolas', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['contexto_extra_form_escolas'], True) #variavel setada TRUE quando o form da ERRO

##################################################################################################

    def test_cadastro_diretor_escola(self):
        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE (POST) - CADASTRO DE ESCOLA
        # POST ERRO
        self.group.name = 'Func_sec'
        self.group.save()

        data = {
            'first_name':'Ezequiel diretor', 
            'email':'test@test.com'} # erro ja existe funcionario com este email
        response = self.c.post(reverse('cadastrar_diretor', kwargs={'escola_id':self.escola.id}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['contexto_extra_form_diretor'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE (POST) - CADASTRO DE ESCOLA
        # POST SUCESSO
        if not Group.objects.filter(name='Diretor_escola').exists():
            self.group2 = Group(name='Diretor_escola')
            self.group2.save()
        else:
            self.group2.name = 'Diretor_escola'
            self.group2.save()
        data = {
            'first_name':'Ezequiel diretor', 
            'email':'email_unicoKFEPFS@test.com'} 
        response = self.c.post(reverse('cadastrar_diretor', kwargs={'escola_id':self.escola.id}), data, follow=True) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/escola/cadastros/Criou_diretor')
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')

##################################################################################################

    def test_cadastro_de_funcionarios_secretaria(self): # FUNC_SEC CADASTRANDO OUTROS FUNC_SEC
        # TESTE USUARIO LOGADO: COORDENADOR
        # TESTE PADRÃO (GET)
        self.classificacao.usuario_coordenador = True
        self.classificacao.save()

        response = self.c.get(reverse('cadastrar_funcionarios_secretaria', kwargs={'user_id':self.user.id,'cad_funcionarios':'sim'})) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')

        # TESTE USUARIO LOGADO: SECRETARIA
        # TESTE (POST) - CADASTRO DE DIRETOR/COORDENADOR/TECNICO
        # TESTE SUCESSO
        self.group2 = Group(name='Func_sec')
        self.group2.save()
        self.group.name = 'Secretaria'
        self.group.save()
        self.classificacao.usuario_coordenador = False
        self.classificacao.save()

        data = {'cargo':'Diretor SUPROT','email':'unico_JFeisaFSd@fes.com','first_name':'Cirino qualquer'}
        kwargs = {'user_id':self.user.id,'cad_funcionarios':'sim'}
        response = self.c.post(reverse('cadastrar_funcionarios_secretaria', kwargs=kwargs), data, follow=True) # Usa o nome da URL e atributos

        usuario_criado = User.objects.filter(first_name='Cirino qualquer') 
        self.assertTrue(usuario_criado)
        usuario_criado2 = get_object_or_404(User, first_name='Cirino qualquer')
        classificacao_teste = Classificacao.objects.filter(user=usuario_criado2)
        self.assertTrue(classificacao_teste)
        escola_matriz = get_object_or_404(Escola, pk=self.escola.id)
        self.assertTrue(escola_matriz.possui_diretor)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/Sim/Criou_func')
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')

        # TESTE USUARIO LOGADO: SECRETARIA
        # TESTE (POST) - CADASTRO DE DIRETOR/COORDENADOR/TECNICO
        # TESTE ERRO
        data = {
        'cargo':'Diretor SUPROT',
        'first_name':'nome qualquer',
        'email':'test@test.com' # Erro email ja existente
        }
        response = self.c.post(reverse('cadastrar_funcionarios_secretaria', kwargs={'user_id':self.user.id,'cad_funcionarios':'sim'}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['contexto_extra_form_funcionarios'], True) #variavel setada TRUE quando há um erro no form

        # TESTE USUARIO LOGADO: SECRETARIA
        # TESTE PESQUISA FUNCIONARIOS
        # TESTE (POST) - CADASTRO DE DIRETOR/COORDENADOR/TECNICO
        response = self.c.get(reverse('pesquisa_cadastro_funcionarios', kwargs={'user_id':self.user.id,'cad_funcionarios':'sim','search':'sim'})) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['chave_var_pesquisa_func'], True) #variavel setada TRUE quando há uma pesquisa

##################################################################################################

    def test_solicita_remocao(self):
        # TESTE POST
        # USUARIO LOGADO: DIRETOR FUNC_SEC
        # SOLICITA REMOÇÃO DFE DIRETOR ESCOLAR
        self.group.name = 'Func_sec'
        self.group.save()
        self.user2 = User.objects.create_user(username="test2", email="test2@test.com", password="test2")
        self.classificacao2 = Classificacao.objects.create(user=self.user2, escola=self.escola)
        self.escola.diretor = self.user2
        self.escola.save()

        response = self.c.post(reverse('solicitar_remocao', kwargs={'user_id':self.user2.id}), follow=True) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/profile/escola/'+str(self.escola.id))
        self.assertTemplateUsed(response, 'Profile_escola.html')
        self.assertEquals(response.context['chave_confirma_remocao_diretor'], True)

##################################################################################################

    def test_cancela_remocao_diretor(self):
        # TESTE POST
        # USUARIO LOGADO: FUNC_SEC
        # CANCELA REMOÇÃO DE DIRETOR ESCOLAR
        # VERIFICA ALTERAÇÕES NA CLASSIFICACAO
        self.group.name = 'Func_sec'
        self.group.save()
        self.classificacao.usuario_diretor = True
        self.classificacao.save()
        self.user2 = User.objects.create_user(username="test2", email="test2@test.com", password="test2")
        self.classificacao2 = Classificacao.objects.create(user=self.user2, escola=self.escola)
        self.classificacao2.marcado_para_exclusao = True
        self.classificacao2.remocao_solicitante = self.user.first_name
        self.classificacao2.save()

        response = self.c.post(reverse('cancelar_remocao', kwargs={'user_id':self.user2.id}), follow=True) # Usa o nome da URL e atributos

        classi_depois = get_object_or_404(Classificacao, pk=self.classificacao2.pk)
        self.assertEqual(classi_depois.marcado_para_exclusao, False)
        self.assertEqual(classi_depois.remocao_solicitante, '')

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/profile/escola/'+str(self.escola.id))
        self.assertTemplateUsed(response, 'Profile_escola.html')