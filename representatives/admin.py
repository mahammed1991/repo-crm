from django.contrib import admin
from representatives.models import Availability, ScheduleLog
from django.db.models import Q
from lib.admin_helpers import CustomAdmin


class AvailabilityAdmin(admin.ModelAdmin):

    list_display = ('team', 'availability_count', 'booked_count', 'date_in_utc', )
    readonly_fields = ['availability_count', 'booked_count', 'date_in_utc', 'team']

    def get_readonly_fields(self, request, obj=None):
        return CustomAdmin.get_readonly_status(request, self.readonly_fields, obj)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = CustomAdmin.get_view_status(request, extra_context)
        return super(AvailabilityAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def queryset(self, request):
        qs = super(AvailabilityAdmin, self).queryset(request)
        return qs.filter(Q(team__team_lead=request.user.id) | Q(team__team_manager=request.user.id))


admin.site.register(Availability, AvailabilityAdmin)


class ScheduleLogAdmin(admin.ModelAdmin):

    def availability_link(self, obj):
        return u"<a href='../availability/%d/'>View</a>" % obj.availability.id
    availability_link.allow_tags = True
    availability_link.short_description = "Avalability"

    list_display = ('user', 'availability_link', 'availability_count', 'booked_count', 'created_date', 'description')
    readonly_fields = ['user', 'availability_link', 'availability_count', 'booked_count', 'created_date', 'description']

    def get_readonly_fields(self, request, obj=None):
        return CustomAdmin.get_readonly_status(request, self.readonly_fields, obj)

    def has_add_permission(self, request):
        return CustomAdmin.get_permission_status(request)

    def has_delete_permission(self, request, obj=None):
        return CustomAdmin.get_permission_status(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = CustomAdmin.get_view_status(request, extra_context)
        return super(ScheduleLogAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(ScheduleLog, ScheduleLogAdmin)
