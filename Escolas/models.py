from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Escola(models.Model):
    nome = models.CharField(max_length=50, blank=True)
    diretor = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    municipio = models.CharField(max_length=50, blank=True)
    codigo_escola = models.IntegerField(default=0, blank=True)
    nte = models.IntegerField(null=True, blank=True)
    quant_funcionarios = models.IntegerField(default=0)
    possui_diretor = models.BooleanField(default=False)
    possui_tesoureiro = models.BooleanField(default=False)
    quant_membro_colegiado = models.IntegerField(default=0, blank=True)
    objeto_suprot = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome