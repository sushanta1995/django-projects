from django import forms
from .models import Bus

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['name', 'source', 'destination', 'seats_available', 'departure_time']
        widgets = {
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
        }