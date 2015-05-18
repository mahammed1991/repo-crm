from django import forms
from leads.models import Location
from django.core.exceptions import ValidationError


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location

    def clean(self):
        """
        Checks that all data is valid.
        """
        ds_time_zones = self.cleaned_data.get('ds_time_zone')
        if not ds_time_zones:
            raise ValidationError("Please provide daylight timezones, because you given daylight start and end date")
        return self.cleaned_data
