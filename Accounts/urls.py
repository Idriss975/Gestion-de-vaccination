"""
URL configuration for Gestion_de_vaccination project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", views.Register_API, name="Account_Register"),
    path("login/", views.Login_API, name="Account_Login"),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("", views.Account_Profile_API, name="Account_Profile"),
    #path("tickets/", views.tickets_API, name="Account_Tickets"),
    path("teapot/", views.teapot_API, name="Teapot")
]