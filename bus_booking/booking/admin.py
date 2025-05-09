from django.contrib import admin
from .models import Bus, Seat

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 10  # You can adjust how many seats show up to be added

class BusAdmin(admin.ModelAdmin):
    inlines = [SeatInline]
    list_display = ['name', 'departure', 'destination', 'date', 'time']

admin.site.register(Bus, BusAdmin)
admin.site.register(Seat)
