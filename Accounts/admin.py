from django.contrib import admin
from .models import Person, Medical_Form, Allergies
from Ticket.models import Ticket
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'Persons'

class AccountInline2(admin.StackedInline):
    model = Medical_Form
    can_delete = False
    verbose_name_plural = 'Medical_Forms'

class AccountInline3(admin.StackedInline):
    model = Ticket
    can_delete = True
    verbose_name_plural = 'Tickets'


class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline, AccountInline2,AccountInline3)

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)