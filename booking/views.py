from django.shortcuts import render

# Create your views here.


# Display the Home Page
def homepage(request):
    return render(request, 'booking/index.html')


def create_booking(request):
    return render(request, 'booking/create-booking.html')