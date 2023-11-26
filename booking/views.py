# Create your views here.

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

from . import morecode
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import random  # TODO
import re

from .common import Common

# TODO
# from .constants import FIRSTNAME_BLANK
# KEEP THIS - TODO
# import constants

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


# Display the Home Page

def homepage(request):
    # On the first display of the Home Page
    # Initialise various settings
    if not Common.initialised:
        Common.initialisation()

    return render(request, "booking/index.html")


def message_error(message_string, request):
    messages.add_message(request, messages.ERROR, message_string)


def is_booking_form_valid(form, request):
    if not form.is_valid():
        for field in form.errors:
            for item in form.errors[field]:
                message_string = Common.format_error(f"{field} - {item}")
                message_error(message_string, request)

        return (False, None)

    # FURTHER VALIDATION NEEDED
    # Check Dates and Flight Availability
    cleaned_data = form.cleaned_data
    print("CD", cleaned_data)
    if (cleaned_data["return_option"] == "Y" and
            cleaned_data["returning_date"] == cleaned_data["departing_date"]):
        # Same Day Travel - Is there enough time between journey times?
        depart_time = cleaned_data["departing_time"]
        return_time = cleaned_data["returning_time"]
        time_diff = morecode.calc_time_difference(return_time, depart_time)
        if time_diff < 0:
            message_error("Returning Time - The time of the return flight "
                          "cannot be in the past.",
                          request)
            return (False, None)

        if time_diff < 90:
            message_error(
                "Returning Time - The interval between flights cannot be "
                "less than 90 minutes.", request)
            return (False, None)

    # The Form's contents has passed all validation checks!
    # Save the information for later processing
    print("CD2", cleaned_data)
    print("CO", Common.save_context)
    # TODO
    save_data = {"return_option": cleaned_data["return_option"]}
    if cleaned_data["return_option"] == "Y":
        # Return Flight - Determine both flight numbers
        thetime = cleaned_data["departing_time"]
        depart_pos = Common.OUTBOUND_TIME_OPTIONS1.index(thetime)
        save_data["depart_pos"] = depart_pos
        outbound_flightno = Common.outbound_listof_flights[depart_pos]            
        thetime = cleaned_data["returning_time"]
        return_pos = Common.INBOUND_TIME_OPTIONS1.index(thetime)
        save_data["return_pos"] = return_pos

    else:

        # One-way: Note the position of the departure flight
        thetime = cleaned_data["departing_time"]
        depart_pos = Common.OUTBOUND_TIME_OPTIONS1.index(thetime)
        save_data["depart_pos"] = depart_pos
        outbound_flightno = Common.outbound_listof_flights[depart_pos]            

    # Check Availability regarding the Selected Journeys
    # Outbound Flight
    outbound_date = cleaned_data["departing_date"]
    outbound_time = cleaned_data["departing_time"]
    
    return_option = cleaned_data["return_option"]
    if return_option == "Y":
        # Return Flight - Check Availability
        inbound_time = cleaned_data["returning_time"]
        return_pos = Common.INBOUND_TIME_OPTIONS1.index(inbound_time)
        inbound_flightno = Common.inbound_listof_flights[return_pos]            
        inbound_date = cleaned_data["returning_date"]
    else:
        inbound_time = None
        inbound_flightno = None
        inbound_date = None

    check_avail = morecode.check_availability(request,
                                              "Departing Flight",
                                              outbound_date, 
                                              outbound_flightno,
                                              outbound_time,
                                              "Returning Flight",
                                              inbound_date, 
                                              inbound_flightno,
                                              inbound_time,
                                              cleaned_data)

    print("CV", check_avail) # TODO
    if not check_avail:
        # Insufficient Availability for Selected Flight(s)
        return (False, None)
    
    # Successful Validation
    return (True, save_data)


# TODO
def create_booking_form(request):
    """ The Handling of the Create Bookings Form """

    if not Common.initialised:
        Common.initialisation()

    form = CreateBookingForm(request.POST or None)

    if request.method == "POST":
        #  create a form instance and populate it with data from the request:
        # check whether it is valid:
        # TODO
        is_form_valid, saved_data = is_booking_form_valid(form, request)
        if is_form_valid:
            context = {"booking": form.cleaned_data}
            # Update dict 'context' with the contents of dict 'saved_data'
            context |= saved_data 

            # ADULTS
            number_of_adults = form.cleaned_data["adults"]
            print("N/A", number_of_adults) # TODO
            AdultsFormSet = formset_factory(AdultsForm,
                                            extra=number_of_adults)
            adults_formset = AdultsFormSet(prefix="adult")

            # CHILDREN
            number_of_children = form.cleaned_data["children"]
            if number_of_children > 0:
                children_included = True
                ChildrenFormSet = formset_factory(MinorsForm,
                                                  extra=number_of_children)
                children_formset = ChildrenFormSet(prefix="child")
            else:
                children_included = False
                children_formset = []

            # INFANTS
            number_of_infants = form.cleaned_data["infants"]
            if number_of_infants > 0:
                infants_included = True
                InfantsFormSet = formset_factory(MinorsForm,
                                                 extra=number_of_infants)
                infants_formset = InfantsFormSet(prefix="infant")
            else:
                infants_included = False
                infants_formset = []

            # Create the 'context'
            hiddenForm = HiddenForm(form.cleaned_data)
            bags_remarks_form = BagsRemarks(prefix="bagrem")
            context["adults_formset"] = adults_formset
            context["children_formset"] = children_formset
            context["children_included"] = children_included
            context["infants_formset"] = infants_formset
            context["infants_included"] = infants_included
            context["hidden_form"] = hiddenForm
            context["bags_remarks_form"] = bags_remarks_form

            # Save a copy in order to fetch any values as and when needed
            Common.save_context = context
            print("SAVED/1", Common.save_context) # TODO
            # TODO
            print("NOW", context)
            return render(request, "booking/passenger-details-form.html",
                          context)

            # CREATE SUCCESS MESSAGE TODO

        else:
            # The Booking Form has failed validation
            form = CreateBookingForm(request.POST)

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)

    
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
    the_fees = morecode.compute_total_price(children_included, infants_included)
    print(the_fees)
    context = morecode.add_fees_to_context(the_fees)

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


# TODO
def passenger_details_form(request):
    """
    The Handling of the Passenger Details Form
    This form consists of three formsets:
    1) AdultsForm - class AdultsForm
    2) ChildrenFormSet - Class MinorsForm
    3) InfantsFormSet - Class MinorsForm
    followed by the BagsRemarks Form

    Therefore,
    1) Validate all the forms
    2) If all the forms are valid,
       Calculate the Fees and Total Price
       Add the results to the 'context' 
       in order to be displayed on the Confirmation Form

    If Validation failed, Continue viewing the Passengers' Details
    """

    (adults_formset, children_formset, infants_formset,
     children_included, infants_included,
     bags_remarks_form, context) = morecode.create_formsets(request)

    if request.method == "POST":
        result = morecode.handle_pax_details_POST(request,
                                                  adults_formset,
                                                  children_included,
                                                  children_formset,
                                                  infants_included,
                                                  infants_formset,
                                                  bags_remarks_form)
        is_valid, context = result
        if is_valid:
#           return render(request, "booking/confirm-booking-form.html", context)  TODO
            return render(request, "booking/confirm-booking-form.html", context)

    else:
        # request.method is "GET"
        number_of_adults = Common.save_context["booking"]["adults"]
        context = morecode.initialise_formset_context(request)

    return render(request, "booking/passenger-details-form.html", context)


def confirm_booking_form(request):
    
    print(request.method, "RQ")
    if request.method == "POST":
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse("home"))
        # TODO
        else:
            # Create new record Booking/Passenger Records
            # Create new Transaction Record
            # Update Schedule Database
                        # TODO
            morecode.create_new_records(request)
            # Then show home page
            return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/confirm-booking-form.html", context)

def view_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    print("BOOKING:", booking)  # PK/ID   TODO
    print("ID", id)
    print("PNR", booking.pnr)
    queryset = Passenger.objects.filter(pnr_id=id).order_by("pax_number")
    #morecode.handle_view_booking(request, booking, queryset)
    #return #TODO
    # TODO REMOVE
    print(queryset)  # TODO
    print(len(queryset))
    # passenger_list = []
    # for pax_record in queryset:  # TODO
    #     print(type(pax_record))
    #     print(pax_record.pax_type, pax_record.pax_number, pax_record.date_of_birth,
    #           pax_record.first_name, pax_record.last_name)
    #     passenger_list.append(pax_record)

    display = dict(created_at=booking.created_at.strftime("%d%b%y").upper(),
                   # EG 17NOV23
                   outbound_date=booking.outbound_date.strftime("%d%b%y").upper())
    if booking.return_flight:
        display["inbound_date"] = booking.inbound_date.strftime("%d%b%y").upper()

    passenger_list = queryset.values()
    count = 0
    for each_record in passenger_list:
        for each_field in each_record:
            if (each_field == "pax_type" 
                    and passenger_list[count]["pax_type"] in "CI"):
                passenger_list[count]["date_of_birth"] = (
                    passenger_list[count]["date_of_birth"]
                             .strftime("%d%b%y").upper())
        count+=1

    context = {"booking": booking, "passengers": passenger_list, "display": display}
    return render(request, "booking/view-booking.html", context)


def search_bookings(request):
    query = request.GET.get("query")
    # Blank Search
    if not query:
        return HttpResponseRedirect(reverse("home"))

    # TODO

    # Each Booking must has one Principal Passenger
    # That Passenger must be the first mentioned (pax_number=1)
    # and an Adult (pax_type="A")

    # Every Booking has 'one' Principal Passenger
    # Adult 1 - query that Passenger i.e.
    # pax_type == "A" and pax_number == 1
    adult1_qs = Passenger.objects.filter(pnr=OuterRef("id"),
                                         
                                         pax_number=1)

    # Case Insensitive Search - in 3 parts

    queryset = (Booking.objects.filter(
                # 1) Matching PNR
                Q(pnr__icontains=query) | (

                 # 2) Or Matching Principal Passenger's First Name
                 Q(passenger__first_name__icontains=query) &
                 #Q(passenger__pax_type__exact="A") &
                 Q(passenger__pax_number=1)) | (

                 # 3) Or Matching Principal Passenger's Last Name
                 Q(passenger__last_name__icontains=query) &
                 #Q(passenger__pax_type__exact="A") &
                 Q(passenger__pax_number=1)))

                # Sort the Query Result by the PNR
                .distinct().order_by("pnr")

                # Include the name of the Principal Passenger
                .annotate(first_name=Subquery(
                         adult1_qs.values("first_name")[:1]),
                          last_name=Subquery(
                         adult1_qs.values("last_name")[:1])))

    if queryset.count() == 0:
        # No Matching Bookings Found
        message_string = f"No Bookings found that matched '{query }'"
        messages.add_message(request, messages.ERROR,
                             message_string)
        return HttpResponseRedirect(reverse("home"))

    print("QS1", queryset)  # TODO
    for element in queryset:
        print("PNR1", element.pnr)  # TODO
        qs = Passenger.objects.filter(pnr=element.id,
                                      #pax_type="A",
                                      pax_number=1)
        print("SUBQ", qs)  # TODO
        for elem2 in qs:
            print(elem2.first_name, elem2.last_name)

    # Pagination as demonstrated in
    # https://testdriven.io/blog/django-pagination/

    # 3 records per page
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get("page", 1)

    try:
        page_object = paginator.page(page_number)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_object = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_object = paginator.page(paginator.num_pages)

    context = {"queryset": queryset, "query": query,
               "page_object": page_object}
    return render(request, "booking/search-bookings.html", context)


def delete_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    context = {"booking": booking}

    if request.method == "POST":
        # Update the Schedule Data base first by free up the seats
        # of the passengers belong to this Booking
        morecode.realloc_seats_first(request, id, booking)
        # Delete the Booking 
        booking.delete()
        messages.add_message(request, messages.SUCCESS,
                             "Booking Deleted Successfully")
        return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/delete-booking.html", context)


def edit_booking(request, id):
    booking = get_object_or_404(Employer, pk=id)
    form = BookingForm(instance=booking)
    context = {"booking": booking, "form": form}
    if request.method == "POST":

        # Update Booking() with the new values
        # TODO

        booking.company_name = request.POST.get("company_name")
        booking.number_of_employees = request.POST.get("number_of_employees")
        # employer_test_flag will either be set to "on" or None
        # Handle it so that it is either "on" or False
        new_employer_test_flag = request.POST.get("employer_test_flag", False)
        # "employer_test_flag" -  convert "on" value to either True or False."]
        booking.employer_test_flag = (True if new_employer_test_flag == "on"
                                      else False)

        booking.save()
        return HttpResponseRedirect(reverse("view-booking",
                                            kwargs={"id": booking.pk}))
        # CREATE SUCCESS MESSAGE TODO

    return render(request, "booking/edit-booking.html", context)
