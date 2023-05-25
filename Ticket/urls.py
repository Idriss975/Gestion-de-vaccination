from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.Register_API, name="Account_Register"),
    path("login/", views.Login_API, name="Account_Login"),
    path("", views.Account_Profile_API, name="Account_Profile"),
    #path("tickets/", views.tickets_API, name="Account_Tickets"),
    path("teapot/", views.teapot_API, name="Teapot")
]