from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import BookingForm
from .forms import InputForm
from .models import Booking

# Create your views here.

# Display the Home Page


def homepage(request):
    return render(request, 'booking/index.html')


def create_booking(request):
    form = InputForm()
    context = {'form': form}

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

    return render(request, 'booking/create-booking.html', context)


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
