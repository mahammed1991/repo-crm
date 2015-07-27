#! /usr/bin/env python
#coding:utf-8

#from django.core.management import setup_environ
#from rglxtools import settings
#setup_environ(settings)
# from leads.models import Location, Timezone

# locations = Location.objects.filter().order_by('location_name')

# location_list = list()

# for location in locations:
#     timezones = location.objects.all()
#     print location.location_name
#     print timezones

# print "Done"

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_portal.settings")
from leads.models import Leads, WPPLeads

wpp_leads = Leads.objects.filter(type_1='WPP').values()

for lead in wpp_leads:
    del lead['id']
    lead['treatment_type'] = lead['wpp_treatment_type']
    del lead['wpp_treatment_type']
    wpp_lead = WPPLeads(**lead)
    wpp_lead.save()

    Leads.objects.filter(sf_lead_id=lead['sf_lead_id']).delete()
