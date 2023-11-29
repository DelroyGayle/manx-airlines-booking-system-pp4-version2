from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('create/', views.create_booking_form, name='create-booking-form'),
    path('confirm/', views.confirm_booking_form, name='confirm-booking-form'),
    path('booking/<id>/', views.view_booking, name='view-booking'),
    path('search/', views.search_bookings, name='search-bookings'),
    path('delete/<id>/', views.delete_booking, name='delete-booking'),
    path('edit/<id>/', views.edit_booking, name='edit-booking'),
    path('details/', views.passenger_details_form,
         name='passenger-details-form'),
    path('changes/', views.confirm_changes_form, name='confirm-changes-form'),
    path('logout_user', views.logout_user, name='logout_user')
]
