from django.contrib import admin
from .models import Classificacao, Turmas, Usuario

# Register your models here.

class ListandoClassificacao(admin.ModelAdmin):
    list_display = ('id', 'user', 'tipo_de_acesso', 'cargo_herdado', 'escola')

admin.site.register(Turmas)
admin.site.register(Classificacao, ListandoClassificacao)

