from django.contrib import admin
from reports.models import Region, QuarterTargetLeads, CSATReport, CSATFilterDetails, KickOffProgram
from reports.forms import RegionForm


class RegionAdmin(admin.ModelAdmin):
    form = RegionForm
    list_display = ('name', 'location_list')
    filter_horizontal = ('location',)

admin.site.register(Region, RegionAdmin)


class QuarterTargetLeadsAdmin(admin.ModelAdmin):
    list_display = ('program', 'location', 'quarter', 'year', 'target_leads')

admin.site.register(QuarterTargetLeads, QuarterTargetLeadsAdmin)


class CSATReportAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'language', 'channel', 'category',)
    list_filter = ('category', 'language', 'channel', 'process')

admin.site.register(CSATReport, CSATReportAdmin)


class CSATFilterDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'lead_owners', 'channel', 'language_category', 'tagteam_location', 'process', 'survey_pin_number')
    list_filter = ('channel', 'language_category', 'tagteam_location', 'process')
    filter_horizontal = ('agent_language',)

admin.site.register(CSATFilterDetails, CSATFilterDetailsAdmin)
admin.site.register(KickOffProgram)
