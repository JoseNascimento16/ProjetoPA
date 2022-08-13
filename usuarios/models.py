from distutils.command.upload import upload
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Min
from django.db.models.signals import post_save
from django.dispatch import receiver
from plano_de_acao.models import Plano_de_acao

# Create your models here.

class Usuario(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100)

class Classificacao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_de_acesso = models.CharField(max_length=50)
    cargo_herdado = models.CharField(max_length=50, blank=True)
    municipio = models.CharField(max_length=50, blank=True)
    matriz = models.CharField(max_length=100, blank=True)
    codigo_escola = models.IntegerField(default=0, blank=True)
    nte = models.CharField(max_length=10, blank=True)
    quant_funcionarios = models.IntegerField(default=0)
    plano_associado = models.ManyToManyField(Plano_de_acao, blank=True)
    assina_plano = models.BooleanField(default=False)
    assinatura = models.ImageField(upload_to='SetupPrincipal/img/signs', blank=True, null=True, verbose_name='Assinatura')
    is_active = models.BooleanField(default=True)
    

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    quantidade_alunos = models.IntegerField()
    plano_associado = models.ManyToManyField(Plano_de_acao)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

# class Turmas_plano(models.Model):
#     plano_associado = models.ManyToManyField(Plano_de_acao)
#     nome = models.CharField(max_length=100)
#     quantidade_alunos = models.IntegerField()
    


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     tipo = models.CharField(max_length=50, blank=True)

# @ receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()