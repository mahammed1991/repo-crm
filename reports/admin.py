from django.contrib import admin
from reports.models import Region, QuarterTargetLeads


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_list')

admin.site.register(Region, RegionAdmin)


class QuarterTargetLeadsAdmin(admin.ModelAdmin):
    list_display = ('program', 'location', 'quarter', 'year', 'target_leads')

admin.site.register(QuarterTargetLeads, QuarterTargetLeadsAdmin)
