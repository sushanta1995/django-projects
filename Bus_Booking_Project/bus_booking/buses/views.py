from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Bus, Booking
from .forms import BusForm

def admin_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_superuser)(view_func))

def home(request):
    buses = Bus.objects.all()
    return render(request, 'buses/home.html', {'buses': buses})

@admin_required
def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BusForm()
    return render(request, 'buses/add_bus.html', {'form': form})

@admin_required
def update_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BusForm(instance=bus)
    return render(request, 'buses/update_bus.html', {'form': form})

@admin_required
def delete_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == 'POST':
        bus.delete()
        return redirect('home')
    return render(request, 'buses/delete_confirm.html', {'bus': bus})

@login_required
def book_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.user.is_superuser:
        messages.error(request, "Admin can't book buses.")
        return redirect('home')

    if bus.seats_available > 0:
        Booking.objects.create(user=request.user, bus=bus)
        bus.seats_available -= 1
        bus.save()
        messages.success(request, f'You booked {bus.name} successfully!')
    else:
        messages.error(request, 'No seats available.')
    return redirect('home')

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related('bus')
    return render(request, 'buses/booking_history.html', {'bookings': bookings})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'buses/signup.html', {'form': form})
