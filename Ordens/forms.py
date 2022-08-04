from django import forms
from Ordens.validation import *
from Ordens.models import Ordens
from tempus_dominus.widgets import DatePicker

class OrdemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.plano_id_super = kwargs.pop('plano_id_super', None)
        self.ordem_id_super = kwargs.pop('ordem_id_super', None)
        super().__init__(*args, **kwargs)

    class Meta:

        model = Ordens
        fields = ['identificacao_numerica','descricao_do_problema','resultados_esperados']
        labels = {
            'identificacao_numerica':'Número:',
            'descricao_do_problema':'Descrição do problema:',
            # 'prazo_execucao_inicial':'Prazo de execução inicial:',
            # 'prazo_execucao_final':'Prazo de execução final:',
            'resultados_esperados':'Resultados esperados::',
        }
        widgets = {
            'identificacao_numerica': forms.NumberInput(attrs={'placeholder': 'Atribua um número para esta ordem...','min':'1','max':'100','class': 'fonte-italic'}),
            'descricao_do_problema': forms.Textarea(attrs={'placeholder': 'Descreva o problema...','class': 'fonte-italic', 'rows': '5'}),
            # 'prazo_execucao_inicial': DatePicker(options={'useCurrent':True}, attrs={'placeholder': 'dd/mm/aaaa','class': 'fonte-italic'}),
            # 'prazo_execucao_final': DatePicker(options={'useCurrent':True}, attrs={'placeholder': 'dd/mm/aaaa','class': 'fonte-italic'}),
            'resultados_esperados': forms.Textarea(attrs={'placeholder': 'Resultados esperados...','class': 'fonte-italic', 'rows': '5'}),
        }

    def clean(self):

        valor_plano_id = self.plano_id_super
        valor_ordem_id = self.ordem_id_super # este valor só é gerado, se estiver vindo de uma edição de ordem
        
        valor_identificacao = self.cleaned_data.get('identificacao_numerica')
        # valor_descricao = self.cleaned_data.get('descricao_do_problema')
        # valor_prazo_inicial = self.cleaned_data.get('prazo_execucao_inicial')
        # valor_prazo_final = self.cleaned_data.get('prazo_execucao_final')
        # valor_resultados = self.cleaned_data.get('resultados_esperados')
        lista_de_erros = {}

        if valor_ordem_id: # Permite manter o mesmo número da ordem durante edição, porém não permite se for outro numero já existente
            permite_manter_mesmo_numero_de_ordem(valor_identificacao, 'identificacao_numerica', lista_de_erros, valor_plano_id, valor_ordem_id)
        else:
            numero_ja_esta_sendo_usado(valor_identificacao, 'identificacao_numerica', lista_de_erros, valor_plano_id)
        numero_menor_que_1(valor_identificacao, 'identificacao_numerica', lista_de_erros)
        numero_maior_que_100(valor_identificacao, 'identificacao_numerica', lista_de_erros)
        # data_final_antes_da_inicial(valor_prazo_inicial, valor_prazo_final, 'prazo_execucao_final', lista_de_erros)
        # data_final_igual_inicial(valor_prazo_inicial, valor_prazo_final, 'prazo_execucao_final', lista_de_erros)


        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class Edita_Ordem_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.plano_id_super = kwargs.pop('plano_id_super', None)
        self.correcao_super = kwargs.pop('correcao_super', None)
        super().__init__(*args, **kwargs)

    class Meta:

        model = Ordens
        fields = ['identificacao_numerica','descricao_do_problema','resultados_esperados']
        labels = {
            'identificacao_numerica':'Ordem Nº:',
            'descricao_do_problema':'Descrição do problema:',
            # 'prazo_execucao_inicial':'Prazo de execução inicial:',
            # 'prazo_execucao_final':'Prazo de execução final:',
            'resultados_esperados':'Resultados esperados:',
        }
        widgets = {
            'identificacao_numerica': forms.NumberInput(attrs={'placeholder': 'Atribua um número para esta ordem...','min':'1','max':'100','class': 'fonte-italic'}),
            'descricao_do_problema': forms.Textarea(attrs={'placeholder': 'Descreva o problema...','class': 'fonte-italic', 'rows': '5'}),
            # 'prazo_execucao_inicial': DatePicker(options={'useCurrent':True}, attrs={'placeholder': 'dd/mm/aaaa','class': 'fonte-italic'}),
            # 'prazo_execucao_final': DatePicker(options={'useCurrent':True}, attrs={'placeholder': 'dd/mm/aaaa','class': 'fonte-italic'}),
            'resultados_esperados': forms.Textarea(attrs={'placeholder': 'Resultados esperados...','class': 'fonte-italic', 'rows': '5'}),
        }

    def clean(self):

        valor_plano_id = self.plano_id_super
        valor_correcao = self.correcao_super # este valor só é gerado, se estiver vindo de uma correção na ordem
        
        valor_identificacao = self.cleaned_data.get('identificacao_numerica')
        # valor_descricao = self.cleaned_data.get('descricao_do_problema')
        # valor_prazo_inicial = self.cleaned_data.get('prazo_execucao_inicial')
        # valor_prazo_final = self.cleaned_data.get('prazo_execucao_final')
        # valor_resultados = self.cleaned_data.get('resultados_esperados')
        lista_de_erros = {}

        if not valor_correcao: # Se o form NAO estiver sendo usado como form de correção ou edição (ou seja, na criação de ordens), faz essa validação
            numero_ja_esta_sendo_usado(valor_identificacao, 'identificacao_numerica', lista_de_erros, valor_plano_id)
        numero_menor_que_1(valor_identificacao, 'identificacao_numerica', lista_de_erros)
        numero_maior_que_100(valor_identificacao, 'identificacao_numerica', lista_de_erros)
        # data_final_antes_da_inicial(valor_prazo_inicial, valor_prazo_final, 'prazo_execucao_final', lista_de_erros)
        # data_final_igual_inicial(valor_prazo_inicial, valor_prazo_final, 'prazo_execucao_final', lista_de_erros)


        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class Cadastra_datas_Ordem_Form(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.plano_id_super = kwargs.pop('plano_id_super', None)
    #     self.ordem_id_super = kwargs.pop('ordem_id_super', None)
    #     super().__init__(*args, **kwargs)

    class Meta:

        model = Ordens
        fields = ['prazo_execucao_inicial','prazo_execucao_final']
        # exclude = ['plano','identificacao_numerica','resultados_esperados','descricao_do_problema','data_de_criação','inserida','codigos_inseridos','ordem_rowspan','possui_sugestao_correcao']
        labels = {
            # 'identificacao_numerica':'Número:',
            # 'descricao_do_problema':'Descrição do problema:',
            'prazo_execucao_inicial':'Prazo de execução inicial:',
            'prazo_execucao_final':'Prazo de execução final:',
            # 'resultados_esperados':'Resultados esperados::',
        }
        widgets = {
            # 'identificacao_numerica': forms.NumberInput(attrs={'placeholder': 'Atribua um número para esta ordem...','min':'1','max':'100','class': 'fonte-italic'}),
            # 'descricao_do_problema': forms.Textarea(attrs={'placeholder': 'Descreva o problema...','class': 'fonte-italic', 'rows': '5'}),
            'prazo_execucao_inicial': DatePicker(options={'useCurrent':True}, attrs={'placeholder': 'dd/mm/aaaa','class': 'fonte-italic'}),
            'prazo_execucao_final': DatePicker(options={'useCurrent':True}, attrs={'placeholder': 'dd/mm/aaaa','class': 'fonte-italic'}),
            # 'resultados_esperados': forms.Textarea(attrs={'placeholder': 'Resultados esperados...','class': 'fonte-italic', 'rows': '5'}),
        }

    def clean(self):

        # valor_plano_id = self.plano_id_super
        # valor_ordem_id = self.ordem_id_super # este valor só é gerado, se estiver vindo de uma edição de ordem
        
        # valor_identificacao = self.cleaned_data.get('identificacao_numerica')
        # valor_descricao = self.cleaned_data.get('descricao_do_problema')
        valor_prazo_inicial = self.cleaned_data.get('prazo_execucao_inicial')
        valor_prazo_final = self.cleaned_data.get('prazo_execucao_final')
        # valor_resultados = self.cleaned_data.get('resultados_esperados')
        lista_de_erros = {}

        data_final_antes_da_inicial(valor_prazo_inicial, valor_prazo_final, 'prazo_execucao_final', lista_de_erros)
        data_final_igual_inicial(valor_prazo_inicial, valor_prazo_final, 'prazo_execucao_final', lista_de_erros)


        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data
