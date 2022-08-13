from django import forms
from django.forms import fields
from codigos.validation import *
from usuarios.models import Classificacao
from .validation import *
from .models import Extra_fia, Modelo_fia


class ModeloFiaForm(forms.ModelForm):
    
    membro1 = forms.ModelChoiceField(
        queryset=Classificacao.objects.order_by('-user').filter(tipo_de_acesso='Funcionario').filter(cargo_herdado='Membro do colegiado'),
        empty_label="------------",
        label='Colegiado escolar 1:',
        widget=forms.Select)

    membro2 = forms.ModelChoiceField(
        queryset=Classificacao.objects.order_by('-user').filter(tipo_de_acesso='Funcionario').filter(cargo_herdado='Membro do colegiado'),
        empty_label="------------",
        label='Colegiado escolar 2:',
        widget=forms.Select)

    def __init__(self, *args, **kwargs):
        self.modelo_fia_super = kwargs.pop('modelo_fia_super', None)
        super(ModeloFiaForm, self).__init__(*args, **kwargs)

        if self.modelo_fia_super:
            self.fields['membro1'].queryset = Classificacao.objects.order_by('-user').filter(matriz=self.modelo_fia_super.plano.usuario.last_name).filter(tipo_de_acesso='Funcionario').filter(cargo_herdado='Membro do colegiado')

    

    class Meta:

        model = Modelo_fia
        fields = ['nome_caixa_escolar','ano_exercicio','discriminacao', 'preco_unitario_item', 'justificativa', 'membro1', 'membro2']
        labels = {
            'nome_caixa_escolar':'Nome Caixa Escolar:',
            'ano_exercicio':'Ano de exercício:',
            'discriminacao':'Discriminação:',
            'preco_unitario_item':'Preço unitário:',
            'justificativa':'Justificativa:',
        }
        
        widgets = {
            'nome_caixa_escolar': forms.TextInput(attrs={'placeholder': 'Insira o nome do Caixa Escolar','class': 'fonte-italic'}),
            'ano_exercicio': forms.NumberInput(attrs={'placeholder': 'Ex: 2022','max':'10000','class': 'fonte-italic'}),
            'discriminacao': forms.Textarea(attrs={'placeholder': 'Especifique itens, serviços, especificações técnicas...','class': 'fonte-italic', 'rows': '5'}),
            'preco_unitario_item': forms.NumberInput(attrs={'placeholder': 'Ex: 100.00','class': 'fonte-italic'}),
            'justificativa': forms.Textarea(attrs={'placeholder': 'Justificativa...','class': 'fonte-italic', 'rows': '5'}),
            }

# VALIDAÇÕES USANDO METODO CLEAN


    def clean(self):
        
        valor_preco_unitario_item = self.cleaned_data.get('preco_unitario_item')
        valor_membro1 = self.cleaned_data.get('membro1')
        valor_membro2 = self.cleaned_data.get('membro2')
        lista_de_erros = {}

        somente_valores_positivos(valor_preco_unitario_item, 'preco_unitario_item', lista_de_erros)
        membros_iguais(valor_membro1, valor_membro2, 'membro1', lista_de_erros)
        membros_iguais(valor_membro1, valor_membro2, 'membro2', lista_de_erros)
        # nao_escolheu_campo(valor_membro1, 'membro1', lista_de_erros)
        # nao_escolheu_campo(valor_membro2, 'membro2', lista_de_erros)
        
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class OrdemExtraForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.modelo_fia_id = kwargs.pop('modelo_fia_id', None)
        self.id_ordem_extra = kwargs.pop('id_ordem_extra', None)
        self.altera_ordem = kwargs.pop('altera_ordem', None)
        super().__init__(*args, **kwargs)

    class Meta:

        model = Extra_fia
        fields = ['valor_numerico','discriminacao','quantidade', 'preco_unitario_item', 'justificativa']
        labels = {
            'valor_numerico':'Identificação numérica:',
            'discriminacao':'Discriminação:',
            'quantidade':'Quantidade:',
            'preco_unitario_item':'Preço unitário:',
            'justificativa':'Justificativa:',
        }
        
        widgets = {
            'valor_numerico': forms.NumberInput(attrs={'placeholder': 'Ex: 2, 3, 4...','max':'10000','class': 'fonte-italic','required':''}),
            'discriminacao': forms.Textarea(attrs={'placeholder': 'Especifique itens, serviços, especificações técnicas...','class': 'fonte-italic', 'rows': '5','required':''}),
            'quantidade': forms.NumberInput(attrs={'placeholder': '1, 2, 3...','min':'1','max':'1000','class': 'fonte-italic','required':''}),
            'preco_unitario_item': forms.NumberInput(attrs={'placeholder': 'Ex: 100.00','min':'0','class': 'fonte-italic','required':''}),
            'justificativa': forms.Textarea(attrs={'placeholder': 'Justificativa...','class': 'fonte-italic', 'rows': '5','required':''}),
            }

# VALIDAÇÕES USANDO METODO CLEAN

    def clean(self):
        
        valor_id_modelo_fia = self.modelo_fia_id
        var_id_ordem_extra = self.id_ordem_extra
        var_altera_ordem = self.altera_ordem

        valor_valor_numerico = self.cleaned_data.get('valor_numerico')
        valor_quantidade = self.cleaned_data.get('quantidade')
        valor_preco_unitario_item = self.cleaned_data.get('preco_unitario_item')
        lista_de_erros = {}

        valor_minimo_2_extra(valor_valor_numerico, 'valor_numerico', lista_de_erros)
        valor_minimo_1_extra(valor_quantidade, 'quantidade', lista_de_erros)
        if not var_altera_ordem:
            numero_ja_esta_sendo_usado_extra(valor_valor_numerico, 'valor_numerico', lista_de_erros, valor_id_modelo_fia)
        else:
            numero_ja_esta_sendo_usado_extra2(valor_valor_numerico, 'valor_numerico', lista_de_erros, valor_id_modelo_fia, var_id_ordem_extra)
        somente_valores_positivos_extra(valor_preco_unitario_item, 'preco_unitario_item', lista_de_erros)
        
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data