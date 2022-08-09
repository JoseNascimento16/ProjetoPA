from django.db.models.signals import post_save
from django.dispatch import receiver
from plano_de_acao.alteracoes import atualiza_assinaturas_sec
from .models import Classificacao
from plano_de_acao.models import Plano_de_acao

# Signal que retorna a situação de planos "Inteiramente assinados" para "Assinados" quando um novo Func_sec é criado.
@receiver(post_save, sender=Classificacao)
def retorna_situacao(sender, instance, created, *args, **kwargs):
    if created:
        if instance.assina_plano:
            print('SIGNAL retorna situacao')
            todos_planos = Plano_de_acao.objects.filter(situacao='Inteiramente assinado')
            for plano in todos_planos:
                plano.situacao = 'Assinado'
                print(plano.situacao)
                plano.save()
            print('CRIOU alto cargo, retorna situação dos planos')
    else:
        # O valor do update_fields não vem no frozenset, somente a KEY, que no nosso caso é o nome da variavel "assina_plano", o valor da variável não vem!
        if kwargs['update_fields']: # SE HOUVER ALTERAÇÃO EM ALGUM CAMPO
            campos = list(kwargs.get('update_fields'))
            print(campos)
            if any(item == 'assina_plano' for item in campos):
                if instance.assina_plano: 
                    print('SIGNAL retorna situacao')
                    todos_planos = Plano_de_acao.objects.filter(situacao='Inteiramente assinado')
                    for plano in todos_planos:
                        plano.situacao = 'Assinado'
                        print('retornou plano ' + str(plano) + ' para: ' + plano.situacao)
                        plano.save()
                    print('transformou em alto cargo, retorna situação dos planos')
                
                else: # SE MUDOU CARGO PARA 'PADRAO'
                    assinaturas = instance.plano_associado.all()
                    print(assinaturas)
                    if assinaturas:
                        for item in assinaturas:
                            if not item.situacao == 'Finalizado':
                                print('deletou assinatura de: ' + str(item))
                                instance.plano_associado.remove(item)

                        elemento_id = item.id
                        atualiza_assinaturas_sec(elemento_id)
                        
                    