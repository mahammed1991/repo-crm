from django.contrib import admin
from leads.models import Leads, Timezone, RegalixTeams, Location, Team, CodeType, Language, LeadForm, LeadFormAccessControl


class LeadsAdmin(admin.ModelAdmin):
    list_display = ('google_rep_name', 'lead_owner_name', 'lead_owner_email', 'first_name', 'last_name',
                    'company', 'lead_status', 'team', 'type_1', 'date_of_installation', 'appointment_date', 'first_contacted_on', 'tat')

admin.site.register(Leads, LeadsAdmin)


class TimezoneAdmin(admin.ModelAdmin):
    list_display = ('zone_name', 'time_value')

admin.site.register(Timezone, TimezoneAdmin)


class RegalixTeamsAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'location_list', 'process_type')
    filter_horizontal = ('location',)

admin.site.register(RegalixTeams, RegalixTeamsAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'timezone_list', 'primary_language',
                    'secondary_language_list', 'flag_image', 'phone', 'is_active')
    filter_horizontal = ('time_zone', 'language')

admin.site.register(Location, LocationAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'is_active',)

admin.site.register(Team, TeamAdmin)


class CodeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

admin.site.register(CodeType, CodeTypeAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language_name', 'is_active',)

admin.site.register(Language, LanguageAdmin)


class LeadFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)

admin.site.register(LeadForm, LeadFormAdmin)


class LeadFormAccessControlAdmin(admin.ModelAdmin):
    list_display = ('lead_form', 'program_list', 'location_list', 'rep_list',)
    filter_horizontal = ('programs', 'target_location', 'google_rep')

admin.site.register(LeadFormAccessControl, LeadFormAccessControlAdmin)
