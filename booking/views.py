from django.shortcuts import render
from .forms import BookingForm

# Create your views here.


# Display the Home Page
def homepage(request):
    return render(request, 'booking/index.html')


def create_booking(request):
    form = BookingForm()
    context = {'form': form}
    print(context)
    return render(request, 'booking/create-booking.html', context)