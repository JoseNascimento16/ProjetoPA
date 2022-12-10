from django.contrib import admin
from .models import Escola

# Register your models here.

class ListandoEscola(admin.ModelAdmin):
    list_display = ('id', 'nome', 'municipio', 'quant_funcionarios', 'get_diretor', 'possui_diretor')

    def get_diretor(self, obj):
        return obj.diretor
    
    get_diretor.short_description = 'Diretor:'

admin.site.register(Escola, ListandoEscola)