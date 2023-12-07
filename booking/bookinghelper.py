"""
In an effort to modularise my code
I have added other methods here
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, OuterRef, Subquery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Booking, Passenger
from .models import Schedule, Transaction

from .forms import AdultsForm, MinorsForm
from .forms import HiddenForm
from .forms import BagsRemarks
from .forms import AdultsEditForm, MinorsEditForm

from .common import Common
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from bitstring import BitArray
from random import randint
import re

# Constants

NULLPAX = "Enter the details for this passenger."
BAD_NAME = ("Names must begin and end with a letter. "
            "Names must consist of only alphabetical characters, "
            "apostrophes and hyphens.")
FIRSTNAME_BLANK = (f"Passenger Name required. "
                   f"Enter the First Name as on the passport.")
LASTNAME_BLANK = (f"Passenger Name required. "
                  f"Enter the Last Name as on the passport.")
CONTACTS_BLANK = ("Adult 1 is the Principal Passenger. "
                  "Contact Details are "
                  "mandatory for this Passenger. "
                  "Enter passenger's phone number and/or email.")
BAD_TELNO = "Enter a phone number of at least six digits."
BAD_EMAIL = "Enter a valid email address."
BAD_DATE = "Enter a valid date of birth."
FUTURE_DATE = "Your date of birth must be in the past."
TOO_YOUNG = ("Newly born infants younger than 14 days "
             " on the {0} will not be accepted for travel.")

ADULT_PRICE = 100  # Age > 15
CHILD_PRICE = 60  # Age 2-15
INFANT_PRICE = 30   # Age < 2
BAG_PRICE = 30
CHANGE_FEE = 20

######################


# Removed similar-looking characters such as l, 1, I, O and 0.
CHARACTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
CHARLIST = [*CHARACTERS]
CHARLIST = list(CHARACTERS)  # 32 CHARACTERS

FIRST_LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"
CHARLIST2 = [*FIRST_LETTERS]  # 24 CHARACTERS

"""
    Airlines generally seat passengers from the back of the aircraft
    So interpret the leftmost bit as position 95
    95 94 93 ... 2 1 0
     0  0  0 ... 0 0 0
"""

# CAPACITY is 96 - Number of seats in the aircraft
CAPACITY = 96  # Number of seats in the aircraft
LEFT_BIT_POS = CAPACITY - 1  # I.E. 95


def row_of_N_seats(number_needed, allocated, available):
    """ Find a 'row' of 'number_needed' seats """
    zeros = "0b" + "0"*number_needed
    result = available.find(zeros)
    if not result:
        return (False, allocated, available)

    # Set the bits to 1 to represent 'taken' seats
    bitrange = range(result[0], result[0] + number_needed)
    available.invert(bitrange)

    """
    Determine the range of seat positions
    e.g. 6 seats at position 77
    77-6+1 = 72
    so range(72, 78) = 72, 73, 74, 75, 76, 77
    Then add that range of seats to the 'allocated' list
    """
    end = LEFT_BIT_POS - result[0]
    start = end - number_needed + 1
    seat_range = range(start, end + 1)
    allocated += [*seat_range]
    return (True, allocated, available)


def find_N_seats(number_needed, allocated, available):
    """
    Find 'N' number of seats
    N being 'number_needed'
    'allocated' are all the seats found so far
    'available' is a bitstring depicting what is available
    This is a recursive algorithm
    """

    result = row_of_N_seats(number_needed, allocated, available)
    if result[0]:
        # Successfully found a row of N seats - so allocation is done!
        return result

    # if N = 1 then no available seats i.e. the flight is full
    if number_needed == 1:
        return (False, allocated, available)

    # Otherwise, starting with M=N-1,
    # see if it is possible to find a row of M seats
    # if so, allocate that row of seats
    # then see if the remainder can be allocated
    minus1 = number_needed - 1
    count = number_needed - 1
    while count != 1:
        result = row_of_N_seats(count, allocated, available)
        if not result[0]:
            # Try a smaller row allocation
            count != 1
            continue

        remainder_needed = number_needed - count
        remainder = find_N_seats(remainder_needed,
                                 allocated + result[1], result[2])
        if remainder[0]:
            # Found all the seats!
            return remainder

    # Not successful in finding any 'row' > 1
    # Therefore, allocate one seat
    # Then repeat 'find_N_seats' for the remainder

    result = row_of_N_seats(1, allocated, available)
    """
    Finding one seat at this stage should not fail
    TODO: Error 500 if this is not the case!
    """

    return find_N_seats(minus1,
                        allocated + result[1], result[2])


def seat_number(number):
    """
    Convert the number into its corresponding 'Seat Number'
    That is,
    0 is 1A, 1 is 1B , 2 is 1C, 3 is 1D, 4 is 2A, ...
    91 is 23D, 92 is 24A, 93 is 24B, 94 is 24C, 95 is 24D

    So, each row has 4 seats
    """

    try:
        # raise ValueError if 'Non numeric value'
        # Strictly speaking, this shouldn't happen!
        number = int(number)
        if number < 0 or number > LEFT_BIT_POS:
            raise ValueError
        divided_by4 = divmod(number, 4)
        result = f"{divided_by4[0] + 1}{chr(divided_by4[1] + 65)}"
    except ValueError:
        """
        TODO: Error 500 If This Happens!
        """

        result = ""
    finally:
        return result


def from_seat_to_number(seat):
    """
    Convert the alphanumeric seat number into a numeric value
    That is,
    1A is 0, 1B is 1, 1C is 2, 1D is 3, 2A is 4...
    23D is 91, 24A is 92, 24B is 93, 24C is 94, 24D is 95
    """

    number = re.search(r"^\d+", seat)
    if number:
        number = (int(number.group(0)) - 1) * 4
        number += ord(seat[-1]) - ord("A")
        return number

    return -1  # Catchall: Just In Case!


def convert_string_to_bitarray(hexstring):
    """
    The seatmap for a 96-seat aircraft is represented as
    a 96-bit-string.
    Ones for allocated seats, Zeros for empty seats
    This bit-string is written as a 24-character hex-string
    in the Schedule Model: seatmap
    Convert this string therefore into a BitArray as used
    by the 'bitstring' library
    """

    bit_array = BitArray(length=96)
    bit_array.overwrite("0x" + hexstring, 0)
    return bit_array


def convert_bitarray_to_hexstring(bit_array):
    """
    Convert the BitArray as used by the 'bitstring' library
    into a 24-character hex-string to be written to the Schedule file
    """
    return str(bit_array.hex.upper())
    """
    The hex-string ought to be 24 characters long
    TODO: Error 500 if this is not the case!
    """


def report_unavailability(request, direction, date_formatted, thetime):
    """ Send a Django Message regarding unavailability of seats """
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
                       inbound_flightno, inbound_time,
                       cleaned_data):
    """
    This routine will check whether there are enough seats
    available for the booking
    """
    queryset = Schedule.objects.filter(flight_date=outbound_date,
                                       flight_number=outbound_flightno)
    if len(queryset) == 0:
        # Empty Flight  - initialise the seatmap
        # 96-bit string = 24 character hex-string
        current_seatmap = "0" * 24
        Common.outbound_schedule_id = 0
        Common.outbound_schedule_instance = (outbound_date,
                                             outbound_flightno)
        Common.outbound_total_booked = 0
    else:
        instance = queryset[0]
        current_seatmap = instance.seatmap
        # Id/Instance of the Schedule Record
        Common.outbound_schedule_id = instance.id
        Common.outbound_total_booked = instance.total_booked
        Common.outbound_schedule_instance = instance

    # ADULTS
    numberof_seats_needed = (cleaned_data["adults"] +
                             cleaned_data["children"])
    # Note: Infants sit on the laps of the Adults
    # I.E. no seats for Infants!

    # Are there enough seats on the Outbound Flight?
    bit_array = convert_string_to_bitarray(current_seatmap)

    all_OK = True
    allocated = []
    result = find_N_seats(numberof_seats_needed, allocated, bit_array)
    if not result[0]:
        # Insufficient Availability!
        date_formatted = outbound_date.strftime("%d/%m/%Y")
        report_unavailability(request, departing,
                              date_formatted, outbound_time)
        Common.outbound_allocated_seats = []
        Common.outbound_seatmap = None
        all_OK = False
    else:
        # Seats Allocated
        Common.outbound_allocated_seats = result[1]
        Common.outbound_allocated_seats.reverse()  # Descending Order
        Common.outbound_seatmap = convert_bitarray_to_hexstring(result[2])
        Common.outbound_total_booked += numberof_seats_needed

    if cleaned_data["return_option"] != "Y":
        # No Return Flight
        return all_OK

    queryset = Schedule.objects.filter(flight_date=inbound_date,
                                       flight_number=inbound_flightno)
    if len(queryset) == 0:
        # Empty Flight  - initialise the seatmap
        # 96-bit string = 24 character hex-string
        current_seatmap = "0" * 24
        Common.inbound_schedule_id = 0
        Common.inbound_schedule_instance = (inbound_date,
                                            inbound_flightno)
        Common.inbound_total_booked = 0
    else:
        instance = queryset[0]
        current_seatmap = instance.seatmap
        # Id/Instance of the Schedule Record
        Common.inbound_schedule_id = instance.id
        Common.inbound_total_booked = instance.total_booked
        Common.inbound_schedule_instance = instance

    # Are there enough seats on the Inbound Flight?
    bit_array = BitArray(length=96)
    bit_array.overwrite("0x" + current_seatmap, 0)

    allocated = []
    result = find_N_seats(numberof_seats_needed, allocated, bit_array)
    if not result[0]:
        # Insufficient Availability!
        date_formatted = inbound_date.strftime("%d/%m/%Y")
        report_unavailability(request, returning, date_formatted, inbound_time)
        Common.inbound_allocated_seats = []
        Common.inbound_seatmap = None
        all_OK = False

    else:
        # Seats Allocated
        Common.inbound_allocated_seats = result[1]
        Common.inbound_allocated_seats.reverse()  # Descending Order
        Common.inbound_seatmap = convert_bitarray_to_hexstring(result[2])
        Common.inbound_total_booked += numberof_seats_needed

    return all_OK

""" 
What follows are a series of patches and Work-arounds
to 'fix' a group of intermittent errors that ONLY occur
when this App runs on Heroku

I CANNOT reproduced these errors on my machine locally
These 'errors' ONLY occur on Heroku
"""

def heroku_children_included_fix(request):
    """
    Fix regarding KeyError 'children_included'
    Ensure that both 'children_included & infants-included' 
    exist with values at this stage
    """

    if (hasattr(Common, "save_context") and
        Common.save_context is not None and
        "children_included" in Common.save_context and
        "infants_included" in Common.save_context):
        return
    
    if not hasattr(Common, "save_context"):
        Common.save_context = {}
    if Common.save_context is None:
        Common.save_context = {}
    if "children_included" not in Common.save_context:
        Common.save_context["children_included"] = (
            int(request.POST.get("children")) > 0)
    if "infants_included" not in Common.save_context:
        Common.save_context["infants_included"] = (
            int(request.POST.get("infants")) > 0)


def heroku_dates_fix(request):
    """
    Fix regarding KeyError 'booking'
    Ensure that both Common.save_context["booking"]["departing_date"]
    and Common.save_context["booking"]["returning_date"]
    exist with values at this stage
    """

    if (hasattr(Common, "save_context") and
        Common.save_context is not None and
        "booking" in Common.save_context and
        "departing_date" in Common.save_context["booking"] and
        "returning_date" in Common.save_context["booking"]):
        return
    
    if not hasattr(Common, "save_context"):
        Common.save_context = {}
    if Common.save_context is None:
        Common.save_context = {}
    if "booking" not in Common.save_context:
        Common.save_context["booking"] = {}

    newdate = request.POST.get("departing_date")
    newdate = datetime.strptime(newdate, "%Y-%m-%d").date()
    Common.save_context["booking"]["departing_date"] = newdate
    return_option = request.POST.get("return_option")
    Common.save_context["booking"]["return_option"] = return_option
    if return_option == "N":
        # dummy nonnull value - one-way journey
        Common.save_context["booking"]["returning_date"] = newdate
    newdate = request.POST.get("returning_date")
    newdate = datetime.strptime(newdate, "%Y-%m-%d").date()
    Common.save_context["booking"]["returning_date"] = newdate
    

def heroku_booking_fix(request):
    """
    Fix regarding KeyError at /details/ 'booking'

    Ensure that both 'children_included & infants-included' 
    exist with values at this stage
    Ensure that 
    Common.save_context["booking"]["adults"]
    Common.save_context["booking"]["children"]
    Common.save_context["booking"]["infants"]
    all exist with values at this stage
    """

    heroku_children_included_fix(request)
    if (hasattr(Common.save_context, "booking") and
        Common.save_context["booking"] is not None and
        "adults" in Common.save_context["booking"] and
        "children" in Common.save_context["booking"] and
        "infants" in Common.save_context["booking"]):
        return
    
    if "booking" not in Common.save_context:
        Common.save_context["booking"] = {}
    Common.save_context["booking"]["adults"] = (
        int(request.POST.get("adults")))
    Common.save_context["booking"]["children"] = (
        int(request.POST.get("children")))
    Common.save_context["booking"]["infants"] = (
        int(request.POST.get("infants")))


def heroku_display_fix():
    """
    Fix regarding KeyError 'display' at /edit/
    Ensure that 
    Common.save_context["display"]["outbound_date"]
    exists with a value
    And if applicable
    Common.save_context["display"]["inbound_date"]
    exists with a value
    """

    if not hasattr(Common, "save_context"):
        Common.save_context = {}
    if Common.save_context is None:
        Common.save_context = {}
    if "display" not in Common.save_context:
        Common.save_context["display"] = {}
    if "outbound_date" not in Common.save_context["display"]:
        Common.save_context["display"]["outbound_date"] = (
              Common.the_outbound_date)
    if Common.save_context["display"]["outbound_date"] is None:
        Common.save_context["display"]["outbound_date"] = (
              Common.the_outbound_date)
    if ("inbound_date" in Common.save_context["display"] and
        Common.save_context["display"]["inbound_date"] is None):
        Common.save_context["display"]["inbound_date"] = (
              Common.the_inbound_date)

        # TODO
        messages.add_message(request, messages.ERROR,
                                     "DISPLAY " + Common.the_outbound_date)


def heroku_editmode_fix(request):
    """
    Heroku fix: just in case 'Common.paxdetails_editmode'
    loses its value - ensure they are identical
    """
    messages.add_message(request, messages.ERROR,
                         "EFIX" + str(Common.paxdetails_editmode))
    messages.add_message(request, messages.ERROR,
                         "EFIX2" + str(Common.heroku_editmode))
    return # TODO
    if Common.paxdetails_editmode != Common.heroku_editmode:
        Common.paxdetails_editmode = Common.heroku_editmode


def heroku_passengers_fix():
    """
    Fix regarding KeyError 'passengers'
    Ensure that Common.save_context["passengers"]
    exists with values at this stage
    """
    if (hasattr(Common, "save_context") and
        Common.save_context is not None and
        hasattr(Common.save_context, "passengers") and
        Common.save_context["passengers"] is not None):
        return

    Common.save_context["passengers"] = Common.context_2ndcopy["passengers"]


def heroku_details_fix():
    """
    Fix regarding KeyError 'passengers'
    Fix regarding KeyError 'original_pax_details'
    Ensure that Common.save_context["original_pax_details"]
    exists with values at this stage
    """

    if (hasattr(Common, "save_context") and
        Common.save_context is not None and
        "original_pax_details" in Common.save_context):
        print("CHECK1", Common.save_context["original_pax_details"]) # TODO
        return
    
    if not hasattr(Common, "save_context"):
        Common.save_context = {}
    if Common.save_context is None:
        Common.save_context = {}
    Common.save_context["original_pax_details"] = (
        Common.the_original_details
    )
    print("CHECK2", Common.the_original_details) # TODO


def heroku_hidden_fix():
    """
    Fix regarding KeyError "hidden_form"
    Ensure that Common.save_context["hidden_form"]
    exists with a value at this stage
    """

    if (hasattr(Common, "save_context") and
        Common.save_context is not None and
        "hidden_form" in Common.save_context and
        Common.save_context["hidden_form"] is not None):
        return
    
    if not hasattr(Common, "save_context"):
        Common.save_context = {}
    if Common.save_context is None:
        Common.save_context = {}
    Common.save_context["hidden_form"] = Common.the_hidden


def generate_random_pnr():
    """ Generate a random 6-character PNR """
    n = 5
    chars5 = "".join(["{}".format(CHARLIST[randint(0, 31)])
                     for num in range(0, n)])
    chars1 = CHARLIST2[randint(0, 23)]
    return chars1 + chars5


def unique_pnr():
    """
    Generate a Random Unique 6-character PNR
    PNR - Passenger Name Record
    """

    matches = 1
    while matches > 0:
        newpnr = generate_random_pnr()
        # Is it Unique?
        matches = Booking.objects.filter(pnr=newpnr)[:1].count()

    return newpnr


def calc_time_difference(return_time, depart_time):
    """
    Calculate the difference between these two times
    Which are represented as 4 character strings
    e.g. '1130'
    """

    return_time = int(return_time)
    quotient_rem = divmod(return_time, 100)
    return_time = (quotient_rem[0] * 60 +
                   quotient_rem[1])

    depart_time = int(depart_time)
    quotient_rem = divmod(depart_time, 100)
    depart_time = (quotient_rem[0] * 60 +
                   quotient_rem[1])
    if return_time < depart_time:  # In the Past!
        return return_time - depart_time

    # Add 1HR45MINS = 105 minutes to the Departure Time
    depart_time += 105
    return return_time - depart_time


def reset_common_fields(request):
    """
    Reset the following fields which are used
    when creating/amending Bookings and Pax records
    Especially 'Common.save_context' which at this stage
    would hold many values
    """
    Common.save_context = {}
    Common.outbound_schedule_instance = None
    Common.inbound_schedule_instance = None
    Common.outbound_seatmap = None
    Common.inbound_seatmap = None
    Common.outbound_allocated_seats = []
    Common.inbound_allocated_seats = []
    # TODO
    messages.add_message(request, messages.ERROR,
                                     "edit mode reset")
    Common.paxdetails_editmode = None
    # Heroku fix
    Common.heroku_editmode = None
    # Remove/Delete it if it exists
    request.session.pop("editmode", None)


def create_transaction_record(request):
    """ Record the Fees charged into the Transaction database """
    # New Instance
    trans_record = Transaction()

    # Heroku fix
    print("TP2", Common.the_pnr, Common.the_total_price) # TODO 
    trans_record.pnr = Common.save_context.get("pnr", Common.the_pnr);    
    trans_record.amount = Common.save_context.get("total_price", Common.the_total_price)


    trans_record.username = request.user
    # Write the new Transaction record
    trans_record.save()


def save_schedule_record(id, instance, total_booked, seatmap):
    """ Save this Instance of the Schedule Database """

    if id:
        # Update Existing Record
        schedule = instance
    else:
        # New Instance
        schedule = Schedule()
        schedule.flight_date = instance[0]
        schedule.flight_number = instance[1]

    schedule.total_booked = total_booked
    schedule.seatmap = seatmap
    # Save Schedule record
    schedule.save()


def update_schedule_database(request):
    """
    Update the Schedule Database
    with an updated seatmap for selected Date/Flight
    reflecting the newly Booked Passengers
    """

    # Outbound Flight
    save_schedule_record(Common.outbound_schedule_id,
                         Common.outbound_schedule_instance,
                         Common.outbound_total_booked,
                         Common.outbound_seatmap)

    if Common.save_context["return_option"] != "Y":
        return

    # Return Flight
    save_schedule_record(Common.inbound_schedule_id,
                         Common.inbound_schedule_instance,
                         Common.inbound_total_booked,
                         Common.inbound_seatmap)


def create_booking_instance(request, pnr):
    """
    Create the Booking Record instance
    All the Booking information is stored
    in the Class Variable 'Common.save_context'
    """

    # New Instance
    booking = Booking()
    booking.pnr = pnr
    # Heroku fix
    # TODO
    print("CD2", Common.save_context)
    # print("CD3", Common.save_context["depart_pos"])
    # print("CD3A", Common.save_context["return_pos"])
    print("CD3B", Common.save_context.get("depart_pos"))
    print("CD3C", Common.save_context.get("return_pos"))
    print("KEYS")

    # Heroku fix
    depart_pos = Common.save_context.get("depart_pos",
                        Common.the_depart_pos)

    # TODO
    print("DPR", Common.the_depart_pos, Common.the_return_pos, Common.the_return_option,
    Common.the_total_price, Common.the_bags, Common.the_remarks)
    # Outbound Flight Info
    outbound_flightno = Common.outbound_listof_flights[depart_pos]
    booking.outbound_date = Common.save_context["booking"]["departing_date"]
    booking.outbound_flightno = outbound_flightno
    booking.flight_from = Common.flight_info[outbound_flightno]["flight_from"]
    booking.flight_to = Common.flight_info[outbound_flightno]["flight_to"]

    # Heroku fix
    return_option = Common.save_context.get("return_option",
                           Common.the_return_option)
    if return_option == "Y":
        # Inbound Flight Info
        booking.return_flight = True
        booking.inbound_date = Common.save_context["booking"]["returning_date"]

        # Heroku fix
        return_pos = Common.save_context.get("return_pos",
                           Common.the_return_pos)

        booking.inbound_flightno = Common.inbound_listof_flights[return_pos]

    else:
        # One-way:
        booking.return_flight = False
        booking.inbound_date = None
        booking.inbound_flightno = ""

    # Heroku fix TODO
    total_price = Common.save_context.get("total_price",
                         Common.the_total_price)
    # TODO
    print("TP",Common.the_total_price)

    booking.fare_quote = total_price
    booking.ticket_class = "Y"
    booking.cabin_class = "Y"
    booking.number_of_adults = Common.save_context["booking"]["adults"]
    number_of_adults = booking.number_of_adults

    booking.number_of_children = (Common.save_context["booking"]["children"]
                                  if Common.save_context["children_included"]
                                  else 0)
    number_of_children = booking.number_of_children

    booking.number_of_infants = (Common.save_context["booking"]["infants"]
                                 if Common.save_context["infants_included"]
                                 else 0)
    number_of_infants = booking.number_of_infants

    booking.departure_time = (
        Common.flight_info[outbound_flightno]["flight_STD"])
    booking.arrival_time = Common.flight_info[outbound_flightno]["flight_STA"]
    # Heroku fix
    booking.number_of_bags = Common.save_context.get("bags",
                                    Common.the_bags)
    remarks = Common.save_context.get("remarks",
                    Common.the_remarks)

    booking.remarks = remarks.strip().upper()
    # Write the new Booking record
    booking.save()

    # Return the Numbers of each Passenger type
    return (booking, number_of_adults, number_of_children, number_of_infants)


def determine_seatnumber(request, paxno, pax_type):
    """
    Convert the numerical seat number into an aircraft seat number
    EG   0 is 1A, 1 is 1B , 2 is 1C, 3 is 1D, 4 is 2A, ...
       91 is 23D, 92 is 24A, 93 is 24B, 94 is 24C, 95 is 24D
    """

    outbound_seatno = (seat_number(Common.outbound_allocated_seats[paxno])
                       if pax_type != "I" else "")

    inbound_seatno = (seat_number(Common.inbound_allocated_seats[paxno])
                      if Common.save_context["return_option"] == "Y"
                      and pax_type != "I" else "")

    return (outbound_seatno, inbound_seatno)


def create_pax_instance(request,
                        booking, dataset_name, key, paxno, pax_type,
                        order_number,
                        infant_status_number,
                        outbound_seatno, inbound_seatno):

    """
    Create the actual Passenger Record instance
    All the Passenger information is stored
    in the Class Variable 'Common.save_context'

    order_number: First Pax numbered 1, 2nd 2, etc
    infant_status_number:
    Infant's Status Number matches each corresponding Adult's Status Number
    which starts at 1 i.e. Adult 1 - the Principal Passenger

    The data for each passenger is in 'dataset'
    'dataset' is a 'list' of each passenger's info e.g.
    [{'title': 'MR', 'first_name': 'FRED', 'last_name': 'BLOGGS',
    'contact_number': '012345678', 'contact_email': '',
    'wheelchair_ssr': '', 'wheelchair_type': ''},
    {'title': 'MR', 'first_name': 'JOE', 'last_name': 'BLOGGS',
    'contact_number': '', 'contact_email': '',
    'wheelchair_ssr': '', 'wheelchair_type': ''}]
    """

    pax = Passenger()
    pax.pnr = booking  # Foreign Key
    # Fetch a record of data which represents a form eg
    data = Common.save_context[dataset_name][paxno]
    pax.title = data["title"].strip().upper()
    pax.first_name = data["first_name"].strip().upper()
    pax.last_name = data["last_name"].strip().upper()
    pax.pax_type = pax_type
    pax.pax_number = order_number

    # Date of Birth is NULL for Adult
    # Contact Details are "" for Non-Adult
    if pax_type == "A":
        pax.date_of_birth = None
        pax.contact_number = data["contact_number"].strip().upper()
        pax.contact_email = data["contact_email"].strip().upper()
    else:
        pax.date_of_birth = data["date_of_birth"]
        pax.contact_number = ""
        pax.contact_email = ""

    pax.outbound_seat_number = outbound_seatno
    pax.inbound_seat_number = inbound_seatno
    pax.status = (f"HK{order_number}" if pax_type != "I"
                  else f"HK{infant_status_number}")
    order_number += 1
    infant_status_number += 1

    # SSR: # Blank or R for WCHR, S for WCHS, C for WCHC
    pax.wheelchair_ssr = data["wheelchair_ssr"]

    # Type: Blank or M for WCMP, L for WCLB; D for WCBD; W for WCBW
    pax.wheelchair_type = data["wheelchair_type"]

    return (pax, order_number, infant_status_number)


def write_passenger_record(request,
                           booking, passenger_type, plural, pax_type,
                           number_of_pax_type,
                           # First Pax numbered 1, 2nd 2, etc
                           order_number, editing_pax_details):
    """
    Passenger Records

    Passenger Info is stored in
    Common.save_context["adults_data"]
    Common.save_context["children_data"]
    Common.save_context["infants_data"]

    For each passenger allocate new seats
    for both the outbound and optionally the inbound flights
    """

    dataset_name = f"{plural}_data"  # EG "adults_data"
    paxno = 0
    key = f"{passenger_type}-{paxno}-"
    infant_status_number = 1
    while paxno < number_of_pax_type:
        outbound_seatno, inbound_seatno = (
                            determine_seatnumber(request,
                                                 order_number - 1,
                                                 pax_type))
        tuple = create_pax_instance(request,
                                    booking, dataset_name, key,
                                    paxno, pax_type,
                                    order_number, infant_status_number,
                                    outbound_seatno, inbound_seatno)
        pax, order_number, infant_status_number = tuple
        pax.save()
        paxno += 1

    return order_number


def create_new_booking_pax_records(request):
    """
    Create the Booking Record
    Create a Passenger Record for each passenger attached to the Booking
    There will be at least ONE Adult Passenger for each booking
    All the information is stored in the Class Variable 'Common.save_context'
    """

    # New Booking Instance
    # TODO
    print("CC3", request.POST.get("pnr"), request.POST)
    print("CC3A", Common.save_context)
    g = Common.save_context.get("pnr")
    print("pnr=", g)
    # TODO
    # f = Common.save_context.get("booking")
    # print("F1",f)
    # print("PNR2=",f.get("pnr"))
    # Include Heroku fix
    pnr = Common.save_context.get("pnr", Common.the_pnr)
    print("PNR=", pnr) # TODO
    tuple = create_booking_instance(request, pnr)
    booking, number_of_adults, number_of_children, number_of_infants = tuple

    # Now create the corresponding Passenger Records
    # Adult Passengers
    passenger_type = "adult"
    plural = "adults"
    pax_type = "A"
    order_number = write_passenger_record(request,
                                          booking, passenger_type,
                                          plural, pax_type,
                                          number_of_adults,
                                          1, False)

    # Child Passengers
    if number_of_children > 0:
        passenger_type = "child"
        plural = "children"
        pax_type = "C"
        order_number = write_passenger_record(request,
                                              booking, passenger_type,
                                              plural, pax_type,
                                              number_of_children,
                                              order_number, False)

    # Infant Passengers
    if number_of_infants > 0:
        passenger_type = "infant"
        plural = "infants"
        pax_type = "I"
        order_number = write_passenger_record(request,
                                              booking, passenger_type,
                                              plural, pax_type,
                                              number_of_infants,
                                              order_number, False)


def create_new_records(request):
    """
    Create the Booking Record
    Create a Passenger Record for each passenger attached to the Booking

    Create a Transaction Record record of the fees charged

    Update the Schedule Database
    with an updated seatmap for selected Dates/Flights
    reflecting the Booked Passengers
    """

    create_new_booking_pax_records(request)
    create_transaction_record(request)
    update_schedule_database(request)

    # Indicate success
    messages.add_message(request, messages.SUCCESS,
                         ("Booking {0} Created Successfully"
                          .format(Common.save_context["pnr"])))

    reset_common_fields(request)  # RESET!


def freeup_seats(thedate, flightno, seat_numbers_list):
    """
    Fetch the relevant flight from the Schedule Database
    using 'thedate & flightno'
    Then for each number in 'seat_numbers_list',
    reset the seats' 'bit-string' positions to 0 indicating
    that the seat is now available.
    Also update the Booked figure.
    """
    queryset = Schedule.objects.filter(flight_date=thedate,
                                       flight_number=flightno)
    if len(queryset) == 0:
        """
        Defensive - should always exist i.e. length nonzero
        TODO: Error 500 If Zero!
        """
        return

    schedule = queryset[0]
    bit_array = convert_string_to_bitarray(schedule.seatmap)
    removed_seats_count = 0

    for seatpos in seat_numbers_list:
        if seatpos < 0 or seatpos >= CAPACITY:
            """
            Defensive - should be between 0-95
            TODO: Error 500 If This Is Not The Case
            """
            continue

        # For the correct 'leftmost' position
        # subtract from 95
        bit_array.overwrite("0b0", LEFT_BIT_POS - seatpos)
        removed_seats_count += 1

    seatmap = convert_bitarray_to_hexstring(bit_array)

    if removed_seats_count == 0:
        """
        Defensive - should be nonzero
        TODO: Error 500 If This Is Not The Case
        """
        return

    schedule.seatmap = seatmap
    # Updated Flight's Booked Figure
    schedule.total_booked -= removed_seats_count

    # Update Schedule Record
    schedule.save()


def list_pax_seatnos(passenger_record, key):
    """ Create a list of each pax's seat number """
    seat_numbers_list = []
    for each_seatnum in passenger_record:
        # Defensive - 'outbound_seat_number', 'inbound_seat_number'
        # ought to be present
        # TODO: Suggest Error 500 if this is not the case
        if each_seatnum[key]:
            seat_numbers_list.append(from_seat_to_number(each_seatnum[key]))

    return seat_numbers_list


def realloc_seats_first(request, id, booking):
    """
    As part of the 'Delete Booking' operation
    Firstly, Determine the Booking's Seated Passengers
    Then fetch the relevant flight from the Schedule Database
    Moreover, reset the seats' 'bit-string' positions to 0 indicating
    that the seats are now available. Also update the Booking figure.
    """

    # Retrieve the Passengers
    queryset = Passenger.objects.filter(pnr_id=id).order_by("pax_number")
    passenger_list = queryset.values()
    seat_numbers_list = list_pax_seatnos(passenger_list,
                                         "outbound_seat_number")
    freeup_seats(booking.outbound_date, booking.outbound_flightno,
                 seat_numbers_list)

    # Return Flight
    if booking.return_flight:
        seat_numbers_list = list_pax_seatnos(passenger_list,
                                             "inbound_seat_number")
        freeup_seats(booking.inbound_date, booking.inbound_flightno,
                     seat_numbers_list)


def display_formset_errors(request, prefix, errors_list):
    """
    Instead of showing form errors within the form
    This routine will display any errors via the Django Messaging facility

    Sample 'errors_list'
    [{'last_name': ['This field is required.'],
      'last_name': ['This field is required.'],
      'contact_number': ['This field is required.'],
      'contact_email': ['This field is required.'],
      'wheelchair_ssr': ['This field is required.'],
      'wheelchair_type': ['This field is required.']}, {}]
    """

    number_of_forms = len(errors_list)
    for form_number in range(number_of_forms):
        prefix_number = form_number + 1
        fields_dict = errors_list[form_number]
        if not fields_dict:  # i.e. empty {}
            continue
        list_of_errors = fields_dict.items()
        for (field, field_errors) in list_of_errors:
            for item in field_errors:
                begin = f"{prefix} {prefix_number}:"
                formatted = Common.format_error(f"{field}")
                message_string = f"{begin} {formatted} - {item}"
                messages.add_message(request, messages.ERROR,
                                     message_string)


def append_to_dict(dict, key, item):
    """
    This dictionary should be of the form
    {item: [ ... , ... , ...]}
    Create a list if one does not exist before appending item
    """

    if item not in dict:
        dict[key] = [item]
    else:
        dict[key] = dict[key] + [item]
    return dict


def name_validation(fields_dict, accum_dict, errors_found):
    """ Handle the Formsets' Validation of First and Last Names """

    # First Name Validation
    temp_field = fields_dict.get("first_name", "").replace(" ", "")
    if temp_field == "":
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "first_name",
                                    FIRSTNAME_BLANK)
    elif not re.search("^[A-Z]$|^[A-Z][A-Za-z'-]*[A-Z]$",
                       temp_field, re.IGNORECASE):
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "first_name", BAD_NAME)

    # Last Name Validation
    temp_field = fields_dict.get("last_name", "").replace(" ", "")
    if temp_field == "":
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "last_name",
                                    LASTNAME_BLANK)
    elif not re.search("^[A-Z]$|^[A-Z][A-Za-z'-]*[A-Z]$",
                       temp_field, re.IGNORECASE):
        errors_found = True
        accum_dict = append_to_dict(accum_dict, "last_name", BAD_NAME)

    return (accum_dict, errors_found)


def adults_formset_validated(cleaned_data, request):
    """ Carry out Custom Validation of the Adults Formset """
    formset_errors = []  # Hopefully this will remain empty
    errors_found = False
    number_of_forms = len(cleaned_data)
    for form_number in range(number_of_forms):
        accum_dict = {}
        prefix_number = form_number + 1
        fields_dict = cleaned_data[form_number]

        # Blank Form?
        if not fields_dict:  # i.e. empty {} which indicates a blank form
            errors_found = True
            accum_dict = append_to_dict(accum_dict, "first_name", NULLPAX)
            formset_errors.append(accum_dict)
            continue

        accum_dict, errors_found = name_validation(fields_dict,
                                                   accum_dict, errors_found)

        # Contact Number/Email Validation can be null except for Adult 1
        telephone = fields_dict.get("contact_number", "").replace(" ", "")
        email = fields_dict.get("contact_email", "").replace(" ", "")
        # These can be null except for Adult 1
        both_blank = telephone == "" and email == ""
        if both_blank and prefix_number == 1:
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "contact_number", CONTACTS_BLANK)

        if not both_blank:
            if telephone != "" and not re.search("^[0-9]{6,}$", telephone):
                errors_found = True
                accum_dict = append_to_dict(accum_dict,
                                            "contact_number", BAD_TELNO)

        # This solution found at
        # https://stackoverflow.com/questions/3217682/how-to-validate-an-email-address-in-django

            if email:
                try:
                    validate_email(email)
                except ValidationError as e:
                    errors_found = True
                    accum_dict = append_to_dict(accum_dict,
                                                "contact_email", BAD_EMAIL)

        formset_errors.append(accum_dict)

    if errors_found:
        # Send as 'Django Messages' the errors that were found
        display_formset_errors(request, "Adult", formset_errors)
        return False

    return True


def date_validation_part2(request, accum_dict, errors_found,
                          date_of_birth, is_child):
    """ Handles the date validation for children and infants """

    todays_date = datetime.now().date()
    # datediff = date_of_birth - todays_date

    # Heroku fix
    heroku_dates_fix(request)

    departing_date = Common.save_context["booking"]["departing_date"]
    output_departing_date = departing_date.strftime("%d/%m/%Y")
    datediff = date_of_birth - todays_date
    days = datediff.days

    # days > 0 caters for hours/minutes/seconds!
    if date_of_birth > todays_date and days > 0:
        errors_found = True
        accum_dict = append_to_dict(accum_dict,
                                    "date_of_birth", FUTURE_DATE)
        return (accum_dict, errors_found)

    # if date_of_birth > todays_date then that means
    # days == 0 i.e. identical to Today's Date
    if days == 0:
        errors_found = True
        accum_dict = append_to_dict(accum_dict,
                                    "date_of_birth",
                                    TOO_YOUNG.format(output_departing_date))

        return (accum_dict, errors_found)

    datediff = departing_date - date_of_birth
    days = datediff.days
    if days < 14:
        errors_found = True
        accum_dict = append_to_dict(accum_dict,
                                    "date_of_birth",
                                    TOO_YOUNG.format(output_departing_date))
        return (accum_dict, errors_found)

    # Calculate the difference in years as shown here
    # https://stackoverflow.com/questions/3278999/how-can-i-compare-a-date-and-a-datetime-in-python
    difference_in_years = relativedelta(departing_date, date_of_birth).years

    if is_child:
        # CHILD
        if difference_in_years > 15:
            error_message = (
                "A child should be at least 2 "
                "and under 16 "
                f"on the Date of Departure: {output_departing_date} "
                f"But this passenger will be {difference_in_years}. "
                "Please enter an Adult Booking for this passenger.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
            return (accum_dict, errors_found)

    if not is_child:
        # INFANT
        if difference_in_years >= 2:
            paxtype = "an Adult" if difference_in_years > 15 else "a Child"
            error_message = (
                "An infant should be under 2 "
                f"on the Date of Departure: {output_departing_date} "
                f"But this passenger will be {difference_in_years}. "
                f"Please enter {paxtype} Booking for this passenger.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
            return (accum_dict, errors_found)

    # Does this Booking have a Return Journey?
    if Common.save_context["booking"]["return_option"] == "N":
        # No! This is a one-way journey!
        return (accum_dict, errors_found)

    # Yes! - This is a Return Journey!
    # Check the D.O.B. against the Return Date
    returning_date = Common.save_context["booking"]["returning_date"]
    output_returning_date = returning_date.strftime("%d/%m/%Y")
    # Method to determine the difference in years was found at
    # https://stackoverflow.com/questions/4436957/pythonic-difference-between-two-dates-in-years
    difference_in_years = relativedelta(returning_date, date_of_birth).years
    paxtype = "an Adult" if difference_in_years > 15 else "a Child"

    if is_child:
        # CHILD
        if difference_in_years > 15:
            error_message = (
                "A child should be at least 2 "
                "and under 16 "
                f"on the Returning Date: {output_returning_date} "
                f"But this passenger will be {difference_in_years}. "
                f"Please enter {paxtype} Booking for this passenger.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
    if not is_child:
        # INFANT
        if difference_in_years >= 2:
            error_message = (
                "An infant should be under 2 "
                f"on the Returning Date: {output_returning_date} "
                f"But this passenger will be {difference_in_years}. "
                f"Please enter {paxtype} Booking for this passenger.")

            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)

    return (accum_dict, errors_found)


def minors_formset_validated(cleaned_data, is_child_formset, request,):
    """
    Formsets have been 'cleaned' at this point
    Carry out Custom Validation of the Children Formset
    and the Infants Formset
    """
    formset_errors = []  # Hopefully this will remain empty
    errors_found = False
    number_of_forms = len(cleaned_data)
    todays_date = datetime.now().date()
    for form_number in range(number_of_forms):
        accum_dict = {}
        prefix_number = form_number + 1
        fields_dict = cleaned_data[form_number]

        # Blank Form?
        if not fields_dict:  # i.e. empty {} which indicates a blank form
            errors_found = True
            accum_dict = append_to_dict(accum_dict, "first_name", NULLPAX)
            formset_errors.append(accum_dict)
            continue

        accum_dict, errors_found = name_validation(fields_dict, accum_dict,
                                                   errors_found)

        # Date of Birth Validation
        # Children must be between 2 and 15
        # Infants must be between at least  14 days old and under 2 years old

        date_of_birth = fields_dict.get("date_of_birth", todays_date)
        # This field SHOULD BE <class 'datetime.date'>
        # Defensive Programming - because the 'cleaned' version
        # ought to be a valid date
        if not isinstance(date_of_birth, date):
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", BAD_DATE)

        else:
            accum_dict, errors_found = date_validation_part2(request,
                                                             accum_dict,
                                                             errors_found,
                                                             date_of_birth,
                                                             is_child_formset)

        formset_errors.append(accum_dict)

    if errors_found:
        # Send as 'Django Messages' the errors that were found
        paxtype = "Child" if is_child_formset else "Infant"
        display_formset_errors(request, paxtype, formset_errors)
        return False

    return True


def initialise_formset_context(request):
    """
    Create the 'context' to be used by the Passenger Details Template
    Necessary preset values have been saved in 'Common.save_context'
    """
    print("ED2", Common.paxdetails_editmode, Common.heroku_editmode)
    if Common.paxdetails_editmode:
        # Editing Pax Details
        return initialise_for_editing(request)

    context = {}

    # Heroku fix
    heroku_booking_fix(request)

    # ADULTS
    number_of_adults = Common.save_context["booking"]["adults"]
    AdultsFormSet = formset_factory(AdultsForm,
                                    extra=number_of_adults)
    adults_formset = AdultsFormSet(request.POST or None, prefix="adult")
    context["adults_formset"] = adults_formset

    # CHILDREN
    children_included = Common.save_context["children_included"]
    context["children_included"] = children_included
    if children_included:
        number_of_children = Common.save_context["booking"]["children"]
        ChildrenFormSet = formset_factory(MinorsForm,
                                          extra=number_of_children)
        children_formset = ChildrenFormSet(request.POST or None,
                                           prefix="child")
        context["children_formset"] = children_formset

    # INFANTS

    infants_included = Common.save_context["infants_included"]
    context["infants_included"] = infants_included
    if infants_included:
        number_of_infants = Common.save_context["booking"]["infants"]
        InfantsFormSet = formset_factory(MinorsForm,
                                         extra=number_of_infants)
        infants_formset = InfantsFormSet(request.POST or None,
                                         prefix="infant")
        context["infants_formset"] = infants_formset

    bags_remarks_form = BagsRemarks(request.POST or None, prefix="bagrem")
    context["bags_remarks_form"] = bags_remarks_form

    # Heroku fix
    heroku_hidden_fix()

    context["hidden_form"] = Common.save_context["hidden_form"]

    return context


def compute_total_price(request, children_included, infants_included):
    """
    Compute the Total Price of the Booking

    Adults   - £100     Age > 15
    Children -  £60     Age 2-15
    Infants  -  £30     Age < 2
    Bags     -  £30

    Then store the values in 'the_fees_template_values'
    in order that they can be rendered on the Confirmation Form
    """

    # Heroku fix
    heroku_booking_fix(request)
    # Heroku fix
    if not "return_option" in Common.save_context:
        Common.save_context["return_option"] = (
            request.POST.get("return_option"))

    multiple = (2 if Common.save_context["return_option"] == "Y"
                else 1)
    adult_price = ADULT_PRICE * multiple
    child_price = CHILD_PRICE * multiple
    infant_price = INFANT_PRICE * multiple

    the_fees_template_values = {}
    number_of_adults = Common.save_context["booking"]["adults"]
    total = number_of_adults * adult_price
    the_fees_template_values["adults_total"] = (
            f"{number_of_adults} x GBP{adult_price:3.2f} = GBP{total:5.2f}")

    if children_included:
        number_of_children = Common.save_context["booking"]["children"]
        product = number_of_children * child_price
        total += product
        the_fees_template_values["children_total"] = (
                    f"{number_of_children} x GBP{child_price:3.2f} = "
                    f"GBP{product:5.2f}")

    if infants_included:
        number_of_infants = Common.save_context["booking"]["infants"]
        product = number_of_infants * infant_price
        total += product
        the_fees_template_values["infants_total"] = (
                    f"{number_of_infants} x GBP{infant_price:3.2f} = "
                    f"GBP{product:5.2f}")

    number_of_bags = int(Common.save_context["bags"])
    if number_of_bags > 0:
        product = number_of_bags * BAG_PRICE
        total += product
        the_fees_template_values["bags_total"] = (
                f"{number_of_bags} x GBP{BAG_PRICE:3.2f} = "
                f"GBP{product:5.2f}")

    the_fees_template_values["total_price_string"] = f"GBP{total:5.2f}"
    # The Actual Total Price
    the_fees_template_values["total_price"] = total
    Common.save_context["total_price"] = total
    # Heroku fix TODO
    Common.the_total_price = total

    return the_fees_template_values


def add_fees_to_context(the_fees_template_values):
    """
    The fees for the selected journey need to be added to
    the Context which in turn will be rendered on the Confirmation Form
    """
    context = {}
    for var in the_fees_template_values:
        context[var] = the_fees_template_values[var]
    return context


def setup_confirm_booking_context(request,
                                  children_included,
                                  infants_included,
                                  context):
    """
    Calculate the Fees and Total Price
    Then add the results to the 'context' in order
    to be displayed on the Confirmation Form
    """

    the_fees = compute_total_price(request,
                                   children_included, infants_included)
    context = add_fees_to_context(the_fees)

    # Update the 'context' with the fees and total price
    context |= the_fees

    # Generate a Random Unique 6-character PNR
    # PNR - Passenger Name Record
    context["pnr"] = unique_pnr()
    # Heroku fix
    Common.the_pnr = context["pnr"]
    return context


def validate_bagrem_again(bags_remarks_form):
    """
    Heroku fix:
    There is an intermittent error that occurs which I cannot explain
    regarding 'bags_remarks_form'
    Even though this routine is called
    AFTER successful validation/cleaning of data
    i.e. after this IF statement:

        if not bags_remarks_form.is_valid:
            display_formset_errors(request, "Bag/Remarks",
                                        bags_remarks_form.errors)
            return (False, None)
    ....

    At this stage the data of 'bags_remarks_form' ought to have been cleaned
    therefore 'bags_remarks_form.cleaned_data' ought to exist!
    However, occasionally I get 500 errors at this stage due to
    the 'non-existence' of 'bags_remarks_form.cleaned_data'

    So my work-around is to create a version of
    'bags_remarks_form.cleaned_data'
    regardless of whether it exists at this stage since its contents
    ought to valid i.e. ought to have been cleaned!
    """

    bags_remarks_cleaned_copy = (
        {"bags": str(bags_remarks_form.data.get("bagrem-bags")),
         "remarks": bags_remarks_form.data.get("bagrem-remarks")})

    Common.the_bags = bags_remarks_form.data.get("bagrem-bags")
    Common.the_remarks = bags_remarks_form.data.get("bagrem-remarks")

    return bags_remarks_cleaned_copy


def any_string_changes(string1, string2):
    """
    For both strings: Remove spaces and convert to uppercase
    Then check if they differ
    """

    string1 = string1.replace(" ", "").upper()
    string2 = string2.replace(" ", "").upper()

    return string1 != string2


def calc_change_fees(request, context, count, key, fees, fee_key,
                     pax_number, minors):
    """ Calculate Change Fees
        £20 per pax
        £30 for each extra bags
        Will not charge for any 'wheelchair' changes
    """

    # Has any passenger been removed from the booking? - £20 fee!
    label = f"{key}remove_pax"
    if context.get(label, None):
        fees[fee_key] += CHANGE_FEE
        fees["changed"] = True
        print("REM") # TODO
        return fees

    label = f"{key}first_name"
    label = f"{key}last_name"
    paxlist = Common.save_context["original_pax_details"]
    print("TITLES", context[f"{key}title"], paxlist[pax_number]["title"])
    print("FN", context[f"{key}first_name"], paxlist[pax_number]["first_name"])
    print("LN", context[f"{key}last_name"], paxlist[pax_number]["last_name"])

    if (context[f"{key}title"] != paxlist[pax_number]["title"] or
        any_string_changes(context[f"{key}first_name"],
                           paxlist[pax_number]["first_name"]) or
        any_string_changes(context[f"{key}last_name"],
                           paxlist[pax_number]["last_name"])):
        print("NAMES") # TODO
        print("TITLES", context[f"{key}title"], paxlist[pax_number]["title"])
        print("FN", context[f"{key}first_name"], paxlist[pax_number]["first_name"])
        print("LN", context[f"{key}last_name"], paxlist[pax_number]["last_name"])
        fees[fee_key] += CHANGE_FEE
        fees["changed"] = True
        return fees

    if not minors:
        # Any changes regarding contact details
        if (any_string_changes(context[f"{key}contact_number"],
                               paxlist[pax_number]["contact_number"]) or
            any_string_changes(context[f"{key}contact_email"],
                               paxlist[pax_number]["contact_email"])):
            fees[fee_key] += CHANGE_FEE
            fees["changed"] = True

    else:

        # Any date of birth changes
        newdate = context[f"{key}date_of_birth"]
        newdate = datetime.strptime(newdate, "%Y-%m-%d").date()
        # TODO
        print("dates")
        print(newdate)
        print(paxlist[pax_number]["date_of_birth"])
        if (newdate != paxlist[pax_number]["date_of_birth"]):
            fees[fee_key] += CHANGE_FEE
            fees["changed"] = True

    print("FEES", fees) # TODO
    return fees


def compute_change_fees(request,
                        context, children_included, infants_included):
    """
    Compute the Total Price for Changing the Booking

    £20 per passenger
    £30 for every extra bag

    Then store the values in 'the_fees_template_values'
    in order that they can be rendered on the Confirmation Form
    """

    the_fees_template_values = {}
    fees = dict(admin=0, adults=0, children=0, infants=0,
                bags=0, changed=False)

    pax_number = 0  # Use this to determine the Pax Details
    # from the Original List of Passengers which is stored at
    # Common.save_context["original_pax_details"

    # ADULT
    number_of_adults = Common.save_context["booking"]["adults"]
    count = 0
    while count < number_of_adults:
        key = f"adult-{count}-"
        fees = calc_change_fees(request, context, count,
                                key, fees, "adults",
                                pax_number, False)
        count += 1
        pax_number += 1

    if fees["adults"]:
        # Adults Details have changed
        amount = fees["adults"]
        the_fees_template_values["adults_total"] = (
                f"Adult Changes = GBP{amount:5.2f}")

    if children_included:
        number_of_children = Common.save_context["booking"]["children"]
        count = 0
        while count < number_of_children:
            key = f"child-{count}-"
            fees = calc_change_fees(request, context, count,
                                    key, fees, "children",
                                    pax_number, True)
            count += 1
            pax_number += 1

        if fees["children"]:
            # Children Details have changed
            amount = fees["children"]
            the_fees_template_values["children_total"] = (
                    f"Child Changes = GBP{amount:5.2f}")

    if infants_included:
        number_of_infants = Common.save_context["booking"]["infants"]
        count = 0
        while count < number_of_infants:
            key = f"infant-{count}-"
            fees = calc_change_fees(request, context, count,
                                    key, fees, "infants",
                                    pax_number, True)
            count += 1
            pax_number += 1

        if fees["infants"]:
            # Infants Details have changed
            amount = fees["infants"]
            the_fees_template_values["infants_total"] = (
                    f"Infant Changes = GBP{amount:5.2f}")

    number_of_bags = int(context["bagrem-bags"])
    orig_number_of_bags = int(Common.save_context["original_bags"])
    if number_of_bags > orig_number_of_bags:
        the_difference = number_of_bags - orig_number_of_bags
        fees["bags"] = the_difference * BAG_PRICE
        fees["changed"] = True
        product = fees["bags"]
        the_fees_template_values["bags_total"] = (
                f"Baggage = {the_difference} x "
                f"GBP{BAG_PRICE:3.2f} = "
                f"GBP{product:5.2f}")

    orig_remarks = Common.save_context["original_remarks"]
    if any_string_changes(context["bagrem-remarks"], orig_remarks):
        fees["admin"] = CHANGE_FEE
        fees["changed"] = True
        the_fees_template_values["admin_total"] = (
                f"Admin Fee = GBP{CHANGE_FEE:5.2f}")

    if not fees["changed"]:
        # Charge 0.00 !
        the_fees_template_values["total_price_string"] = "GBP0.00"
        # The Actual Total Price
        the_fees_template_values["total_price"] = 0
        Common.save_context["total_price"] = 0
        # Heroku fix TODO
        Common.the_total_price = 0

    else:

        total = (fees["adults"] + fees["children"] + fees["infants"]
                                + fees["bags"] + fees["admin"])
        the_fees_template_values["total_price_string"] = f"GBP{total:5.2f}"
        # The Actual Total Price
        the_fees_template_values["total_price"] = total
        Common.save_context["total_price"] = total
        # Heroku fix TODO
        Common.the_total_price = total

    return the_fees_template_values


def setup_confirm_changes_context(request,
                                  children_included,
                                  infants_included,
                                  context):
    """
    Calculate the Change Fees and Total Price
    Then add the results to the 'context' in order
    to be displayed on the Confirmation Form
    """

    the_fees = compute_change_fees(request, context, children_included,
                                   infants_included)
    context = add_fees_to_context(the_fees)

    # Update the 'context' with the fees and total price
    context |= the_fees

    return context


def setup_formsets_for_create(request):
    """
    For the Creating of Passenger Details:
    Create up to three formsets
    for Adults, Children and Infants
    Adults Formset is Mandatory
    """

    context = {}

    # ADULTS
    AdultsFormSet = formset_factory(AdultsForm, extra=0)
    adults_formset = AdultsFormSet(request.POST or None, prefix="adult")

    ## TODO
    print("CC2", int(request.POST.get("children")) > 0, request.POST)
    # CHILDREN

    # Add Heroku fix
    heroku_children_included_fix(request)

    children_included = Common.save_context["children_included"]
    if children_included:
        ChildrenFormSet = formset_factory(MinorsForm, extra=0)
        children_formset = ChildrenFormSet(request.POST or None,
                                           prefix="child")
    else:
        children_formset = []

    # INFANTS
    infants_included = Common.save_context["infants_included"]
    if infants_included:
        InfantsFormSet = formset_factory(MinorsForm, extra=0)
        infants_formset = InfantsFormSet(request.POST or None, prefix="infant")
    else:
        infants_formset = []

    bags_remarks_form = BagsRemarks(request.POST or None, prefix="bagrem")

    return (adults_formset, children_formset, infants_formset,
            children_included, infants_included, bags_remarks_form,
            context)


def all_formsets_valid(request, adults_formset,
                       children_included, children_formset,
                       infants_included, infants_formset,
                       bags_remarks_form):
    """
    Carry out validation on up to three formsets
    1) Adults
    2) Children
    3) Infants

    They differ slightly:
    Adults have contact telephone/email
    Children/Infants have the Date of Birth - no contact details

    4) If the above are all valid, then validate the BagsRemarks Form
    """

    # Are there any Django Validations Errors to begin with?

    errors_found = False
    if adults_formset.is_valid():
        pass
    else:
        # The Adults Formset is Invalid - Report the Errors
        errors_found = True
        display_formset_errors(request, "Adult", adults_formset.errors)
        # Are there any 'non-form errors' in the Adults Formset?
        formset_non_form_errors = adults_formset.non_form_errors()
        if formset_non_form_errors:
            display_formset_errors(request,
                                   "Adult", formset_non_form_errors)

    if children_included:
        if children_formset.is_valid():
            pass
        else:
            # The Children Formset is Invalid - Report the Errors
            errors_found = True
            display_formset_errors(request, "Child", children_formset.errors)
            # Are there any 'non-form errors' in the Children Formset?
            formset_non_form_errors = children_formset.non_form_errors()
            if formset_non_form_errors:
                display_formset_errors(request,
                                       "Child", formset_non_form_errors)

    if infants_included:
        if infants_formset.is_valid():
            pass
        else:
            # The Infants Formset is Invalid - Report the Errors
            errors_found = True
            display_formset_errors(request, "Infant", infants_formset.errors)
            # Are there any 'non-form errors' in the Infants Formset?
            formset_non_form_errors = infants_formset.non_form_errors()
            if formset_non_form_errors:
                display_formset_errors(request,
                                       "Infant", formset_non_form_errors)

    if errors_found:
        # Proceed no further because errors have been discovered
        return (False, None)

    # Are the forms blank?
    is_empty = False

    # ADULTS
    cleaned_data = adults_formset.cleaned_data
    if not any(cleaned_data):
        is_empty = True
        messages.add_message(request, messages.ERROR,
                             "Enter the Adult's Passenger Details "
                             "for this booking.")
    else:
        Common.save_context["adults_data"] = cleaned_data

    # CHILDREN
    if children_included:
        cleaned_data = children_formset.cleaned_data
        if not any(children_formset.cleaned_data):
            is_empty = True
            messages.add_message(request, messages.ERROR,
                                 "Enter the Child's Passenger Details "
                                 "for this booking.")
        else:
            Common.save_context["children_data"] = cleaned_data

    if is_empty:
        return (False, None)

    # INFANTS
    if infants_included:
        cleaned_data = infants_formset.cleaned_data
        if not any(infants_formset.cleaned_data):
            is_empty = True
            messages.add_message(request, messages.ERROR,
                                 "Enter the Infant's Passenger Details "
                                 "for this booking.")
        else:
            Common.save_context["infants_data"] = cleaned_data

    if is_empty:
        return (False, None)

    # Validate all three formsets
    if not adults_formset_validated(adults_formset.cleaned_data, request):
        return (False, None)

    if (children_included and
        not minors_formset_validated(children_formset.cleaned_data,
                                     True, request)):
        return (False, None)

    if (infants_included and
        not minors_formset_validated(infants_formset.cleaned_data,
                                     False, request)):
        return (False, None)

    # Validate BagsRemarks Form
    if not bags_remarks_form.is_valid:
        display_formset_errors(request, "Bag/Remarks",
                                        bags_remarks_form.errors)
        return (False, None)

    """
    At this stage "bags" and "remarks" ought to be valid & 'cleaned'
    My work-around:
    Instead of returning
                        return (True, bags_remarks_form.cleaned_data)
    Return a 'new' copy instead
    """
    bags_remarks_cleaned_copy = (
            validate_bagrem_again(bags_remarks_form))
    return (True, bags_remarks_cleaned_copy)


def handle_pax_details_POST(request,
                            adults_formset,
                            children_included,
                            children_formset,
                            infants_included,
                            infants_formset,
                            bags_remarks_form):
    """
    The Handling of the Passenger Details Form
    This form consists of three formsets:
    1) AdultsForm - class AdultsForm
    2) ChildrenFormSet - Class MinorsForm
    3) InfantsFormSet - Class MinorsForm
    followed by the BagsRemarks Form

    Therefore, this method processes the validation
    of all the forms
    """

    context = request.POST
    are_all_forms_valid = all_formsets_valid(request,
                                             adults_formset,
                                             children_included,
                                             children_formset,
                                             infants_included,
                                             infants_formset,
                                             bags_remarks_form)
    if are_all_forms_valid[0]:
        cleaned_data = are_all_forms_valid[1]
        Common.save_context["bags"] = cleaned_data.get("bags")
        Common.save_context["remarks"] = cleaned_data.get("remarks")
        context_copy = request.POST.copy()  # Because of Immutability

        # Is it Editing Pax Details?
        print("ED3", Common.paxdetails_editmode, Common.heroku_editmode)
        if Common.paxdetails_editmode:
            new_context = setup_confirm_changes_context(request,
                                                        children_included,
                                                        infants_included,
                                                        context_copy)
            new_context["pnr"] = Common.save_context["booking"]["pnr"]

            # Heroku fix TODO
            print(request.POST)

            # Editing: Therefore Proceed with Updating The Record
            Common.save_context["confirm-booking-context"] = context_copy
            return (True, new_context)

        # Otherwise Creating New Pax Details
        new_context = setup_confirm_booking_context(request,
                                                    children_included,
                                                    infants_included,
                                                    context_copy)

        # Proceed with Creating a New Record
        Common.save_context["pnr"] = new_context["pnr"]
        Common.save_context["confirm-booking-context"] = context_copy
        return (True, new_context)

    else:
        context = initialise_formset_context(request)
        return (False, context)


def handle_editpax_GET(request, id, booking):
    """
    The Handling of the Passenger Details Edit Form
    This form consists of three formsets:
    1) AdultsForm - class AdultsForm
    2) ChildrenFormSet - Class MinorsForm
    3) InfantsFormSet - Class MinorsForm
    followed by the BagsRemarks Form

    Therefore, this method retrieves the information
    Then creates the formsets so that they
    can be displayed
    """

    # Heroku fix
    heroku_display_fix()

    # Convert from "16NOV23" format to Datevalue i.e. 16/11/2023
    departing_date = Common.save_context["display"]["outbound_date"]

    # TODO
    messages.add_message(request, messages.ERROR,
                         "AFTER DISPLAY FIX")
    messages.add_message(request, messages.ERROR,
                         Common.the_outbound_date)
    messages.add_message(request, messages.ERROR,
                         Common.save_context["display"]["outbound_date"])

    # Heroku fix TODO
    if departing_date is None:
        departing_date = Common.the_outbound_date

    departing_date = datetime.strptime(departing_date,
                                       "%d%b%y").date()
    if "inbound_date" in Common.save_context["display"]:
        returning_date = Common.save_context["display"]["inbound_date"]
        returning_date = datetime.strptime(returning_date, "%d%b%y").date()
        return_option = "Y"
    else:
        # Set to the same nonnull value
        # since these dates are not part of the 'update' process
        returning_date = departing_date
        return_option = "N"

    context = {}
    context["booking"] = booking.__dict__
    context["booking"].pop("_state", None)
    context["booking"]["return_option"] = ("Y" if (
                      context["booking"]["return_flight"])
                                               else "N")

# TODO

    heroku_passengers_fix()

    # Get all the Passengers related to the Booking
    # At this point 'pax' is a QuerySet
    pax = Common.save_context["passengers"]
    # Convert the QuerySet to a Dictionary
    pax = pax.__dict__
    """
    _result_cache looks like this:
    '_result_cache': [{'id': 327, 'title': 'MR', 
    'first_name': 'ALAN', 'last_name': 'SMITH', 'pax_type': 'A', 
    'pax_number': 1, ...}]

    So, I will use these values to initialise
    """

    pax_initial_list = pax["_result_cache"]
    # TODO
    pax2 = Common.context_2ndcopy["passengers"]
    print("PAX2")
    print(1,pax2)
    pax2 = pax2.__dict__
    print(2,pax2)
    pax2_initial_list = pax2["_result_cache"]
    print(3, pax2_initial_list)

    count = 0
    # Convert from "12JAN12" format to Datevalue i.e. 12/01/2012
    for paxitem in pax_initial_list:
        date_of_birth = paxitem.get("date_of_birth")
        if date_of_birth:
            pax_initial_list[count]["date_of_birth"] = (
                datetime.strptime(date_of_birth, "%d%b%y").date()
            )
        count += 1
    pax = None  # reset

    # ADULTS
    number_of_adults = context["booking"]["number_of_adults"]
    context["adults"] = context["booking"]["number_of_adults"]

    AdultsEditFormSet = formset_factory(AdultsEditForm, extra=0)
    initial_list = list(filter(lambda f: (f["pax_type"] == "A"),
                        pax_initial_list))
    adults_formset = AdultsEditFormSet(prefix="adult", initial=initial_list)
    initial = filter(lambda f: (f["pax_type"] == "A"), pax_initial_list)

    # CHILDREN
    number_of_children = context["booking"]["number_of_children"]
    if number_of_children > 0:
        context["children_included"] = True
        ChildrenEditFormSet = formset_factory(MinorsEditForm, extra=0)
        initial_list = list(filter(lambda f: (f["pax_type"] == "C"),
                            pax_initial_list))
        children_formset = ChildrenEditFormSet(prefix="child",
                                               initial=initial_list)
    else:
        context["children_included"] = False
        children_formset = []

    # INFANTS
    number_of_infants = context["booking"]["number_of_infants"]
    if number_of_infants > 0:
        context["infants_included"] = True
        InfantsEditFormSet = formset_factory(MinorsEditForm, extra=0)
        initial_list = list(filter(lambda f: (f["pax_type"] == "I"),
                            pax_initial_list))
        infants_formset = InfantsEditFormSet(prefix="infant",
                                             initial=initial_list)
    else:
        context["infants_included"] = False
        infants_formset = []

    # Update the 'context' in order for
    # the form to be displayed and processed
    form = {"adults": number_of_adults, "children": number_of_children,
            "infants": number_of_infants,
            "return_option": return_option,
            "departing_date": departing_date,
            "returning_date": returning_date,
            # Set to misc. values e..g. 0800, 1830
            # since time fields are not part of the 'update' process
            "departing_time": "0800",
            "returning_time": "1830"}

    hiddenForm = HiddenForm(form)
    initial_dict = {"bags": context["booking"]["number_of_bags"],
                    "remarks": context["booking"]["remarks"]}
    bags_remarks_form = BagsRemarks(prefix="bagrem", initial=initial_dict)
    context["original_bags"] = context["booking"]["number_of_bags"]
    context["original_remarks"] = context["booking"]["remarks"]
    context["adults_formset"] = adults_formset
    context["children_formset"] = children_formset
    context["infants_formset"] = infants_formset
    context["hidden_form"] = hiddenForm
    context["bags_remarks_form"] = bags_remarks_form

    # Heroku fix
    Common.the_hidden = hiddenForm
    Common.the_bags_remarks = bags_remarks_form # TODO?

    # Save a copy in order to fetch any values as and when needed
    Common.save_context = context

    # 2nd copies needed for validation purposes
    Common.save_context["booking"]["adults"] = number_of_adults
    Common.save_context["booking"]["children"] = number_of_children
    Common.save_context["booking"]["infants"] = number_of_infants
    Common.save_context["booking"]["departing_date"] = departing_date
    Common.save_context["booking"]["returning_date"] = returning_date
    Common.save_context["original_pax_details"] = pax_initial_list
    # Heroku fix
    Common.the_original_details = pax_initial_list

    Common.save_context["children_included"] = number_of_children
    Common.save_context["infants_included"] = number_of_infants

    # Indicate that 'Editing' is being perform
    # Definitely needed for Heroku - Heroku fix
    # TODO
    messages.add_message(request, messages.ERROR,
                         "REDO EDITMODE> BEFORE" + str(Common.paxdetails_editmode))
    Common.paxdetails_editmode = True
    # TODO
    messages.add_message(request, messages.ERROR,
                         "REDO EDITMODE> AFTER" + str(Common.paxdetails_editmode))
    print("ED4", Common.paxdetails_editmode, Common.heroku_editmode)
    return context


def initialise_for_editing(request):
    """
    Create the 'context' to be used by
    the Passenger Details 'Editing' Template
    Necessary preset values have been saved in 'Common.save_context'
    """

    context = {}

    # Heroku fix
    heroku_booking_fix(request)

    # ADULTS
    number_of_adults = Common.save_context["booking"]["adults"]
    AdultsEditFormSet = formset_factory(AdultsEditForm,
                                        extra=number_of_adults)
    adults_formset = AdultsEditFormSet(request.POST or None,
                                       prefix="adult")
    context["adults_formset"] = adults_formset

    # CHILDREN
    children_included = Common.save_context["children_included"]
    context["children_included"] = children_included
    if children_included:
        number_of_children = Common.save_context["booking"]["children"]
        ChildrenEditFormSet = formset_factory(MinorsEditForm,
                                              extra=number_of_children)
        children_formset = ChildrenEditFormSet(request.POST or None,
                                               prefix="child")
        context["children_formset"] = children_formset

    # INFANTS

    infants_included = Common.save_context["infants_included"]
    context["infants_included"] = infants_included
    if infants_included:
        number_of_infants = Common.save_context["booking"]["infants"]
        InfantsEditFormSet = formset_factory(MinorsEditForm,
                                             extra=number_of_infants)
        infants_formset = InfantsEditFormSet(request.POST or None,
                                             prefix="infant")
        context["infants_formset"] = infants_formset

    bags_remarks_form = BagsRemarks(request.POST or None, prefix="bagrem")
    context["bags_remarks_form"] = bags_remarks_form

    # Heroku fix
    heroku_hidden_fix()

    context["hidden_form"] = Common.save_context["hidden_form"]

    return context


def setup_formsets_for_edit(request):
    """
    For the Editing of Passenger Details:
    Build up to three formsets
    for Adults, Children and Infants
    Adults Formset is Mandatory
    """

    result = initialise_for_editing(request)
    context = {}
    print("rp", request.POST)

    # ADULTS
    AdultsFormSet = formset_factory(AdultsForm, extra=0)
    adults_formset = result["adults_formset"]

    # CHILDREN
    children_included = Common.save_context["children_included"]
    if children_included:
        children_formset = result["children_formset"]
    else:
        children_formset = []

    # INFANTS
    infants_included = Common.save_context["infants_included"]
    if infants_included:
        infants_formset = result["infants_formset"]
    else:
        infants_formset = []

    bags_remarks_form = BagsRemarks(request.POST or None, prefix="bagrem")

    return (adults_formset, children_formset, infants_formset,
            children_included, infants_included, bags_remarks_form,
            context)


def update_pax_records(request):
    """
    Update the Passenger Records with any amendments and deletions
    There will be at least ONE Adult Passenger for each booking
    This is mandatory so 'Adult 1' cannot be deleted
    All the information is stored in the Class Variable 'Common.save_context'

    Procedure:
    Delete ALL the PAX records from the Passenger record
    Then write out the updated data taking into consideration any deletions
    """

    # TODO
    messages.add_message(request, messages.ERROR,
                         "PNR1 " + Common.the_pnr)
    messages.add_message(request, messages.ERROR,
                         hasattr(Common, "save_context"))
    messages.add_message(request, messages.ERROR,
                         Common.save_context.get("confirm-booking-context"))

    # Need a second copy of the PNR!
    Common.save_context["pnr"] = Common.the_pnr
    print("2ND COPY", Common.the_pnr)

    newdata = Common.save_context.get("confirm-booking-context")
    
    # Delete all the Passengers in the Booking
    booking_id = Common.the_booking_id
    Passenger.objects.filter(pnr_id=booking_id).delete()

    outbound_seats_list = []
    inbound_seats_list = []
    number_outbound_seats_deleted = 0
    number_inbound_seats_deleted = 0
    #    pax_orig_data_list = context["original_pax_details"]
    # TODO
    # Derived from Common.save_context["original_pax_details"]
    # Heroku fix
    heroku_details_fix()
    pax_orig_data_list = Common.save_context["original_pax_details"]
    # Fetch all Adults into one list
    adults_list = list(filter(lambda f: (f["pax_type"] == "A"),
                              pax_orig_data_list))
    # Fetch all Children into one list
    children_list = list(filter(lambda f: (f["pax_type"] == "C"),
                                pax_orig_data_list))
    # Fetch all Infants into one list
    infants_list = list(filter(lambda f: (f["pax_type"] == "I"),
                               pax_orig_data_list))

    # Remove any pairs of Adult and Infant marked for deletion
    # Record the seat numbers of all Adults
    count = 0
    while True:
        # 'adult-1-title'
        key = f"adult-{count}-title"
        if not newdata.get(key):
            break

        # Record Adult's Seat Number
        outbound_seats_list.append(from_seat_to_number(
                adults_list[count]["outbound_seat_number"]))
        if "inbound_seat_number" in adults_list[count]:
            inbound_seats_list.append(from_seat_to_number(
                adults_list[count]["inbound_seat_number"]))

        # Is this Adult Marked for deletion?
        # e.g. 'adult-1-remove_pax': ['on']
        key = f"adult-{count}-remove_pax"
        if newdata.get(key):
            """
            (NOTE: The value of 'count' should never be 0
            That is, key should never represent 'adult-0-remove_pax': ['on']
            That is, -0-
            This is because the first Adult passenger is
            a mandatory part of the booking
            Suggest Error 500)
            """

            number_outbound_seats_deleted += 1
            if "inbound_seat_number" in adults_list[count]:
                number_inbound_seats_deleted += 1

            # Remove Adult from the list
            adults_list[count] = None

            # Any corresponding infant attached to this Adult?
            # EG 'adult-1-title' plus a corresponding
            #   'infant-1-title'
            if newdata.get(f"infant-{count}-title"):
                # Remove Infant from the list
                infants_list[count] = None

        count += 1

    # Remove any Infants marked for deletion
    count = 0
    while True:
        # 'infant-0-title'
        key = f"infant-{count}-title"
        if not newdata.get(key):
            break

        # Marked for deletion?
        # e.g. 'infant-0-remove_pax': ['on']
        key = f"infant-{count}-remove_pax"
        if newdata.get(key):
            # Remove Infant from the list
            infants_list[count] = None
        count += 1

    # Remove any children marked for deletion
    count = 0
    while True:
        # 'child-0-title'
        key = f"child-{count}-title"
        if not newdata.get(key):
            break

        # Record Child's Seat Number
        outbound_seats_list.append(from_seat_to_number(
                children_list[count]["outbound_seat_number"]))
        if "inbound_seat_number" in children_list[count]:
            inbound_seats_list.append(from_seat_to_number(
                children_list[count]["inbound_seat_number"]))

        # Is this Child Marked for deletion?
        # e.g. 'child-0-remove_pax': ['on']
        key = f"child-{count}-remove_pax"
        if newdata.get(key):
            number_outbound_seats_deleted += 1
            if "inbound_seat_number" in children_list[count]:
                number_inbound_seats_deleted += 1

            # Remove child from the list
            children_list[count] = None

        count += 1

    # Filter Out The Deleted Items
    adults_list = list(filter(None, adults_list))
    children_list = list(filter(None, children_list))
    infants_list = list(filter(None, infants_list))
    """
    len(adults_list) should never be zero!
    TODO: Error 500 If This Happens!
    """
    number_outbound_seated_adults = len(adults_list)
    # Unlike this value which could be zero
    number_outbound_seated_children = len(children_list)
    number_seated_pax = (number_outbound_seated_adults +
                         number_outbound_seated_children)

    Common.outbound_allocated_seats = None
    Common.outbound_removed_seats = None
    Common.inbound_allocated_seats = None
    Common.inbound_removed_seats = None

    outbound_seats_list.sort()
    outbound_seats_list.reverse()  # Descending Order
    inbound_seats_list.sort()
    inbound_seats_list.reverse()   # Descending Order

    # Outbound
    if number_outbound_seats_deleted > 0:
        # Determine the seats that need to be removed from the Booking
        # Keep these
        Common.outbound_allocated_seats = (
            outbound_seats_list[0:number_seated_pax])
        # Remove these
        Common.outbound_removed_seats = (
            outbound_seats_list[-number_outbound_seats_deleted:])
    else:
        # No seats to remove
        Common.outbound_allocated_seats = outbound_seats_list

    # Inbound
    if number_inbound_seats_deleted > 0:
        # Determine the seats that need to be removed
        # Keep these
        Common.inbound_allocated_seats = (
            inbound_seats_list[0:number_seated_pax])
        # Remove these
        Common.inbound_removed_seats = (
            inbound_seats_list[-number_inbound_seats_deleted:])
    else:
        # No seats to remove
        Common.inbound_allocated_seats = inbound_seats_list

    # In fact these two values ought to be identical
    # if the Booking contains a return flight
    # number_outbound_seats_deleted
    # number_inbound_seats_deleted
    # TODO: Otherwise Error 500 If This Happens!

    # Fetch Booking Instance
    booking = get_object_or_404(Booking, pk=booking_id)

    # Need a second copy of the PNR before proceeding
    Common.save_context["pnr"] = Common.save_context["booking"]["pnr"]
    # Need a second copy of 'return_option' before proceeding
    Common.save_context["return_option"] = (
           Common.save_context["booking"]["return_option"])
    pnr = Common.save_context["pnr"]
    number_of_adults = len(adults_list)
    number_of_children = len(children_list)
    number_of_infants = len(infants_list)

    # Now create the corresponding Passenger Records
    # Adult Passengers
    passenger_type = "adult"
    plural = "adults"
    pax_type = "A"
    order_number = write_passenger_record(request,
                                          booking, passenger_type,
                                          plural, pax_type,
                                          number_of_adults, 1, True)

    # Child Passengers
    if number_of_children > 0:
        passenger_type = "child"
        plural = "children"
        pax_type = "C"
        order_number = write_passenger_record(request,
                                              booking, passenger_type,
                                              plural, pax_type,
                                              number_of_children,
                                              order_number, True)

    # Infant Passengers
    if number_of_infants > 0:
        passenger_type = "infant"
        plural = "infants"
        pax_type = "I"
        order_number = write_passenger_record(request,
                                              booking, passenger_type,
                                              plural, pax_type,
                                              number_of_infants,
                                              order_number, True)

    return (booking,
            number_of_adults, number_of_children,
            number_of_infants,
            number_outbound_seats_deleted,
            number_inbound_seats_deleted)


def update_booking(request, booking,
                   number_of_adults, number_of_children,
                   number_of_infants):
    """
    Update the Booking Record with
    any changes to Baggage or Remarks
    Update the number of passengers
    """

    booking.number_of_bags = int(Common.save_context["bags"])
    booking.remarks = Common.save_context["remarks"].strip().upper()
    booking.number_of_adults = number_of_adults
    booking.number_of_children = number_of_children
    booking.number_of_infants = number_of_infants
    booking.save()


def update_booked_figure_seatmap(schedule,
                                 number_deleted, seatnumbers_list):
    """
    # Adjust the Total Booked Figure and the Seatmap
    # in regards to the deleted passengers
    """

    schedule.total_booked -= number_deleted
    # Adjust the seatmap
    bit_array = convert_string_to_bitarray(schedule.seatmap)
    for each_seatno in seatnumbers_list:
        if each_seatno < 0 or each_seatno >= CAPACITY:
            """
            Defensive - should be between 0-95
            TODO: Error 500 If This Is Not The Case
            """
            continue

        # For the correct 'leftmost' position
        # subtract from 95
        bit_array.overwrite("0b0", LEFT_BIT_POS - each_seatno)

    schedule.seatmap = convert_bitarray_to_hexstring(bit_array)
    schedule.save()


def update_schedule_seating(request,
                            number_outbound_deleted,
                            number_inbound_deleted):
    """
    Update the Schedule Database with any seat changes
    due to removal/deletions of passengers from the Booking
    """

    # Outbound Flight
    if number_outbound_deleted == 0:
        # No Adults or Children removed
        # Just infants which do not occupy seats
        return

    the_flightdate = Common.save_context["booking"]["outbound_date"]
    the_flightno = Common.save_context["booking"]["outbound_flightno"]

    # Fetch Schedule Instance
    queryset = Schedule.objects.filter(flight_date=the_flightdate,
                                       flight_number=the_flightno)
    schedule = get_object_or_404(queryset)
    # Adjust the Total Booked Figure and the Seatmap
    update_booked_figure_seatmap(schedule,
                                 number_outbound_deleted,
                                 Common.outbound_removed_seats)

    if Common.save_context["booking"]["return_option"] != "Y":
        return

    the_flightdate = Common.save_context["booking"]["inbound_date"]
    the_flightno = Common.save_context["booking"]["inbound_flightno"]

    # Fetch Schedule Instance
    queryset = Schedule.objects.filter(flight_date=the_flightdate,
                                       flight_number=the_flightno)
    schedule = get_object_or_404(queryset)
    # Adjust the Total Booked Figure and the Seatmap
    update_booked_figure_seatmap(schedule,
                                 number_inbound_deleted,
                                 Common.inbound_removed_seats)


def update_pax_details(request):
    """
    Update the Passenger Records with any amendments and deletions

    Update the Booking if either Baggage has increased
    or the Remarks field has been changed

    Create a Transaction Record record of the fees charged

    Update the Schedule Database with any seat changes
    due to removal/deletions of passengers from the Booking
    """

    (booking,
     number_of_adults, number_of_children,
     number_of_infants,
     number_outbound_deleted,
     number_inbound_deleted) = update_pax_records(request)

    update_booking(request, booking,
                   number_of_adults,
                   number_of_children,
                   number_of_infants)
    create_transaction_record(request)

    update_schedule_seating(request,
                            number_outbound_deleted,
                            number_inbound_deleted)

    # Indicate success
    messages.add_message(request, messages.SUCCESS,
                         ("Booking {0} Updated Successfully"
                          .format(Common.save_context["pnr"])))

    reset_common_fields(request)  # RESET!