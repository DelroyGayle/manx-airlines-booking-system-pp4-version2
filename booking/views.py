from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import BookingForm, CreateBookingForm, PassengerDetailsForm
# TODO PaxForm?
from .forms import AdultsForm, MinorsForm, PaxForm
from django.forms import formset_factory
# TODO BasePaxFormSet?
from .forms import BasePaxFormSet, HiddenForm
from .models import Booking, Passenger
from datetime import datetime
from datetime import date # TODO
import random # TODO


# Create your views here.

# Display the Home Page


def homepage(request):
    return render(request, "booking/index.html")


# TODO
def create_booking_form(request):
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
        # create a form instance and populate it with data from the request:
        form = CreateBookingForm(request.POST)
        # check whether it"s valid:
        # TODO
        if form.is_valid():
            PaxFormSet = formset_factory(PaxForm, formset=BasePaxFormSet,
                                         extra=0)
            formset = PaxFormSet()
            # TODO "form"
            print("CLEANED", form.cleaned_data)
            context = {"booking": form.cleaned_data, "form": form.cleaned_data,
                       "range": range(form.cleaned_data["adults"]),
                       "range3": range(3),
                       "formset": formset}
            # TODO
            AdultsFormSet = formset_factory(AdultsForm)
            adults_formset = AdultsFormSet(prefix="adult")
            # for form in adults_formset:
            #      print(form.as_p())
            ChildrenFormSet = formset_factory(MinorsForm)
            children_formset = ChildrenFormSet(prefix="child")
            # for form in children_formset:
            #      print(form.as_p())

            data = {
                "adults": 10,
                "children": 20
            }
            hiddenForm = HiddenForm(form.cleaned_data)
            # hiddenForm.adults = 10
            print(hiddenForm)
            print(form.cleaned_data)
            context["adults_formset"] = adults_formset
            context["children_formset"] = children_formset
            context["hidden_form"] = hiddenForm

            return render(request, "booking/passenger-details-form.html",
                          context)

        else:
            # TODO
            for field in form.errors:
                for field in form.errors:
                    for item in form.errors[field]:
                        message_string = f"{field} - {item}"
                        messages.add_message(request, messages.ERROR,
                                             message_string)

    else:
        form = CreateBookingForm()

    context = {"form": form}
    return render(request, "booking/create-booking-form.html", context)


def view_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    context = {"booking": booking}
    return render(request, "booking/view-booking.html", context)


def search_bookings(request):
    query = request.GET.get("query")
    # Blank Search
    if not query:
        return HttpResponseRedirect(reverse("home"))

    # Case Insensitive Search
    #   queryset = Employer.objects.filter(company_name__icontains=query)
    #               .order_by('company_name')
    #   queryset =
    #           Employer.objects.filter(employee__first_name__icontains=query)
    #                                   .order_by('company_name')
    #   queryset =
    #           Employer.objects.filter(employee__last_name__icontains=query)
    #                                   .order_by('company_name')
    queryset = (Employer.objects
                .filter(Q(company_name__icontains=query) |
                        Q(employee__first_name__icontains=query) |
                        Q(employee__last_name__icontains=query))
                .order_by("company_name"))
    if queryset.count() == 0:
        # No Matching Bookings Found
        context = {"query": query}
        return render(request, "booking/no-matches.html", context)

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
    booking = get_object_or_404(Employer, pk=id)
    context = {"booking": booking}

    if request.method == "POST":
        booking.delete()
        return HttpResponseRedirect(reverse("home"))

    return render(request, "booking/delete-booking.html", context)


def edit_booking(request, id):
    booking = get_object_or_404(Employer, pk=id)
    form = BookingForm(instance=booking)
    context = {"booking": booking, "form": form}
    if request.method == "POST":

        # Update Booking() with the new values

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

    return render(request, "booking/edit-booking.html", context)


def create_records(request):

        # For now use a random number
        booking = Booking()
        print("BOOKING", booking) # TODO        
        random_string = str(random.randrange(100,1000)) # 3 digits
        pnr = "SMI" + random_string
        print(pnr)
        booking.flight_from = "LCY"
        booking.flight_to = "IOM"
        # 'return_flight' = either True or False.
        booking.return_flight = True if request["return_option"] == "Y" else False

        # Outbound Date (YYYYMMDD) + Flight No (e.g. MX0485)
        # EG 'departing_date': ['2023-11-12']
        thedate = datetime.strptime(request["departing_date"], "%Y-%m-%d")
        thedate = thedate.strftime("%Y%m%d")
        booking.outbound = f"{thedate}MX485"

        thedate = datetime.strptime(request["returning_date"], "%Y-%m-%d")
        thedate = thedate.strftime("%Y%m%d")

        booking.inbound = f"{thedate}MX486"
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
        booking.principal_contact_number = "123456"
        booking.principal_email = "test@email.com"
        booking.remarks = ""
        print(booking) # TODO
        print(pnr)
        # TODO
        # Booking.objects.filter(pk=1).delete()
        booking.save()
        adhoc_date = date(2005, 7, 27) # TODO
# Create the Passenger Records - 2 adhoc recs - TODO
        for i in range(2):
             # TODO
            pax = Passenger(title="MR",
                            first_name="JOE",
                            last_name="BLOGGS",
                            pax_type="A",
                            date_of_birth=adhoc_date, #TODO CAN BE NULL FOR ADULTS
                            contact_number="123456",
                            contact_email="test@email.com",
                            seat_number=i, # TODO
                            status=f"HK{i + 1}",
                            ticket_class = "Y",
                            pnr = booking)
        pax.save()
        print(pax)

        # RETURN TO HOME PAGE = # TODO: SHOW MESSAGE
        return HttpResponseRedirect(reverse("home"))


# TODO
def passenger_details_form(request):
    print("REQ", request.method)
    # form = CreateBookingForm()
    # context = {'form': form}

    AdultsFormSet = formset_factory(AdultsForm)
    ChildrenFormSet = formset_factory(MinorsForm)
    adult_formset = AdultsFormSet(request.POST or None, request.FILES or None, prefix="adult")
    children_formset = ChildrenFormSet(request.POST or None, prefix="child")

    if request.method == "POST":
        # TODO
        # AdultsFormSet = formset_factory(AdultsForm)
        # ChildrenFormSet = formset_factory(MinorsForm)
        # adult_formset = AdultsFormSet(request.POST, request.FILES, prefix="adult")
        # children_formset = ChildrenFormSet(request.POST, request.FILES, prefix="child")
        print(adult_formset.is_valid(), children_formset.is_valid(), "WELL?")
        # print(100,children_formset)
        # print(200,children_formset.errors)
        # print(300,children_formset.non_form_errors)
        if adult_formset.is_valid() and children_formset.is_valid():
            print("CLEAN A")
            for f in adult_formset:
                cd = f.cleaned_data
                print(cd)
            print("CLEAN C")
            print(children_formset.cleaned_data)
            print("RP")
            print(request.POST)
  
            create_records(request.POST)

        else:
            # TODO
            for field in adult_formset.errors:
                if field:
                    print(adult_formset.errors)
                    message_string = adult_formset.errors
                    messages.add_message(request, messages.ERROR,
                                         message_string)
            messages.add_message(request, messages.ERROR,
                                 adult_formset.non_form_errors())
            print("D", children_formset.errors)
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
