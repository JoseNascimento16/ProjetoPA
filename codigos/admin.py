from django.contrib import admin
from codigos.models import ModeloCodigos

# Register your models here.

class ListandoCodigos(admin.ModelAdmin):
    
    list_display = ('identificacao', 'get_ordem', 'get_plano', 'especificacao', 'quantidade', 'id')

    def get_ordem(self, obj):
        return obj.ordem.identificacao_numerica

    def get_plano(self, obj):
        return obj.ordem.plano.ano_referencia
    
    get_ordem.short_description = 'Pertence a ordem:'
    get_plano.short_description = 'Pertence ao plano:'

admin.site.register(ModeloCodigos, ListandoCodigos)