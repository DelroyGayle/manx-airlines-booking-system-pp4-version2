from django.contrib import admin

# Register your models here.
from .models import Employer, Employee

admin.site.register(Employer)
admin.site.register(Employee)
