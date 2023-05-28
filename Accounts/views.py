from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from json import loads
from re import match
from django.contrib.auth.models import User, Group
from .models import Person, Medical_Form
from django.contrib.auth import authenticate, login 


# Create your views here.

def Register_API(request:HttpRequest):
    if request.user.is_authenticated:
        return JsonResponse({"message":"Is authenticated"},status=401)
    if not request.method == "POST":
        return HttpResponse({"message":"Request is not using POST Method."},status=405)
    
    HTTP_Data = loads(request.body)

    if not "Email" in HTTP_Data or not "Password" in HTTP_Data or len(HTTP_Data.keys()) != 3:
        return JsonResponse({"message":"Json data must contain Email and Password keys."},status=400)

    if not bool(match(r"^\S+@\S+.[a-zA-Z]+", HTTP_Data["Email"])):
        return JsonResponse({"message":"Email is not well formated."},status=400)

    if User.objects.filter(username=HTTP_Data["Email"]).exists():
        return JsonResponse({"message":"Email already exists."},status=409)

    U = User(username=HTTP_Data["Email"], is_active=True)
    U.set_password(HTTP_Data["Password"])
    U.save()
    U.groups.add(Group.objects.get(name=HTTP_Data["Group"]))
    U.save()
    Person(User = U).save()

    return JsonResponse({"message":"Created."},status=201)

def Login_API(request:HttpRequest):
    if request.user.is_authenticated:
        return JsonResponse({"message":"User already logged in"}, status=401)
    if not request.method == "POST":
        return JsonResponse({"message":"Request is not using POST Method."}, status=405)
    
    HTTP_Data = loads(request.body)

    U = authenticate(username=HTTP_Data["Email"], password=HTTP_Data["Password"])
    if U  is None:
        return JsonResponse({"message":"Email or password incorrect"}, status=401)
    else:
        login(request, U)
        return JsonResponse({"message":"Done."}, status=200)

def Account_Profile_API(request:HttpRequest):  # Receive: All Data + if(patient) FormMed + Group
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=401)
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

def teapot_API(request:HttpRequest):
    return JsonResponse({
        "message":"iafb cydoeuf'grhei jrkelamdnionpgq,r sytouuv whxayvzeA BfCoDuEnFdG HtIhJeK LsMeNcOrPeQtR.S"[::2]
        }, status=418)

def Get_Medical_form_API(request:HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=401)
    if not request.method == "GET":
        return JsonResponse({"message":"Request is not using GET Method."},status=405)
    
    if request.user.groups.filter(name="Patient").exists():
        if Medical_Form.objects.filter(Patient = request.user).exists():
            M=Medical_Form.objects.filter(Patient = request.user).all()[0]
            return JsonResponse({
                "Height" : M.Heigth,
                "Weight" : M.Weight,
                "Blood_type" : M.Blood_type,
                "Allergies" : [i.Name for i in M.Allergies.all()]
            },status=200)
        else:
            return JsonResponse({"message":"You do not have a Medical_Form."}, status=404)
    elif request.user.groups.filter(name="Nurse").exists():
        if request.GET.get("Email") is None:
            return JsonResponse({"message" : "Unexpected format."}, status=400)
        if not Medical_Form.objects.filter(Patient = User.objects.filter(username = request.GET.get("Email"))).exists():
            return JsonResponse({"message":"Medical form not found."}, status=404)

        M = Medical_Form.objects.filter(Patient = User.objects.filter(username = request.GET.get("Email"))).all()[0]
        return JsonResponse({
            "Height" : M.Heigth,
            "Weight" : M.Weight,
            "Blood_type" : M.Blood_type,
            "Allergies" : [i.Name for i in M.Allergies.all()]
        }, status=200)
    else:
        return JsonResponse({"message": "User does not have Group"}, status=401)

def Modify_Medical_form_API(request:HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=401)
    if not request.method == "POST":
        return JsonResponse({"message":"Request is not using POST Method."},status=405)
    HTTP_data = loads(request.body)
    
    if request.user.groups.filter(name="Patient").exists():
        if Medical_Form.objects.filter(Patient = request.user).exists():
            if "Email" in HTTP_data:
                if HTTP_data["Email"] is not None:
                    return JsonResponse({"message": "Patients aren't allowed to enter Email"}, status=400)
            M=Medical_Form.objects.filter(Patient = request.user)
            if "Heigth" in HTTP_data:
                if HTTP_data["Heigth"] is not None:
                    M.Heigth = HTTP_data["Heigth"]
            if "Weigth" in HTTP_data:
                if HTTP_data["Weigth"] is not None:
                    M.Weigth = HTTP_data["Weigth"]
            if "Blood_type" in HTTP_data:
                if HTTP_data["Blood_type"] is not None:
                    M.Blood_type = HTTP_data["Blood_type"]
            if "Blood_type" in HTTP_data:
                if HTTP_data["Blood_type"] is not None:
                    M.Allergies.clear()
                    M.Allergies.add(*HTTP_data["Allergies"])
            return JsonResponse({"message" : "Done."}, status=200)
        else:
            return JsonResponse({"message":"You do not have a Medical_Form."}, status=404)
    elif request.user.groups.filter(name="Nurse").exists():

        if HTTP_data.get("Email", None) is None:
            return JsonResponse({"message": "Nurses should enter patient Email"}, status=400)

        if not Medical_Form.objects.filter(Patient = User.objects.filter(username = HTTP_data["Email"])).exists():
            return JsonResponse({"message":"Medical form not found in Patient."}, status=404)

        M = Medical_Form.objects.filter(Patient = User.objects.filter(username = HTTP_data["Email"])).all()[0]
        if "Heigth" in HTTP_data:
            if HTTP_data["Heigth"] is not None:
                M.Heigth = HTTP_data["Heigth"]
        if "Weigth" in HTTP_data:
            if HTTP_data["Weigth"] is not None:
                M.Weigth = HTTP_data["Weigth"]
        if "Blood_type" in HTTP_data:
            if HTTP_data["Blood_type"] is not None:
                M.Blood_type = HTTP_data["Blood_type"]
        if "Blood_type" in HTTP_data:
            if HTTP_data["Blood_type"] is not None:
                M.Allergies.clear()
                for i in HTTP_data["Allergies"]:
                    M.Allergies.create(Name=i)
        return JsonResponse({"message" : "Done."}, status=200)
    else:
        return JsonResponse({"message": "User does not have Group"}, status=401)