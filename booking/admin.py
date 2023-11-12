from django.contrib import admin

# Register your models here.
from .models import Booking, Passenger

admin.site.register(Booking)
admin.site.register(Passenger)