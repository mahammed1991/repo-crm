from django.contrib import admin
from leads.models import Leads, Timezone, RegalixTeams, Location


class LeadsAdmin(admin.ModelAdmin):
    list_display = ('google_rep_name', 'lead_owner_name', 'lead_owner_email', 'first_name', 'last_name',
                    'company', 'lead_status', 'team', 'type_1', 'date_of_installation', 'appointment_date', 'first_contacted_on')

admin.site.register(Leads, LeadsAdmin)


class TimezoneAdmin(admin.ModelAdmin):
    list_display = ('zone_name', 'time_value')

admin.site.register(Timezone, TimezoneAdmin)


class RegalixTeamsAdmin(admin.ModelAdmin):
    list_display = ('team_name',)
    filter_horizontal = ('location',)

admin.site.register(RegalixTeams, RegalixTeamsAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name',)
    filter_horizontal = ('time_zone',)

admin.site.register(Location, LocationAdmin)
