from django import forms
from main.models import OlarkChatGroup
from django.core.exceptions import ValidationError


class OlarkChatGroupForm(forms.ModelForm):
    class Meta:
        model = OlarkChatGroup

    def clean(self):

        operator_group = self.cleaned_data.get('operator_group')
        programs = self.cleaned_data.get('programs')
        target_location = self.cleaned_data.get('target_location')
        google_rep = self.cleaned_data.get('google_rep')
        olark_script = self.cleaned_data.get('olark_script')

        if len(google_rep) is 0:
            if len(programs) is 0:
                raise ValidationError('Select Programs and Target Location or Google rep to save the valid Chat Group')
            elif len(target_location) is 0:
                raise ValidationError('Select Programs and Target Location or Google rep to save the valid Chat Group')
        else:
            if len(programs) is not 0 and len(target_location) is not 0:
                pass
            elif len(programs) is 0 and len(target_location) is 0:
                pass
            else:
                raise ValidationError('Select Programs and Target Location or Google rep to save the valid Chat Group')

        exist_group_with_pgm_loc = OlarkChatGroup.objects.exclude(operator_group=operator_group).filter(programs__in=programs, target_location__in=target_location)
        if len(exist_group_with_pgm_loc) > 0:
            raise ValidationError('Selected Programs and Target Locations are already mapped in olark Chat Gruop')

        exist_group_with_ldap = OlarkChatGroup.objects.exclude(operator_group=operator_group).filter(google_rep__in=google_rep)
        if len(exist_group_with_ldap) > 0:
            raise ValidationError('Selected Google Rep is already mapped in olark Chat Gruop')

        exist_group_with_script = OlarkChatGroup.objects.exclude(operator_group=operator_group).filter(olark_script=olark_script)
        if len(exist_group_with_script) > 0:
            raise ValidationError('Entered Olark Script is already mapped in olark Chat Gruop')

        return self.cleaned_data
