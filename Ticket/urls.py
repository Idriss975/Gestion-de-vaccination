from django.urls import path
from . import views

urlpatterns = [
    path("create_tickets/", views.Create_tickets_API, name="Create_tickets"),
    path("cancel_tickets/", views.Cancel_tickets_API, name="Cancel_tickets"),
    path("participate_ticket/", views.Participate_ticket_API, name="Participate_ticket"),
]