from django import forms
from django.forms import fields
# from django.db import Models
from codigos.validation import *
from codigos.models import ModeloCodigos


class CodigosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.ordem_id = kwargs.pop('ordem_id', None)
        self.edita_super = kwargs.pop('edita_super', None)
        self.correcao_super = kwargs.pop('correcao_super', None)
        super().__init__(*args, **kwargs)
        
    class Meta:

        model = ModeloCodigos
        # fields = '__all__'
        exclude = ['ordem','data_de_criação','inserido','preco_total_capital','preco_total_custeio','possui_sugestao_correcao','quebra_de_linha']

        labels = {
            'identificacao':'Identificação:',
            'especificacao':'Especificação da ação negociável:',
            'justificativa':'Justificativa para aquisição do item:',
            'embalagem':'Tipo de embalagem:',
            'quantidade':'Quantidade:',
            'preco_unitario':'Valor unitário (R$):',
            'tipo_produto':'Tipo de produto:',
        }
        
        widgets = {
            'identificacao': forms.TextInput(attrs={'placeholder': 'Insira uma letra (A, B, C...)','class': 'fonte-italic','maxlength': '1'}),
            'especificacao': forms.Textarea(attrs={'placeholder': 'Especifique com o máximo de detalhamento possível...','class': 'fonte-italic', 'rows': '5'}),
            'justificativa': forms.Textarea(attrs={'placeholder': 'Justificativa...','class': 'fonte-italic', 'rows': '5'}),
            'quantidade': forms.NumberInput(attrs={'placeholder': '1, 2, 3...','max':'10000','class': 'fonte-italic'}),
            # 'preco_unitario': forms.TextInput(attrs={'pattern': '[0-9]+([,\.][0-9]+)?','step':'.01'})
            # 'preco_unitario': forms.NumberInput(attrs={'placeholder': 'Ex: 100.00','class': 'fonte-italic','pattern': '^\d*(\.\d{1,2})?$'})
            'preco_unitario': forms.NumberInput(attrs={'placeholder': 'Ex: 100.00','class': 'fonte-italic'}),
            # 'preco_total_capital': forms.NumberInput(attrs={'placeholder': 'Ex: 100.00','class': 'fonte-italic'}),
            # 'preco_total_custeio': forms.NumberInput(attrs={'placeholder': 'Ex: 100.00','class': 'fonte-italic'}),
            # 'ordem': forms.TextInput(attrs={'disabled':'True'})
            # 'ordem': forms.HiddenInput()
            }

    # identificacao = forms.CharField(label='Identificação', max_length=1, widget=forms.TextInput(attrs={'placeholder': 'Insira uma letra (A, B, C...)','class': 'fonte-italic', 'style': 'text-transform:uppercase;'}))
    # especificacao = forms.CharField(label='Especificação da ação negociável', widget=forms.Textarea(attrs={'placeholder': 'Especifique com o máximo de detalhamento possível...','class': 'fonte-italic'}))
    # justificativa = forms.CharField(label='Justificativa para aquisição do item', widget=forms.Textarea(attrs={'placeholder': 'Justificativa...','class': 'fonte-italic'}))
    # TIPO = {('-------','-------'),('unidade','unidade'),('caixa','caixa')}
    # embalagem = forms.ChoiceField(label='Tipo de embalagem', choices=TIPO, initial='-------')
    # quantidade = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'placeholder': '1, 2, 3...','class': 'fonte-italic'}))
    

# VALIDAÇÕES USANDO METODO CLEAN


    def clean(self):
        
        valor_ordem_id = self.ordem_id
        valor_correcao_super = self.correcao_super
        valor_edita_super = self.edita_super
        
        valor_identificacao = self.cleaned_data.get('identificacao')
        valor_especificacao = self.cleaned_data.get('especificacao')
        valor_justificativa = self.cleaned_data.get('justificativa')
        valor_embalagem = self.cleaned_data.get('embalagem')
        valor_quantidade = self.cleaned_data.get('quantidade')
        valor_preco_unitario = self.cleaned_data.get('preco_unitario')
        valor_tipo_produto = self.cleaned_data.get('tipo_produto')
        # valor_preco_total_custeio = self.cleaned_data.get('preco_total_custeio')
        lista_de_erros = {}

        if not valor_correcao_super: # Se o form NAO estiver sendo usado como form de correção, faz essas validações
            campo_tem_algum_numero(valor_identificacao, 'identificacao', lista_de_erros)
            campo_possui_mais_de_1_caractere(valor_identificacao, 'identificacao', lista_de_erros)
            if not valor_edita_super:
                valor_ja_esta_sendo_usado(valor_identificacao, 'identificacao', lista_de_erros, valor_ordem_id)
        campos_sao_iguais(valor_especificacao, valor_justificativa, 'justificativa', lista_de_erros)
        campos_sao_iguais(valor_especificacao, valor_justificativa, 'especificacao', lista_de_erros)
        nao_escolheu_field(valor_embalagem, 'embalagem', lista_de_erros)
        nao_escolheu_field(valor_tipo_produto, 'tipo_produto', lista_de_erros)
        valor_minimo_1(valor_quantidade, 'quantidade', lista_de_erros)
        somente_valores_positivos(valor_preco_unitario, 'preco_unitario', lista_de_erros)
        # somente_valores_positivos(valor_preco_total_custeio, 'preco_total_custeio', lista_de_erros)
        

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

        # def clean_identificacao(self):
    #     identificacao = self.cleaned_data.get('identificacao')
    #     if any(char.isdigit() for char in identificacao):
    #         raise forms.ValidationError('Identificação inválida: não inclua números')
    #     else:
    #         return identificacao

class Mini_form_Codigos(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.ordem_id = kwargs.pop('ordem_id', None)
        super().__init__(*args, **kwargs)
        
    class Meta:

        model = ModeloCodigos
        fields = ['identificacao','especificacao']
        # exclude = ['ordem','justificativa','embalagem','quantidade','preco_unitario','tipo_produto','data_de_criação','inserido','preco_total_capital','preco_total_custeio','possui_sugestao_correcao']

        labels = {
            'identificacao':'Código: ',
            'especificacao':'Descrição:',
        }

        widgets = {
            'identificacao': forms.TextInput(attrs={'placeholder': 'Insira uma letra (A, B, C...)','class': 'fonte-italic'}),
            'especificacao': forms.Textarea(attrs={'placeholder': 'Especifique com o máximo de detalhamento possível...','class': 'fonte-italic', 'rows': '5'}),
            }

    def clean(self):
        
        valor_ordem_id = self.ordem_id
        
        valor_identificacao = self.cleaned_data.get('identificacao')
        valor_especificacao = self.cleaned_data.get('especificacao')
        lista_de_erros = {}

        campo_tem_algum_numero(valor_identificacao, 'identificacao', lista_de_erros)

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data
