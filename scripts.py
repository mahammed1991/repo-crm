#! /usr/bin/env python
# coding:utf-8

# from django.core.management import setup_environ
# from rglxtools import settings
# setup_environ(settings)
# from leads.models import Location, Timezone

# locations = Location.objects.filter().order_by('location_name')

# location_list = list()

# for location in locations:
#     timezones = location.objects.all()
#     print location.location_name
#     print timezones

# print "Done"

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_portal.settings-staging")
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

# from django.conf import settings
# import json
# import gspread
# from oauth2client.client import SignedJwtAssertionCredentials
# from reports.models import CallLogAccountManager
# from datetime import datetime

# json_file = settings.MEDIA_ROOT + '/gtrack-test-0e3eb2372302.json'

# json_key = json.load(open(json_file))
# scope = ['https://spreadsheets.google.com/feeds']

# credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

# gc = gspread.authorize(credentials)

# sheet_url = settings.SPREADSHEET_URL

# worksheet = gc.open_by_url(sheet_url).sheet1

# print worksheet

# all_records = worksheet.get_all_records()

# objects_list = list()

# for record in all_records[1:]:
#     if record['Meeting Time']:
#         log_details = CallLogAccountManager()
#         log_details.username = record['Username']
#         log_details.seller_name = record['Seller Name']
#         log_details.seller_id = record['Seller ID']
#         log_details.phone_number = record['Phone Number']
#         log_details.alternate_number = record['Alternate Number']
#         try:
#             meeting_time_in_cst = datetime.strptime(record['Meeting Time'], "%m/%d/%Y %H:%M:%S")
#         except Exception:
#             continue
#         # Meeting time from cst to ist
#         # cst_time = datetime.strptime(record[6], "%m/%d/%Y %H:%M:%S")
#         # tz_cst = Timezone.objects.get(zone_name='CST')
#         # utc_date = SalesforceApi.get_utc_date(cst_time, tz_cst.time_value)
#         # tz_ist = Timezone.objects.get(zone_name='IST')
#         # meeting_time_ist = SalesforceApi.convert_utc_to_timezone(utc_date, tz_ist.time_value)

#         log_details.meeting_time = meeting_time_in_cst  # record['Meeting Time']
#         log_details.call_status = record['Call Status']
#         log_details.log_time_stamp = datetime.strptime(record['Timestamp'], "%m/%d/%Y %H:%M:%S")  # record['Timestamp']
#         log_details.sheet_row_count = worksheet.row_count
#         objects_list.append(log_details)

# # # total records - 1 saved
# CallLogAccountManager.objects.bulk_create(objects_list)

# from reports.report_services import ReportService
# from django.conf import settings
# from datetime import datetime, timedelta
# import logging
# from lib.salesforce import SalesforceApi
# from leads.models import Leads, SfdcUsers, WPPLeads, PicassoLeads
# from django.core.exceptions import ObjectDoesNotExist
# import pytz
# from representatives.models import GoogeRepresentatives, RegalixRepresentatives
# from oauth2client.client import SignedJwtAssertionCredentials
# from reports.models import CallLogAccountManager
# from datetime import datetime


# end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
# start_date = end_date - timedelta(days=1)
# start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
# end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
# sf = SalesforceApi.connect_salesforce()
# select_items = settings.SFDC_FIELDS
# tech_team_id = settings.TECH_TEAM_ID
# code_type = 'WPP'
# where_clause_picasso = "WHERE (LastModifiedDate >= %s AND LastModifiedDate <= %s)" % (start_date, end_date)
# sql_query_picasso = "select %s from Lead %s" % (select_items, where_clause_picasso)
# try:
#     picasso_leads = sf.query_all(sql_query_picasso)
#     # create_or_update_picasso_leads(picasso_leads['records'], sf)
# except Exception as e:
#     print e
#     logging.info("Fail to get updated leads from %s to %s" % (start_date, end_date))
#     logging.info("%s" % (e))


import datetime
from operator import itemgetter
from leads.models import Leads
from django.db.models import Count

start_date = datetime.datetime(2015, 10, 01)
end_date = datetime.datetime(2015, 10, 01, 23, 59, 59)

leads_dict = Leads.objects.filter(rescheduled_appointment_in_ist__gt=start_date, rescheduled_appointment_in_ist__lte=end_date).values('rescheduled_appointment_in_ist').annotate(count=Count('pk'))
sorted_dict = sorted(leads_dict, key=itemgetter('rescheduled_appointment_in_ist'))

for ed in sorted_dict:
    if len(str(ed['rescheduled_appointment_in_ist'].time().hour)) == 1:
        hour = '0%s' % (str(ed['rescheduled_appointment_in_ist'].time().hour))
    else:
        hour = str(ed['rescheduled_appointment_in_ist'].time().hour)
    if len(str(ed['rescheduled_appointment_in_ist'].time().minute)) == 1:
        minute = '0%s' % (str(ed['rescheduled_appointment_in_ist'].time().minute))
    else:
        minute = str(ed['rescheduled_appointment_in_ist'].time().minute)

    tym = '%s:%s' % (hour, minute)

    print tym

collumn_attr = ['Hours', 'Team']
result = list()

for i in range(0, 24):
    for j in ['00', '30']:
        mydict = {}
        if len(str(i)) == 1:
            indx = '0%s' % (i)
        else:
            indx = str(i)
        hour = "%s:%s" % (indx, j)
        for ele in collumn_attr:
            if ele == 'Team':
                mydict[ele] = 'team_name'
            elif ele == 'Hours':
                mydict[ele] = hour
            elif 'Resh' in ele:
                mydict[ele] = ''
            else:
                mydict[ele] = '0|0'

        result.append(mydict)
print result
