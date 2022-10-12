from http import HTTPStatus
from urllib.parse import urlencode
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from Escolas.models import Escola
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
        imagem = SimpleUploadedFile(name='test_image.jpg', content=open('SetupPrincipal/static/img/canvas_data_test.jpg', 'rb').read(), content_type='image/jpeg')
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

    def test_altera_nome(self):

        #FORM VALIDO
        data = {'first_name':'nome qualquer'}
        response = self.c.post('/profile/altera/'+str(self.user.id), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

        #FORM INVALIDO
        data = {'first_name':'nome4444'}
        response = self.c.post('/profile/altera/'+str(self.user.id), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

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
        # KWARGS altera == 'alt_name'
        response = self.c.get(reverse('abre_altera_nome', kwargs={'user_id':self.user.id, 'altera':'alt_name'})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['chave_abre_altera_nome'], True) #variavel setada TRUE quando altera == 'alt_name'

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
        self.group.name = 'Diretor_escola'
        self.group.save()
        self.user2 = User.objects.create_user(username="test2", email="test2@test.com", password="test")
        self.classificacao2 = Classificacao.objects.create(user=self.user2)
        self.classificacao2.tipo_de_acesso = 'Funcionario'
        self.classificacao2.cargo_herdado = 'Membro do colegiado'
        self.classificacao2.escola = self.escola
        self.classificacao2.save()
        self.escola2 = Escola.objects.create(nome='escola_teste2')
        self.escola.quant_membro_colegiado = 1
        self.escola.save()
        self.user2.classificacao.escola = self.escola2
        self.user2.save()

        response = self.c.get(reverse('deletando_funcionario', kwargs={'elemento_id':self.classificacao2.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastro_funcionarios_escola/'+str(self.user.id)+'/Deletou')

    def test_deleta_funcionario2(self):
        # TESTE USUARIO LOGADO: FUNC SEC
        # DELETA FUNCIONARIO SECRETARIA
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

        response = self.c.get(reverse('deletando_funcionario', kwargs={'elemento_id':self.classificacao3.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/Sim/Deletou')

    def test_deleta_funcionario3(self):
        # TESTE USUARIO LOGADO: FUNC SEC
        # DELETA DIRETOR ESCOLA
        self.group.name = 'Func_sec'
        self.group.save()
        self.classificacao.usuario_diretor=True
        self.classificacao.save()
        self.group2 = Group(name='Diretor_escola')
        self.group2.save()
        self.user3 = User.objects.create_user(username="test4", email="test3@test.com", password="test")
        self.escola3 = Escola.objects.create(nome='escola_teste4')
        self.classificacao3 = Classificacao.objects.create(user=self.user3, escola=self.escola3)
        self.user3.groups.add(self.group2)
        self.user3.save()

        response = self.c.get(reverse('deletando_funcionario', kwargs={'elemento_id':self.classificacao3.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/Sim/Deletou')

##################################################################################################

    def test_cadastros_escola(self): # ESCOLAS CADASTRANDO FUNCIONARIOS
        # TESTE USUARIO LOGADO: DIRETOR ESCOLA
        # FORMULARIO VALIDO
        self.group.name = 'Diretor_escola'
        self.group.save()

        data = {'first_name':'nome qualquer2','cargo':'Tesoureiro(a)','username':'username2','password':'jfwoeaiHFOHAW','password2':'jfwoeaiHFOHAW'}
        response = self.c.post(reverse('cadastrar_funcionarios', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastro_funcionarios_escola/'+str(self.user.id)+'/Criou')

        # TESTE USUARIO LOGADO: DIRETOR ESCOLA
        # FORMULARIO INVALIDO
        self.group.name = 'Diretor_escola'
        self.group.save()

        data = {'first_name':'nome qualquer','cargo':'ERRADO','username':'username','password':'jfwoeaiHFOHAW','password2':'jfwoeaiHFOHAW'}
        response = self.c.post(reverse('cadastrar_funcionarios', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros.html')

##################################################################################################

    def test_cadastro_de_escolas(self): # FUNC_SEC CADASTRANDO ESCOLAS
        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE PADRÃO (GET)
        self.group.name = 'Func_sec'
        self.group.save()

        response = self.c.get(reverse('cadastrar_escolas', kwargs={'user_id':self.user.id})) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')

        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE (POST) - CADASTRO DE ESCOLA
        # POST SUCESSO
        data = {'last_name':'nome qualquer','municipio':'qualquer','codigo_escola':'12345','nte':'30'}
        response = self.c.post(reverse('cadastrar_escolas', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastro_escolas/'+str(self.user.id)+'/Criou')

        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE (POST) - CADASTRO DE ESCOLA
        # POST ERRO
        data = {'last_name':'escola_teste','municipio':'qualquer','codigo_escola':'12345','nte':'30'}
        response = self.c.post(reverse('cadastrar_escolas', kwargs={'user_id':self.user.id}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['contexto_extra_form_escolas'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE USUARIO LOGADO: FUNC SEC
        # TESTE SEARCH POR ESCOLAS
        response = self.c.get(reverse('pesquisa_cadastro_escolas', kwargs={'user_id':self.user.id,'search':'sim'})) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['chave_var_pesquisa_escola'], True) #variavel setada TRUE quando há uma pesquisa

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

        data = {'cargo':'Diretor','first_name':'nome qualquer','username':'username','password':'jfwoeaiHFOHAW','password2':'jfwoeaiHFOHAW'}
        response = self.c.post(reverse('cadastrar_funcionarios_secretaria', kwargs={'user_id':self.user.id,'cad_funcionarios':'sim'}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cadastros_secretaria/'+str(self.user.id)+'/Sim/Criou')

        # TESTE USUARIO LOGADO: SECRETARIA
        # TESTE (POST) - CADASTRO DE DIRETOR/COORDENADOR/TECNICO
        # TESTE ERRO
        data = {'cargo':'Diretor','first_name':'nome qualquer','username':'username','password':'jfwoeaiHFOHAW','password2':'senha_nao_coincidente'}
        response = self.c.post(reverse('cadastrar_funcionarios_secretaria', kwargs={'user_id':self.user.id,'cad_funcionarios':'sim'}), data) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['contexto_extra_form_funcionarios'], True) #variavel setada TRUE quando há um erro no form

        # TESTE USUARIO LOGADO: SECRETARIA
        # TESTE (POST) - CADASTRO DE DIRETOR/COORDENADOR/TECNICO
        response = self.c.get(reverse('pesquisa_cadastro_funcionarios', kwargs={'user_id':self.user.id,'cad_funcionarios':'sim','search':'sim'})) # Usa o nome da URL e atributos

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastros-secretaria.html')
        self.assertEquals(response.context['chave_var_pesquisa_func'], True) #variavel setada TRUE quando há uma pesquisa
