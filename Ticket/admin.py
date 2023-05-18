from django.contrib import admin
from .models import Vaccine, Ticket

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Vaccine)