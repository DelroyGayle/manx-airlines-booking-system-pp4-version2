# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, OuterRef, Subquery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.core.validators import validate_email

from .models import Booking, Passenger

from .forms import BookingForm, CreateBookingForm
from .forms import AdultsForm, MinorsForm
from .forms import HiddenForm
from .forms import BagsRemarks

from . import bookinghelper as m
import datetime
from datetime import datetime

from .common import Common

# Display the Home Page


@login_required
def homepage(request):
    """
    On the first display of the Home Page
    Initialise various settings
    """
    m.reset_common_fields(request)
    if not Common.initialised:
        Common.initialisation()

    return render(request, "booking/index.html")


def message_error(message_string, request):
    """
    Used the Django Messaging system to display errors
    as opposed to using 'forms.errors'
    """
    messages.add_message(request, messages.ERROR, message_string)


def is_booking_form_valid(form, request):
    """ Booking Form Validation """
    if not form.is_valid():
        for field in form.errors:
            for item in form.errors[field]:
                message_string = Common.format_error(f"{field} - {item}")
                message_error(message_string, request)

        return (False, None)

    # FURTHER VALIDATION NEEDED
    # Check Dates and Flight Availability
    cleaned_data = form.cleaned_data

    if (cleaned_data["return_option"] == "Y" and
            cleaned_data["returning_date"] == cleaned_data["departing_date"]):
        # Same Day Travel - Is there enough time between journey times?
        depart_time = cleaned_data["departing_time"]
        return_time = cleaned_data["returning_time"]
        time_diff = m.calc_time_difference(return_time, depart_time)
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

    if (cleaned_data["departing_date"] == datetime.now().date()):
        # User has selected today's date - check the time HH:MM
        timenow = datetime.now().strftime("%H%M")
        depart_time = cleaned_data["departing_time"]
        time_diff = m.calc_time_difference(depart_time, timenow)
        if time_diff < 0:
            message_error("Departing Time - The time of the outbound flight "
                          "cannot be in the past.",
                          request)
            return (False, None)

    # The Form's contents has passed all validation checks!
    # Save the information for later processing
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

    check_avail = m.check_availability(request,
                                       "Departing Flight",
                                       outbound_date,
                                       outbound_flightno,
                                       outbound_time,
                                       "Returning Flight",
                                       inbound_date,
                                       inbound_flightno,
                                       inbound_time,
                                       cleaned_data)

    if not check_avail:
        # Insufficient Availability for Selected Flight(s)
        return (False, None)

    # Successful Validation
    return (True, save_data)


@login_required
def create_booking_form(request):
    """ The Handling of the Create Bookings Form """

    m.reset_common_fields(request)
    if not Common.initialised:
        Common.initialisation()

    form = CreateBookingForm(request.POST or None)

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        # check whether it is valid:
        print(164)
        is_form_valid, saved_data = is_booking_form_valid(form, request)
        print(166, is_form_valid)
        print(167, saved_data)
        print(168, is_form_valid)
        if is_form_valid:
            context = {"booking": form.cleaned_data}
            # Update dict 'context' with the contents of dict 'saved_data'
            context |= saved_data

            # Heroku fix:
            # Another copy of the above Update 
            # with the contents of dict 'saved_data'
            # TODO
            # Heroku fix
            Common.the_depart_pos = saved_data["depart_pos"]
            Common.the_return_pos = saved_data["return_pos"]
            Common.the_return_option = saved_data["return_option"]
            
            # ADULTS
            number_of_adults = form.cleaned_data["adults"]
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

            print("CD1", Common.save_context)

            return render(request, "booking/passenger-details-form.html",
                          context)

        else:
            # The Booking Form has failed validation
            form = CreateBookingForm(request.POST)

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)


@login_required
def passenger_details_form(request):
    """
    The Handling of the Passenger Details Form
    This form consists of three formsets:
    1) AdultsForm - Class AdultsForm
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
    # TODO
    messages.add_message(request, messages.ERROR,
                         "EDITMODE>" + str(Common.paxdetails_editmode))
    messages.add_message(request, messages.ERROR,
                         "EDITMODE2>" + str(Common.heroku_editmode_editmode))
    m.heroku_editmode_fix()
    print("ED5", Common.paxdetails_editmode, Common.heroku_editmode)

    (adults_formset, children_formset, infants_formset,
     children_included, infants_included,
     bags_remarks_form, context) = (
                m.setup_formsets_for_create(request)
            if not Common.paxdetails_editmode
            else 
                m.setup_formsets_for_edit(request))

    if request.method == "POST":
        result = m.handle_pax_details_POST(request,
                                           adults_formset,
                                           children_included,
                                           children_formset,
                                           infants_included,
                                           infants_formset,
                                           bags_remarks_form)
        is_valid, context = result
        if is_valid:
            print("EDITMODE", Common.paxdetails_editmode)
            print("ED6", Common.paxdetails_editmode, Common.heroku_editmode)
            if not Common.paxdetails_editmode:
                return render(request, "booking/confirm-booking-form.html",
                              context)
            else:
                return render(request, "booking/confirm-changes-form.html",
                              context)

    else:
        # request.method is "GET"
        number_of_adults = Common.save_context["booking"]["adults"]
        context = m.initialise_formset_context(request)

    return render(request, "booking/passenger-details-form.html", context)


@login_required
def confirm_booking_form(request):
    """ Confirm whether the passenger wants to go ahead with the Booking? """

    if request.method == "POST":
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse("home"))

        else:
            # Create new record Booking/Passenger Records
            # Create new Transaction Record
            # Update Schedule Database
            m.create_new_records(request)
            # Then show home page
            return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/confirm-booking-form.html", context)


@login_required
def confirm_changes_form(request):
    """
    After the user has made amendments to the Pax Details
    Display the fee incurred and if the user confirms
    proceed to:
    1) Update the Pax Details
    2) Create new Transaction Record
    3) Update Schedule Database regarding any seat changes
       because of any removal/deletions of passengers from the Booking
    """

    if request.method == "POST":
        if "cancel" in request.POST:
            m.reset_common_fields(request)  # RESET!
            # Home Page
            return HttpResponseRedirect(reverse("home"))
        else:
            m.update_pax_details(request)
            # Then show home page
            return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/confirm-changes-form.html", context)


@login_required
def view_booking(request, id):
    """ View The Booking """
    booking = get_object_or_404(Booking, pk=id)
    queryset = Passenger.objects.filter(pnr_id=id).order_by("pax_number")

    display = dict(created_at=booking.created_at.strftime("%d%b%y").upper(),
                   # EG 17NOV23
                   outbound_date=(booking.outbound_date.strftime("%d%b%y")
                                  .upper()),
                   # These 'time' fields are not part of
                   # the 'update' process so set to ""
                   departing_time="", returning_time="")

    # Heroku fix
    Common.the_outbound_date = display["outbound_date"]
    Common.the_pnr = booking.pnr
    Common.the_booking_id = booking.id

    if booking.return_flight:
        display["return_option"] = "Y"
        display["inbound_date"] = (booking.inbound_date.strftime("%d%b%y")
                                   .upper())
        # Heroku fix
        Common.the_return_option = "Y"
        Common.the_inbound_date = display["inbound_date"]

    else:
        display["return_option"] = "N"
        # Heroku fix
        Common.the_return_option = "N"
        # Dummy nonnull value
        Common.the_inbound_date = display["outbound_date"]

    passenger_list = queryset.values()
    count = 0
    for each_record in passenger_list:
        for each_field in each_record:
            if (each_field == "pax_type"
                    and passenger_list[count]["pax_type"] in "CI"):
                passenger_list[count]["date_of_birth"] = (
                    passenger_list[count]["date_of_birth"]
                    .strftime("%d%b%y").upper())
        count += 1

    context = {"booking": booking, "passengers": passenger_list,
               "display": display}
    # Keep a Copy for 'Edit Passengers' functionality
    Common.save_context = context
    Common.context_2ndcopy = context
    print("CC1",context)
    return render(request, "booking/view-booking.html", context)


@login_required
def search_bookings(request):
    """
    Search for the Booking using either
    1) The PNR
    2) The Principal Pax (Adult 1)'s First Name
    3) The Principal Pax (Adult 1)'s Last Name
    """

    query = request.GET.get("query").strip()
    # Blank Search
    if not query:
        return HttpResponseRedirect(reverse("home"))

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
                 Q(passenger__pax_number=1)) | (

                 # 3) Or Matching Principal Passenger's Last Name
                 Q(passenger__last_name__icontains=query) &
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

    for element in queryset:
        qs = Passenger.objects.filter(pnr=element.id,
                                      pax_number=1)

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


@login_required
def delete_booking(request, id):
    """ Delete a Booking """
    booking = get_object_or_404(Booking, pk=id)
    context = {"booking": booking}

    if request.method == "POST":
        # Update the Schedule Data base first by free up the seats
        # of the passengers belong to this Booking
        m.realloc_seats_first(request, id, booking)
        # Delete the Booking
        booking.delete()
        messages.add_message(request, messages.SUCCESS,
                             "Booking Deleted Successfully")
        return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/delete-booking.html", context)


def edit_booking(request, id):
    """ Update a Booking """
    booking = get_object_or_404(Booking, pk=id)
    form = BookingForm(instance=booking)
    context = {"booking": booking, "form": form}

    # Heroku fix
    Common.the_pnr = booking.pnr
    Common.the_booking_id = booking.id
    Common.paxdetails_editmode = True

    # TODO
    messages.add_message(request, messages.ERROR,
                         "7A" + str(Common.paxdetails_editmode))

    if request.method == "POST":
        return HttpResponseRedirect(reverse("view-booking",
                                            kwargs={"id": booking.pk}))

    else:
        # TODO
        messages.add_message(request, messages.ERROR,
                         "7BPOST" + str(Common.paxdetails_editmode))
        print("ED7b", Common.paxdetails_editmode, Common.heroku_editmode)
        Common.paxdetails_editmode = True # TODO
        # Heroku fix
        Common.heroku_editmode = True
        print("ED8", Common.paxdetails_editmode, Common.heroku_editmode)
        context = m.handle_editpax_GET(request, id, booking)

    return render(request, "booking/edit-booking.html", context)


@login_required
def logout_user(request):
    """ Handle the Log Out of the User """

    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         "Successfully logged out")

    return redirect(reverse("login"))


def handle_not_found(request, exception):
    """ 404 Custom Error Handling """
    return render(request, "includes/404_not_found.html", status=404)


def handle_500(request):
    """ 500 Custom Error Handling """
    return render(request, "includes/500_error.html", status=500)