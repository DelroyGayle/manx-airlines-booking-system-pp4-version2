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
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Booking, Passenger

from .forms import BookingForm, CreateBookingForm
from .forms import AdultsForm, MinorsForm
from .forms import HiddenForm
from .forms import BagsRemarks

from . import morecode
import datetime
from datetime import datetime

from .common import Common

# Display the Home Page


@login_required
def homepage(request):
    # TODO """"
    # On the first display of the Home Page
    # Initialise various settings
    if not Common.initialised:
        Common.initialisation()

    return render(request, "booking/index.html")


def message_error(message_string, request):
    # TODO """"
    messages.add_message(request, messages.ERROR, message_string)


def is_booking_form_valid(form, request):
    # TODO """"
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

    if (cleaned_data["departing_date"] == datetime.now().date()):
        # User has selected today's date - check the time HH:MM
        timenow = datetime.now().strftime("%H%M")
        depart_time = cleaned_data["departing_time"]
        time_diff = morecode.calc_time_difference(depart_time, timenow)  # TODO
        if time_diff < 0:
            message_error("Departing Time - The time of the outbound flight "
                          "cannot be in the past.",
                          request)
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

    if not check_avail:
        # Insufficient Availability for Selected Flight(s)
        return (False, None)

    # Successful Validation
    return (True, save_data)


# TODO
@login_required
def create_booking_form(request):
    """ The Handling of the Create Bookings Form """

    print(request.user.is_authenticated)
    print(request.user.username)
    morecode.reset_common_fields()
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
            # TODO
            return render(request, "booking/passenger-details-form.html",
                          context)

            # CREATE SUCCESS MESSAGE TODO

        else:
            # The Booking Form has failed validation
            form = CreateBookingForm(request.POST)

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)


# TODO
@login_required
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
     bags_remarks_form, context) = (
            morecode.setup_formsets_for_create(request)
            if not Common.paxdetails_editmode
            else morecode.setup_formsets_for_edit(request))

    if request.method == "POST":
        # TODO
        print(request.POST)
        print(request.POST.get("adult-0-last_name", 100))
        print(request.POST.dict)
        result = morecode.handle_pax_details_POST(request,
                                                  adults_formset,
                                                  children_included,
                                                  children_formset,
                                                  infants_included,
                                                  infants_formset,
                                                  bags_remarks_form)
        is_valid, context = result
        if is_valid:
            if not Common.paxdetails_editmode:
                return render(request, "booking/confirm-booking-form.html",
                              context)
            else:
                return render(request, "booking/confirm-changes-form.html",
                              context)

    else:
        # request.method is "GET"
        number_of_adults = Common.save_context["booking"]["adults"]
        context = morecode.initialise_formset_context(request)

    return render(request, "booking/passenger-details-form.html", context)


@login_required
def confirm_booking_form(request):
    # TODO """"

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
            reset_common_fields()  # RESET!
            # Home Page
            return HttpResponseRedirect(reverse("home"))
        # TODO
        else:
            morecode.update_pax_details(request)
            # Then show home page
            return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/confirm-changes-form.html", context)


@login_required
def view_booking(request, id):
    # TODO """"
    booking = get_object_or_404(Booking, pk=id)
    queryset = Passenger.objects.filter(pnr_id=id).order_by("pax_number")

    display = dict(created_at=booking.created_at.strftime("%d%b%y").upper(),
                   # EG 17NOV23
                   outbound_date=(booking.outbound_date.strftime("%d%b%y")
                                  .upper()))
    if booking.return_flight:
        display["inbound_date"] = (booking.inbound_date.strftime("%d%b%y")
                                   .upper())

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
    Common.save_context = context  # TODO
    return render(request, "booking/view-booking.html", context)


@login_required
def search_bookings(request):
    # TODO """"
    query = request.GET.get("query").strip()
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


@login_required
def delete_booking(request, id):
    # TODO """"
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
    # TODO """"
    booking = get_object_or_404(Booking, pk=id)
    form = BookingForm(instance=booking)
    context = {"booking": booking, "form": form}
    if request.method == "POST":
        return HttpResponseRedirect(reverse("view-booking",
                                            kwargs={"id": booking.pk}))
        # CREATE SUCCESS MESSAGE TODO

    else:
        context = morecode.handle_editpax_GET(request, id, booking)

    return render(request, "booking/edit-booking.html", context)


@login_required
def logout_user(request):

    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out')

    return redirect(reverse('login'))
