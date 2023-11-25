"""
In an effort to modularise my code
I have added other methods here
"""

from django.contrib import messages
from .models import Booking, Passenger
from .models import Flight, Schedule, Transaction

from .common import Common
from bitstring import BitArray

"""
    Airlines generally seat passengers from the back of the aircraft
    So interpret the leftmost bit as position 95
    95 94 93 ... 2 1 0
     0  0  0 ... 0 0 0
"""

CAPACITY = 96  # Number of seats in the aircraft
LEFT_BIT_POS = CAPACITY - 1  # I.E. 95


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
    if return_time < depart_time: # In the Past!
        return return_time - depart_time

    # Add 1HR45MINS = 105 to the Departure Time
    depart_time += 105
    print(105, return_time, depart_time, return_time - depart_time)
    return return_time - depart_time

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
    print("TYP1", bit_array, hexstring) #  TODO
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
                                       flight_number = outbound_flightno)
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
        Common.outbound_schedule_id =instance.id
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
    print(bit_array)
    print(bit_array.bin)

    all_OK = True
    allocated = []
    result = find_N_seats(numberof_seats_needed, allocated, bit_array)
    if not result[0]:
        # Insufficient Availability!
        print("RO", result, result[2].bin)
        date_formatted = outbound_date.strftime("%d/%m/%Y")
        report_unavailability(request, departing, date_formatted, outbound_time)
        Common.outbound_allocated_seats = []
        Common.outbound_seatmap = None
        all_OK = False
    else:
        # Seats Allocated
        Common.outbound_allocated_seats = result[1]
        Common.outbound_seatmap = convert_bitarray_to_hexstring(result[2])
        print("OUT>",Common.outbound_total_booked, numberof_seats_needed,
        result[1])
        Common.outbound_total_booked += numberof_seats_needed

    if cleaned_data["return_option"] != "Y":
        # No Return Flight
        return all_OK

    print(inbound_date, inbound_flightno)
    print(type(inbound_date))
    queryset = Schedule.objects.filter(flight_date=inbound_date,
                                       flight_number = inbound_flightno)
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
        Common.inbound_schedule_id =instance.id
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
        print("RI", result, result[2].bin)
        date_formatted = inbound_date.strftime("%d/%m/%Y")
        report_unavailability(request, returning, date_formatted, inbound_time)
        Common.inbound_allocated_seats = []
        Common.inbound_seatmap = None
        all_OK = False

    else:
        # Seats Allocated
        Common.inbound_allocated_seats = result[1]
        Common.inbound_seatmap = convert_bitarray_to_hexstring(result[2])
        print("IN>",Common.inbound_total_booked, numberof_seats_needed,
        result[1])
        Common.inbound_total_booked += numberof_seats_needed

    print("ROK", all_OK)
    return all_OK


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
    trans_record.username = "user"
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
    print("SCH/ID/in", Common.inbound_schedule_id)
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
    booking.departure_time = Common.flight_info[outbound_flightno]["flight_STD"]
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

    # print("PAXNO out", paxno, pax_type, Common.outbound_allocated_seats[paxno])
    print(Common.outbound_allocated_seats, paxno)
    outbound_seatno = (seat_number(Common.outbound_allocated_seats[paxno])
                       if pax_type != "I" else "")
 
    # print("PAXNO in", paxno, pax_type, Common.inbound_allocated_seats[paxno]) TODO
    print(Common.inbound_allocated_seats, paxno)
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
    'contact_number': '012345678', 'contact_email': '', 'wheelchair_ssr': '', 'wheelchair_type': ''}, 
    {'title': 'MR', 'first_name': 'JOE', 'last_name': 'BLOGGS', 
    'contact_number': '', 'contact_email': '', 'wheelchair_ssr': '', 'wheelchair_type': ''}]
    """

    pax = Passenger()
    pax.pnr = booking # Foreign Key
    # TODO
    print("TYPE/P/KF",type(pax), key,dataset_name) # TODO
    print(dataset_name in Common.save_context)
    #print(f"{key}title", f"{key}title" in Common.save_context[dataset])#TODO
    #print(type(Common.save_context[dataset])) #TODO
    # Fetch a record of data which represents a form eg
    data = Common.save_context[dataset_name][paxno]
    print("DN", dataset_name, paxno)
    print("FETCHED", data)
    pax.title = (
        data["title"]
              .strip().upper())
    print("TITLE>", data["title"], pax.title)
    pax.first_name = (
        data["first_name"]
              .strip().upper())
    pax.last_name = (
        data["last_name"]
              .strip().upper())
    pax.pax_type=pax_type
    print("TYPE>", pax_type, pax.pax_type)
    pax.pax_number = order_number
    print("ORDER", pax_type, order_number, pax.pax_number)
    # Date of Birth is NULL for Adult
    # Contact Details are "" for Non-Adult
    if pax_type == "A":
        pax.date_of_birth = None
        pax.contact_number = (data["contact_number"]
                                    .strip().upper())
        pax.contact_email = (data["contact_email"]
                                   .strip().upper())
    else:
        pax.date_of_birth = data["date_of_birth"]
        pax.contact_number = ""
        pax.contact_email = ""

    pax.outbound_seat_number = outbound_seatno
    pax.inbound_seat_number = inbound_seatno
    pax.status = (f"HK{order_number}" if pax_type != "I"
                                      else f"HK{infant_status_number}")
    print("PCH", pax, order_number, infant_status_number) # TODO
    print("PCH2", pax.pax_number, order_number, infant_status_number) # TODO
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
    dataset_name = f"{plural}_data" # EG "adults_data"
    paxno = 0
    key = f"{passenger_type}-{paxno}-" # TODO
    infant_status_number = 1
    while paxno < number_of_pax_type:
        outbound_seatno, inbound_seatno = determine_seatnumber(order_number - 1, pax_type)
        tuple = create_pax_instance(booking, dataset_name, key, paxno, pax_type,
                                    order_number, infant_status_number,
                                    outbound_seatno, inbound_seatno)
        pax, order_number, infant_status_number = tuple
        print("PAX", pax)
        print("PAX>", paxno, order_number, pax_type, number_of_pax_type) # TODO
        pax.save()
        paxno += 1

    return order_number


def create_new_booking_pax_records():
    """
    Create the Booking Record
    And a Passenger Record for each passenger attached to the Booking
    There will be at least ONE Adult Passenger for each booking
    All the information is stored in the Class Variable 'Common.save_context'
    """

    print(Common.save_context) # TODO
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
    order_number = write_passenger_record(booking, passenger_type, plural, pax_type,
                                          number_of_adults)
    print("A AFTER", order_number)

    # Child Passengers
    if number_of_children > 0: 
        passenger_type = "child"
        plural = "children"
        pax_type = "C"
        order_number = write_passenger_record(booking, passenger_type, plural, pax_type,
                                              number_of_children, order_number)
    print("C AFTER", order_number)

    # Infant Passengers
    if number_of_infants > 0: 
        passenger_type = "infant"
        plural = "infants"
        pax_type = "I"
        order_number = write_passenger_record(booking, passenger_type, plural, pax_type,
                                              number_of_infants, order_number)
                                                                                    

def create_new_records(request):
    """
    Create the Booking Record
    And a Passenger Record for each passenger attached to the Booking

    Create a Transaction Record record the fees charged

    Update the Schedule Database 
    with an updated seatmap for selected Date/Flight
    reflecting the Booked Passengers
    """

    create_new_booking_pax_records()
    create_transaction_record()
    update_schedule_database()
                                                                                    
    # Indicate success
    messages.add_message(request, messages.SUCCESS,
                         ("Booking {0} Created Successfully"
                         .format(Common.save_context["pnr"])))

    reset_common_fields() # RESET!

