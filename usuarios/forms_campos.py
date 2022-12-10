from django import forms
from usuarios.forms import FuncionariosSecretariaForm

# Sobrescreve o padrao do campo 'cargo'
def campo_cargo_func_sec(request, tipo_usuario):
    if tipo_usuario == 'Secretaria':
        FuncionariosSecretariaForm.base_fields['cargo']  = forms.ChoiceField(
        choices=[('-------','-------'),('Corretor (Técnico)','Corretor (Técnico)'),('Coordenador','Coordenador'),('Diretor SUPROT','Diretor SUPROT')],
        label='Cargo:',
        widget=forms.Select(attrs={
            'class': 'fonte-italic'
        }))
    else: # diretor / coordenador
        FuncionariosSecretariaForm.base_fields['cargo']  = forms.ChoiceField(
        choices=[('-------','-------'),('Corretor (Técnico)','Corretor (Técnico)'),('Coordenador','Coordenador')],
        label='Cargo:',
        widget=forms.Select(attrs={
            'class': 'fonte-italic'
        }))

    form = FuncionariosSecretariaForm()

    return form