from django.http import HttpResponse
from django.shortcuts import redirect


def usuario_nao_autenticado(funcao):
    def funcao_de_checagem(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return funcao(request, *args, *kwargs)

    return funcao_de_checagem