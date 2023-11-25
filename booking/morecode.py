"""
In an effort to modularise my code
I have added other methods here
"""

from django.contrib import messages
from .models import Schedule
from .common import Common

def report_unavailability(request, direction, date_formatted, thetime):
    message_string = (
        "There is insufficent availability "
        "for the requested {0} on {1} at {2}:{3}. "
        "Please choose an alternative flight."
        ).format(direction, date_formatted, thetime[0:2], thetime[2:])
    messages.add_message(request, messages.ERROR,
                         message_string)


def check_availability(request, departing, outbound_date,
                       outbound_flightno, outbound_time,
                       returning, inbound_date,
                       inbound_flightno, inbound_time):
    """
    This routine will check whether there enough seats 
    available for the booking?
    """    
    print(outbound_date, outbound_flightno)
    print(type(outbound_date))
    queryset = Schedule.objects.filter(flight_date=outbound_date,
                                       flight_number = outbound_flightno)
    print(len(queryset))
    date_formatted = outbound_date.strftime("%d/%m/%Y")
    report_unavailability(request, departing, date_formatted, outbound_time)

    print(inbound_date, inbound_flightno)
    print(type(inbound_date))
    queryset = Schedule.objects.filter(flight_date=inbound_date,
                                       flight_number = inbound_flightno)
    print(len(queryset))
    date_formatted = inbound_date.strftime("%d/%m/%Y")
    report_unavailability(request, returning, date_formatted, inbound_time)

    return False