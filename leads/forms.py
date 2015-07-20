from django import forms
from leads.models import Location, LeadFormAccessControl
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


class LeadFormAccessControlAdminForm(forms.ModelForm):
    class Meta:
        model = LeadFormAccessControl

    def clean(self):
        """
        validates the fields
        """
        lead_form = self.cleaned_data.get('lead_form')
        programs = self.cleaned_data.get('programs')
        target_location = self.cleaned_data.get('target_location')
        google_rep = self.cleaned_data.get('google_rep')

        if len(google_rep) is 0:
            if len(programs) is 0:
                raise ValidationError('Select Programs and Target Location or Google rep to save the Lead Form Access Control')
            elif len(target_location) is 0:
                raise ValidationError('Select Programs and Target Location or Google rep to save the Lead Form Access Control')
        else:
            if len(programs) is not 0 and len(target_location) is not 0:
                pass
            elif len(programs) is 0 and len(target_location) is 0:
                pass
            else:
                raise ValidationError('Select Programs and Target Location or Google rep to save the Lead Form Access Control')

        existing_lead_form_access_controls = LeadFormAccessControl.objects.exclude(lead_form=lead_form).filter(programs__in=programs, target_location__in=target_location)
        if len(existing_lead_form_access_controls) > 0:
            raise ValidationError('Selected Programs and Target Locations are already mapped in Other Lead Form Access Control')

        existing_lfac_with_rep = LeadFormAccessControl.objects.exclude(lead_form=lead_form).filter(google_rep__in=google_rep)
        if len(existing_lfac_with_rep) > 0:
            raise ValidationError('Selected Google Rep is already mapped in Other Lead Form Access Control')

        return self.cleaned_data
