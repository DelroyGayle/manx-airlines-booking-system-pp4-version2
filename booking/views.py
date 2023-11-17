from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, OuterRef, Subquery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.forms import formset_factory

from .models import Booking, Passenger
from .forms import BookingForm, CreateBookingForm, PassengerDetailsForm
# TODO PaxForm?
from .forms import AdultsForm, MinorsForm, PaxForm
# TODO BasePaxFormSet?
from .forms import BasePaxFormSet
from .forms import HiddenForm
from .common import Common
from datetime import datetime
from datetime import date  # TODO
import random  # TODO
from .models import Flight


# Create your views here.

# Display the Home Page


def homepage(request):
    # On the first display of the Home Page
    # Initialise various settings
    if not Common.initialised:
        Common.initialisation()

    return render(request, "booking/index.html")


# TODO
def create_booking_form(request):

    if not Common.initialised:
        Common.initialisation()

    form = CreateBookingForm(request.POST or None)

    # form = CreateBookingForm1()
    # context = {'form': form}

    # if request.method == 'POST':
    #     company_name = request.POST.get('company_name')
    #     number_of_employees = request.POST.get('number_of_employees')
    #     # employer_test_flag will either be set to "on" or None
    #     # Handle it so that it is either "on" or False
    #     employer_test_flag = request.POST.get('employer_test_flag', False)

    #     new_employer = Employer()

    #     new_employer.company_name = company_name
    #     new_employer.number_of_employees = number_of_employees
    #     # 'employer_test_flag' -  convert "on" value
    #      to either True or False.']
    #
    #     new_employer.employer_test_flag = True if employer_test_flag == 'on'
    #     else False
    #     new_employer.save()

    #     return HttpResponseRedirect(reverse('view-booking',
    #            kwargs={'id': new_employer.pk}))

    if request.method == "POST":
        #  create a form instance and populate it with data from the request:
        #  form = CreateBookingForm(request.POST)
        # check whether it"s valid:
        # TODO
        if form.is_valid():
            PaxFormSet = formset_factory(PaxForm, extra=0)
            formset = PaxFormSet()
            # TODO "form"
            print("CLEANED", form.cleaned_data)
            print(100, formset)
            context = {"booking": form.cleaned_data, "form": form.cleaned_data,
                       "booking_cleaned_data": form.cleaned_data,
                       "range3": range(3),
                       "formset": formset}
            # TODO
            AdultsFormSet = formset_factory(AdultsForm, extra=2, formset=BasePaxFormSet)
            adults_formset = AdultsFormSet(prefix="adult")
            # for form in adults_formset:
            #      print(form.as_p()) # TODO
            ChildrenFormSet = formset_factory(MinorsForm, extra=2)
            children_formset = ChildrenFormSet(prefix="child")
            # for form in children_formset:
            #      print(form.as_p()) # TODO

            data = {
                "adults": 10,
                "children": 20
            }
            hiddenForm = HiddenForm(form.cleaned_data)
            # hiddenForm.adults = 10  # TODO
            print(hiddenForm)  # TODO
            # print(form.cleaned_data) TODO
            context["adults_formset"] = adults_formset
            context["children_formset"] = children_formset
            context["hidden_form"] = hiddenForm

            print("CONTEXT", context)
            return render(request, "booking/passenger-details-form.html",
                          context)

            # CREATE MESSAGE TODO

        else:
            # TODO
            print("CONTEXT/error", context)
            for field in form.errors:
                for item in form.errors[field]:
                    message_string = Common.format_error(f"{field} - {item}")
                    messages.add_message(request, messages.ERROR,
                                         message_string)
            # RERENDER
            form = CreateBookingForm(request.POST)

    else:
        # form = CreateBookingForm()
        pass  # TODO

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)



# TODO
def passenger_details_form(request):
    print("REQ", request.method)  # TODO
    # form = CreateBookingForm()  # TODO
    # context = {'form': form}

    AdultsFormSet = formset_factory(AdultsForm, extra=2, formset=BasePaxFormSet)
    ChildrenFormSet = formset_factory(MinorsForm, extra=2, formset=BasePaxFormSet)
    adult_formset = AdultsFormSet(request.POST or None, prefix="adult")
    children_formset = ChildrenFormSet(request.POST or None, prefix="child")
    print("CONTEXT FETCH", request.POST)

    if request.method == "POST":
        # TODO
        print(adult_formset.is_valid(), children_formset.is_valid(), "WELL?")
        if adult_formset.is_valid() and children_formset.is_valid():
            print("CLEAN A")  # TODO
            for f in adult_formset:
                cd = f.cleaned_data
                print(cd)  # TODO
            print("CLEAN C")  # TODO
            print(children_formset.cleaned_data)
            print("RP")  # TODO
            print(request.POST)

            create_records(request.POST)

        else:
            # TODO
            print("SEE", adult_formset.non_form_errors())
            for field in adult_formset.non_form_errors():
                print("ERR", field)
            for field in adult_formset.errors:
                if field:
                    print(adult_formset.errors)  # TODO
                    message_string = adult_formset.errors
                    messages.add_message(request, messages.ERROR,
                                         message_string)
            messages.add_message(request, messages.ERROR,
                                 adult_formset.non_form_errors())
            print("D", children_formset.errors)  # TODO
            for field in children_formset.errors:
                if field:
                    message_string = children_formset.errors
                    messages.add_message(request, messages.ERROR,
                                         message_string)
            messages.add_message(request, messages.ERROR,
                                 children_formset.non_form_errors())

    else:
        # TODO
        # form = PassengerDetailsForm(3)
        pass

    context = {"form": "form"}
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
    # print(pax.title, pax.first_name, pax.last_name) TODO
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
