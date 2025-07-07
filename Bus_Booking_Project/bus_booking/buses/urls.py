from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-bus/', views.add_bus, name='add_bus'),
    path('update-bus/<int:bus_id>/', views.update_bus, name='update_bus'),
    path('delete-bus/<int:bus_id>/', views.delete_bus, name='delete_bus'),
    path('book/<int:bus_id>/', views.book_bus, name='book_bus'),
    path('my-bookings/', views.booking_history, name='booking_history'),
    path('signup/', views.signup_view, name='signup'),
]
