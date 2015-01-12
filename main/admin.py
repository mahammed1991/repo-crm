from django.contrib import admin
from main.models import ContectList, CustomerTestimonials


class ContactAdmin(admin.ModelAdmin):
    list_display = ('position_type', 'first_name', 'last_name', 'email', 'phone_number', 'skype_id', 'region', 'profile_photo')

admin.site.register(ContectList, ContactAdmin)


class CustomerTestimonialsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'statement_text')

admin.site.register(CustomerTestimonials, CustomerTestimonialsAdmin)
