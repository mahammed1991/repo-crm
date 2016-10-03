from django.db import models


class UmmDailyTracker(models.Model):
    ldap = models.CharField(max_length=200, blank=False, unique=True)
    name = models.CharField(max_length=200, blank=True, default=None)
    days_worked = models.IntegerField(default=0)
    days_out_of_office = models.IntegerField(default=0)
    uaa_target = models.FloatField(default=0)
    uaa_achieved = models.FloatField(default=0)
    pts_target = models.FloatField(default=0)
    pts_won = models.FloatField(default=0)
    region = models.CharField(max_length=100, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        db_table = 'umm_daily_tracker'
        ordering = ['created_date']
        verbose_name_plural = "UMM Daily Tracker"


class QualityFeedbackForm(models.Model):
    ldap = models.CharField(max_length=200, blank=False, unique=True)
    date_of_review = models.DateTimeField(blank=False)
    feedback_notes = models.TextField(blank=True)
    final_score = models.FloatField(default=0, blank=True)

    class Meta:
        db_table = 'quality_feedback_form'
        verbose_name_plural = "Quality Feedback Form"


class UmmCallData(models.Model):
    ldap = models.CharField(max_length=200, blank=False, unique=True)
    umm_call_date = models.DateTimeField(blank=False)
    extn_out_call = models.IntegerField(default=0)
    total_call_time = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = 'umm_call_data'
        ordering = ['umm_call_date']
        verbose_name_plural = "UMM Call Data"
