from django import forms
from reports.models import Region
from django.core.exceptions import ValidationError


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region

    def clean(self):
        super(RegionForm, self).clean()
        location = self.cleaned_data.get('location')
        name = self.cleaned_data.get('name')
        # grp_name = Region.objects.filter(name=name)
        # loc = Region.objects.filter(location=location)

        other_region_locations_ids = Region.objects.exclude(name=name).values_list('location')
        current_region_locations = [(loc1.id, ) for loc1 in location]

        common_location = set(other_region_locations_ids) & set(current_region_locations)
        if len(common_location) != 0:
            raise ValidationError('This location is already in use')

        # if loc:
        #     raise ValidationError('This location is already in use')

        # if grp_name:
        #     raise ValidationError('This name is already in use')
        return self.cleaned_data
