from django.contrib import admin
from .models import Classificacao, Usuario

# Register your models here.

class ListandoClassificacao(admin.ModelAdmin):
    list_display = ('id', 'user', 'tipo_de_acesso', 'matriz', 'quant_funcionarios')

admin.site.register(Usuario)
admin.site.register(Classificacao, ListandoClassificacao)

