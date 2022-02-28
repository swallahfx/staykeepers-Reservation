from django.urls import path
from reservations.views import Booking, SearchBooking

urlpatterns = [      
    path('book/', Booking.as_view(), name='room-listings'),           
    path('units/', SearchBooking.as_view(), name='search'),           
  ]