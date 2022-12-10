from distutils.command.upload import upload
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Min
from django.db.models.signals import post_save
from django.dispatch import receiver
from plano_de_acao.models import Plano_de_acao
from Escolas.models import Escola

# Create your models here.

class Usuario(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100)

class Classificacao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_de_acesso = models.CharField(max_length=50)
    matriz = models.CharField(max_length=100, blank=True)
    cargo_herdado = models.CharField(max_length=50, blank=True)
    plano_associado = models.ManyToManyField(Plano_de_acao, blank=True)
    assina_plano = models.BooleanField(default=False)
    assinatura = models.ImageField(upload_to='SetupPrincipal/img/signs', blank=True, null=True, verbose_name='Assinatura')
    is_active = models.BooleanField(default=True)
    usuario_diretor = models.BooleanField(default=False)
    usuario_coordenador = models.BooleanField(default=False)
    diretor_escolar = models.BooleanField(default=False)
    email_ativado = models.BooleanField(default=False)
    primeira_senha = models.BooleanField(default=True)
    login_original = models.BooleanField(default=True)
    marcado_para_exclusao = models.BooleanField(default=False)
    remocao_solicitante = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.first_name

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

class Turmas(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    quantidade_alunos = models.IntegerField()
    plano_associado = models.ManyToManyField(Plano_de_acao)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
