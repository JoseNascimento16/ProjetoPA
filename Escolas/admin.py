from django.contrib import admin
from .models import Escola

# Register your models here.

class ListandoEscola(admin.ModelAdmin):
    list_display = ('id', 'nome', 'municipio', 'quant_funcionarios', 'diretor', 'possui_diretor')


admin.site.register(Escola, ListandoEscola)