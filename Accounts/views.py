from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from json import loads
from re import match
from django.contrib.auth.models import User

# Create your views here.

def Register_API(request:HttpRequest):
    if request.user.is_authenticated:
        return JsonResponce({"message":"Is authenticated"},status=401)
    if not request.method == "POST":
        return HttpResponse({"message":"Request is not using POST Method."},status=405)
    
    HTTP_Data = loads(request.body)

    if not "Email" in HTTP_Data or not "Password" in HTTP_Data or len(HTTP_Data.keys()) != 2:
        return HttpResponse({"message":"Json data must contain Email and Password keys."},status=400)

    if not bool(match(r"^\S+@\S+.[a-zA-Z]+", HTTP_Data["Email"])):
        return HttpResponse({"message":"Email is not well formated."},status=400)

    if User.objects.filter(username=HTTP_Data["Email"]).exists():
        return HttpResponse({"message":"Email already exists."},status=409)

    User(username=HTTP_Data["Email"], password=HTTP_Data["Password"]).save()
    return JsonResponse({"message":"Created."},status=201)

def Login_API(request:HttpRequest):
    pass

def Account_Profile_API(request:HttpRequest):
    pass
    