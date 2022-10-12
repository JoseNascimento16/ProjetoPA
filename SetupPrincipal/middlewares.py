from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated == False:
            while not (request.path == reverse('fazendo_login')):
                return redirect(reverse('fazendo_login'))
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