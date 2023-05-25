from django.db import models
from django.conf import settings

# Create your models here.
class Vaccine(models.Model):
    Name = models.CharField(max_length=20)
    Virus = models.CharField(max_length=20)

    def __str__(self):
        return self.Name

class Ticket(models.Model):
    Time = models.DateTimeField()
    Location = models.CharField(max_length=50)
    Status = models.CharField(max_length=2,choices=(("Cr","Created"), ("Co","Confirmed"), ("Ca","Cancelled")))
    Vaccine = models.ForeignKey(Vaccine, on_delete=models.SET_NULL, null=True)
    Patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="Patients",limit_choices_to={"groups_name":"Patient"})
    Nurses = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="Nurses",limit_choices_to={"groups_name":"Nurse"})

    def __str__(self):
        return f"{self.Location} at {self.Time}"