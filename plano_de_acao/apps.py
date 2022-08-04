from django.apps import AppConfig


class PlanoDeAcaoConfig(AppConfig):
    name = 'plano_de_acao'

    def ready(self):
        import plano_de_acao.signals
