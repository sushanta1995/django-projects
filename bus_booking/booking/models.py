from django.db import models
from django.conf import settings

class Bus(models.Model):
    name = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.departure} to {self.destination} on {self.date}"

class Seat(models.Model):
    bus = models.ForeignKey(Bus, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bus.name} - Seat {self.seat_number}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.seat}"