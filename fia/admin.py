from django.contrib import admin

from fia.models import Extra_fia, Modelo_fia

# Register your models here.

class ListandoFias(admin.ModelAdmin):
    
    list_display = ('plano', 'ano_exercicio',  'preco_unitario_item', 'valor_total_item', 'valor_total_fia', 'id')

class ListandoExtras(admin.ModelAdmin):
    
    list_display = ('valor_numerico', 'quantidade',  'preco_unitario_item',  'valor_total_item',  'fia_matriz', 'id')


admin.site.register(Modelo_fia, ListandoFias)
admin.site.register(Extra_fia, ListandoExtras)