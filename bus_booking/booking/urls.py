from django.urls import path
from . import views


urlpatterns = [
    path('buses/', views.list_buses, name='list_buses'),
    path('buses/<int:bus_id>/seats/', views.view_seats, name='view_seats'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('update-booking/<int:booking_id>/', views.update_booking, name='update_booking'),
]
