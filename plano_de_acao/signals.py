from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import date
from fia.models import Modelo_fia
from .models import Plano_de_acao
from django.contrib.auth.models import User

@receiver(post_save, sender=Plano_de_acao)
def atualiza_alterabilidade(sender, instance, created, *args, **kwargs):
    if kwargs['update_fields']: # SE HOUVER ALTERAÇÃO EM ALGUM CAMPO
        campos = list(kwargs.get('update_fields'))
        if any(item == 'situacao' for item in campos):
            # print('Alterou situação, gerou signals!')
            if instance.situacao == 'Pendente' or instance.situacao == 'Corrigido pela escola':
                instance.alterabilidade = 'Secretaria'
                instance.save()
            elif instance.situacao == 'Em desenvolvimento' or instance.situacao == 'Publicado' or instance.situacao == 'Necessita correção':
                instance.alterabilidade = 'Escola'
                instance.save()
            elif instance.situacao == 'Aprovado' or instance.situacao == 'Pronto' or instance.situacao == 'Assinado' or instance.situacao == 'Inteiramente assinado' or instance.situacao == 'Finalizado':
                instance.alterabilidade = 'Desativada'
                instance.save()

# Cria um modelo_fia para um plano, caso não exista por qualquer motivo que seja
@receiver(post_save, sender=Plano_de_acao)
def cria_modelo_fia(sender, instance, created, *args, **kwargs):
    if created and instance.tipo_fia or instance.forca_criacao_modelo_fia == True:
        modelo_fia = Modelo_fia.objects.create(
            plano = instance,
            valor_total_anterior = 0.00,
            preco_unitario_item = 0.00,
            valor_total_item = 0.00,
            valor_total_fia = 0.00,
        )
        modelo_fia.save()
        # print('Plano não possuia modelo_fia, gerou modelo_fia por SIGNAL')

        instance.forca_criacao_modelo_fia = False
        instance.save()

@receiver(pre_save, sender=Plano_de_acao)
def define_ultima_modificacao(sender, instance, **kwargs):
    
    if not getattr(instance, '_disable_signals', False):
        instance.ultima_modificacao = date.today()
        instance.save_without_signals()

