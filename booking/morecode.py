"""
In an effort to modularise my code
I have added other methods here
"""

from django.contrib import messages
from .models import Schedule
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

    So each row has 4 seats
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
        return result


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
                       inbound_flightno, inbound_time):
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
        seatmap = "0" * 24
    else:
        seatmap = Schedule.seatmap

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