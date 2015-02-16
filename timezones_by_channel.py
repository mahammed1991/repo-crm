#! /usr/bin/env python
#coding:utf-8

#from django.core.management import setup_environ
#from rglxtools import settings
#setup_environ(settings)
from leads.models import Location, Timezone

locations = Location.objects.filter().order_by('location_name')

location_list = list()

for location in locations:
    timezones = location.objects.all()
    print location.location_name
    print timezones

print "Done"
