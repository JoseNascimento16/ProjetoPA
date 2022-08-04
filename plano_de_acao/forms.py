from django import forms
from plano_de_acao.validation import *
from plano_de_acao.models import Plano_de_acao, Correcoes
from tempus_dominus.widgets import DatePicker

from usuarios.models import Classificacao

class PlanoForm(forms.ModelForm):

    class Meta:

        model = Plano_de_acao
        fields = ['ano_referencia']
        labels = {
            'ano_referencia':'Nome do plano:',
        }
        widgets = {
            'ano_referencia': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            # 'usuario': forms.HiddenInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
        }

    def clean(self):
        
        valor_ano = self.cleaned_data.get('ano_referencia')
        lista_de_erros = {}

        plano_ja_existe(valor_ano, 'ano_referencia', lista_de_erros)
        inicia_com_FIA(valor_ano, 'ano_referencia', lista_de_erros)


        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class FiaForm(forms.ModelForm):

    class Meta:

        model = Plano_de_acao
        fields = ['ano_referencia']
        labels = {
            'ano_referencia':'Nome do FIA:',
        }
        widgets = {
            'ano_referencia': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            # 'usuario': forms.HiddenInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
        }

    def clean(self):
        
        valor_ano = self.cleaned_data.get('ano_referencia')
        lista_de_erros = {}

        plano_ja_existe(valor_ano, 'ano_referencia', lista_de_erros)


        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class Edita_planoForm(forms.ModelForm):

    class Meta:

        model = Plano_de_acao
        fields = ['ano_referencia']
        labels = {
            'ano_referencia':'Ano de referência:',
        }
        widgets = {
            'ano_referencia': forms.TextInput(attrs={'placeholder': 'Insira aqui o novo nome...','class': 'fonte-italic','required':''}),
            # 'usuario': forms.HiddenInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
        }

    def clean(self):
        
        valor_ano = self.cleaned_data.get('ano_referencia')
        lista_de_erros = {}

        plano_ja_existe2(valor_ano, 'ano_referencia', lista_de_erros)


        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class Correcao_acaoForm(forms.ModelForm):

    class Meta:

        model = Correcoes
        exclude = ['plano_associado','codigo_associado',]
        labels = {
            'plano_nome':'Plano:',
            'documento_associado':'Documento:',
            'ordem_associada':'Ordem N°:',
            'sugestao':'Qual ou quais a(s) sugestão(ões) de correção?:',
        }
        widgets = {
            'plano_nome': forms.TextInput(attrs={'placeholder': 'Nome do Plano...','class': 'fonte-italic','required':''}),
            'documento_associado': forms.TextInput(attrs={'placeholder': 'Documento a receber a sugestão...','class': 'fonte-italic','required':''}),
            'ordem_associada': forms.NumberInput(attrs={'placeholder': 'Informe o número da ordem...','min':'1','max':'100','class': 'fonte-italic'}),
            'sugestao': forms.Textarea(attrs={'placeholder': 'Descreva aqui as suas sugestões para este bloco, separe-as por tópicos se preferir...\n\n1 - Tópico 1...\n\n2 - Tópico 2...','class': 'fonte-italic', 'rows': '10'}),
        }

    def clean(self):
        
        # Neste caso, o unico campo que o usuario altera é o de "sugestao".
        # O unico problema seria, o usuário deixar este campo em branco.
        # O proprio clean já faz essa verificação, não precisamos configurar.
        
        lista_de_erros = {}

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class Correcao_despesaForm(forms.ModelForm):

    class Meta:

        model = Correcoes
        exclude = ['plano_associado','ordem_associada']
        labels = {
            'plano_nome':'Plano:',
            'documento_associado':'Documento:',
            'codigo_associado':'Código:',
            'sugestao':'Qual ou quais a(s) sugestão(ões) de correção?:',
        }
        widgets = {
            'plano_nome': forms.TextInput(attrs={'placeholder': 'Nome do Plano...','class': 'fonte-italic','required':''}),
            'documento_associado': forms.TextInput(attrs={'placeholder': 'Documento a receber a sugestão...','class': 'fonte-italic','required':''}),
            'codigo_associado': forms.TextInput(attrs={'placeholder': 'Informe o código...','class': 'fonte-italic','required':''}),
            'sugestao': forms.Textarea(attrs={'placeholder': 'Descreva aqui as suas sugestões para este bloco, separe-as por tópicos se preferir...','class': 'fonte-italic', 'rows': '10'}),
        }

    def clean(self):
        
        # Neste caso, o unico campo que o usuario altera é o de "sugestao".
        # O unico problema seria, o usuário deixar este campo em branco.
        # O proprio clean já faz essa verificação, não precisamos configurar.
        
        lista_de_erros = {}

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class Correcao_FiaForm(forms.ModelForm):

    class Meta:

        model = Correcoes
        fields = ['plano_nome','documento_associado','ordem_associada','sugestao']
        labels = {
            'plano_nome':'Plano:',
            'documento_associado':'Documento:',
            'ordem_associada':'Número da ordem:',
            'sugestao':'Qual ou quais a(s) sugestão(ões) de correção?',
        }
        widgets = {
            'plano_nome': forms.TextInput(attrs={'placeholder': 'Nome do Plano...','class': 'fonte-italic','required':''}),
            'documento_associado': forms.TextInput(attrs={'placeholder': 'Documento a receber a sugestão...','class': 'fonte-italic','required':''}),
            'ordem_associada': forms.TextInput(attrs={'placeholder': 'Informe a ordem...','class': 'fonte-italic','required':''}),
            'sugestao': forms.Textarea(attrs={'placeholder': 'Descreva aqui as suas sugestões para este bloco, separe-as por tópicos se preferir...','class': 'fonte-italic', 'rows': '10'}),
        }

    def clean(self):
        
        # Neste caso, o unico campo que o usuario altera é o de "sugestao".
        # O unico problema seria, o usuário deixar este campo em branco.
        # O proprio clean já faz essa verificação, não precisamos configurar.
        
        lista_de_erros = {}

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class PreAssinaturaForm(forms.ModelForm):

    pre_assinatura = forms.BooleanField(
        label='Permitir pré assinatura:',
        widget=forms.CheckboxInput(attrs={
            'class': 'fonte-italic',
        }),
        required=False,
        )

    class Meta:

        model = Plano_de_acao
        fields = ['pre_assinatura']
        # labels = {
        #     'ano_referencia':'Ano de referência:',
        # }
        # widgets = {
        #     'ano_referencia': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            # 'usuario': forms.HiddenInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
        # }
    def clean(self):
        return self.cleaned_data
    
class AlteraCorretorForm(forms.ModelForm):

    campo = forms.ModelChoiceField(
        queryset=Classificacao.objects.order_by('-user').filter(tipo_de_acesso='Func_sec'),
        empty_label="------------",
        label='Novo corretor:',
        widget=forms.Select)

    class Meta:

        model = Classificacao
        fields = ['campo']
        # labels = { 
        #     'campo':'Novo corretor:'
        #     }
        # widgets = {
        #     'ano_referencia': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            # 'usuario': forms.HiddenInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
        # }
        
    def __init__(self, *args, **kwargs):
        super(AlteraCorretorForm, self).__init__(*args, **kwargs)
        self.fields['campo'].required = False

    # def __str__(self):
    #     return self.first_name

    def clean(self):
        return self.cleaned_data