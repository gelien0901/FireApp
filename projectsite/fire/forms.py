from django import forms
from .models import FireStation, Incident, Locations

class FireStationForm(forms.ModelForm):
    class Meta:
        model = FireStation
        fields = ['name', 'latitude', 'longitude', 'address', 'city', 'country']

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['location', 'date_time', 'severity_level', 'description']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = ['name', 'latitude', 'longitude', 'address', 'city', 'country']