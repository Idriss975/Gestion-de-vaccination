from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

# Create your views here.
def Create_tickets_API(request:HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"message":"User is not authenticated."},status=401)
    if not request.method == "POST":
        return JsonResponse({"message":"Request is not using POST Method."},status=405)
    if not request.user.groups.filter(name = "Patient").exists():
        return JsonResponse({"message" : "User is not a Patient."}, status=400)

    #TODO: Check user input
    #TODO: Create ticket from post data (status Created)
    
def Participate_ticket_API(request:HttpRequest):
    pass #TODO: Nurse Participates (change status to Confirmed)