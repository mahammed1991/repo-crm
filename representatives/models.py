from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from leads.models import RegalixTeams


# Create your models here.
class GoogeRepresentatives(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    role = models.IntegerField(default=settings.GOOGLE_DEFAULT_ROLE, null=False)
    user_supporting_region = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100)

    created_date = models.DateTimeField(default=datetime.utcnow())

    class Meta:
        db_table = 'google_representatives'


class RegalixRepresentatives(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    supervisor = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    role = models.IntegerField(default=settings.REGALIX_DEFAULT_ROLE, null=False)

    created_date = models.DateTimeField(default=datetime.utcnow())

    class Meta:
        db_table = 'regalix_representatives'
        ordering = ['name']


class Availability(models.Model):
    availability_count = models.IntegerField()
    booked_count = models.IntegerField(default=0)
    date_in_utc = models.DateTimeField()
    team = models.ForeignKey(RegalixTeams, default=1)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        db_table = 'availability'


class ScheduleLog(models.Model):
    user = models.ForeignKey(User)
    availability = models.ForeignKey(Availability)
    availability_count = models.IntegerField()
    booked_count = models.IntegerField()

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'schedule_log'
        verbose_name_plural = "Schedule Log"
