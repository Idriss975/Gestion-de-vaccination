from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from json import loads
from . import models
from datetime import datetime 

# Create your views here.
def Create_tickets_API(request:HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=401)
    if not request.method == "POST":
        return JsonResponse({"message":"Request is not using POST Method."},status=405)
    if not request.user.groups.filter(name = "Patient").exists():
        return JsonResponse({"message" : "User is not a Patient."}, status=400)

    HTTP_DATA = loads(request.body)

    T = models.Ticket(Time = datetime.strptime(HTTP_DATA["Time"], "%d/%m/%Y %H:%M:%S"), 
    Location = HTTP_DATA["Location"],
    Status = "Cr",
    Patient = request.user)
    for i in HTTP_DATA["Vaccine"]:
        if models.Vaccine.objects.filter(Name=i["Name"], Virus=i["Virus"]).exists():
            T.Vaccine.add(Vaccine.objects.filter(Name=i["Name"], Virus=i["Virus"]).all()[0])
        else:
            T.Vaccine.create(Name=i["Name"], Virus=i["Virus"])
    T.save()
    return JsonResponse({"message": "Ticket Created"}, status=200)

def Cancel_tickets_API(request:HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=401)
    if not request.method == "POST":
        return JsonResponse({"message":"Request is not using POST Method."},status=405)
    if not request.user.groups.filter(name = "Patient").exists():
        return JsonResponse({"message" : "User is not a Patient."}, status=400)

    HTTP_DATA = loads(request.body)

    if not models.Ticket.objects.filter(id = HTTP_DATA["id"]).exists():
        return JsonResponse({"message":"Ticket doesn't exist"}, status=404)
    T = models.Ticket.objects.get(id = HTTP_DATA["id"])
    T.Status = "Ca"
    T.save()
    return JsonResponse({"message": "Done."}, status=200)
    
def Participate_ticket_API(request:HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=401)
    if not request.method == "POST":
        return JsonResponse({"message":"Request is not using POST Method."},status=405)
    if not request.user.groups.filter(name = "Nurse").exists():
        return JsonResponse({"message" : "User is not a Patient."}, status=400)

    HTTP_DATA = loads(request.body)
    
    if not models.Ticket.objects.filter(id = HTTP_DATA["id"]).exists():
        return JsonResponse({"message":"Ticket doesn't exist"}, status=404)
    
    T = models.Ticket.objects.get(id = HTTP_DATA["id"])
    T.Nurses.add(request.user)
    T.save()