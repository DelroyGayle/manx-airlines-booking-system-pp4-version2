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
from .forms import BagRemarks

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import random  # TODO
import re

from .common import Common
# TODO
# from .constants import FIRSTNAME_BLANK
# KEEP THIS - TODO
# import constants
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
                  "mandatory for this Passenger. "
                  "Enter passenger's phone number and/or email.")
BAD_TELNO = "Enter a phone number of at least six digits."
BAD_EMAIL = "Enter a valid email address."
BAD_DATE = "Enter a valid date of birth."
FUTURE_DATE = "Your date of birth must be in the past."
TOO_YOUNG = ("Newly born infants younger than 14 days "
             " on the {0} will not be accepted for travel.")


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
# def adults_formset_validated(cleaned_data, request):

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

    return True


def date_validation_part2(accum_dict, errors_found,
                          date_of_birth, is_child):
    """ Handles the date validation for children and infants """

    todays_date = datetime.now().date()
    # datediff = date_of_birth - todays_date

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

    # Yes - Check the D.O.B. against the Return Date
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


def all_formsets_valid(request, adults_formset,
                       children_included, children_formset,
                       infants_included, infants_formset):
    """
    Carry out validation on up to three formsets
    1) Adults
    2) Children
    3) Infants

    They differ slightly:
    Adults have contact telephone/email
    Children/Infants have the Date of Birth - no contact details
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
        return False

    # Are the forms blank?
    is_empty = False

    # ADULTS
    cleaned_data = adults_formset.cleaned_data
    if not any(cleaned_data):
        is_empty = True
        messages.add_message(request, messages.ERROR,
                             "Enter the Adult's Passenger Details "
                             "for this booking.")

    # CHILDREN
    if children_included:
        cleaned_data = children_formset.cleaned_data
        if not any(children_formset.cleaned_data):
            is_empty = True
            messages.add_message(request, messages.ERROR,
                                 "Enter the Child's Passenger Details "
                                 "for this booking.")
    if is_empty:
        return False

    # INFANTS
    if infants_included:
        cleaned_data = infants_formset.cleaned_data
        if not any(infants_formset.cleaned_data):
            is_empty = True
            messages.add_message(request, messages.ERROR,
                                 "Enter the Infant's Passenger Details "
                                 "for this booking.")
    if is_empty:
        return False

    # Validate all three formsets
    if not adults_formset_validated(adults_formset.cleaned_data, request):
        return False

    if (children_included and
        not minors_formset_validated(children_formset.cleaned_data,
                                     True, request)):
        return False

    if (infants_included and
        not minors_formset_validated(infants_formset.cleaned_data,
                                     False, request)):
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
        for field in form.errors:
            for item in form.errors[field]:
                message_string = Common.format_error(f"{field} - {item}")
                message_error(message_string, request)

        return False

    # FURTHER VALIDATION NEEDED
    # Check Dates and Flight Availability
    cleaned_data = form.cleaned_data
    if (cleaned_data["return_option"] == "Y" and
            cleaned_data["returning_date"] == cleaned_data["departing_date"]):
        # Same Day Travel - Is there enough time between journey times?
        thetime = cleaned_data["departing_time"]
        departPos = Common.OUTBOUND_TIME_OPTIONS1.index(thetime)
        thetime = cleaned_data["returning_time"]
        returnPos = Common.INBOUND_TIME_OPTIONS1.index(thetime)
        if departPos > returnPos:
            message_error("Returning Time - The time of the return flight "
                          "cannot be in the past.",
                          request)
            return False

        if departPos == returnPos:
            message_error(
                "Returning Time - The interval between flights cannot be "
                "less than 90 minutes.", request)
            return False

    # The Form's contents has passed all validation checks!
    return True


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
        if is_booking_form_valid(form, request):
            context = {"booking": form.cleaned_data, "form": form.cleaned_data,
                       # TODO HAVE IT TWICE?
                       "booking_cleaned_data": form.cleaned_data,
                       }

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
            bag_remarks_form = BagRemarks(prefix="bagrem")
            context["adults_formset"] = adults_formset
            context["children_formset"] = children_formset
            context["children_included"] = children_included
            context["infants_formset"] = infants_formset
            context["infants_included"] = infants_included
            context["hidden_form"] = hiddenForm
            context["bag_remarks_form"] = bag_remarks_form

            # Save a copy in order to fetch any values as and when needed
            Common.save_context = context
            return render(request, "booking/passenger-details-form.html",
                          context)

            # CREATE SUCCESS MESSAGE TODO

        else:
            # The Booking Form has failed validation
            form = CreateBookingForm(request.POST)

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)


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

    context["hidden_form"] = Common.save_context["hidden_form"]
    context["bag_remarks_form"] = Common.save_context["bag_remarks_form"]
    context["hidden_form"] = Common.save_context["hidden_form"]
    # TODO
    print("CON", context)
    print("SAVED_CONTEXT", Common.save_context)

    return context


# TODO
def passenger_details_form(request):
    """
    The Handling of the Passenger Details Form
    This form consists of three formsets:
    1) AdultsForm - class AdultsForm
    2) ChildrenFormSet - Class MinorsForm
    2) InfantsFormSet - Class MinorsForm
    followed by the BagRemarks Form
    Therefore, this method processes the validation
    of all 3 form types.
    """

    print("REQ", request.method)  # TODO
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

    bag_remarks_form = BagRemarks(request.POST or None, prefix="bagrem")
    print(request.method, "CONTEXT FETCH",
          children_included, request.POST)  # TODO
    print(context)

    if request.method == "POST":
        context = request.POST
        # TODO
        # if bag_remarks_form.is_valid:
        #     print("YES")
        #     print(bag_remarks_form.cleaned_data)
        if all_formsets_valid(request,
                              adults_formset,
                              children_included,
                              children_formset,
                              infants_included,
                              infants_formset):
            # TODO: CREATE THE RECORD!!
            return render(request, "booking/index.html")
            create_records(request.POST)

        else:
            context = initialise_formset_context(request)
            #  TODO
            print(type(Common.save_context))
            print("TT", Common.save_context)
            print("CON", context)
            print("SAVED_CONTEXT", Common.save_context)

    else:
        # request.method is "GET"
        number_of_adults = Common.save_context["booking"]["adults"]
        context = initialise_formset_context(request)

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
        # CREATE SUCCESS MESSAGE TODO

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
