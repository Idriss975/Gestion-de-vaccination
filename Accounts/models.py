from django.db import models
from django.conf import settings

# Create your models here.
class Person(models.Model):
    CIN = models.CharField(max_length=9, null=True)
    Nom = models.CharField(max_length=20, null=True)
    Prenom = models.CharField(max_length=40, null=True)
    tel = models.CharField(max_length=13, null=True)
    address = models.CharField(max_length=50, null=True)
    Bday = models.DateField( null=True)
    User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Specialization = models.CharField(max_length=30,blank=True, null=True)

    def __str__(self):
        return f"{self.Nom} {self.Prenom}"

class Allergies(models.Model):
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name

class Medical_Form(models.Model):
    Heigth = models.FloatField(null=True)
    Weigth = models.FloatField(null=True)
    Blood_type = models.CharField(max_length=2, null=True)
    Patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Allergies = models.ManyToManyField(Allergies, null=True)