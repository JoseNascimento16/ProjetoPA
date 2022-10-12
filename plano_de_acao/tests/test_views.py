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

    def test_adiciona_remove_turma(self):
        # TESTE PADRÃO (GET)
        # INACESSÍVEL - ALTERABILIDADE ERRADA
        # PLANO NORMAL
        turma = Turmas.objects.create(escola=self.escola, quantidade_alunos=10)
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()
        response = self.c.get(reverse('adicionando_removendo_turma', kwargs={'plano_id':self.plano.id,'turma_id':turma.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Acesso_negado_situacao')

        # TESTE PADRÃO (GET)
        # INACESSÍVEL - ALTERABILIDADE ERRADA
        # PLANO TIPO FIA
        turma = Turmas.objects.create(escola=self.escola, quantidade_alunos=10)
        self.plano.alterabilidade = 'Secretaria'
        self.plano.tipo_fia = True
        self.plano.save()
        response = self.c.get(reverse('adicionando_removendo_turma', kwargs={'plano_id':self.plano.id,'turma_id':turma.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/not_allowed')

        # TESTE PADRÃO (GET)
        # USUARIO LOGADO: DIRETOR ESCOLA
        # SUCESSO
        turma = Turmas.objects.create(escola=self.escola, quantidade_alunos=10)
        self.plano.alterabilidade = 'Escola'
        self.plano.tipo_fia = False
        self.plano.save()
        response = self.c.get(reverse('adicionando_removendo_turma', kwargs={'plano_id':self.plano.id,'turma_id':turma.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Sucesso')

        # TESTE PADRÃO (GET)
        # USUARIO LOGADO: DIRETOR ESCOLA
        # SUCESSO
        turma = Turmas.objects.create(escola=self.escola, quantidade_alunos=10)
        self.plano.alterabilidade = 'Escola'
        self.plano.tipo_fia = True
        self.plano.save()
        response = self.c.get(reverse('adicionando_removendo_turma', kwargs={'plano_id':self.plano.id,'turma_id':turma.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/Sucesso')

    def test_aprova_plano(self):
        # TESTE PADRÃO (GET)
        # ACESSO NEGADO
        # USUARIO LOGADO: ERRADO (Diretor_escola)
        response = self.c.get(reverse('aprovar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado/msg')

        # TESTE (POST)
        # USUARIO LOGADO: CORRETO (Func_sec)
        self.group.name = 'Func_sec'
        self.group.save()

        response = self.c.post(reverse('aprovar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Aprovou/msg')

    def test_atribui_corretor(self):
        # TESTE PADRÃO (GET)
        # ACESSO NEGADO
        # USUARIO LOGADO: ERRADO (Diretor_escola)
        response = self.c.get(reverse('chamando_atribui_corretor', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado_situacao/msg')

        # TESTE PADRÃO (GET)
        # USUARIO LOGADO: CORRETO (Func_sec)
        # ATRIBUIU CORRETOR
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()

        response = self.c.get(reverse('chamando_atribui_corretor', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Atribuiu/msg')

        # TESTE PADRÃO (GET)
        # USUARIO LOGADO: CORRETO (Func_sec)
        # JÁ POSSUI CORRETOR
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.corretor_plano = self.user
        self.plano.save()

        response = self.c.get(reverse('chamando_atribui_corretor', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Ja_possui/msg')

    def test_quebra_de_linha(self):
        # TESTE PADRÃO (GET)
        # ERRO, ACESSO SEM ARGS NO GET
        # REDIRECIONA DASHBOARD
        response = self.c.get(reverse('insere_quebra_de_linha', kwargs={'plano_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard')

        # TESTE PADRÃO (GET)
        # ARGUMENTO GET: 'ordemid' e 'valor'
        data = {'ordemid':self.ordem.id,'valor':1}
        response = self.c.get(reverse('insere_quebra_de_linha', kwargs={'plano_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Sucesso2/q/q_linha')

        # TESTE PADRÃO (GET)
        # ARGUMENTO GET: 'codigoid' e 'valor'
        data = {'codigoid':self.codigo.id,'valor':1}
        response = self.c.get(reverse('insere_quebra_de_linha', kwargs={'plano_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Sucesso2/q/q_linha')

        # TESTE PADRÃO (GET)
        # ARGUMENTO GET: 'modelo_fiaid' e 'valor'
        self.plano.tipo_fia = True
        self.plano.save()
        data = {'modelo_fiaid':self.modelo_fia.id,'valor':1}
        response = self.c.get(reverse('insere_quebra_de_linha', kwargs={'plano_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/Sucesso3/q/q_linha')

        # TESTE PADRÃO (GET)
        # ARGUMENTO GET: 'modelo_fiaid' e 'valor'
        self.plano.tipo_fia = True
        self.plano.save()
        data = {'extra_fiaid':self.extra_fia.id,'valor':1}
        response = self.c.get(reverse('insere_quebra_de_linha', kwargs={'plano_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/Sucesso3/q/q_linha')

    def test_altera_corretor(self):
        # TESTE PADRÃO (GET)
        # ERRO, USUARIO NAO AUTORIZADO 
        # REDIRECIONA DASHBOARD
        response = self.c.get(reverse('altera_corretor', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado/msg')

        # TESTE PADRÃO (GET)
        # ACESSO NEGADO
        # ALTERABILIDADE DESATIVADA
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Desativada'
        self.plano.save()
        response = self.c.get(reverse('altera_corretor', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado_situacao/msg')

        # TESTE (POST)
        # CORRETOR = 'test'
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()
        self.classificacao.tipo_de_acesso = 'Func_sec'
        self.classificacao.save()

        # ' 1 ' é o id do usuário selecionado. É este argumento que é verificado nas choices do campo queryset
        # Este campo recebe um ID como atributo. No template é mostrado o str() do objeto
        data = {'campo':self.user.id}
        response = self.c.post(reverse('altera_corretor', kwargs={'elemento_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Alterou/msg')

        # TESTE (POST)
        # CORRETOR = ''
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.corretor_plano = self.user
        self.plano.save()
        self.classificacao.tipo_de_acesso = 'Func_sec'
        self.classificacao.save()

        # '' é a simulação de remoção de corretor de plano. É este argumento que é verificado nas choices do campo queryset
        # Este campo recebe um ID ou 'vazio' como atributo. No template é mostrado o str() do objeto
        data = {'campo':''}
        response = self.c.post(reverse('altera_corretor', kwargs={'elemento_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Alterou/msg')

    def test_concluir_sugestao(self):
        # TESTE PADRÃO (GET)
        # ERRO, SOMENTE METODO POST
        # REDIRECIONA PAGINA PLANOS_DE_AÇÃO
        response = self.c.get(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'acao'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/main')

        # TESTE POST
        # DOCUMENTO: AÇÃO
        # ERRO: NÃO É O CORRETOR
        response = self.c.post(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'acao'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Nao_corretor')

        # TESTE POST
        # DOCUMENTO: AÇÃO
        # ERRO: NAO CADASTROU ALGUMA DATA
        self.plano.corretor_plano = self.user
        self.plano.save()
        self.ordem.inserida = True
        self.ordem.prazo_execucao_inicial = None
        self.ordem.save()
        response = self.c.post(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'acao'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Datas')

        # TESTE POST
        # DOCUMENTO: DESPESA
        # ERRO: NÃO É O CORRETOR
        self.plano.corretor_plano = None
        self.plano.save()
        response = self.c.post(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'despesa'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Nao_corretor')

        # TESTE POST
        # DOCUMENTO: DESPESA
        # ERRO: NÃO É O CORRETOR
        response = self.c.post(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'fia'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Nao_corretor')

        # TESTE POST
        # DOCUMENTO: AÇÃO
        # SUCESSO
        self.plano.corretor_plano = self.user
        self.plano.save()
        self.ordem.inserida = False
        self.ordem.save()
        response = self.c.post(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'acao'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sucesso/msg')

        # TESTE POST
        # DOCUMENTO: DESPESA
        # SUCESSO
        self.plano.corretor_plano = self.user
        self.plano.save()
        response = self.c.post(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'despesa'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sucesso/msg')

        # TESTE POST
        # DOCUMENTO: FIA
        # SUCESSO
        self.plano.corretor_plano = self.user
        self.plano.save()
        response = self.c.post(reverse('chamando_concluir_sugestao', kwargs={'elemento_id':self.plano.id,'documento':'fia'}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sucesso/msg')

    def test_reseta_plano(self):
        # TESTE PADRÃO (GET)
        # USUARIO NAO AUTORIZADO
        # REDIRECIONA PAGINA AÇÃO_PLANO
        response = self.c.get(reverse('resetar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Acesso_negado')

        # TESTE (POST)
        # ERRO: NÃO É O CORRETOR
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.corretor_plano = None
        self.plano.situacao = 'Assinado'
        self.plano.save()
        response = self.c.post(reverse('resetar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/reset_corretor/msg')

        # TESTE (POST)
        # PLANO NORMAL
        # SUCESSO
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.corretor_plano = self.user
        self.plano.save()
        response = self.c.post(reverse('resetar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Sucesso')

        # TESTE (POST)
        # PLANO TIPO FIA
        # SUCESSO
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.corretor_plano = self.user
        self.plano.tipo_fia = True
        self.plano.save()
        response = self.c.post(reverse('resetar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/formulario/'+str(self.plano.id)+'/inclusao/acoes/sucesso2')

    def test_finaliza_plano(self):
        # TESTE PADRÃO (GET)
        # USUARIO NAO AUTORIZADO
        # REDIRECIONA PAGINA PLANOS_DE_ACAO_MENSAGEM
        response = self.c.get(reverse('finalizar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado/msg')

        # TESTE (POST)
        # SUCESSO
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Desativada'
        self.plano.save()
        response = self.c.post(reverse('finalizar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Finalizado/msg')

    def test_conclui_plano(self):
        # TESTE (POST)
        # SUCESSO
        self.plano.alterabilidade = 'Desativada'
        self.plano.save()
        response = self.c.post(reverse('concluir_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Concluiu/msg')

    def test_devolve_plano(self):
        # TESTE (POST)
        # USUARIO FUNC SEC
        # ALTERABILIDADE: SECRETARIA, SITUAÇÃO: PENDENTE
        # FORM: pre_assinatura = True
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Desativada'
        self.plano.situacao = 'Pendente'
        self.plano.save()

        data = {'pre_assinatura':True}
        response = self.c.post(reverse('devolver_plano', kwargs={'elemento_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Devolveu/msg')

    def test_envia_plano(self):
        # TESTE PADRÃO (GET)
        # REDIRECIONA DASHBOARD
        response = self.c.get(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard')

        # TESTE (POST)
        # PLANO TIPO FIA
        # ERRO: NÃO PREENCHEU ALGUM CAMPO OBRIGATORIO
        self.plano.tipo_fia = True
        self.modelo_fia.nome_caixa_escolar == ''
        self.plano.save()
        self.modelo_fia.save()

        response = self.c.post(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/preenchimento/msg')

        # TESTE (POST)
        # PLANO NORMAL
        # ERRO: PLANO NÃO POSSUI NENHUMA ORDEM
        self.plano.tipo_fia = False
        self.plano.save()
        self.plano2 = Plano_de_acao.objects.create(escola=self.escola, ano_referencia='nome_qualquer2')
        self.plano2.save()
        self.ordem.plano = self.plano2
        self.ordem.save()

        response = self.c.post(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sem_ordem/msg')

        # TESTE (POST)
        # PLANO NORMAL
        # ERRO: PLANO POSSUI ORDEM, MAS NENHUMA INSERIDA
        self.ordem.plano = self.plano
        self.ordem.save()
        
        response = self.c.post(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sem_ordem/msg')

        # TESTE (POST)
        # PLANO NORMAL
        # ERRO: TEM ORDEM INSERIDA, MAS NÃO TEM CODIGO
        self.ordem.inserida = True
        self.ordem.save()
        self.ordem2 = Ordens.objects.create(plano=self.plano, identificacao_numerica=2, data_de_criação=timezone.now())
        self.ordem2.save()
        self.codigo.ordem = self.ordem2
        self.codigo.save()

        response = self.c.post(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sem_codigo/msg')

        # TESTE (POST)
        # PLANO NORMAL
        # ERRO: TEM ORDEM INSERIDA, TEM CODIGO, MAS CODIGO NAO INSERIDO
        self.ordem.inserida = True
        self.ordem.save()
        self.codigo.ordem = self.ordem
        self.codigo.save()

        response = self.c.post(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sem_codigo/msg')

        # TESTE (POST)
        # PLANO NORMAL
        # ERRO: TEM CODIGO INSERIDO, MAS NÃO TEM MINIMO DE TESOUREIRO OU MEMBRO DO COLEGIADO CADASTRADOS
        self.codigo.inserido = True
        self.codigo.save()
        response = self.c.post(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Sem_funcionarios/msg')

        # TESTE (POST)
        # PLANO NORMAL
        # SUCESSO: ENVIOU
        self.escola.possui_tesoureiro = True
        self.escola.quant_membro_colegiado = 1
        self.escola.save()

        response = self.c.post(reverse('enviar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Enviou/msg')

    def test_autoriza_plano_func_sec(self):
        # TESTE PADRÃO (GET)
        # USUARIO ERRADO: Diretor_escola
        # REDIRECIONA PAGINA PLANOS DE ACAO
        response = self.c.get(reverse('autorizar_plano_sec', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado/msg')

        # TESTE (GET)
        # USUARIO CORRETO: Func_sec
        # ALTERABILIDADE: DESATIVADA
        # SUCESSO: ASSINOU
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Desativada'
        self.plano.save()
        response = self.c.get(reverse('autorizar_plano_sec', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Assinado/msg')

        # TESTE (GET)
        # USUARIO CORRETO: Func_sec
        # ALTERABILIDADE: DESATIVADA
        # MENSAGEM: JA ASSINOU ESTE PLANO (assinatura realizada pelo teste anterior)
        response = self.c.get(reverse('autorizar_plano_sec', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Ja_assinado/msg')

    def test_autoriza_plano(self):
        # TESTE PADRÃO (GET)
        # USUARIO ERRADO: Func_sec
        # REDIRECIONA PAGINA PLANOS DE ACAO
        self.group.name = 'Func_sec'
        self.group.save()
        response = self.c.get(reverse('autorizar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado/msg')
      
        # TESTE (GET)
        # USUARIO CORRETO: Diretor_escola ou Funcionario
        # PLANO COMUM
        # ALTERABILIDADE: DESATIVADA ou pre_assinatura = True
        # SUCESSO: ASSINOU
        self.group.name = 'Diretor_escola'
        self.group.save()
        self.plano.alterabilidade = 'Desativada'
        self.plano.save()
        response = self.c.get(reverse('autorizar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Assinado/msg')

        # TESTE (GET)
        # USUARIO CORRETO: Diretor_escola ou Funcionario
        # PLANO COMUM
        # ALTERABILIDADE: DESATIVADA ou pre_assinatura = True
        # MENSAGEM: JÁ POSSUI ASSINATURA
        response = self.c.get(reverse('autorizar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Ja_assinado/msg')

        # TESTE (GET)
        # USUARIO CORRETO: Diretor_escola ou Funcionario
        # PLANO TIPO FIA
        # ALTERABILIDADE: DESATIVADA ou pre_assinatura = True
        # ERRO: GRUPO PARA ASSINATURAS INCOMPLETO
        self.group.name = 'Diretor_escola'
        self.group.save()
        self.plano2.alterabilidade = 'Desativada'
        self.plano2.tipo_fia = True
        self.plano2.save()
        self.modelo_fia2 = Modelo_fia.objects.create(plano=self.plano2)
        self.modelo_fia2.save()
        response = self.c.get(reverse('autorizar_plano', kwargs={'elemento_id':self.plano2.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/grupo_incompleto/msg')

        # TESTE (GET)
        # USUARIO CORRETO: Diretor_escola ou Funcionario
        # PLANO TIPO FIA
        # ALTERABILIDADE: DESATIVADA ou pre_assinatura = True
        # SUCESSO: ASSINOU FIA
        self.modelo_fia2.membro_colegiado_1 = self.user
        self.modelo_fia2.membro_colegiado_2 = self.user
        self.modelo_fia2.tecnico_responsavel = 'qualquer nome'
        self.modelo_fia2.save()
        response = self.c.get(reverse('autorizar_plano', kwargs={'elemento_id':self.plano2.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Assinado/msg')

    def test_publica_plano(self):
        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: Escola
        response = self.c.post(reverse('publicar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Publicou/msg')

    def test_deleta_plano(self):
        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # SITUAÇÃO: Finalizado
        # ERRO: PLANOS FINALIZADOS NÃO PODEM SER APAGADOS
        self.plano.situacao = 'Finalizado'
        self.plano.save()
        response = self.c.post(reverse('deletar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Arquivado/msg')

        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # SITUAÇÃO: Qualquer
        # SUCESSO: PLANO EXCLUÍDO
        self.plano.situacao = 'Em desenvolvimento'
        self.plano.save()
        response = self.c.post(reverse('deletar_plano', kwargs={'elemento_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Deletou/msg')

    def test_editar_plano(self):
        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: Secretaria
        # ERRO: ALTERABILIDADE ERRADA
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()
        response = self.c.post(reverse('editar_plano', kwargs={'plano_id':self.plano.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado_situacao/msg')

        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: Escola
        # ERRO FORM: NOME PARA O PLANO JÁ ESTA SENDO USADO
        self.plano.alterabilidade = 'Escola'
        self.plano.save()
        data = {'ano_referencia':'nome_qualquer'}
        response = self.c.post(reverse('editar_plano', kwargs={'plano_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['contexto_extra_edita_plano'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: Escola
        # SUCESSO: NOME PLANO ALTERADO
        data = {'ano_referencia':'nome_unico'}
        response = self.c.post(reverse('editar_plano', kwargs={'plano_id':self.plano.id}), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Editou/msg')

    def test_criar_plano(self):
        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ERRO FORM: NOME PARA O PLANO JÁ ESTA SENDO USADO
        data = {'ano_referencia':'nome_qualquer'}
        response = self.c.post(reverse('criar_plano'), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['contexto_extra_plano'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # SUCESSO: PLANO CRIADO
        data = {'ano_referencia':'nome_unico'}
        response = self.c.post(reverse('criar_plano'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Criou/msg')

    def test_corrigindo_acao(self):
        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: ESCOLA
        # ERRO FORM: IDENTIFICACAO ERRADA
        self.objeto_correcao_acao = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=self.ordem.identificacao_numerica, documento_associado = '1 - Identificação das ações')
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        data = {
            'identificacao_numerica':-1, #gera um erro
            'descricao_do_problema':'b',
            'resultados_esperados':'c',
            }
        response = self.c.post(reverse('chama_corrige_ordem', kwargs=kwargs), data)
        # print(response.context['chave_form_ordem'])

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        self.assertEquals(response.context['chave_contexto_corrigindo_acao'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: ESCOLA
        # SUCESSO
        self.codigo.inserido = True
        self.codigo.save()
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        data_1 = {
            'identificacao_numerica':'1',
            'descricao_do_problema':'b',
            'resultados_esperados':'c',
            }
        data_2 = {
            'A-identificacao':'A',
            'A-especificacao':'b',
            }
        data = {**data_1, **data_2}
        response = self.c.post(reverse('chama_corrige_ordem', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/correcoes/'+str(self.plano.id)+'/Sucesso')

    def test_corrigindo_despesas(self):
        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: ESCOLA
        # ERRO FORM: IDENTIFICACAO ERRADA
        self.objeto_correcao_despesa = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=self.ordem.identificacao_numerica, codigo_associado=self.codigo.identificacao, documento_associado = '2 - Detalhamento das Despesas')
        kwargs={'plano_id':self.plano.id,'ordem_assoc':self.ordem.identificacao_numerica,'codigo_ident':self.codigo.identificacao}
        data = {
            'identificacao':'', #gera um erro
            'especificacao':'b',
            'justificativa':'c',
            'embalagem':'unidade',
            'quantidade':1, 
            'preco_unitario':1,
            'tipo_produto':'Custeio',
            }
        response = self.c.post(reverse('chama_corrige_despesa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        self.assertEquals(response.context['chave_contexto_corrigindo_despesa'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE (POST)
        # USUARIO CORRETO: Diretor_escola
        # ALTERABILIDADE: ESCOLA
        # SUCESSO: CORREÇÃO EFETUADA (CORRIGIDA)     
        self.plano.correcoes_a_fazer = 2   
        self.plano.save()
        kwargs={'plano_id':self.plano.id,'ordem_assoc':self.ordem.identificacao_numerica,'codigo_ident':self.codigo.identificacao}
        data = {
            'identificacao':'a', 
            'especificacao':'b',
            'justificativa':'c',
            'embalagem':'unidade',
            'quantidade':1, 
            'preco_unitario':1,
            'tipo_produto':'Custeio',
            }
        response = self.c.post(reverse('chama_corrige_despesa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/correcoes/'+str(self.plano.id)+'/Sucesso')   

    def test_pagina_correcoes(self):
        # TESTE PADRÃO (GET)
        # CARREGA PÁGINA PADRÃO
        kwargs={'elemento_id':self.plano.id}
        response = self.c.get(reverse('pagina_correcoes', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')

        # TESTE (GET)
        # ATUALIZA SITUAÇÃO DO PLANO PARA PUBLICADO QUANDO ACABAREM AS CORREÇÕES
        self.plano.devolvido = True
        self.plano.correcoes_a_fazer = 0
        self.plano.save()

        kwargs={'elemento_id':self.plano.id}
        response = self.c.get(reverse('pagina_correcoes', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        self.assertEquals(response.context['chave_correcoes_concluidas'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE (GET)
        # ABREFORM ACOES
        # RENDERIZA PAGINA
        self.plano.devolvido = False
        self.plano.save()

        kwargs={'elemento_id':self.plano.id,'ident_numerica':self.ordem.identificacao_numerica, 'abreForm':'sim'}
        response = self.c.get(reverse('abrindo_correcao_acao', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        self.assertEquals(response.context['chave_contexto_corrigindo_acao'], True) #variavel setada TRUE quando o form da ERRO

        # TESTE (GET)
        # ABREFORM DESPESAS
        # RENDERIZA PAGINA
        self.objeto_correcao_despesa = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=self.ordem.identificacao_numerica, codigo_associado=self.codigo.identificacao, documento_associado = '2 - Detalhamento das Despesas')
        kwargs={'elemento_id':self.plano.id, 'ident_numerica':self.ordem.identificacao_numerica, 'codigo_ident':self.codigo.identificacao, 'abreFormDespesa':'sim'}
        response = self.c.get(reverse('abrindo_correcao_despesa', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correcoes.html')
        self.assertEquals(response.context['chave_contexto_corrigindo_despesa'], True) #variavel setada TRUE quando o form da ERRO

    def test_deleta_correcao_despesa(self):
        # TESTE PADRÃO (GET)
        # ALTERABILIDADE ERRADA: Escola
        # REDIRECIONA PAGINA CORRECAO DESPESAS MENSAGEM
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.get(reverse('chamando_deleta_correcao_despesa', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Acesso_negado_situacao')

        # TESTE (POST)
        # ALTERABILIDADE CORRETA: Secretaria
        # TIPO USUARIO: FUNC_SEC
        # REDIRECIONA PAGINA CORRECAO DESPESAS MENSAGEM
        self.plano.alterabilidade = 'Secretaria'
        self.plano.correcoes_a_fazer = 1
        self.plano.save()
        self.group.name = 'Func_sec'
        self.group.save()
        self.objeto_correcao_despesa = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=self.ordem.identificacao_numerica, codigo_associado=self.codigo.identificacao, documento_associado = '2 - Detalhamento das Despesas')

        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.post(reverse('chamando_deleta_correcao_despesa', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Deletou')

    def test_cria_altera_correcao_despesa(self):
        # TESTE (POST)
        # SUCESSO: CRIOU
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()
        self.group.name = 'Func_sec'
        self.group.save()
        data = {
            'plano_nome':self.plano.ano_referencia,
            'documento_associado':'2 - Detalhamento das Despesas',
            'codigo_associado':self.codigo.id,
            'sugestao':'a',
            }
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.post(reverse('chamando_cria_altera_correcao_despesa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Criou')

        # TESTE (POST)
        # JA POSSUI SUGESTÃO, ENTÃO EDITA
        # SUCESSO: EDITOU
        self.plano.alterabilidade = 'Secretaria'
        self.plano.correcoes_a_fazer = 1
        self.plano.save()
        self.group.name = 'Func_sec'
        self.group.save()
        self.codigo.possui_sugestao_correcao = True
        self.codigo.save()
        self.objeto_correcao_despesa = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=self.ordem.identificacao_numerica, codigo_associado=self.codigo.identificacao, documento_associado = '2 - Detalhamento das Despesas')

        data = {
            'plano_nome':self.plano.ano_referencia,
            'documento_associado':'2 - Detalhamento das Despesas',
            'codigo_associado':self.codigo.id,
            'sugestao':'a',
            }
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.post(reverse('chamando_cria_altera_correcao_despesa', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Editou')

    def test_despesa_plano_correcao(self):
        # TESTE PADRÃO (GET)
        # ERRO: NAO É O CORRETOR DO PLANO
        self.user2 = User.objects.create_user(first_name='test2' ,username="test2", email="test2@test.com", password="test2")
        self.plano.corretor_plano = self.user2
        self.plano.save()
        
        kwargs={'elemento_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.get(reverse('chamando_correcao_despesa_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/despesas/Nao_corretor')

        # TESTE PADRÃO (GET)
        # RENDERIZA PÁGINA
        self.plano.corretor_plano = self.user
        self.plano.save()
        
        kwargs={'elemento_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.get(reverse('chamando_correcao_despesa_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'despesas-visualizacao.html')

    def test_despesa_plano(self):
        # TESTE PADRÃO (GET)
        # RENDERIZA PÁGINA
        kwargs={'elemento_id':self.plano.id}
        response = self.c.get(reverse('chamando_despesa_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'despesas-visualizacao.html')

        # TESTE PADRÃO (GET)
        # KWARGS: q_linha
        # MENSAGEM: SUCESSO
        # RENDERIZA PÁGINA
        kwargs={'elemento_id':self.plano.id,'q_linha':True,'mensagem':'Sucesso'}
        response = self.c.get(reverse('chamando_despesa_mensagem_q_linha', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'despesas-visualizacao.html')
        self.assertEquals(response.context['chave_q_linha'], True)

        # TESTE PADRÃO (GET)
        # MENSAGENS
        # RENDERIZA PÁGINA
        kwargs={'elemento_id':self.plano.id,'mensagem':'Sucesso2'}
        response = self.c.get(reverse('chamando_despesa_plano_mensagem', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'despesas-visualizacao.html')

    def test_acao_plano_modifica_codigo(self):
        # TESTE PADRÃO (GET)
        # CODIGO NAO ISERIDO: INSERE E ATUALIZA INFORMAÇÕES
        # REDIRECIONA: AÇÃO PLANO
        self.codigo2 = ModeloCodigos.objects.create(ordem=self.ordem, identificacao='B', quantidade=1, inserido=True)
        self.codigo3 = ModeloCodigos.objects.create(ordem=self.ordem, identificacao='C', quantidade=1, inserido=True)
        self.ordem.codigos_inseridos = 2
        self.ordem.ordem_rowspan = 2
        self.ordem.save()
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.get(reverse('chamando_acao_plano_adiciona_codigo', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes')

        # TESTE PADRÃO (GET)
        # CODIGO JÁ INSERIDO: REMOVE E ATUALIZA INFORMAÇÕES
        # REDIRECIONA: AÇÃO PLANO
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id,'codigo_id':self.codigo.id}
        response = self.c.get(reverse('chamando_acao_plano_adiciona_codigo', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes')

    def test_acao_plano_adiciona_ordem(self):
        # TESTE PADRÃO (GET)
        # RECEBE ID DE ORDEM, MODIFICA ESSA ORDEM!
        # ORDEM NÃO INSERIDA: ENTÃO INSERE
        # REDIRECIONA: AÇÃO PLANO
        kwargs={'plano_id':self.plano.id,'elemento_id':self.ordem.id}
        response = self.c.get(reverse('chamando_acao_plano_adiciona', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes')

        # TESTE PADRÃO (GET)
        # RECEBE ID DE ORDEM, MODIFICA ESSA ORDEM!
        # ORDEM JÁ INSERIDA: ENTÃO REMOVE
        # REDIRECIONA: AÇÃO PLANO
        kwargs={'plano_id':self.plano.id,'elemento_id':self.ordem.id}
        response = self.c.get(reverse('chamando_acao_plano_adiciona', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes')

        # TESTE PADRÃO (GET)
        # NÃO RECEBE ID DE ORDEM, MODIFICA TODAS!
        # plano.todas_inseridas = False, ENTAO INSERE TODAS
        # REDIRECIONA: AÇÃO PLANO
        kwargs={'plano_id':self.plano.id}
        response = self.c.get(reverse('chamando_acao_plano_modifica_todas', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes')

        # TESTE PADRÃO (GET)
        # NÃO RECEBE ID DE ORDEM, MODIFICA TODAS!
        # plano.todas_inseridas = True, ENTAO REMOVE TODAS
        # REDIRECIONA: AÇÃO PLANO
        kwargs={'plano_id':self.plano.id}
        response = self.c.get(reverse('chamando_acao_plano_modifica_todas', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes')

    def test_deleta_correcao_acao(self):
        # TESTE PADRÃO (GET)
        # USUARIO E ALTERABILIDADE ERRADAS!
        # REDIRECIONA: AÇÃO PLANO
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.get(reverse('chamando_deleta_correcao_acao', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Acesso_negado_situacao')

        # TESTE (POST)
        # USUARIO E ALTERABILIDADE CORRETAS!
        # REDIRECIONA: AÇÃO PLANO
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.correcoes_a_fazer = 1
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()
        self.objeto_correcao_despesa = Correcoes.objects.create(plano_associado=self.plano, ordem_associada=self.ordem.identificacao_numerica, documento_associado = '1 - Identificação das ações')
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.post(reverse('chamando_deleta_correcao_acao', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Deletou')

    def test_cria_altera_correcao_acao(self):
        # TESTE (POST)
        # SUCESSO: FORM JA MOSTRA PREENCHIDO PARA O USUARIO
        # ORDEM SEM SUGESTÃO: ENTÃO CRIA SUGESTÃO
        # REDIRECIONA: AÇÃO PLANO
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()
        
        data = {
            'plano_nome':self.plano.ano_referencia,
            'documento_associado':'1 - Identificação das ações',
            'ordem_associada':self.ordem.identificacao_numerica,
            'sugestao':'a',
        }
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.post(reverse('chamando_cria_altera_correcao_acao', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Criou')

        # TESTE (POST)
        # SUCESSO: FORM JA MOSTRA PREENCHIDO PARA O USUARIO
        # ORDEM JA TEM SUGESTÃO: ENTÃO ALTERA SUGESTÃO
        # REDIRECIONA: AÇÃO PLANO
        data = {
            'plano_nome':self.plano.ano_referencia,
            'documento_associado':'1 - Identificação das ações',
            'ordem_associada':self.ordem.identificacao_numerica,
            'sugestao':'a',
        }
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.post(reverse('chamando_cria_altera_correcao_acao', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Editou')

    def test_acao_plano_correcao(self):
        # TESTE PADRÃO (GET)
        # USUARIO NÃO É O CORRETOR DO PLANO
        # REDIRECIONA: AÇÃO PLANO MENSAGEM NÃO CORRETOR
        self.user2 = User.objects.create_user(first_name='test2' ,username="test2", email="test2@test.com", password="test2")
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.alterabilidade = 'Secretaria'
        self.plano.corretor_plano = self.user2
        self.plano.save()
        
        kwargs={'elemento_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.get(reverse('chamando_correcao_acao_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Nao_corretor')

        # TESTE PADRÃO (GET)
        # USUARIO CORRETO = CORRETOR
        # RENDERIZA PAGINA: ACAO VISUALIZAÇÃO
        self.plano.corretor_plano = self.user
        self.plano.save()
        
        kwargs={'elemento_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.get(reverse('chamando_correcao_acao_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acao-visualizacao.html')

    def test_acao_plano(self):
        # TESTE PADRÃO (GET)
        # 'ordem_id' nos KWARGS
        # NÃO É CORRETOR, REDIRECIONA
        kwargs={'elemento_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.get(reverse('chamando_acao_plano_datas', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/plano/'+str(self.plano.id)+'/acoes/Nao_corretor')

        # TESTE PADRÃO (GET)
        # 'ordem_id' nos KWARGS
        # É o CORRETOR, RENDERIZA E ABRE FORM
        self.plano.corretor_plano = self.user
        self.plano.save()
        kwargs={'elemento_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.get(reverse('chamando_acao_plano_datas', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acao-visualizacao.html')
        self.assertEquals(response.context['chave_contexto_abre_form_datas'], True)

        # TESTE PADRÃO (GET)
        # 'q_linha' nos KWARGS
        kwargs={'elemento_id':self.plano.id,'mensagem':'Sucesso','q_linha':'1'}
        response = self.c.get(reverse('chamando_acao_plano_mensagem_q_linha', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acao-visualizacao.html')
        self.assertEquals(response.context['chave_q_linha'], True)

        # TESTE PADRÃO (GET)
        # CONDIÇÃO - PLANO SITUACAO: ASSINADO
        # CONDIÇÃO - 'postprint' in GET
        self.plano.situacao = 'Assinado'
        self.plano.save()

        data = {'postprint':'sim'}
        kwargs={'elemento_id':self.plano.id}
        response = self.c.get(reverse('chamando_acao_plano', kwargs=kwargs), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acao-visualizacao.html')
        self.assertEquals(response.context['chave_reset_plano'], True)
        self.assertEquals(response.context['chave_apos_print'], 'sim')

        # TESTE PADRÃO (GET)
        # CONDIÇÕES PARA PLANO SER PRE-APROVADO
        self.plano.situacao = 'Publicado'
        self.plano.devolvido = True
        self.plano.correcoes_a_fazer = 0
        self.plano.pre_assinatura = True
        self.plano.save()

        kwargs={'elemento_id':self.plano.id}
        response = self.c.get(reverse('chamando_acao_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acao-visualizacao.html')
        self.assertEquals(response.context['plano_aprovado'], True)

        # TESTE PADRÃO (GET)
        # CONDIÇÕES PARA PLANO SER PRE-APROVADO
        self.plano.situacao = 'Aprovado'
        self.plano.save()

        kwargs={'elemento_id':self.plano.id}
        response = self.c.get(reverse('chamando_acao_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acao-visualizacao.html')
        self.assertEquals(response.context['plano_aprovado'], True)

    def test_abre_edicao_ordem(self):
        # TESTE PADRÃO (GET)
        # ALTERABILIDADE ERRADA
        # REDIRECIONA: PAGINA PLANOS DE ACAO
        self.plano.alterabilidade = 'Secretaria'
        self.plano.save()
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.get(reverse('abrindo_edicao_ordem', kwargs=kwargs))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/planos_de_acao/Acesso_negado_situacao2/msg')

        # TESTE PADRÃO (GET)
        # ALTERABILIDADE CORRETA
        # RENDERIZA PAGINA ORDENS
        self.plano.alterabilidade = 'Escola'
        self.plano.save()
        kwargs={'plano_id':self.plano.id,'ordem_id':self.ordem.id}
        response = self.c.get(reverse('abrindo_edicao_ordem', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plano.html')
        self.assertEquals(response.context['chave_edita_ordem_existente'], True)

    def test_plano(self):
        # TESTE PADRÃO (GET)
        # RENDERIZA PAGINA DE ORDENS
        kwargs={'plano_id':self.plano.id}
        response = self.c.get(reverse('chamando_1_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plano.html')
        self.assertEquals(response.context['chave_abre_nova_ordem'], False)

        # TESTE PADRÃO (GET)
        # RECEBE GERA_ORDEM NO KWARGS
        # RENDERIZA PAGINA DE ORDENS
        kwargs={'plano_id':self.plano.id,'gera_ordem':'sim'}
        response = self.c.get(reverse('nova_ordem', kwargs=kwargs))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plano.html')
        self.assertEquals(response.context['chave_abre_nova_ordem'], True)

        # TESTE PADRÃO (GET)
        # RENDERIZA MENSAGEM
        kwargs={'plano_id':self.plano.id,'mensagem':'Criou'}
        response = self.c.get(reverse('chamando_1_plano_mensagem', kwargs=kwargs))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plano.html')

    def test_planos_a_serem_corrigidos(self):
        # TESTE PADRÃO (GET)
        # RENDERIZA PAGINA DE PLANOS DE ACAO COM CORREÇÕES
        kwargs={'variavel':True}
        response = self.c.get(reverse('pagina_planos_a_serem_corrigidos', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_pagina_correcoes'], True)

    def test_planos_finalizados(self):
        # TESTE PADRÃO (GET)
        # RENDERIZA PAGINA DE PLANOS DE ACAO FINALIZADOS
        response = self.c.get(reverse('pagina_planos_finalizados'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_planos_finalizados'], True)

    def test_planos_de_acao(self):
        # TESTE PADRÃO (GET)
        # SEM KWARGS
        # USUARIO: Func_sec
        # VERIFICA SE ENCONTRA PLANOS NO QUERYSET (planos) para diretor secretaria
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Func_sec'
        self.group.save()
        self.plano.situacao = 'Assinado'
        self.plano.save()
        self.classificacao.usuario_diretor = True
        self.classificacao.save()
        response = self.c.get(reverse('pagina_planos_de_acao'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertTrue(response.context['dicionario_planos'])

        # TESTE PADRÃO (GET)
        # SEM KWARGS
        # USUARIO: Func_sec
        # VERIFICA SE ENCONTRA PLANOS NO QUERYSET (planos) para coordenador secretaria
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.classificacao.usuario_diretor = False
        self.classificacao.usuario_coordenador = True
        self.classificacao.save()
        response = self.c.get(reverse('pagina_planos_de_acao'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertTrue(response.context['dicionario_planos'])

        # TESTE PADRÃO (GET)
        # SEM KWARGS
        # USUARIO: Func_sec
        # VERIFICA SE ENCONTRA PLANOS NO QUERYSET (planos) para Func_sec corretores
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.classificacao.usuario_coordenador = False
        self.classificacao.save()
        self.plano.situacao = 'Pendente'
        self.plano.save()
        response = self.c.get(reverse('pagina_planos_de_acao'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertTrue(response.context['dicionario_planos'])

        # TESTE PADRÃO (GET)
        # search nos KWARGS
        # USUARIO: Func_sec
        # VERIFICA SE ENTRA NA PESQUISA
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        kwargs = {'search':'sim'}
        response = self.c.get(reverse('pagina_planos_de_acao_pesquisa', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_var_pesquisa'], True) #variavel setada true quando ha uma pesquisa

        # TESTE PADRÃO (GET)
        # SEM KWARGS
        # USUARIO: DIRETOR ESCOLA
        # VERIFICA SE ENCONTRA PLANOS NO QUERYSET (planos)
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Diretor_escola'
        self.group.save()
        response = self.c.get(reverse('pagina_planos_de_acao'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertTrue(response.context['dicionario_planos'])

        # TESTE PADRÃO (GET)
        # search nos KWARGS
        # USUARIO: Diretor_escola
        # VERIFICA SE ENTRA NA PESQUISA
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        kwargs = {'search':'sim'}
        response = self.c.get(reverse('pagina_planos_de_acao_pesquisa', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_var_pesquisa'], True) #variavel setada true quando ha uma pesquisa

        # TESTE PADRÃO (GET)
        # SEM KWARGS
        # USUARIO: Funcionario escola
        # VERIFICA SE ENCONTRA PLANOS NO QUERYSET (planos)
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Funcionario'
        self.group.save()
        response = self.c.get(reverse('pagina_planos_de_acao'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertTrue(response.context['dicionario_planos'])

        # TESTE PADRÃO (GET)
        # 'atribui' no KWARGS
        # USUARIO: Funcionario escola
        # VERIFICA SE RENDERIZA COM VARIAVEL DE CONTEXTO CORRETA
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Func_sec'
        self.group.save()

        kwargs = {'elemento_id':self.plano.id,'atribui':'sim'}
        response = self.c.get(reverse('abrindo_atribui_corretor', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_confirma_corrige'], True) #variavel setada true quando recebe 'atribui'

        # TESTE PADRÃO (GET)
        # alt_corretor' no KWARGS
        # USUARIO: Funcionario escola
        # VERIFICA SE RENDERIZA COM VARIAVEL DE CONTEXTO CORRETA
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Func_sec'
        self.group.save()

        kwargs = {'elemento_id':self.plano.id,'alt_corretor':'sim'}
        response = self.c.get(reverse('abrindo_altera_corretor', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_altera_corretor'], True) #variavel setada true quando recebe 'atribui'

        # TESTE PADRÃO (GET)
        # 'alt_corretor' no KWARGS
        # USUARIO: Funcionario escola
        # VERIFICA SE RENDERIZA COM VARIAVEL DE CONTEXTO CORRETA
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Func_sec'
        self.group.save()

        kwargs = {'elemento_id':self.plano.id,'alt_corretor':'sim'}
        response = self.c.get(reverse('abrindo_altera_corretor', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_altera_corretor'], True) #variavel setada true quando recebe 'alt_corretor'

        # TESTE PADRÃO (GET)
        # 'devolve'' no KWARGS
        # USUARIO: Funcionario escola
        # VERIFICA SE RENDERIZA COM VARIAVEL DE CONTEXTO CORRETA
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Func_sec'
        self.group.save()

        kwargs = {'elemento_id':self.plano.id,'devolve':'sim'}
        response = self.c.get(reverse('abre_modal_devolve', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertEquals(response.context['chave_confirma_devolve'], True) #variavel setada true quando recebe 'devolve'

        # TESTE PADRÃO (GET)
        # 'devolve'' no KWARGS
        # USUARIO: Diretor_escola
        # VERIFICA SE RENDERIZA COM VARIAVEL DE CONTEXTO CORRETA
        # RENDERIZA PAGINA DE PLANOS DE AÇÃO
        self.group.name = 'Diretor_escola'
        self.group.save()

        kwargs = {'elemento_id':self.plano.id,'edita_plano':'sim'}
        response = self.c.get(reverse('abrindo_edicao_plano', kwargs=kwargs))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'planos_de_acao.html')
        self.assertTrue(response.context['contexto_edicao_plano']) # Verifica a existencia dessa variavel no contexto