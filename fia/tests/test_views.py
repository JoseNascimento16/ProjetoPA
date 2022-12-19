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
        # self.ordem = Ordens.objects.create(plano=self.plano, identificacao_numerica=1, data_de_criação=timezone.now())
        # self.ordem.save()
        # self.codigo = ModeloCodigos.objects.create(ordem=self.ordem, identificacao='A', quantidade=1)
        # self.codigo.save()
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

    def test_remove_assinatura_tecnico(self):
        # TESTE (POST)
        # USUARIO: Diretor
        # REDIRECIONA
        self.classificacao.plano_associado.add(self.plano)
        self.classificacao.save()
        self.modelo_fia.assinatura_tecnico = SimpleUploadedFile(name='test_image.jpg', content=open('static/img/hexagonal.jpg', 'rb').read(), content_type='image/jpeg')
        self.modelo_fia.save()
        # print(len(self.plano.classificacao_set.all()))
        self.plano.assinaturas = 2
        self.plano.save()

        kwargs = {'modelo_fia_id':self.modelo_fia.id}
        response = self.c.post(reverse('apaga_assinatura_tecnico', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes')

    def test_salva_assinatura_tecnico_fia(self):
        # TESTE (POST)
        # GRUPO INCOMPLETO
        # REDIRECIONA
        kwargs = {'modelo_fia_id':self.modelo_fia.id}
        response = self.c.post(reverse('salvando_assinatura_tecnico', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/grupo_incompleto')

        # TESTE (POST)
        # SALVOU IMAGEM ASSINATURA TECNICO FIA
        self.modelo_fia.membro_colegiado_1 = self.user
        self.modelo_fia.membro_colegiado_2 = self.user
        self.modelo_fia.tecnico_responsavel = 'Queiroz'
        self.modelo_fia.save()
        imagem = SimpleUploadedFile(name='test_image.jpg', content=open('static/img/canvas_data_test.jpg', 'rb').read(), content_type='image/jpeg')
        imgTo_base64_str = base64.b64encode(imagem.read()).decode('utf-8')
        prefixo = 'data:image/jpeg;base64,'
        DataUrl = prefixo + imgTo_base64_str
        # print(DataUrl)
        
        data = {'canvasData':DataUrl}
        kwargs = {'modelo_fia_id':self.modelo_fia.id}
        response = self.c.post(reverse('salvando_assinatura_tecnico', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes')

    def test_corrige_fia(self):
        # TESTE (POST)
        # ERRO ANO_EXERCICIO
        # ident_numerica != 1 (extra_fia)
        self.correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=2, documento_associado = '1 - Identificação das ações')
        
        data = {
            'valor_numerico':2,
            'discriminacao':'a',
            'quantidade':1,
            'preco_unitario_item':'', # erro, vazio
            'justificativa':'a',
        }
        kwargs = {'elemento_id':self.plano.id,'ident_numerica':2}
        response = self.c.post(reverse('corrigindo_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        
        # TESTE (POST)
        # SUCESSO
        # ident_numerica != 1 (extra_fia)
        data = {
            'valor_numerico':2,
            'discriminacao':'a',
            'quantidade':1,
            'preco_unitario_item':1,
            'justificativa':'a',
        }
        kwargs = {'elemento_id':self.plano.id,'ident_numerica':2}
        response = self.c.post(reverse('corrigindo_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/correcoes/'+str(self.plano.id)+'/Sucesso')

        # TESTE (POST)
        # ERRO ANO_EXERCICIO
        # ident_numerica = 1 (modelo_fia)
        self.correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=1, documento_associado = '1 - Identificação das ações')
        
        data = {
            'nome_caixa_escolar':'a',
            'ano_exercicio':2022,
            'discriminacao':'a',
            'preco_unitario_item':100,
            'justificativa':'a',
            'membro1':self.classificacao.id,
            'membro2':self.classificacao.id,
        }
        kwargs = {'elemento_id':self.plano.id,'ident_numerica':1}
        response = self.c.post(reverse('corrigindo_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')

        # TESTE (POST)
        # SUCESSO
        # ident_numerica = 1 (modelo_fia)
        self.classificacao.tipo_de_acesso = 'Funcionario'
        self.classificacao.cargo_herdado = 'Membro do colegiado'
        self.classificacao.save()
        self.user2 = User.objects.create_user(first_name='test2' ,username="test2", email="test2@test.com", password="test2")
        self.classificacao2 = Classificacao.objects.create(user=self.user2, escola=self.escola, tipo_de_acesso='Funcionario', cargo_herdado='Membro do colegiado')
        
        data = {
            'nome_caixa_escolar':'a',
            'ano_exercicio':2022,
            'discriminacao':'a',
            'preco_unitario_item':100,
            'justificativa':'a',
            'membro1':self.classificacao.id,
            'membro2':self.classificacao2.id,
        }
        kwargs = {'elemento_id':self.plano.id,'ident_numerica':1}
        response = self.c.post(reverse('corrigindo_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/correcoes/'+str(self.plano.id)+'/Sucesso')

    def test_abre_correcao_fia(self):
        # TESTE (GET)
        # ident_numerica = 1 (modelo_fia)
        self.correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=1, documento_associado = 'FIA - Formulário de Inclusão de Ações')
        
        kwargs = {'elemento_id':self.plano.id,'ident_numerica':1}
        response = self.c.get(reverse('abrindo_correcao_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        self.assertEquals(response.context['chave_corrigindo_modelo_fia'], True)

        # TESTE (GET)
        # ident_numerica != 1 (Extra_fia)
        self.correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=2, documento_associado = 'FIA - Formulário de Inclusão de Ações')
        
        kwargs = {'elemento_id':self.plano.id,'ident_numerica':2}
        response = self.c.get(reverse('abrindo_correcao_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        self.assertEquals(response.context['chave_corrigindo_extra_fia'], True)

    def test_deleta_correcao_fia(self):
        # TESTE (POST)
        # Acesso restrito
        # redireciona dashboard
        kwargs = {'plano_id':self.plano.id,'ordem_fia_id':self.modelo_fia.id,'tipo_ordem':'modelo_fia'}
        response = self.c.post(reverse('chamando_deleta_correcao_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard')
        
        # TESTE (POST)
        # Tipo_ordem = 'modelo_fia'
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.corretor_plano = self.user
        self.plano.save()
        self.correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=1, documento_associado = 'FIA - Formulário de Inclusão de Ações')
        
        kwargs = {'plano_id':self.plano.id,'ordem_fia_id':self.modelo_fia.id,'tipo_ordem':'modelo_fia'}
        response = self.c.post(reverse('chamando_deleta_correcao_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/excluiu_sugestao')

        # TESTE (POST)
        # Tipo_ordem = 'extra_fia'
        self.correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=2, documento_associado = 'FIA - Formulário de Inclusão de Ações')
        
        kwargs = {'plano_id':self.plano.id,'ordem_fia_id':self.extra_fia.id,'tipo_ordem':'extra_fia'}
        response = self.c.post(reverse('chamando_deleta_correcao_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/excluiu_sugestao')

    def test_cria_altera_correcao_fia(self):
        # TESTE (POST)
        # ordem_associada = 1
        # Não possui correção: CRIA!
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.corretor_plano = self.user
        self.plano.save()
        
        data = {
            'plano_nome':self.plano.ano_referencia,
            'documento_associado':'FIA - Formulário de Inclusão de Ações',
            'ordem_associada':1,
            'sugestao':'a'}
        kwargs = {'plano_id':self.plano.id,'ordem_fia_id':self.modelo_fia.id}
        response = self.c.post(reverse('chamando_cria_altera_correcao_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/criou')

        # TESTE (POST)
        # ordem_associada = 1
        # já possui correção: ALTERA!
        self.correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=1, documento_associado = 'FIA - Formulário de Inclusão de Ações')
        
        data = {
            'plano_nome':self.plano.ano_referencia,
            'documento_associado':'FIA - Formulário de Inclusão de Ações',
            'ordem_associada':1,
            'sugestao':'b'}
        kwargs = {'plano_id':self.plano.id,'ordem_fia_id':self.modelo_fia.id}
        response = self.c.post(reverse('chamando_cria_altera_correcao_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/editou')

    def test_correcao_plano_fia(self):
        # TESTE (GET)
        # modelo_fia_id
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.corretor_plano = self.user
        self.plano.save()

        kwargs = {'elemento_id':self.plano.id,'modelo_fia_id':self.modelo_fia.id}
        response = self.c.get(reverse('chamando_correcao_modelo_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertEquals(response.context['chave_contexto_corrigir_fia'], True)

        # TESTE (GET)
        # ordem_extra_id
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.corretor_plano = self.user
        self.plano.save()

        kwargs = {'elemento_id':self.plano.id,'ordem_extra_id':self.extra_fia.id}
        response = self.c.get(reverse('chamando_correcao_extra_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertEquals(response.context['chave_contexto_corrigir_fia'], True)

    def test_exclui_ordem_extra_fia(self):
        # TESTE (POST)
        # ACESSO RESTRITO
        self.group.name = 'Func_sec'
        self.group.save()

        kwargs = {'ordem_extra_id':self.extra_fia.id}
        response = self.c.post(reverse('excluir_extra_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/not_allowed')

        # TESTE (POST)
        # EXCLUIR ORDEM EXTRA
        self.group.name = 'Diretor_escola'
        self.group.save()

        kwargs = {'ordem_extra_id':self.extra_fia.id}
        response = self.c.post(reverse('excluir_extra_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/excluiu_extra')

    def test_altera_ordem_extra_fia(self):
        # TESTE (POST)
        # ERRO: Form invalido
        data = {
            'valor_numerico':1, #erro, valor minimo é 2
            'discriminacao':'a',
            'quantidade':1,
            'preco_unitario_item':1,
            'justificativa':'a',
        }
        kwargs = {'modelo_fia_id':self.modelo_fia.id, 'ordem_extra_id':self.extra_fia.id}
        response = self.c.post(reverse('altera_extra_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertEquals(response.context['contexto_extra_ordem_fia'], True)

        # TESTE (POST)
        # SUCESSO: ALTEROU ORDEM EXTRA
        data = {
            'valor_numerico':2, 
            'discriminacao':'a',
            'quantidade':1,
            'preco_unitario_item':1,
            'justificativa':'a',
        }
        kwargs = {'modelo_fia_id':self.modelo_fia.id, 'ordem_extra_id':self.extra_fia.id}
        response = self.c.post(reverse('altera_extra_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/sucesso2')

    def test_cria_ordem_extra_fia(self):
        # TESTE (POST)
        # ERRO: Form invalido
        # Ordem já existe
        data = {
            'valor_numerico':2, #erro, valor de ordem que ja existe
            'discriminacao':'a',
            'quantidade':1,
            'preco_unitario_item':1,
            'justificativa':'a',
        }
        kwargs = {'modelo_fia_id':self.modelo_fia.id}
        response = self.c.post(reverse('cria_extra_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertEquals(response.context['contexto_extra_ordem_fia'], True)

        # TESTE (POST)
        # SUCESSO: CRIA ORDEM EXTRA
        data = {
            'valor_numerico':3, 
            'discriminacao':'a',
            'quantidade':1,
            'preco_unitario_item':1,
            'justificativa':'a',
        }
        kwargs = {'modelo_fia_id':self.modelo_fia.id}
        response = self.c.post(reverse('cria_extra_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/criou_extra')

    def test_altera_fia(self):
        # TESTE (POST)
        # ERRO: Form com erro - membros iguais
        self.classificacao.tipo_de_acesso = 'Funcionario'
        self.classificacao.cargo_herdado = 'Membro do colegiado'
        self.classificacao.save()
    
        data = {
            'membro1':self.classificacao.id,
            'membro2':self.classificacao.id, # Erro, membros nao podem ser iguais
            'nome_caixa_escolar':'a',
            'ano_exercicio':2022,
            'discriminacao':'a',
            'preco_unitario_item':1,
            'justificativa':'a',
            'tecnico_responsavel':'a',
        }
        kwargs = {'elemento_id':self.modelo_fia.id}
        response = self.c.post(reverse('chama_altera_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertEquals(response.context['contexto_extra_modelo_fia'], True)

        
        # TESTE (POST)
        # SUCESSO: ALTEROU MODELO FIA
        self.user2 = User.objects.create_user(first_name='test2' ,username="test2", email="test2@test.com", password="test2")
        self.classificacao2 = Classificacao.objects.create(user=self.user2, escola=self.escola, tipo_de_acesso='Funcionario', cargo_herdado='Membro do colegiado')
        self.classificacao2.save()

        data = {
            'nome_caixa_escolar':'a',
            'ano_exercicio':2022,
            'discriminacao':'a',
            'preco_unitario_item':1,
            'justificativa':'a',
            'tecnico_responsavel':'a',
            'membro1':self.classificacao.id,
            'membro2':self.classificacao2.id, 
        }
        kwargs = {'elemento_id':self.modelo_fia.id}
        response = self.c.post(reverse('chama_altera_fia', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/sucesso2')

    def test_documento_fia(self):
        # TESTE (GET)
        # PLANO FIA NÃO POSSUI MODELO_FIA
        # TESTA CRIAÇÃO DE MODELO_FIA CASO NAO EXISTA
        self.modelo_fia.plano = self.plano2 # Desta forma o 'plano' id=1 fica sem modelo_fia atribuido e podemos testar isso mandando o 'plano' para o kwargs
        self.modelo_fia.save()

        kwargs = {'elemento_id':self.plano.id}
        response = self.c.get(reverse('chamando_documento_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')

        # TESTE (GET)
        # JÁ EXISTE ORDEM_EXTRA(extra_fia) CRIADA (SETUP)
        # VERIFICA SE ENCONTRA ORDENS_EXTRAS NO CONTEXTO
        kwargs = {'elemento_id':self.plano2.id}
        response = self.c.get(reverse('chamando_documento_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertTrue(response.context['chave_ordens_extra'])

        # TESTE (GET)
        # Chama cria extra_fia
        # URL com SLUG: abreform_extra_criacao
        kwargs = {'elemento_id':self.plano2.id, 'abreform_extra_criacao':'sim'}
        response = self.c.get(reverse('chama_cria_extra_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertTrue(response.context['chave_abre_form_extra_criacao'])

        # TESTE (GET)
        # Chama altera extra_fia
        # URL com SLUG: abreform_extra_edicao e ordem_extra_id
        kwargs = {'elemento_id':self.plano2.id, 'abreform_extra_edicao':'sim', 'ordem_extra_id':self.extra_fia.id}
        response = self.c.get(reverse('chama_altera_extra_fia', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fia-visualizacao.html')
        self.assertTrue(response.context['chave_abre_form_extra_edicao'])
        self.assertTrue(response.context['chave_modo_edicao'])

    def test_cria_fia(self):
        # TESTE (POST)
        # ERRO: JA EXISTE PLANO COM ESTE NOME
        self.modelo_fia.plano = self.plano2 # Desta forma o 'plano' id=1 fica sem modelo_fia atribuido e podemos testar isso mandando o 'plano' para o kwargs
        self.modelo_fia.save()

        data = {'ano_referencia':'nome_qualquer'} # erro nome ja existe
        response = self.c.post(reverse('criando_fia'), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['contexto_extra_fia'], True)

        # TESTE (POST)
        # SUCESSO: CRIOU PLANO FIA
        self.modelo_fia.plano = self.plano2 # Desta forma o 'plano' id=1 fica sem modelo_fia atribuido e podemos testar isso mandando o 'plano' para o kwargs
        self.modelo_fia.save()

        data = {'ano_referencia':'nome_unico'}
        response = self.c.post(reverse('criando_fia'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Criou/msg')