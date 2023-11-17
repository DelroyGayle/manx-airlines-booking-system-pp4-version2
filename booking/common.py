# common.py

from .models import Flight
from django.shortcuts import get_list_or_404


class Common:
    """
    I use this class as the repository of global variables, settings
    and methods needed throughout this App.
    """

# Class Variables
    initialised = None
    outbound_flights = None
    inbound_flights = None
    flight_info = None
    save_context = None
    OUTBOUND_TIME_OPTIONS1 = None
    OUTBOUND_TIME_OPTIONS2 = None

    TITLE_CHOICES = [
        ("DR", "DOCTOR"),
        ("LADY", "LADY"),
        ("LORD", "LORD"),
        ("MSTR", "MASTER"),
        ("MISS", "MISS"),
        ("MR", "MR"),
        ("MRS", "MRS"),
        ("MS", "MS"),
        ("PROF", "PROFESSOR"),
        ("SIR", "SIR"),
        ("SIS", "SISTER"),
    ]

    def __init__(self):
        pass

    def format_radio_button_option(flight_STD,
                                   flight_from,
                                   flight_STA,
                                   flight_to):
        """
        STD: Standard Time of Departure
        STA: Standard Time of Arrival
        Produce the following format for the radio buttons:
        STD FROM - STA TO
        EG
        08:00 LCY - 09:45 IOM
        11:00 IOM - 12:45 LCY
        """
        return (f"{flight_STD[0:2]}:{flight_STD[2:4]} "
                f"{flight_from} - "
                f"{flight_STA[0:2]}:{flight_STA[2:4]} "
                f"{flight_to}")

    def initialisation():
        """ Fetch the contents of the Flights Database
        which holds the available flights' times, routes and capacity
        information and set them up in variables to be accessed by this App.
        """

        all_flight_entries = get_list_or_404(Flight.objects.all())

        # Two dictionaries for outbound and inbound
        outbound = {}
        inbound = {}
        # Nested Dictionary
        newdict = {}
        # odd flight no.  - outbound
        # even flight no. - inbound
        # however use a boolean flag
        boolean_flag = True

        # Needed to create the radio button options for each flight
        out_time_options1 = []
        out_time_options2 = []
        in_time_options1 = []
        in_time_options2 = []

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
                out_time_options1.append(each.flight_STD)
                out_time_options2.append(Common.format_radio_button_option(
                                                each.flight_STD,
                                                each.flight_from,
                                                each.flight_STA,
                                                each.flight_to))
            else:
                inbound[each.flight_number] = {}
                inbound[each.flight_number]["flight_from"] = each.flight_from
                inbound[each.flight_number]["flight_to"] = each.flight_to
                inbound[each.flight_number]["flight_STD"] = each.flight_STD
                inbound[each.flight_number]["flight_STA"] = each.flight_STA
                inbound[each.flight_number]["capacity"] = each.capacity
                in_time_options1.append(each.flight_STD)
                in_time_options2.append(Common.format_radio_button_option(
                                               each.flight_STD,
                                               each.flight_from,
                                               each.flight_STA,
                                               each.flight_to))

            boolean_flag = not boolean_flag

        newdict["numberof_oneway_flights"] = len(all_flight_entries) // 2

        # Store the results in Class variables
        Common.flight_info = newdict
        Common.outbound_flights = outbound
        Common.inbound_flights = inbound
        Common.OUTBOUND_TIME_OPTIONS1 = out_time_options1
        Common.OUTBOUND_TIME_OPTIONS2 = out_time_options2
        Common.INBOUND_TIME_OPTIONS1 = in_time_options1
        Common.INBOUND_TIME_OPTIONS2 = in_time_options2

        # Indicate that Initialisation has been done
        Common.initialised = True

    def format_error(text):
        """ Convert any underscores to spaces and capitalise the text. """
        text = text.replace("_", " ")
        return f"{text[0].capitalize()}{text[1:]}"
