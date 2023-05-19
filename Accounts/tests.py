from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from string import ascii_letters
from random import choice
from json import dumps, loads
from re import match
from datetime import datetime
from .models import Medical_Form

# Create your tests here.
class Test_Account_views(TestCase):

    def test_Register_API(self):
        Register_Path = reverse("Account_Register")
        Response = self.client.get("/")

        csrf =  str(Response.cookies).split(";")[0].split("=")[1]

        Response = self.client.post(
            Register_Path, 
            data={"Email": "Test@Test.com", "Password":"".join([choice(ascii_letters) for i in range(10)]) }, 
            headers={ "X-CSRFToken":csrf},
            content_type="application/json"
        )

        self.assertTrue(Response.status_code == 201)

        Response = self.client.post(
            Register_Path, 
            data={"Email": "Test@Test.com", "Password":"".join([choice(ascii_letters) for i in range(10)])},
            content_type="application/json"
            )
        self.assertTrue(Response.status_code == 409)

        Response = self.client.post(
            Register_Path, 
            data={"Email": "TestTest.com", "Password":"".join([choice(ascii_letters) for i in range(10)])},
            content_type="application/json"
            )

        self.assertTrue(Response.status_code == 400)

        Response = self.client.get(Register_Path)
        self.assertTrue(Response.status_code == 405)

        self.assertTrue(User.objects.filter(username="Test@Test.com").exists())
    
    def test_Login_API(self):
        Login_Path = reverse("Account_Login")
        Response = self.client.get("/")
       
        csrf =  str(Response.cookies).split(";")[0].split("=")[1]

        User_Login_Data = {
            "username" : "Login@Test.com",
            "password" : "".join([choice(ascii_letters) for i in range(10)]) 
        }
        U=User(username=User_Login_Data["username"], is_active=True)
        U.set_password(User_Login_Data["password"])
        U.save()

        Response = self.client.post(
            Login_Path,
            data = {"Email": User_Login_Data["username"], "Password": User_Login_Data["password"]+"x"},
            headers={ "X-CSRFToken":csrf},
            content_type="application/json"
        )

        self.assertTrue(Response.status_code == 401)

        self.client.logout()
        Response = self.client.post(
            Login_Path,
            data = {"Email": User_Login_Data["username"], "Password": User_Login_Data["password"]},
            headers={ "X-CSRFToken":csrf},
            content_type="application/json"
        )
        self.assertTrue(Response.status_code == 200)

    def Test_Profile_API(self):
        Profile_Path = reverse("Account_Profile")
        Response = self.client.get("/")
       
        csrf =  str(Response.cookies).split(";")[0].split("=")[1]

        Patients_Login_Data = {
            "username" : "Patients@Test.com",
            "password" : "".join([choice(ascii_letters) for i in range(10)]) 
        }
        Nurses_Login_Data = {
            "username" : "Nurses@Test.com",
            "password" : "".join([choice(ascii_letters) for i in range(10)]) 
        }
        Patients = Group.objects.get(name="Patient")
        Nurses = Group.objects.get(name="Nurse")
        P = User(username=Patients_Login_Data["username"], password=Patients_Login_Data["password"])
        N = User(username=Nurses_Login_Data["username"], password=Nurses_Login_Data["password"])
        P.save()
        N.save()
        P.groups.set(Patients)
        N.groups.set(Nurses)

        self.client.force_login(P)
        Response=self.client.get(Profile_Path, headers={ "X-CSRFToken":csrf})
        self.assertTrue(Response.status_code==200)

        self.assertTrue(bool(match(r"^[A-Z]{2}[0-9]{6}$",Response.content.json()["CIN"])))
        self.assertTrue(bool(match(r"^[A-Z][a-z]+$",Response.content.json()["Nom"])))
        self.assertTrue(bool(match(r"^[A-Z][a-z]+$",Response.content.json()["Prenom"])))
        self.assertTrue(bool(match(r"^0[5678][09]{8}$",Response.content.json()["Tel"])))
        self.assertTrue(bool(match(r"[1-9][0-9]*,\S+",Response.content.json()["Address"])))
        self.assertTrue(datetime.strptime(Response.content.json()["Birth_day"], "%d/%m/%Y") < datetime.today())
        self.assertTrue(bool(match(r"^\S@\S.\S$",Response.content.json()["Email"])))
        self.client.logout()

        self.client.force_login(N)
        Response=self.client.get(Profile_Path, headers={ "X-CSRFToken":csrf})
        self.assertTrue(Response.status_code==200)

        self.assertTrue(bool(match(r"^[A-Z]{2}[0-9]{6}$",Response.content.json()["CIN"])))
        self.assertTrue(bool(match(r"^[A-Z][a-z]+$",Response.content.json()["Nom"])))
        self.assertTrue(bool(match(r"^[A-Z][a-z]+$",Response.content.json()["Prenom"])))
        self.assertTrue(bool(match(r"^0[5678][09]{8}$",Response.content.json()["Tel"])))
        self.assertTrue(bool(match(r"[1-9][0-9]*,\S+",Response.content.json()["Address"])))
        self.assertTrue(datetime.strptime(Response.content.json()["Birth_day"], "%d/%m/%Y") < datetime.today())
        self.assertTrue(bool(match(r"^\S@\S.\S$",Response.content.json()["Email"])))

        self.assertFalse(Medical_Form.objects.filter(Patients=N).exists())
        
        self.client.logout()
        