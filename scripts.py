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
# from leads.models import Leads, WPPLeads

# total_leads_before_delete = Leads.objects.all().count()
# print 'Total Number of Leads in Leads is before WPP Leads Delete is', total_leads_before_delete

# wpp_leads = Leads.objects.filter(type_1='WPP').values()
# print 'Number of WPP Leads in Leads is ', len(wpp_leads)

# for lead in wpp_leads:
#     del lead['id']
#     lead['treatment_type'] = lead['wpp_treatment_type']
#     del lead['wpp_treatment_type']
#     wpp_lead = WPPLeads(**lead)
#     wpp_lead.save()

#     Leads.objects.filter(sf_lead_id=lead['sf_lead_id']).delete()

# total_leads_after_delete = Leads.objects.all().count()
# print 'Total Number of Leads in Leads is After WPP Leads Delete is', total_leads_after_delete

from django.conf import settings
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from reports.models import CallLogAccountManager
from datetime import datetime

json_file = settings.MEDIA_ROOT + '/gtrack-test-0e3eb2372302.json'

json_key = json.load(open(json_file))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gc = gspread.authorize(credentials)

sheet_url = settings.SPREADSHEET_URL

worksheet = gc.open_by_url(sheet_url).sheet1

print worksheet

all_records = worksheet.get_all_records()

objects_list = list()

for record in all_records[1:]:
    if record['Meeting Time']:
        log_details = CallLogAccountManager()
        log_details.username = record['Username']
        log_details.seller_name = record['Seller Name']
        log_details.seller_id = record['Seller ID']
        log_details.phone_number = record['Phone Number']
        log_details.alternate_number = record['Alternate Number']
        try:
            meeting_time_in_cst = datetime.strptime(record['Meeting Time'], "%m/%d/%Y %H:%M:%S")
        except Exception:
            continue
        # Meeting time from cst to ist
        # cst_time = datetime.strptime(record[6], "%m/%d/%Y %H:%M:%S")
        # tz_cst = Timezone.objects.get(zone_name='CST')
        # utc_date = SalesforceApi.get_utc_date(cst_time, tz_cst.time_value)
        # tz_ist = Timezone.objects.get(zone_name='IST')
        # meeting_time_ist = SalesforceApi.convert_utc_to_timezone(utc_date, tz_ist.time_value)

        log_details.meeting_time = meeting_time_in_cst  # record['Meeting Time']
        log_details.call_status = record['Call Status']
        log_details.log_time_stamp = datetime.strptime(record['Timestamp'], "%m/%d/%Y %H:%M:%S")  # record['Timestamp']
        log_details.sheet_row_count = worksheet.row_count
        objects_list.append(log_details)

# # total records - 1 saved
CallLogAccountManager.objects.bulk_create(objects_list)
