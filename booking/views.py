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
from .common import Common
# TODO
# from .constants import FIRSTNAME_BLANK
from datetime import datetime
from datetime import date  # TODO
# import constants
import random  # TODO
import re
# from .helpers import test TODO

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
                  "mandatory for this Passenger.\n"
                  "Enter passenger's phone number and/or email.")
BAD_TELNO = "Enter a phone number of at least six digits."
BAD_EMAIL = "Enter a valid email address."


def display_formset_errors(request, prefix, errors_list):
    """Instead of showing form errors within the form
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
    """This dictionary should be of the form
    {item: [ ... , ... , ...]}
    Create a list if one does not exist before appending item
    """

    if item not in dict:
        dict[key] = [item]
    else:
        dict[key] = dict[key] + [item]
    return dict


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
            if telephone != "" and not re.search("[0-9]{6,}", telephone):
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
        print("ACC", accum_dict, formset_errors)  # TODO

    if errors_found:
        # Send as a 'message' the errors that were found
        print("OKAY", formset_errors)  # TODO
        display_formset_errors(request, "Adult", formset_errors)
        return False

    return True


def is_formset_valid(request, adults_formset,
                     children_included, children_formset):
    formset = adults_formset
    errors_found = False
    print("INB", adults_formset.is_bound, adults_formset.has_changed())  # TODO

# Are there any Django Validations to begin with?
# TODO REMOVE
    # if False and not adults_formset.is_valid():
    #     errors_found = True
    #     display_formset_errors(request, "Adult", adults_formset.errors)
    # if False and children_included and not children_formset.is_valid():
    #     errors_found = True
    #     display_formset_errors(request, "Child", children_formset.errors)
    # # TODO
    # if errors_found:
    #     return False

    # TODO
    print("A1", adults_formset.data)
    if adults_formset.is_valid():
        pass
    else:
        print("ERRORS", adults_formset.errors)
    
    if children_included:
        children_formset.is_valid()

# TODO INF

    # TODO
    # print(adults_formset)
    print("CLEANDATA>>2", adults_formset.cleaned_data)
    cleaned_data = adults_formset.cleaned_data

    # Are the forms blank?
    is_empty = False
#    print(type(adults_formset))  TODO
    if not any(cleaned_data):
        is_empty = True
        messages.add_message(request, messages.ERROR,
                             "Enter the Adult's Passenger Details "
                             "for this booking.")

    if children_included:
        cleaned_data = children_formset.cleaned_data
        if not any(children_formset.cleaned_data):
            is_empty = True
            messages.add_message(request, messages.ERROR,
                                 "Enter the Children's Passenger Details "
                                 "for this booking.")
    if is_empty:
        return False
# TODO INF

    if not adults_formset_validated(adults_formset.cleaned_data, request):
        return False

    return True

# Create your views here.

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
        print("CONTEXT/error", context)
        for field in form.errors:
            for item in form.errors[field]:
                    message_string = Common.format_error(f"{field} - {item}")
                    message_error(message_string, request)
        return False

    print("CLEANED", form.cleaned_data)
    print(100, form.cleaned_data["adults"])
    # print("TEST", test()) TODO

    # FURTHER VALIDATION NEEDED
    # Check Dates and Flight Availability
    cleaned_data = form.cleaned_data
    if (cleaned_data["return_option"] == "Y" and 
        cleaned_data["returning_date"] == cleaned_data["departing_date"]):
        # Same Day Travel - Is there enough time between journey times?
            departPos = Common.OUTBOUND_TIME_OPTIONS1.index(cleaned_data["departing_time"])
            returnPos = Common.INBOUND_TIME_OPTIONS1.index(cleaned_data["returning_time"])
            if departPos > returnPos:
                message_error("The time of the return flight cannot be in the past.",
                              request)
                return False

            if departPos == returnPos:
                message_error("The interval between flights cannot be "
                              "less than 90 minutes.", request)
                return False

    # The Form's contents had passed all validation checks!
    return True


# TODO
def create_booking_form(request):

    if not Common.initialised:
        Common.initialisation()

    form = CreateBookingForm(request.POST or None)

    if request.method == "POST":
        #  create a form instance and populate it with data from the request:
        # check whether it is valid:
        # TODO
        if is_booking_form_valid(form, request):
            context = {"booking": form.cleaned_data, "form": form.cleaned_data,
                       # TODO HAVE IT TWICE?
                       "booking_cleaned_data": form.cleaned_data,
                       }
            # TODO
            number_of_adults = form.cleaned_data["adults"]
            AdultsFormSet = formset_factory(AdultsForm,
                                            extra=number_of_adults)  # TODO
            adults_formset = AdultsFormSet(prefix="adult")
            # for form in adults_formset:
            #      print(form.as_p()) # TODO
            # ChildrenFormSet = formset_factory(MinorsForm, extra=2)
            # children_formset = ChildrenFormSet(prefix="child")
            children_formset = []  # TODO
            # for form in children_formset:
            #      print(form.as_p()) # TODO

            hiddenForm = HiddenForm(form.cleaned_data)
            # hiddenForm.adults = 10  # TODO
            print(hiddenForm)  # TODO
            # print(form.cleaned_data) TODO
            context["adults_formset"] = adults_formset
            context["children_formset"] = children_formset
            context["hidden_form"] = hiddenForm

            print("CONTEXT", context)
            Common.save_context = context
            return render(request, "booking/passenger-details-form.html",
                          context)

            # CREATE MESSAGE TODO

        else:
            # Form had failed validation
            # TODO
            # RE-RENDER
            form = CreateBookingForm(request.POST)

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)


# TODO
def passenger_details_form(request):
    children_included = True  # TODO
    print("REQ", request.method)  # TODO
    # form = CreateBookingForm()  # TODO
    # context = {'form': form}

    AdultsFormSet = formset_factory(AdultsForm, extra=2)
    # TODO
    # ChildrenFormSet = formset_factory(MinorsForm, extra=2)
    #                                 # formset=BasePaxFormSet)
    print("TYPE 1", type(AdultsFormSet))
    adults_formset = AdultsFormSet(request.POST or None, prefix="adult")
    print("TYPE 2", type(adults_formset))
    # children_formset = ChildrenFormSet(request.POST or None, prefix="child")
    children_formset = []  # TODO
    print(request.method, "CONTEXT FETCH", request.POST)
    if request.method != "POST":
        context = {}

    if request.method == "POST":
        # TODO
        context = request.POST
        # TODO
        print("TYPE 3", type(adults_formset))
    # print(adults_formset.is_valid(), children_formset.is_valid(), "WELL?")

        children_included = None  # TODO
        if is_formset_valid(request,
                            adults_formset,
                            children_included,
                            children_formset):
            print("CLEAN A1", adults_formset.non_form_errors())  # TODO
            print(adults_formset.total_error_count(),
                  adults_formset.has_changed())
            print("CLEANDATA", adults_formset.cleaned_data)
            for f in adults_formset:
                cd = f.cleaned_data
                print(cd)  # TODO
            print("CLEAN C")  # TODO
            # print(children_formset.cleaned_data)
            print("RP")  # TODO
            print(request.POST)
            return render(request, "booking/index.html")   # TODO
            create_records(request.POST)

        else:
            # TODO
            fetch_all_errors = adults_formset.non_form_errors()
            print("ANYERRORS", fetch_all_errors)
            for each_error in fetch_all_errors:
                print("ERR", each_error)
                messages.add_message(request, messages.ERROR,
                                     each_error)
            # print("D", children_formset.errors,
            #       children_formset.non_form_errors())  # TODO
            # fetch_all_errors = children_formset.non_form_errors()
            for each_error in fetch_all_errors:
                print("ERR", each_error)
                messages.add_message(request, messages.ERROR,
                                     each_error)
            adults_formset = AdultsFormSet(request.POST or None,
                                           prefix="adult")
            # children_formset = ChildrenFormSet(request.POST or None,
            #                                    prefix="child")
            context = {}
            context["adults_formset"] = adults_formset
            context["children_formset"] = children_formset
            print(type(Common.save_context))
            print("TT", Common.save_context)
            context["hidden_form"] = Common.save_context["hidden_form"]
            # print("AF3", adults_formset.cleaned_data)
            print("CON", context)
            print("SAVED_CONTEXT", Common.save_context)

    else:
        # request.method is == "GET"
        print("EX", Common.save_context.booking.adults)
        number_of_adults = Common.save_context.booking.adults
        adults_formset = AdultsFormSet(request.POST or None,
                                       prefix="adult",
                                       extra=number_of_adults)
        # children_formset = ChildrenFormSet(request.POST or None,
        #                                        prefix="child")
        children_formset = []

        # TODO
        pass

    #  #context = {"form": form} TODO
    return render(request, "booking/passenger-details-form.html", context)


def view_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    print("BOOKING:", booking)  # PK/ID   TODO
    print("ID", id)
    print("PNR", booking.pnr)
    # context = {"booking": booking}
    # qs = Passenger.objects.filter(booking=b)
    qs = Passenger.objects.filter(pnr_id=id).order_by("pax_type",
                                                      "pax_order_number")
    print(qs)  # TODO
    print(len(qs))
    passenger_list = []
    for pax_record in qs:  # TODO
        print(type(pax_record))
        print(pax_record.pax_type, pax_record.pax_order_number)
        passenger_list.append(pax_record)
    #  print(type(passenger_list)) #  TODO
    context = {"booking": booking, "passengers": passenger_list}
    # print(pax.title, pax.last_name, pax.last_name) TODO
    return render(request, "booking/view-booking.html", context)


def search_bookings(request):
    query = request.GET.get("query")
    # Blank Search
    if not query:
        return HttpResponseRedirect(reverse("home"))

    # TODO

    # Each Booking must has one Principal Passenger
    # That Passenger must be the first mentioned (pax_order_number=1)
    # and an Adult (pax_type="A")

    # Every Booking has 'one' Principal Passenger
    # Adult 1 - query that Passenger i.e.
    # pax_type == "A" and pax_order_number == 1
    adult1_qs = Passenger.objects.filter(pnr=OuterRef("id"),
                                         pax_type="A",
                                         pax_order_number=1)

    # Case Insensitive Search - in 3 parts

    queryset = (Booking.objects.filter(
                # 1) Matching PNR
                Q(pnr__icontains=query) | (

                 # 2) Or Matching Principal Passenger's First Name
                 Q(passenger__first_name__icontains=query) &
                 Q(passenger__pax_type__exact="A") &
                 Q(passenger__pax_order_number=1)) | (

                 # 3) Or Matching Principal Passenger's Last Name
                 Q(passenger__last_name__icontains=query) &
                 Q(passenger__pax_type__exact="A") &
                 Q(passenger__pax_order_number=1)))

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
                                      pax_type="A",
                                      pax_order_number=1)
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
        # CREATE MESSAGE TODO

    return render(request, "booking/edit-booking.html", context)


def create_records(request):

    # For now use a random number - TODO
    booking = Booking()
    # print("BOOKING", booking)  # TODO
    random_string = str(random.randrange(100, 1000))  # 3 digits TODO
    pnr = "SMI" + random_string
    print(pnr)  # TODO
    booking.pnr = pnr
    booking.flight_from = "LCY"
    booking.flight_to = "IOM"
    # 'return_flight' = either True or False.
    booking.return_flight = True if request["return_option"] == "Y" else False
    # TODO
    # Outbound Date & Flight No (e.g. MX0485)
    booking.outbound_date = datetime.now()  # TODO
    booking.outbound_flightno = "MX485"
    # Inbound  Date & Flight No (e.g. MX0486)
    # Note: this is optional in the case of a One-Way Journey
    booking.inbound_date = datetime.now()  # TODO
    booking.inbound_flightno = "MX486"
    booking.ticket_class = "Y"
    booking.cabin_class = "Y"
    number_of_adults = int(request["adults"])
    number_of_children = int(request["children"])
    number_of_infants = int(request["infants"])
    booking.number_of_pax = number_of_adults + number_of_children
    booking.number_of_infants = number_of_infants
    booking.number_of_bags = 0
    booking.departure_time = "0800"
    booking.arrival_time = "0930"
    booking.remarks = ""  # TODO
    # TODO
    # Booking.objects.filter(pk=1).delete()
    booking.save()
    adhoc_date = date(2005, 7, 27)  # TODO
    # Create the Passenger Records - 2 adhoc recs - TODO
    for i in range(2):
        print("ISCORE=", i)
    for i in range(2):
        # TODO
        pax = Passenger(title="MR",
                        first_name="JOE",
                        last_name="BLOGGS",
                        pax_type="A",
                        pax_order_number=i+1,  # TODO
                        # TODO CAN BE NULL FOR ADULTS
                        date_of_birth=adhoc_date,
                        contact_number="123456",
                        contact_email="test@email.com",
                        seat_number=i,  # TODO
                        status=f"HK{i + 1}",
                        ticket_class="Y",
                        pnr=booking)
        pax.save()
        print("I=", i, pax)  # TODO

        # RETURN TO HOME PAGE =  # TODO: SHOW MESSAGE
        return HttpResponseRedirect(reverse("home"))
