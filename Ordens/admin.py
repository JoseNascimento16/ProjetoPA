from django.contrib import admin
from .models import Ordens

# Register your models here.

class ListandoOrdens(admin.ModelAdmin):
    
    list_display = ('identificacao_numerica', 'get_plano', 'id')

    def get_plano(self, obj):
        return obj.plano.ano_referencia
    
    get_plano.short_description = 'Pertence ao plano:'  #Renames column head

admin.site.register(Ordens, ListandoOrdens)
