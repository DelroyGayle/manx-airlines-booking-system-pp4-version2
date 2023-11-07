from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BookingForm
from .models import Employer

# Create your views here.


# Display the Home Page
def homepage(request):
    return render(request, 'booking/index.html')


def create_booking(request):
    form = BookingForm()
    context = {'form': form}

    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        number_of_employees = request.POST.get('number_of_employees')
        # employer_test_flag will either be set to "on" or None
        # Handle it so that it is either "on" or False
        employer_test_flag = request.POST.get('employer_test_flag', False)
        
        new_employer = Employer()

        new_employer.company_name = company_name
        new_employer.number_of_employees = number_of_employees
        # 'employer_test_flag' -  convert "on" value to either True or False.']
        new_employer.employer_test_flag = True if employer_test_flag == 'on' else False
        new_employer.save()

        return HttpResponseRedirect(reverse('view-booking', kwargs={'id': new_employer.pk}))
            
    return render(request, 'booking/create-booking.html', context)


def view_booking(request, id):
    booking = get_object_or_404(Employer, pk=id)
    context = {'booking': booking}
    return render(request, 'booking/view-booking.html', context)


def search_bookings(request):
    query = request.GET.get('query')
    # Blank Search
    if not query:
        return render(request, 'booking/index.html')

    # Case Insensitive Search
    queryset = Employer.objects.filter(company_name__icontains=query).order_by('company_name')
    context = {'queryset': queryset, 'query':query}
            
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
        booking.employer_test_flag = True if new_employer_test_flag == 'on' else False

        booking.save()
        return HttpResponseRedirect(reverse('view-booking', kwargs={'id': booking.pk}))

    return render(request, 'booking/edit-booking.html', context)
