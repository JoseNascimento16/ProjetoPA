from ast import arg
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from plano_de_acao.views import *

class Testurls(SimpleTestCase):
    
    def test_pagina_planos_de_acao_resolve(self):
        url = reverse('pagina_planos_de_acao')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_de_acao)

    def test_pagina_planos_de_acao_mensagem_resolve(self):
        url = reverse('pagina_planos_de_acao_mensagem', args=['slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_de_acao)

    def test_abrindo_edicao_plano_resolve(self):
        url = reverse('abrindo_edicao_plano', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_de_acao)
    
    def test_pagina_planos_concluidos_resolve(self):
        url = reverse('pagina_planos_finalizados')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_finalizados)

    def test_pagina_planos_a_serem_corrigidos_resolve(self):
        url = reverse('pagina_planos_a_serem_corrigidos', args=['slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_a_serem_corrigidos)

    def test_pagina_correcoes_resolve(self):
        url = reverse('pagina_correcoes', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, pagina_correcoes)
    
    def test_pagina_correcoes_mensagem_resolve(self):
        url = reverse('pagina_correcoes_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, pagina_correcoes)

    def test_abrindo_correcao_acao_resolve(self):
        url = reverse('abrindo_correcao_acao', args=[1,1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, pagina_correcoes)

    def test_abrindo_correcao_despesa_resolve(self):
        url = reverse('abrindo_correcao_despesa', args=[1,1,'slug','slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, pagina_correcoes)

    def test_chama_corrige_ordem_resolve(self):
        url = reverse('chama_corrige_ordem', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, corrigindo_acao)

    def test_chama_corrige_despesa_resolve(self):
        url = reverse('chama_corrige_despesa', args=[1,1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, corrigindo_despesas)

    def test_criar_plano_resolve(self):
        url = reverse('criar_plano')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cria_plano)

    def test_editar_plano_resolve(self):
        url = reverse('editar_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, edita_plano)

    def test_deletar_plano_resolve(self):
        url = reverse('deletar_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, deleta_plano)

    def test_publicar_plano_resolve(self):
        url = reverse('publicar_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, publica_plano)

    def test_autorizar_plano_resolve(self):
        url = reverse('autorizar_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, autoriza_plano)

    def test_enviar_plano_resolve(self):
        url = reverse('enviar_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, envia_plano)

    def test_devolver_plano_resolve(self):
        url = reverse('devolver_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, devolve_plano)

    def test_aprovar_plano_resolve(self):
        url = reverse('aprovar_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, aprova_plano)

    def test_concluir_plano_resolve(self):
        url = reverse('concluir_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, conclui_plano)

    def test_chamando_1_plano_resolve(self):
        url = reverse('chamando_1_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, plano)

    def test_chamando_1_plano_mensagem_resolve(self):
        url = reverse('chamando_1_plano_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, plano)

    def test_chamando_concluir_sugestao_resolve(self):
        url = reverse('chamando_concluir_sugestao', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, concluir_sugestao)

    def test_nova_ordem_resolve(self):
        url = reverse('nova_ordem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, plano)

    def test_abrindo_edicao_ordem_resolve(self):
        url = reverse('abrindo_edicao_ordem', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, abre_edicao_ordem)

    def test_chamando_acao_plano_resolve(self):
        url = reverse('chamando_acao_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, acao_plano)

    def test_chamando_acao_plano_mensagem_resolve(self):
        url = reverse('chamando_acao_plano_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, acao_plano)

    def test_chamando_acao_plano_modifica_todas_resolve(self):
        url = reverse('chamando_acao_plano_modifica_todas', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, acao_plano_adiciona_ordem)

    def test_chamando_acao_plano_adiciona_resolve(self):
        url = reverse('chamando_acao_plano_adiciona', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, acao_plano_adiciona_ordem)

    def test_chamando_acao_plano_adiciona_codigo_resolve(self):
        url = reverse('chamando_acao_plano_adiciona_codigo', args=[1,1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, acao_plano_modifica_codigo)

    def test_chamando_correcao_acao_plano_resolve(self):
        url = reverse('chamando_correcao_acao_plano', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, acao_plano_correcao)

    def test_chamando_cria_altera_correcao_acao_resolve(self):
        url = reverse('chamando_cria_altera_correcao_acao', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cria_altera_correcao_acao)

    def test_chamando_deleta_correcao_acao_resolve(self):
        url = reverse('chamando_deleta_correcao_acao', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, deleta_correcao_acao)

    def test_chamando_despesa_plano_resolve(self):
        url = reverse('chamando_despesa_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, despesa_plano)

    def test_chamando_despesa_plano_mensagem_resolve(self):
        url = reverse('chamando_despesa_plano_mensagem', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, despesa_plano)

    def test_chamando_correcao_despesa_plano_resolve(self):
        url = reverse('chamando_correcao_despesa_plano', args=[1,1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, despesa_plano_correcao)

    def test_chamando_cria_altera_correcao_despesa_resolve(self):
        url = reverse('chamando_cria_altera_correcao_despesa', args=[1,1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, cria_altera_correcao_despesa)

    def test_chamando_deleta_correcao_despesa_resolve(self):
        url = reverse('chamando_deleta_correcao_despesa', args=[1,1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, deleta_correcao_despesa)

    def test_adicionando_removendo_turma_resolve(self):
        url = reverse('adicionando_removendo_turma', args=[1,1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, adiciona_remove_turma)

    def test_gera_pdf_acao_resolve(self):
        url = reverse('gera_pdf_acao', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, gera_pdf)

    def test_autoriza_plano_sec_resolve(self):
        url = reverse('autorizar_plano_sec', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, autoriza_plano_func_sec)

    def test_finaliza_plano_resolve(self):
        url = reverse('finalizar_plano', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, finaliza_plano)

    def test_atribui_corretor_resolve(self):
        url = reverse('chamando_atribui_corretor', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, atribui_corretor)

    def test_abrindo_atribui_corretor_resolve(self):
        url = reverse('abrindo_atribui_corretor', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_de_acao)
    
    def test_abrindo_altera_corretor_resolve(self):
        url = reverse('abrindo_altera_corretor', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_de_acao)

    def test_altera_corretor_resolve(self):
        url = reverse('altera_corretor', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, altera_corretor)

    def test_pesquisa_plano_resolve(self):
        url = reverse('pesquisar_plano')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, pesquisa_plano)

    def test_pagina_plano_pesquisa_resolve(self):
        url = reverse('pagina_planos_de_acao_pesquisa', args=['slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_de_acao)

    def test_abre_modal_devolve_resolve(self):
        url = reverse('abre_modal_devolve', args=[1,'slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, planos_de_acao)

    def test_insere_quebra_linha_resolve(self):
        url = reverse('insere_quebra_de_linha', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, quebra_de_linha)

    def test_q_linha_resolve(self):
        url = reverse('chamando_acao_plano_mensagem_q_linha', args=[1,'slug','slug'])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, acao_plano)