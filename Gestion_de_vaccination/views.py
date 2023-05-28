from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@ensure_csrf_cookie
def Main_Page(request:HttpRequest): # Main page if not_auth, profile if auth
    return render(request, "Gestion_de_vaccination/index.html")
@ensure_csrf_cookie
def Register_Page(request:HttpRequest):
    return render(request, "Accounts/enregistrer.html")
@ensure_csrf_cookie
def Login_Page(request:HttpRequest):
    return render(request, "Accounts/login.html")

def Profile(request:HttpRequest):
    return render(request, "Accounts/personne.html")

def Easter_Egg(request:HttpRequest):
    pass

def N404_Page(request:HttpRequest): # render(request, 404.html)
    pass