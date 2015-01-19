from django.contrib import admin
from main.models import ContectList, CustomerTestimonials, UserDetails, Notification


class ContactAdmin(admin.ModelAdmin):
    list_display = ('position_type', 'first_name', 'last_name', 'email', 'phone_number', 'skype_id', 'region', 'profile_photo')

admin.site.register(ContectList, ContactAdmin)


class CustomerTestimonialsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'statement_text')

admin.site.register(CustomerTestimonials, CustomerTestimonialsAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'user_supporting_region', 'user_manager_name',
                    'user_manager_email', 'phone', 'team', 'location', 'profile_photo_url')

    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__username']

admin.site.register(UserDetails, UserDetailsAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_visible', )

admin.site.register(Notification, NotificationAdmin)
