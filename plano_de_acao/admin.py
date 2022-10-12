from django.contrib import admin
from .models import Plano_de_acao, Correcoes


# Register your models here.

class ListandoPlanos(admin.ModelAdmin):
    
    list_display = ('ano_referencia', 'escola',  'situacao', 'assinaturas', 'id')

    def get_username(self, obj):
        return obj.escola
    
    get_username.short_description = 'Escola'  #Renames column head
    # get_username.admin_order_field  = 'username'  #Allows column order sorting
    
class ListandoCorrecoes(admin.ModelAdmin):
    
    list_display = ('get_plano', 'get_documento', 'get_ordem', 'get_codigo', 'id')

    def get_plano(self, obj):
        return obj.plano_nome

    def get_documento(self, obj):
        return obj.documento_associado

    def get_ordem(self, obj):
        return obj.ordem_associada

    def get_codigo(self, obj):
        return obj.codigo_associado
    
    get_plano.short_description = 'Plano associado:'
    get_documento.short_description = 'Pertence ao documento:'
    get_ordem.short_description = 'Ordem associada:'
    get_codigo.short_description = 'Código associado:'

admin.site.register(Plano_de_acao, ListandoPlanos)
admin.site.register(Correcoes, ListandoCorrecoes)