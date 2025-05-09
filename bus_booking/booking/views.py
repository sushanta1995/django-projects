from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus, Seat
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bus, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


@login_required
def list_buses(request):
    buses = Bus.objects.all()
    return render(request, 'booking/bus_list.html', {'buses': buses})

@login_required
def view_seats(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    seats = Seat.objects.filter(bus=bus)

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = Seat.objects.get(id=seat_id)
        if not seat.is_booked:
            seat.is_booked = True
            seat.save()
            messages.success(request, f"Seat {seat.seat_number} booked successfully!")
            return redirect('list_buses')
        else:
            messages.error(request, "This seat is already booked.")

    return render(request, 'booking/seat_list.html', {'bus': bus, 'seats': seats})

@login_required
def view_seats(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    seats = Seat.objects.filter(bus=bus)

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = Seat.objects.get(id=seat_id)

        if not seat.is_booked:
            # Update seat status
            seat.is_booked = True
            seat.save()

            # Save booking
            booking = Booking.objects.create(user=request.user, seat=seat)

            # Trigger Celery email task
            #send_booking_confirmation_email.delay(request.user.email, bus.name, seat.seat_number)

            messages.success(request, f"Seat {seat.seat_number} booked successfully!")
            return redirect('list_buses')
        else:
            messages.error(request, "This seat is already booked.")

    return render(request, 'booking/seat_list.html', {'bus': bus, 'seats': seats})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    bus = booking.seat.bus
    seats = Seat.objects.filter(bus=bus, is_booked=False)

    if request.method == 'POST':
        new_seat_id = request.POST.get('seat_id')
        new_seat = get_object_or_404(Seat, id=new_seat_id, bus=bus)

        # Free old seat
        booking.seat.is_booked = False
        booking.seat.save()

        # Book new seat
        new_seat.is_booked = True
        new_seat.save()

        # Update booking
        booking.seat = new_seat
        booking.save()

        messages.success(request, f"Your booking has been updated to seat {new_seat.seat_number}.")
        return redirect('my_bookings')

    return render(request, 'booking/update_booking.html', {'booking': booking, 'seats': seats})