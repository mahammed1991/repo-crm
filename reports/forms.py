from django import forms
from reports.models import Region
from django.core.exceptions import ValidationError


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region

    def clean(self):
        location = self.cleaned_data.get('location')
        name = self.cleaned_data.get('name')
        grp_name = Region.objects.filter(name=name)
        loc = Region.objects.filter(location=location)
        if len(loc) > 0:
            raise ValidationError('This location is already in use')

        if len(grp_name) > 0:
            raise ValidationError('This name is already in use')
        return self.cleaned_data
