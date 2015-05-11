from django.contrib import admin
from umm.models import UmmDailyTracker, QualityFeedbackForm, UmmCallData


class UmmDailyTrackerAdmin(admin.ModelAdmin):
    list_display = ('ldap', 'name', 'days_worked', 'days_out_of_office', 'uaa_target',
                    'uaa_achieved', 'pts_target', 'pts_won', 'region', 'created_date', 'updated_date')

admin.site.register(UmmDailyTracker, UmmDailyTrackerAdmin)


class QualityFeedbackFormAdmin(admin.ModelAdmin):
    list_display = ('ldap', 'date_of_review', 'feedback_notes', 'final_score')

admin.site.register(QualityFeedbackForm, QualityFeedbackFormAdmin)


class UmmCallDataAdmin(admin.ModelAdmin):
    list_display = ('ldap', 'umm_call_date', 'extn_out_call', 'total_call_time')

admin.site.register(UmmCallData, UmmCallDataAdmin)
