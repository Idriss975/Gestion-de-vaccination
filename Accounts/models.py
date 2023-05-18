from django.db import models
from django.conf import settings

# Create your models here.
class Person(models.Model):
    CIN = models.CharField(max_length=9)
    Nom = models.CharField(max_length=20)
    Prenom = models.CharField(max_length=40)
    tel = models.CharField(max_length=13)
    address = models.CharField(max_length=50)
    Bday = models.DateField()
    User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Specialization = models.CharField(max_length=30,blank=True)

    def __str__(self):
        return f"{self.Nom} {self.Prenom}"

class Allergies(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name

class Medical_Form(models.Model):
    Heigth = models.FloatField()
    Weigth = models.FloatField()
    Blood_type = models.CharField(max_length=2)
    Patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Allergies = models.ManyToManyField(Allergies)