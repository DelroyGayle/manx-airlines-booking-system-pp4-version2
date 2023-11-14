from django.contrib import admin

# Register your models here.
from .models import Flight, Schedule, Transactions
from .models import Booking, Passenger

admin.site.register(Flight)
admin.site.register(Schedule)
admin.site.register(Transactions)
admin.site.register(Booking)
admin.site.register(Passenger)