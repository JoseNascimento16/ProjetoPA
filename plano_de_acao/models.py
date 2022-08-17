from django.db import models
from datetime import date, datetime
# from usuarios.models import Usuario
from django.contrib.auth.models import User

# from fia.models import Modelo_fia


# Create your models here.

class Plano_de_acao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Criador')
    corretor_plano = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='corretor')
    ano_referencia = models.CharField(max_length=50)
    situacao = models.CharField(default='Em desenvolvimento', max_length=50)
    data_de_criação = models.DateField(default=date.today, blank=True)
    assinaturas = models.IntegerField(default=0, blank=True)
    assinaturas_sec = models.IntegerField(default=0, blank=True)
    user_autorizou = models.BooleanField(default=False) # Define se o usuário atual já assinou este plano específico
    correcoes_a_fazer = models.IntegerField(default=0, blank=True)
    pre_analise_acao = models.BooleanField(default=False)
    pre_analise_despesa = models.BooleanField(default=False)
    pre_assinatura = models.BooleanField(default=False) # Define se escola ja pode assinar depois de corrigido
    devolvido = models.BooleanField(default=False)
    alterabilidade = models.CharField(default='Escola', max_length=50)
    tipo_fia = models.BooleanField(default=False)
    pre_analise_fia = models.BooleanField(default=False)
    forca_criacao_modelo_fia = models.BooleanField(default=False)
    # modelo_fia = models.ForeignKey(Modelo_fia, on_delete=models.SET_NULL, null=True, related_name='modelo_fia')

    def __str__(self):
        return self.ano_referencia

    def save(self, *args, **kwargs):
            if self.pk:
                # If self.pk is not None then it's an update.
                cls = self.__class__
                old = cls.objects.get(pk=self.pk)
                # This will get the current model state since super().save() isn't called yet.
                new = self  # This gets the newly instantiated Mode object with the new values.
                changed_fields = []
                for field in cls._meta.get_fields():
                    field_name = field.name
                    try:
                        if getattr(old, field_name) != getattr(new, field_name):
                            changed_fields.append(field_name)
                    except Exception as ex:  # Catch field does not exist exception
                        pass
                kwargs['update_fields'] = changed_fields
            super().save(*args, **kwargs)

class Log_de_eventos(models.Model):
    plano =  models.ForeignKey(Plano_de_acao, on_delete=models.CASCADE)
    evento =  models.CharField(max_length=50)
    momento_do_ocorrido = models.DateTimeField(default=datetime.now, blank=True)

class Correcoes(models.Model):
    plano_associado =  models.ForeignKey(Plano_de_acao, on_delete=models.CASCADE)
    plano_nome = models.CharField(max_length=50, blank=True)
    documento_associado = models.CharField(max_length=50)
    ordem_associada = models.IntegerField(blank=True, null=True)
    codigo_associado = models.CharField(max_length=5, null=True)
    sugestao = models.TextField(max_length=1400)

