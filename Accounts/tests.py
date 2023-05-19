from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class Test_Account_views(TestCase):

    def test_Register_API(self):
        Register_Path = reverse("Account_Register")
        Responce = self.client.get("/")

        csrf =  str(Responce.cookies).split(";")[0].split("=")[1]

        Responce = self.client.post(
            Register_Path, 
            data={"Email": "Test@Test.com", "Password":"ABCD"}, 
            headers={ "X-CSRFToken":csrf},
            content_type="application/json"
        )

        self.assertTrue(Responce.status_code == 201)

        Responce = self.client.post(
            Register_Path, 
            data={"Email": "Test@Test.com", "Password":"ABCD"},
            content_type="application/json"
            )
        self.assertTrue(Responce.status_code == 409)

        Responce = self.client.post(
            Register_Path, 
            data={"Email": "TestTest.com", "Password":"ABCD"},
            content_type="application/json"
            )

        self.assertTrue(Responce.status_code == 400)

        Responce = self.client.get(Register_Path)
        self.assertTrue(Responce.status_code == 405)