from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import Group

from Escolas.models import Escola
from usuarios.models import Classificacao


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # REDIRECIONA PARA O INDEX
        # SE O USUÁRIO NÃO ESTIVER AUTENTICADO
        if request.user.is_authenticated == False:
            while not (request.path == reverse('fazendo_login')):
                return redirect(reverse('fazendo_login'))

    # def process_request(self, request):
        # MIDDLEWARE QUE ANALISA SE É SUPERUSER
        # ADICIONA AO GRUPO DA SECRETARIA
        # SE NÃO HOUVER GRUPO, CRIA GRUPO SECRETARIA E DEPOIS ASSOCIA
        if request.user.is_superuser:
            if not request.user.groups.exists():
                if Group.objects.filter(name='Secretaria').exists():
                    grupo = get_object_or_404(Group, name='Secretaria')
                    request.user.groups.add(grupo)
                else:
                    Group.objects.create(name='Secretaria')
                    grupo = get_object_or_404(Group, name='Secretaria')
                    request.user.groups.add(grupo)
                    print('criou grupo Secretaria')
                    # Gerra um SIGNAL que irá criar os outros grupos

    # def process_request(self, request):
        # CRIA MATRIZ (ESCOLAR) "SECRETARIA DA EDUCAÇÃO" CASO AINDA NAO EXISTA
        # CRIA CLASSIFICACAO DO USUARIO "SECRETARIA" CASO AINDA NAO EXISTA
        if request.user.is_superuser:
            if not Escola.objects.filter(nome='Secretaria da educação').exists():
                suprot = Escola.objects.create(nome='Secretaria da educação', objeto_suprot=True)
            if not Classificacao.objects.filter(user=request.user).exists():
                Classificacao.objects.create(
                    user=request.user,
                    escola=suprot,
                    tipo_de_acesso='Secretaria',
                    matriz='Secretaria da educação')
                    


            
    # pass



    # def __init__(self, get_response):
    #     self.get_response = get_response   
        
  
    # def __call__(self, request):
    #     # Code to be executed for each request before
    #     # the view (and later middleware) are called.

        

    #     response = self.get_response(request)
    #     if not request.user.is_authenticated:
    #         print(request.user.is_authenticated)

    #     # Code to be executed for each request/response after
    #     # the view is called.

    #     return response

    # def __call__(self, request):
    #     # Here I call login if not authenticated and request is not login page
    #     if request.user.is_authenticated == False and request.path != reverse('fazendo_login'):
    #         return redirect(reverse('fazendo_login'))
    #     response = self.get_response(request)
    #     return response