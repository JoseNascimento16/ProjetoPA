from django import forms
from django.contrib.auth.models import User
from usuarios.validation import *
from django.core.validators import EmailValidator
from usuarios.models import Turmas
from codigos.validation import *

class EscolasForms(forms.ModelForm):

    municipio = forms.CharField(label='Município:', widget=forms.TextInput(attrs={

        'placeholder': 'Insira aqui...',
        'class': 'fonte-italic',
        'required': ''
    }))

    codigo_escola = forms.IntegerField(label='Código da escola:', widget=forms.NumberInput(attrs={

        'placeholder': 'Insira aqui...',
        'class': 'fonte-italic',
        'required': ''
    }))

    nte = forms.IntegerField(label='NTE:', widget=forms.NumberInput(attrs={

        'placeholder': 'Ex: 26, 27, 28...',
        'class': 'fonte-italic',
        'required': ''
    }))

    # password2 = forms.CharField(label='Confirme a senha:', widget=forms.PasswordInput(attrs={

    #     'placeholder': 'Repita a senha...',
    #     'class': 'fonte-italic',
    #     'autocomplete': 'new-password',
    #     'required': ''
    # }))

    class Meta:
        model = User
        fields = ['last_name', 'municipio', 'codigo_escola', 'nte']
        labels = {
            'last_name':'Nome da escola:',
            # Municipio já tem label configurado pelo Field mesmo
            # codigo_escola já tem label configurado pelo Field mesmo
            # nte já tem label configurado pelo Field mesmo
            # 'first_name':'Nome do(a) diretor(a):',
            'username':'Usuário/DIREC:',
            'password':'Senha:',
            # password2 já tem label também
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            # Municipio já tem widget,
            # codigo_escola já tem widget,
            # nte já tem widget,
            # 'first_name': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            'username': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','autocomplete': 'new-password'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Insira uma senha...','class': 'fonte-italic','autocomplete': 'new-password'}),
            # password2 já tem widget,
            }

    def clean(self):
        
        valor_last_name = self.cleaned_data.get('last_name')
        valor_municipio = self.cleaned_data.get('municipio')
        valor_codigo_escola = self.cleaned_data.get('codigo_escola')
        valor_nte = self.cleaned_data.get('nte')
        lista_de_erros = {}

        escola_ja_cadastrada(valor_last_name, 'last_name', lista_de_erros)
        escola_ja_cadastrada2(valor_codigo_escola, 'codigo_escola', lista_de_erros)

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class DiretorEscolaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.escola_super = kwargs.pop('escola_super', None)
        super().__init__(*args, **kwargs)

    # password2 = forms.CharField(label='Confirme a senha:', widget=forms.PasswordInput(attrs={

    #     'placeholder': 'Repita a senha...',
    #     'class': 'fonte-italic',
    #     'autocomplete': 'new-password',
    #     'required': ''
    # }))

    class Meta:
        model = User
        fields = ['first_name', 'email']
        labels = {
            'first_name':'Nome do(a) diretor(a):',
            'email':'E-mail:',
            # 'username':'Usuário:',
            # 'password':'Senha:',
            # password2 já tem label também
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            'email': forms.EmailInput(attrs={'placeholder': 'Informe o e-mail pessoal ou corporativo do(a) diretor(a)...','required':''}),
            # 'username': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','autocomplete': 'new-password'}),
            # 'password': forms.PasswordInput(attrs={'placeholder': 'Insira uma senha...','class': 'fonte-italic','autocomplete': 'new-password'}),
            # password2 já tem widget,
        }

    def clean(self):
        
        escola = self.escola_super
        valor_first_name = self.cleaned_data.get('first_name')
        valor_email = self.cleaned_data.get('email')
        # valor_username = self.cleaned_data.get('username')
        # valor_password1 = self.cleaned_data.get('password')
        # valor_password2 = self.cleaned_data.get('password2')
        lista_de_erros = {}

        # login_ja_existe(valor_username, 'username', lista_de_erros)
        funcionario_ja_cadastrado(valor_first_name, 'first_name', lista_de_erros)
        nome_contem_numeros(valor_first_name, 'first_name', lista_de_erros)
        sem_sobrenome(valor_first_name, 'first_name', lista_de_erros)
        email_ja_cadastrado2(valor_email, 'email', lista_de_erros)
        # senhas_nao_sao_iguais(valor_password1, valor_password2, 'password2', lista_de_erros)
        escola_ja_possui_diretor_ativo(escola, 'email', lista_de_erros)

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class FuncionariosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.escola_super = kwargs.pop('escola_super', None)
        super().__init__(*args, **kwargs)

    cargo = forms.ChoiceField(
        choices=[('-------','-------'),('Membro do colegiado','Membro do colegiado'),('Tesoureiro(a)','Tesoureiro(a)')],
        label='Cargo:',
        widget=forms.Select(attrs={
            'class': 'fonte-italic'
        }))
    # funcao = forms.CharField(max_length=20)

    class Meta:

        model = User
        fields = ['first_name', 'email', 'cargo']
        labels = {
            'first_name':'Nome do funcionário:',
            'email':'E-mail:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome completo...','class': 'fonte-italic','required':''}),
            'email': forms.EmailInput(attrs={'placeholder': 'Informe o e-mail pessoal ou corporativo do(a) funcionário(a)...','required':''}),
            #forms.DateInput(format = '%d/%m/%Y'), input_formats=('%d/%m/%Y',))
            }

    def clean(self):
        escola = self.escola_super

        valor_first_name = self.cleaned_data.get('first_name')
        valor_cargo = self.cleaned_data.get('cargo')
        valor_email = self.cleaned_data.get('email')
        lista_de_erros = {}

        funcionario_ja_cadastrado(valor_first_name, 'first_name', lista_de_erros)
        campo_none(valor_first_name, 'first_name', lista_de_erros)
        sem_sobrenome(valor_first_name, 'first_name', lista_de_erros)
        funcao_nao_foi_selecionada(valor_cargo, 'cargo', lista_de_erros)
        chega_disponibilidade_do_cargo(valor_cargo, 'cargo', escola, lista_de_erros)
        email_ja_cadastrado2(valor_email, 'email', lista_de_erros)
        

        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class FuncionariosSecretariaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.escola_super = kwargs.pop('escola_super', None)
        super().__init__(*args, **kwargs)

    cargo = forms.ChoiceField(
        choices=[('-------','-------'),('Corretor (Técnico)','Corretor (Técnico)'),('Coordenador','Coordenador'),('Diretor SUPROT','Diretor SUPROT')],
        label='Cargo:',
        widget=forms.Select(attrs={
            'class': 'fonte-italic'
        }))

    # assina = forms.BooleanField(
    #     label='Assina Planos:',
    #     widget=forms.CheckboxInput(attrs={
    #         'placeholder': 'Tem o poder de assinar planos...',
    #         'class': 'fonte-italic',
    #     }),
    #     required=False,
    #     )
        
    # funcao = forms.CharField(max_length=20)

    class Meta:

        model = User
        fields = ['first_name', 'email', 'cargo']
        labels = {
            'first_name':'Nome do funcionário:',
            'email':'E-mail:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome completo...','class': 'fonte-italic','required':''}),
            'email': forms.EmailInput(attrs={'placeholder': 'Informe o e-mail pessoal ou corporativo do(a) funcionário(a)...','required':''}),
            #forms.DateInput(format = '%d/%m/%Y'), input_formats=('%d/%m/%Y',))
            }
        # validators = [
        #     'password':'MinValueValidator'
        # ]

    def clean(self):
        escola = self.escola_super

        valor_first_name = self.cleaned_data.get('first_name')
        valor_email = self.cleaned_data.get('email')
        valor_cargo = self.cleaned_data.get('cargo')
        lista_de_erros = {}

        funcionario_ja_cadastrado(valor_first_name, 'first_name', lista_de_erros)
        campo_none(valor_first_name, 'first_name', lista_de_erros)
        sem_sobrenome(valor_first_name, 'first_name', lista_de_erros)
        funcao_nao_foi_selecionada(valor_cargo, 'cargo', lista_de_erros)
        email_ja_cadastrado2(valor_email, 'email', lista_de_erros)
        matriz_ja_possui_diretor_ativo(valor_cargo, escola, 'cargo', lista_de_erros)
        
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class AlteraCargoForm(forms.ModelForm):

    campo = forms.ChoiceField(
        choices=[('Corretor (Técnico)','Corretor (Técnico)'),('Coordenador','Coordenador')],
        label='Tipo de cargo:',
        widget=forms.Select(attrs={
            'class': 'fonte-italic'
        }))

    class Meta:

        model = User
        fields = ['campo']
        # labels = { 
        #     'campo':'Novo corretor:'
        #     }
        # widgets = {
        #     'ano_referencia': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            # 'usuario': forms.HiddenInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
        # }
        
    def __init__(self, *args, **kwargs):
        super(AlteraCargoForm, self).__init__(*args, **kwargs)
        self.fields['campo'].required = False

    def clean(self):
        return self.cleaned_data

class TurmasForm(forms.ModelForm):

    class Meta:

        model = Turmas
        fields = ['nome','quantidade_alunos']
        labels = {
            'nome':'Nome da turma:',
            'quantidade_alunos':'Quantidade de alunos:',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            'quantidade_alunos': forms.NumberInput(attrs={'placeholder': 'Insira a quantidade de alunos...','class': 'fonte-italic'}),
        }

    def clean(self):
        
        valor_nome = self.cleaned_data.get('nome')
        valor_quantidade_alunos = self.cleaned_data.get('quantidade_alunos')
        lista_de_erros = {}

        somente_valores_positivos(valor_quantidade_alunos, 'quantidade_alunos', lista_de_erros)


        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class FormAlteraNome(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name']
        labels = {
            'first_name':'Novo nome:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Insira aqui...','class': 'fonte-italic','required':''}),
            }

    def clean(self):
        
        valor_first_name = self.cleaned_data.get('first_name')
        lista_de_erros = {}

        nome_contem_numeros(valor_first_name, 'first_name', lista_de_erros)
        campo_em_branco(valor_first_name, 'first_name', lista_de_erros)
        sem_sobrenome(valor_first_name, 'first_name', lista_de_erros)
        
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class FormAlteraLogin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_super = kwargs.pop('user_super', None)
        super().__init__(*args, **kwargs)

    novo_username = forms.CharField(label='Novo Login:', widget=forms.TextInput(attrs={

        'placeholder': 'Insira um novo login...',
        'class': 'fonte-italic',
        'required': ''
    }))

    novo_username2 = forms.CharField(label='Confirme novo Login:', widget=forms.TextInput(attrs={

        'placeholder': 'Repita o Login novo...',
        'class': 'fonte-italic',
        'required': ''
    }))

    class Meta:
        model = User
        fields = ['username', 'novo_username', 'novo_username2']
        labels = {
            'username':'Login atual:',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Insira seu login atual...','class': 'fonte-italic','required':''}),
            }

    def clean(self):
        
        valor_user_super = self.user_super
        valor_username = self.cleaned_data.get('username')
        valor_novo_login = self.cleaned_data.get('novo_username')
        valor_novo_login2 = self.cleaned_data.get('novo_username2')
        lista_de_erros = {}

        seu_login_nao_e_esse(valor_user_super, valor_username, 'username', lista_de_erros)
        campo_em_branco(valor_username, 'username', lista_de_erros)
        campo_em_branco(valor_novo_login, 'novo_username', lista_de_erros)
        campo_em_branco(valor_novo_login2, 'novo_username2', lista_de_erros)
        campo_contem_espacos(valor_novo_login, 'novo_username', lista_de_erros)
        campo_contem_espacos(valor_novo_login2, 'novo_username2', lista_de_erros)
        logins_nao_sao_iguais(valor_novo_login, valor_novo_login2, 'novo_username', lista_de_erros)
        logins_nao_sao_iguais(valor_novo_login, valor_novo_login2, 'novo_username2', lista_de_erros)
        minimo_5_digitos_login(valor_novo_login, 'novo_username', lista_de_erros)
        minimo_5_digitos_login(valor_novo_login2, 'novo_username2', lista_de_erros)
        
        
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

class FormAlteraMail(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_id_super = kwargs.pop('user_id_super', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email':'Novo e-mail:',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'exemplo@exemplo.com....','required':''}),
            }

    def clean(self):
        
        user_id = self.user_id_super
        valor_email = self.cleaned_data.get('email')
        lista_de_erros = {}

        email_ja_cadastrado(valor_email, user_id, 'email', lista_de_erros)
        campo_em_branco(valor_email, 'email', lista_de_erros)
        
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data