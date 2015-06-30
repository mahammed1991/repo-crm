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
        daylight_start = self.cleaned_data.get('daylight_start')
        daylight_end = self.cleaned_data.get('daylight_end')
        if daylight_start and daylight_end:
            if not ds_time_zones:
                raise ValidationError("Please provide daylight timezones, because you given daylight start and end date")
        return self.cleaned_data
