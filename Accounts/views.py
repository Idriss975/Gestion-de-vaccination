from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from json import loads
from re import match
from django.contrib.auth.models import User
#from django.contrib.auth import 

# Create your views here.
def Register_API(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect("")
    if not request.method == "POST":
        return HttpResponse({"message":"Request is not using POST Method."},status_code=405)
    
    HTTP_Data = loads(request.body)

    if not "Email" in HTTP_Data and not "Password" in HTTP_Data or len(HTTP_Data.keys()) != 2:
        return JsonResponse({"message":"Json data must contain Email and Password keys."},status_code=400)

    if bool(match(r"^\S@\S.[a-zA-Z]+", HTTP_Data["Email"])):
        return JsonResponse({"message":"Email is not well formated."},status_code=400)

    if User.objects.get(username=HTTP_Data["Email"]) is None:
        return JsonResponse({"message":"Email already exists."},status_code=409)

    User(username=HTTP_Data["Email"], password=HTTP_Data["Password"]).save()
    returnJsonResponse({"message":"Done."},status_code=201)

    