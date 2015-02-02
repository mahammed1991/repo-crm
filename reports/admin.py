from django.contrib import admin
from reports.models import Region


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_list')

admin.site.register(Region, RegionAdmin)
