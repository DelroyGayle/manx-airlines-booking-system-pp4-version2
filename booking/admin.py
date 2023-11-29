from django.contrib import admin

# Register your models here.
from .models import Flight, Schedule, Transaction
from .models import Booking, Passenger

admin.site.register(Flight)
admin.site.register(Schedule)
admin.site.register(Transaction)
admin.site.register(Booking)
admin.site.register(Passenger)
