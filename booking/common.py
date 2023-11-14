# common.py

from .models import Flight
from django.shortcuts import get_list_or_404


class Common:
    """
    I use this class as the repository of global variables
    settings needed throughout this App
    """

# Class Variables
    initialised = None
    outbound_flights = None
    inbound_flights = None

    def __init__(self):
        pass

    def initialisation():
        all_flight_entries = get_list_or_404(Flight.objects.all())
        count = 0
        # Two dictionaries for outbound and inbound
        outbound = {}
        inbound = {}
        # Nested Dictionary
        newdict = {}
        # odd flight no.  - outbound
        # even flight no. - inbound
        # however use a boolean flag
        boolean_flag = True
        for each in all_flight_entries:
            newdict[each.flight_number] = {}
            newdict[each.flight_number]["flight_from"] = each.flight_from
            newdict[each.flight_number]["flight_to"] = each.flight_to
            newdict[each.flight_number]["flight_STD"] = each.flight_STD
            newdict[each.flight_number]["flight_STA"] = each.flight_STA
            newdict[each.flight_number]["outbound"] = each.outbound
            newdict[each.flight_number]["capacity"] = each.capacity
            if boolean_flag:
                outbound[each.flight_number] = {}
                outbound[each.flight_number]["flight_from"] = each.flight_from
                outbound[each.flight_number]["flight_to"] = each.flight_to
                outbound[each.flight_number]["flight_STD"] = each.flight_STD
                outbound[each.flight_number]["flight_STA"] = each.flight_STA
                outbound[each.flight_number]["capacity"] = each.capacity
            else:
                inbound[each.flight_number] = {}
                inbound[each.flight_number]["flight_from"] = each.flight_from
                inbound[each.flight_number]["flight_to"] = each.flight_to
                inbound[each.flight_number]["flight_STD"] = each.flight_STD
                inbound[each.flight_number]["flight_STA"] = each.flight_STA
                inbound[each.flight_number]["capacity"] = each.capacity

            boolean_flag = not boolean_flag

        newdict["num_daily_flight"] = len(all_flight_entries) // 2

        # Store the results in Class variables
        Common.flight_info = newdict
        Common.outbound_flights = outbound
        Common.inbound_flights = inbound

        # Indicate that Initialisation has been done
        Common.initialised = True
