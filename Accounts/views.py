from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from json import loads
from re import match
from django.contrib.auth.models import User
from .models import Person
from django.contrib.auth import authenticate

# Create your views here.

def Register_API(request:HttpRequest):
    if request.user.is_authenticated:
        return JsonResponse({"message":"Is authenticated"},status=401)
    if not request.method == "POST":
        return HttpResponse({"message":"Request is not using POST Method."},status=405)
    
    HTTP_Data = loads(request.body)

    if not "Email" in HTTP_Data or not "Password" in HTTP_Data or len(HTTP_Data.keys()) != 2:
        return HttpResponse({"message":"Json data must contain Email and Password keys."},status=400)

    if not bool(match(r"^\S+@\S+.[a-zA-Z]+", HTTP_Data["Email"])):
        return HttpResponse({"message":"Email is not well formated."},status=400)

    if User.objects.filter(username=HTTP_Data["Email"]).exists():
        return HttpResponse({"message":"Email already exists."},status=409)

    U = User(username=HTTP_Data["Email"], is_active=True)
    U.set_password(HTTP_Data["Password"])
    U.save()
    Person(User = U).save()

    return JsonResponse({"message":"Created."},status=201)

def Login_API(request:HttpRequest):
    if request.user.is_authenticated:
        return JsonResponse({"message":"User already logged in"}, status=401)
    if not request.method == "POST":
        return JsonResponse({"message":"Request is not using POST Method."}, status=405)
    
    HTTP_Data = loads(request.body)

    if authenticate(username=HTTP_Data["Email"], password=HTTP_Data["Password"]) is None:
        return JsonResponse({"message":"Email or password incorrect"}, status=401)
    else:
        return JsonResponse({"message":"Done."}, status=200)

def Account_Profile_API(request:HttpRequest):  # Receive: All Data + if(patient) FormMed + Group
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=501)
    if not request.method == "GET":
        return JsonResponse({"message":"Request is not using GET Method."},status=405)

    P = Person.objects.get(User = request.user)
    print(request.user.username)
    return JsonResponse({
        "Email" : request.user.username,
        "CIN" : P.CIN,
        "Nom" : P.Nom,
        "Prenom" : P.Prenom,
        "Tel" : P.tel,
        "Address" : P.address,
        "Birth_day" : P.Bday.strftime("%d/%m/%Y") if P.Bday is not None else None,
    })

def tickets_API(request:HttpRequest):
    pass

def teapot_API(request:HttpRequest):
    pass

def Get_Medical_form_API(request:HttpRequest):
    pass

def Modify_Medical_form_API(request:HttpRequest):
    pass
    