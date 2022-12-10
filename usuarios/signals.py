from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from plano_de_acao.alteracoes import atualiza_assinaturas_sec
from django.contrib.auth.models import User
from .models import Classificacao
from plano_de_acao.models import Plano_de_acao
from django.contrib.auth.models import Group

# Signal que retorna a situação de planos "Inteiramente assinados" para "Assinados" quando um novo Func_sec é criado.
@receiver(post_save, sender=Classificacao)
def retorna_situacao(sender, instance, created, *args, **kwargs):
    if created:
        if instance.assina_plano:
            # print('SIGNAL retorna situacao')
            todos_planos = Plano_de_acao.objects.filter(situacao='Inteiramente assinado')
            for plano in todos_planos:
                plano.situacao = 'Assinado'
                plano.save()
    else:
        # O valor do update_fields não vem no frozenset, somente a KEY, que no nosso caso é o nome da variavel "assina_plano", o valor da variável não vem!
        if kwargs['update_fields']: # SE HOUVER ALTERAÇÃO EM ALGUM CAMPO
            campos = list(kwargs.get('update_fields'))
            if any(item == 'assina_plano' for item in campos):
                if instance.assina_plano: 
                    # print('SIGNAL retorna situacao')
                    todos_planos = Plano_de_acao.objects.filter(situacao='Inteiramente assinado')
                    for plano in todos_planos:
                        plano.situacao = 'Assinado'
                        print('retornou plano ' + str(plano) + ' para: ' + plano.situacao)
                        plano.save()
                    print('transformou em alto cargo, retorna situação dos planos')
                
                else: # SE MUDOU CARGO PARA 'PADRAO'
                    assinaturas = instance.plano_associado.all()
                    if assinaturas:
                        for item in assinaturas:
                            if not item.situacao == 'Finalizado':
                                print('deletou assinatura de: ' + str(item))
                                instance.plano_associado.remove(item)

                        elemento_id = item.id
                        atualiza_assinaturas_sec(elemento_id)
                        
# Signal que detecta se houve mudança de senha                        
@receiver(pre_save, sender=User)
def user_updated(sender, **kwargs):
    user = kwargs.get('instance', None)
    if user:
        new_password = user.password
        try:
            old_password = User.objects.get(pk=user.pk).password
        except User.DoesNotExist:
            old_password = None
        if new_password != old_password:
            classific_usuario = Classificacao.objects.filter(user=user)
            if classific_usuario:
                user.classificacao.primeira_senha = False
                user.classificacao.save()
                # do what you need here
                    
# Signal que detecta a criação de um grupo (Secretaria) e cria o restante                    
@receiver(post_save, sender=Group)
def group_criado(sender, instance, created, *args, **kwargs):
    if instance.name == 'Secretaria':
        if not Group.objects.filter(name='Escola').exists():
            Group.objects.create(name='Escola')
            # print('criou grupo Escola')
        if not Group.objects.filter(name='Diretor_escola').exists():
            Group.objects.create(name='Diretor_escola')
            # print('criou grupo diretor escola')
        if not Group.objects.filter(name='Funcionario').exists():
            Group.objects.create(name='Funcionario')
            # print('criou grupo Funcionario')
        if not Group.objects.filter(name='Func_sec').exists():
            Group.objects.create(name='Func_sec')
            # print('criou grupo Func_sec')
