from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('create/', views.create_booking, name='create-booking'),
    path('booking/<id>/', views.view_booking, name='view-booking'),
]