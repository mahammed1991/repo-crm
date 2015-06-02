from django.contrib import admin
from representatives.models import Availability, ScheduleLog


class AvailabilityAdmin(admin.ModelAdmin):

    list_display = ('availability_count', 'booked_count', 'date_in_utc', 'team', )

admin.site.register(Availability, AvailabilityAdmin)


class ScheduleLogAdmin(admin.ModelAdmin):

    def availability_link(self, obj):
        return u"<a href='../availability/%d/'>View</a>" % obj.availability.id
    availability_link.allow_tags = True
    availability_link.short_description = "Avalability"

    list_display = ('user', 'availability_link', 'availability_count', 'booked_count', 'created_date')

admin.site.register(ScheduleLog, ScheduleLogAdmin)
