from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import BookingForm, CreateBookingForm, PassengerDetailsForm
from .forms import AdultsForm, MinorsForm
from django.forms import formset_factory
# TODO
from .forms import BasePaxFormSet, PaxForm
from .models import Booking


# Create your views here.

# Display the Home Page


def homepage(request):
    return render(request, 'booking/index.html')


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

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateBookingForm(request.POST)
        # check whether it's valid:
        # TODO
        if form.is_valid():
            PaxFormSet = formset_factory(PaxForm, formset=BasePaxFormSet,
                                         extra=0)
            formset = PaxFormSet()
            # TODO 'form'
            context = {'booking': form.cleaned_data, 'form': form.cleaned_data,
                       'range': range(form.cleaned_data['adults']),
                       'range3': range(3),
                       'formset': formset}
            # TODO
            AdultsFormSet = formset_factory(AdultsForm)
            for form in AdultsFormSet(prefix='adult'):
                 print(form.as_p())
            ChildrenFormSet = formset_factory(MinorsForm)
            for form in ChildrenFormSet(prefix='child'):
                 print(form.as_p())
            context['adults_formset'] = AdultsFormSet
            context['children_formset'] = ChildrenFormSet

            return render(request, 'booking/passenger-details-form.html',
                          context)

        else:
            # TODO
            for field in form.errors:
                messages.add_message(request, messages.ERROR, "MESSAGE")
                for field in form.errors:
                    for item in form.errors[field]:
                        message_string = f"{field} - {item}"
                        messages.add_message(request, messages.ERROR,
                                             message_string)

    else:
        form = CreateBookingForm()

    context = {'form': form}
    return render(request, 'booking/create-booking-form.html', context)


def view_booking(request, id):
    booking = get_object_or_404(Booking, pk=id)
    context = {'booking': booking}
    return render(request, 'booking/view-booking.html', context)


def search_bookings(request):
    query = request.GET.get('query')
    # Blank Search
    if not query:
        return HttpResponseRedirect(reverse('home'))

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
                .order_by('company_name'))
    if queryset.count() == 0:
        # No Matching Bookings Found
        context = {'query': query}
        return render(request, 'booking/no-matches.html', context)

    # Pagination as demonstrated in
    # https://testdriven.io/blog/django-pagination/

    # 3 records per page
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get('page', 1)

    try:
        page_object = paginator.page(page_number)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_object = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_object = paginator.page(paginator.num_pages)

    context = {'queryset': queryset, 'query': query,
               'page_object': page_object}
    return render(request, 'booking/search-bookings.html', context)


def delete_booking(request, id):
    booking = get_object_or_404(Employer, pk=id)
    context = {'booking': booking}

    if request.method == 'POST':
        booking.delete()
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'booking/delete-booking.html', context)


def edit_booking(request, id):
    booking = get_object_or_404(Employer, pk=id)
    form = BookingForm(instance=booking)
    context = {'booking': booking, 'form': form}
    if request.method == 'POST':

        # Update Booking() with the new values

        booking.company_name = request.POST.get('company_name')
        booking.number_of_employees = request.POST.get('number_of_employees')
        # employer_test_flag will either be set to "on" or None
        # Handle it so that it is either "on" or False
        new_employer_test_flag = request.POST.get('employer_test_flag', False)
        # 'employer_test_flag' -  convert "on" value to either True or False.']
        booking.employer_test_flag = (True if new_employer_test_flag == 'on'
                                      else False)

        booking.save()
        return HttpResponseRedirect(reverse('view-booking',
                                            kwargs={'id': booking.pk}))

    return render(request, 'booking/edit-booking.html', context)


# TODO
def passenger_details_form(request):
    print("REQ", request)
    # form = CreateBookingForm()
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

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateBookingForm(request.POST)
        # check whether it's valid:
        # TODO
        if form.is_valid():
            print("YES1")
            return render(request, 'booking/passenger-details-form.html',
                          context)

        else:
            # TODO
            for field in form.errors:
                messages.add_message(request, messages.ERROR, "MESSAGE")
                for field in form.errors:
                    for item in form.errors[field]:
                        message_string = f"{field} - {item}"
                        messages.add_message(request, messages.ERROR,
                                             message_string)

    else:
        # TODO
        # form = PassengerDetailsForm(3)
        pass

    context = {'form': form}
    return render(request, 'booking/create-booking-form.html', context)
