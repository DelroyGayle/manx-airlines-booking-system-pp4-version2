"""
In an effort to modularise my code
I have added other methods here
"""

########## TODO
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
from .models import Flight

from .forms import BookingForm, CreateBookingForm
from .forms import AdultsForm, MinorsForm
from .forms import HiddenForm
from .forms import BagsRemarks
###########


from django.shortcuts import render
# TODO
# get_object_or_404
# from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Booking, Passenger
from .models import Flight, Schedule, Transaction

from .common import Common
from .constants import CAPACITY
from bitstring import BitArray
import random  # TODO RE GENERATE PNR
import re


############# TODO


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

ADULT_PRICE = 100   # Age > 15
CHILD_PRICE = 60 # Age 2-15
INFANT_PRICE = 30   # Age < 2
BAG_PRICE = 30

######################

"""
    Airlines generally seat passengers from the back of the aircraft
    So interpret the leftmost bit as position 95
    95 94 93 ... 2 1 0
     0  0  0 ... 0 0 0
"""

# CAPACITY is 96 - Number of seats in the aircraft
LEFT_BIT_POS = CAPACITY - 1  # I.E. 95


def row_of_N_seats(number_needed, allocated, available):
    """ Find a 'row' of 'number_needed' seats """
    zeros = "0b" + "0"*number_needed
    result = available.find(zeros)
    if not result:
        return (False, allocated, available)

    print(number_needed, zeros)
    print("Z", zeros, result)
    print(available, result)
    print(type(available))
    # Set the bits to 1 to represent 'taken' seats
    bitrange = range(result[0], result[0] + number_needed)
    available.invert(bitrange)
    print(available)

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
    'allocated' are all seats found so far
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
            # Found all seats!
            return remainder

    # Not successful in finding any 'row' > 1
    # Therefore, allocate one seat
    # Then repeat 'find_N_seats' for the remainder

    result = row_of_N_seats(1, allocated, available)
    # Finding one seat at this stage should not fail
    # TODO

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
    except ValueError:  # TODO
        result = ""
    finally:
        print("SEAT:", number, result)
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
        print(number, number.group(0), seat, type(seat), seat[-1])
        number = (int(number.group(0)) - 1) * 4
        number += ord(seat[-1]) - ord("A")
        return number

    return -1  # Catchall: Just In Case!


def convert_string_to_bitarray(hexstring):
    """
    The seatmap for a 96-seat aircraft is represented as
    a 96-bit-string.
    Ones for allocated, Zeros for empty
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
    # TODO - 24 CHARACTER CHECK


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
    print(outbound_date, outbound_flightno)
    print(type(outbound_date))
    queryset = Schedule.objects.filter(flight_date=outbound_date,
                                       flight_number=outbound_flightno)
    print(len(queryset))
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
    print(numberof_seats_needed)
    # Note: Infants sit on the laps of the Adults
    # I.E. no seats for Infants!

    # Are there enough seats on the Outbound Flight?
    bit_array = convert_string_to_bitarray(current_seatmap)
    # TODO
    print(bit_array)
    print(bit_array.bin)

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
        Common.outbound_seatmap = convert_bitarray_to_hexstring(result[2])
        # TODO
        Common.outbound_total_booked += numberof_seats_needed

    if cleaned_data["return_option"] != "Y":
        # No Return Flight
        return all_OK

    print(inbound_date, inbound_flightno)
    print(type(inbound_date))
    queryset = Schedule.objects.filter(flight_date=inbound_date,
                                       flight_number=inbound_flightno)
    print(len(queryset))
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
    print(bit_array)
    print(bit_array.bin)

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
        Common.inbound_seatmap = convert_bitarray_to_hexstring(result[2])
        Common.inbound_total_booked += numberof_seats_needed

    print("ROK", all_OK)
    return all_OK


def calc_time_difference(return_time, depart_time):
    """
    Calculate the difference between these two times
    Which are represented as 4 character strings
    e.g. '1130'
    """

    print(return_time, depart_time)
    return_time = int(return_time)
    quotient_rem = divmod(return_time, 100)
    print(quotient_rem)
    return_time = (quotient_rem[0] * 60 +
                   quotient_rem[1])

    depart_time = int(depart_time)
    quotient_rem = divmod(depart_time, 100)
    print(quotient_rem)
    depart_time = (quotient_rem[0] * 60 +
                   quotient_rem[1])
    print(return_time, depart_time, return_time - depart_time)
    if return_time < depart_time:  # In the Past!
        return return_time - depart_time

    # Add 1HR45MINS = 105 minutes to the Departure Time
    depart_time += 105
    print(105, return_time, depart_time, return_time - depart_time)
    return return_time - depart_time


def reset_common_fields():
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


def create_transaction_record():
    """ Record the Fees charged into the Transaction database """
    # New Instance
    trans_record = Transaction()
    trans_record.pnr = Common.save_context["pnr"]
    trans_record.amount = Common.save_context["total_price"]
    # TODO
    trans_record.username = "username"
    # Write the new Transaction record
    trans_record.save()
    print("TRANS", trans_record)  # TODO


def save_schedule_record(id, instance, total_booked, seatmap):
    """ Save this Instance of the Schedule Database """

    print("SCH/ID", id)
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
    print("SEATMAP:", seatmap)
    # Save Schedule record
    schedule.save()


def update_schedule_database():
    """
    Update the Schedule Database
    with an updated seatmap for selected Date/Flight
    reflecting the newly Booked Passengers
    """

    # Outbound Flight
    print("SCH/ID/OUT", Common.outbound_schedule_id)
    save_schedule_record(Common.outbound_schedule_id,
                         Common.outbound_schedule_instance,
                         Common.outbound_total_booked,
                         Common.outbound_seatmap)

    if Common.save_context["return_option"] != "Y":
        return

    # Return Flight
    print("SCH/ID/in", Common.inbound_schedule_id,
          Common.inbound_schedule_instance,
          Common.inbound_total_booked)
    save_schedule_record(Common.inbound_schedule_id,
                         Common.inbound_schedule_instance,
                         Common.inbound_total_booked,
                         Common.inbound_seatmap)


def create_booking_instance(pnr):
    """
    Create the Booking Record instance
    All the Booking information is stored
    in the Class Variable 'Common.save_context'
    """

    # New Instance
    booking = Booking()
    print("CONTEXT", Common.save_context)
    print(pnr)  # TODO
    booking.pnr = pnr
    depart_pos = Common.save_context["depart_pos"]
    # Outbound Flight Info
    outbound_flightno = Common.outbound_listof_flights[depart_pos]
    booking.outbound_date = Common.save_context["booking"]["departing_date"]
    booking.outbound_flightno = outbound_flightno
    booking.flight_from = Common.flight_info[outbound_flightno]["flight_from"]
    booking.flight_to = Common.flight_info[outbound_flightno]["flight_to"]

    if Common.save_context["return_option"] == "Y":
        # Inbound Flight Info
        booking.return_flight = True
        return_pos = Common.save_context["return_pos"]
        booking.inbound_date = Common.save_context["booking"]["returning_date"]
        booking.inbound_flightno = Common.inbound_listof_flights[return_pos]

    else:
        # One-way:
        booking.return_flight = False
        booking.inbound_date = None
        booking.inbound_flightno = ""

    booking.fare_quote = Common.save_context["total_price"]
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

    booking.number_of_bags = Common.save_context["bags"]
    booking.departure_time = (
        Common.flight_info[outbound_flightno]["flight_STD"])
    booking.arrival_time = Common.flight_info[outbound_flightno]["flight_STA"]
    booking.remarks = Common.save_context["remarks"].strip().upper()
    print("BOOKING", booking)  # TODO
    # Write the new Booking record
    booking.save()

    # Return the Numbers of each Passenger type
    return (booking, number_of_adults, number_of_children, number_of_infants)


def determine_seatnumber(paxno, pax_type):
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

    print("CONVERTED", outbound_seatno, inbound_seatno)
    return (outbound_seatno, inbound_seatno)


def create_pax_instance(booking, dataset_name, key, paxno, pax_type,
                        order_number,
                        infant_status_number,
                        outbound_seatno, inbound_seatno):

    """
    Create the actual Passenger Record instance
    All the Passenger information is stored
    in the Class Variable 'Common.save_context'

    order_number: First Pax numbered 1, 2nd 2, etc
    infant_status_number:
    Infant's Status Number matches each Adult's Status Number
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
    print("DN", dataset_name, paxno)
    print("FETCHED", data)
    pax.title = data["title"].strip().upper()
    print("TITLE>", data["title"], pax.title)
    pax.first_name = data["first_name"].strip().upper()
    pax.last_name = data["last_name"].strip().upper()
    pax.pax_type = pax_type
    print("TYPE>", pax_type, pax.pax_type)
    pax.pax_number = order_number
    print("ORDER", pax_type, order_number, pax.pax_number)
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
    print("PCH", pax, order_number, infant_status_number)  # TODO
    print("PCH2", pax.pax_number, order_number, infant_status_number)  # TODO
    order_number += 1
    infant_status_number += 1

    # SSR: # Blank or R for WHCR, S for WCHS, C for WCHC
    pax.wheelchair_ssr = data["wheelchair_ssr"]

    # Type: Blank or M for WCMP, L for WCLB; D for WCBD; W for WCBW
    pax.wheelchair_type = data["wheelchair_type"]

    return (pax, order_number, infant_status_number)


def write_passenger_record(booking, passenger_type, plural, pax_type,
                           number_of_pax_type,
                           # First Pax numbered 1, 2nd 2, etc
                           order_number=1):

    """
    Passenger Records

    Passenger Info is stored in
    Common.save_context["adults_data"]
    Common.save_context["children_data"]
    Common.save_context["infants_data"]
    """
    # SEATNO TODO seat_numbers
    dataset_name = f"{plural}_data"  # EG "adults_data"
    paxno = 0
    key = f"{passenger_type}-{paxno}-"  # TODO
    infant_status_number = 1
    while paxno < number_of_pax_type:
        outbound_seatno, inbound_seatno = (
            determine_seatnumber(order_number - 1, pax_type))
        tuple = create_pax_instance(booking, dataset_name, key,
                                    paxno, pax_type,
                                    order_number, infant_status_number,
                                    outbound_seatno, inbound_seatno)
        pax, order_number, infant_status_number = tuple
        print("PAX", pax)  # TODO
        print("PAX>", paxno, order_number, pax_type, number_of_pax_type)
        pax.save()
        paxno += 1

    return order_number


def create_new_booking_pax_records():
    """
    Create the Booking Record
    Create a Passenger Record for each passenger attached to the Booking
    There will be at least ONE Adult Passenger for each booking
    All the information is stored in the Class Variable 'Common.save_context'
    """

    print(Common.save_context)  # TODO
    # New Booking Instance
    pnr = Common.save_context["pnr"]
    print(1004, type(pnr), pnr)
    tuple = create_booking_instance(pnr)
    booking, number_of_adults, number_of_children, number_of_infants = tuple

    # Now create the corresponding Passenger Records
    # Adult Passengers
    passenger_type = "adult"
    plural = "adults"
    pax_type = "A"
    print("WRITE BEFORE")
    order_number = write_passenger_record(booking, passenger_type,
                                          plural, pax_type,
                                          number_of_adults)
    print("A AFTER", order_number)

    # Child Passengers
    if number_of_children > 0:
        passenger_type = "child"
        plural = "children"
        pax_type = "C"
        order_number = write_passenger_record(booking, passenger_type,
                                              plural, pax_type,
                                              number_of_children, order_number)
    print("C AFTER", order_number)

    # Infant Passengers
    if number_of_infants > 0:
        passenger_type = "infant"
        plural = "infants"
        pax_type = "I"
        order_number = write_passenger_record(booking, passenger_type,
                                              plural, pax_type,
                                              number_of_infants, order_number)


def create_new_records(request):
    """
    Create the Booking Record
    Create a Passenger Record for each passenger attached to the Booking

    Create a Transaction Record record the fees charged

    Update the Schedule Database
    with an updated seatmap for selected Dates/Flights
    reflecting the Booked Passengers
    """

    create_new_booking_pax_records()
    create_transaction_record()
    update_schedule_database()

    # Indicate success
    messages.add_message(request, messages.SUCCESS,
                         ("Booking {0} Created Successfully"
                          .format(Common.save_context["pnr"])))

    reset_common_fields()  # RESET!


def freeup_seats(thedate, flightno, seat_numbers_list):
    """
    Fetch the relevant flight from the Schedule Database
    using 'thedate & flightno'
    Then for each number in 'seat_numbers_list',
    reset the seat's 'bit-string' positions to 0 indicating
    that the seat is now available.
    Also update the Booked figure.
    """
    queryset = Schedule.objects.filter(flight_date=thedate,
                                       flight_number=flightno)
    print("F", len(queryset), thedate, flightno)
    if len(queryset) == 0:
        return  # Defensive - should exist

    print(thedate, flightno)  # TODO
    schedule = queryset[0]
    print("BEFORE", schedule.seatmap)
    bit_array = convert_string_to_bitarray(schedule.seatmap)
    removed_seats_count = 0

    for seatpos in seat_numbers_list:
        if seatpos < 0 or seatpos >= CAPACITY:
            # Defensive - should be between 0-95
            continue

        # For the correct 'leftmost' position
        # subtract from 95
        bit_array.overwrite("0b0", LEFT_BIT_POS - seatpos)
        removed_seats_count += 1

    seatmap = convert_bitarray_to_hexstring(bit_array)
    print("AFTER", seatmap, removed_seats_count)

    if removed_seats_count == 0:  # Defensive - should be nonzero
        return

    print(schedule)
    schedule.seatmap = seatmap
    # Updated Flight's Booked Figure
    schedule.total_booked -= removed_seats_count

    # Update Schedule Record
    print("SEATMAP:", schedule.seatmap, "BOOKED", schedule.total_booked)
    # Save Schedule record
    schedule.save()


def list_pax_seatnos(passenger_record, key):
    """ Create a list of each pax's seat number """
    seat_numbers_list = []
    # TODO
    print("P", passenger_record)
    for each_seatnum in passenger_record:
        print(each_seatnum)
        # Defensive - 'outbound_seat_number', 'inbound_seat_number'
        # ought to be present
        if each_seatnum[key]:
            print("E", each_seatnum[key])
            seat_numbers_list.append(from_seat_to_number(each_seatnum[key]))

    return seat_numbers_list


def realloc_seats_first(request, id, booking):
    """
    As part of the 'Delete Booking' operation
    Firstly, Determine the Booking's Seated Passengers
    Then fetch the relevant flight from the Schedule Database
    Moreover, reset the seat 'bit-string' positions to 0 indicating
    that the seats are now available. Also update the Booking figure.
    """

    # Retrieve the Passengers
    queryset = Passenger.objects.filter(pnr_id=id).order_by("pax_number")
    passenger_list = queryset.values()
    seat_numbers_list = list_pax_seatnos(passenger_list,
                                         "outbound_seat_number")
    print(seat_numbers_list)  # TODO
    freeup_seats(booking.outbound_date, booking.outbound_flightno,
                 seat_numbers_list)

    if booking.return_flight:
        print(booking.inbound_date, booking.inbound_flightno)  # TODO
        seat_numbers_list = list_pax_seatnos(passenger_list,
                                             "inbound_seat_number")
        print(seat_numbers_list)
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
# def adults_formset_validated(cleaned_data, request):  # TODO

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
        # https://stackoverflow.com/questions/3217682/
        # how-to-validate-an-email-address-in-django

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

    print(500) # TODO
    return True


def date_validation_part2(accum_dict, errors_found,
                          date_of_birth, is_child):
    """ Handles the date validation for children and infants """

    todays_date = datetime.now().date()
    # datediff = date_of_birth - todays_date

    departing_date = Common.save_context["booking"]["departing_date"]
    print(9881, Common.save_context["booking"]["departing_date"], "DEP")
    print(9882, Common.save_context["booking"]["returning_date"], "RET")
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
                f"But this passenger will be {difference_in_years}.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
            return (accum_dict, errors_found)

    if not is_child:
        # INFANT
        if difference_in_years >= 2:
            error_message = (
                "An infant should be under 2 "
                f"on the Date of Departure: {output_departing_date} "
                f"But this passenger will be {difference_in_years}.")
            errors_found = True
            accum_dict = append_to_dict(accum_dict,
                                        "date_of_birth", error_message)
            return (accum_dict, errors_found)

    # Does this Booking have a Return Journey?
    if Common.save_context["booking"]["return_option"] == "N":
        # No!
        return (accum_dict, errors_found)

    # Yes! - Check the D.O.B. against the Return Date
    returning_date = Common.save_context["booking"]["returning_date"]
    output_returning_date = returning_date.strftime("%d/%m/%Y")
    # Method to determine the years was found at
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
            accum_dict, errors_found = date_validation_part2(accum_dict,
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
    context = {}

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

    #context["bags_remarks_form"] = Common.save_context["bags_remarks_form"]
    bags_remarks_form = BagsRemarks(request.POST or None, prefix="bagrem")
    context["bags_remarks_form"] = bags_remarks_form
    context["hidden_form"] = Common.save_context["hidden_form"]
    # TODO
    print("CON", context)
    print("SAVED_CONTEXT", Common.save_context)

    return context

    
def generate_pnr():
    """ 
    Generate a Random Unique 6-character PNR
    PNR - Passenger Name Record
    """

    # For now use a random number - TODO
    # For testing purposes use this naive approach:
    # a 3-character string prefixed with SMI
    # However ensure it is unique!
    matches = 1
    while matches > 0:
        random_string = str(random.randrange(100, 1000))  # 3 digits TODO
        newpnr = "SMI" + random_string
        matches = Booking.objects.filter(pnr=newpnr)[:1].count()
    # Unique PNR
    print(newpnr, "TYPE", type(newpnr)) # TODO
    return newpnr


def compute_total_price(children_included, infants_included):
    """ 
    Compute the Total Price of the Booking 

    Adults   - £100     Age > 15
    Children -  £60     Age 2-15
    Infants  -  £30     Age < 2
    Bags     -  £30 

    Then store the values in 'the_fees_template_values'
    in order that they can be rendered on the Confirmation Form
    """

    the_fees_template_values = {}
    number_of_adults = Common.save_context["booking"]["adults"]
    print("N/A2", number_of_adults)
    total = number_of_adults * ADULT_PRICE
    the_fees_template_values["adults_total"] = (
            f"{number_of_adults} x GBP{ADULT_PRICE:3.2f} = GBP{total:5.2f}")

    if children_included:
        number_of_children = Common.save_context["booking"]["children"]
        product = number_of_children * CHILD_PRICE 
        total += product
        the_fees_template_values["children_total"] = (
                    f"{number_of_children} x GBP{CHILD_PRICE:3.2f} = "
                    f"GBP{product:5.2f}")

    if infants_included:
        number_of_infants = Common.save_context["booking"]["infants"]
        product = number_of_infants * INFANT_PRICE
        total += product
        the_fees_template_values["infants_total"] = (
                    f"{number_of_infants} x GBP{INFANT_PRICE:3.2f} = "
                    f"GBP{product:5.2f}")
    
    print("BAGS",Common.save_context["bags"] ) # TODO
    number_of_bags = Common.save_context["bags"]
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
    print("TYPE/C1", the_fees_template_values) # TODO
    return the_fees_template_values


def add_fees_to_context(the_fees_template_values):
    """
    The fees for the selected journey need to be added to
    the Context which in turn will be rendered on the Confirmation Form
    """ 
    # print(702, type(context)) # TODO
    context = {}
    for var in the_fees_template_values:
        context[var] = the_fees_template_values[var]
    print(703, type(context)) # TODO
    return context


def setup_confirm_booking_context(request,
                                  children_included,
                                  infants_included,
                                  context):
    # TODO
    """
    Calculate the Fees and Total Price
    Then add the results to the 'context' in order
    to be displayed on the Confirmation Form
    """

    print("CONTEXTIN", context)
    print(701, type(context))
    the_fees = compute_total_price(children_included, infants_included)
    print(the_fees)
    context = add_fees_to_context(the_fees)

    # TODO
    # Update the 'context' with the fees and total price
    context |= the_fees
    print("900DONE", context)


    # Generate a Random Unique 6-character PNR
    # PNR - Passenger Name Record
    context["pnr"] = generate_pnr()
    print("type pnr", 1001, context["pnr"], type(context["pnr"]))

    #print("CONTEXTIN2", context)
    # context = booking_total_price(context, 
    #                               children_included, infants_included)

    # Render the Booking Confirmation Form
    print("CONFIRM BOOKING FORM", context) # TODO
    print(type(context))
    # TODO
    return context


def create_formsets(request):
    """
    Create up to three formsets 
    for Adults, Children and Infants
    Adults Formset is Mandatory
    """

    print(800, "REQ", request.method)  # TODO
    context = {}

    # ADULTS
    AdultsFormSet = formset_factory(AdultsForm, extra=0)
    adults_formset = AdultsFormSet(request.POST or None, prefix="adult")

    # CHILDREN
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
    print(802, request.method, "CONTEXT FETCH",
          children_included, request.POST)  # TODO
    print(803, context)

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
        print(400) #TODO
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
    print(401) # TODO
    cleaned_data = adults_formset.cleaned_data
    if not any(cleaned_data):
        print(402) # TODO
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

    print(403) # TODO
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

    print(860, type(bags_remarks_form), bags_remarks_form) # TODO
    # Validate BagsRemarks Form
    if not bags_remarks_form.is_valid:
        print(865) # TODO
        display_formset_errors(request, "Bag/Remarks", bags_remarks_form.errors)
        return (False, None)

    print(870, bags_remarks_form.cleaned_data) # TODO
    return (True, bags_remarks_form.cleaned_data)


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
    print(804, "A POST")
    are_all_forms_valid = all_formsets_valid(request,
                                             adults_formset,
                                             children_included,
                                             children_formset,
                                             infants_included,
                                             infants_formset,
                                             bags_remarks_form)
    print(880, are_all_forms_valid)
    if are_all_forms_valid[0]:
        print(881)

        depart_pos = Common.save_context["depart_pos"]
        #outbound_date = Common.save_context["booking"]["departing_date"]
        #outbound_flightno = Common.outbound_listof_flights[depart_pos]            
        print(882)

        print(Common.save_context["booking"]["departing_date"], "DEP")
        print(Common.save_context["booking"]["returning_date"], "RET")

        cleaned_data = are_all_forms_valid[1]
        Common.save_context["bags"] = cleaned_data.get("bags")
        Common.save_context["remarks"] = cleaned_data.get("remarks")
        print(100) # TODO
        context_copy = request.POST.copy()
        print(200) # TODO
        new_context = setup_confirm_booking_context(request,
                                                    children_included,
                                                    infants_included,
                                                    context_copy)
        print(300, new_context) # TODO
        Common.save_context["pnr"] = new_context["pnr"]
        # TODO: CREATE THE RECORD!!
        print(810, "C1", Common.save_context["bags"], new_context["pnr"])
        print("C2", Common.save_context["remarks"])
        print(type(new_context))
        print(new_context)
        print("C3", context_copy)
        Common.save_context["confirm-booking-context"] = context_copy
        print(2000, Common.save_context["confirm-booking-context"])
        #       return render(request, "booking/confirm-booking-form.html", context)  TODO
        #return render(request, "booking/confirm-booking-form.html", new_context)
        return (True, new_context)

    else:
        context = initialise_formset_context(request)
        #  TODO
        print(820, type(Common.save_context))
        print("TT", Common.save_context)
        print("CON", context)
        print("SAVED_CONTEXT", Common.save_context)
        return(False, context)
