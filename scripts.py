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



# from representatives.models import Availability

# # name = raw_input("enter date")
# # utc_date = raw_input("enter date")
# # availability = Availability.objects.get(date_in_utc=utc_date, team=selected_team)

# selected_team = 1
# # created_date = raw_input("enter team date")

# # availability = Availability.objects.get(team=selected_team).filter(availability_count)
# import ipdb;ipdb.set_trace()
# availability = Availability.objects.filter(team=selected_team)

# print availability



# default_process_type = ['TAG', 'SHOPPING']
# default_teams = RegalixTeams.objects.filter(process_type__in=default_process_type, is_active=True).exclude(team_name='default team')

# for teams in default_teams:
# 	slots_data = Availability.objects.filter(
#             # date_in_utc__range=(from_utc_date, to_utc_date),
#             team__id=teams.id,
#             # team__process_type=teams.process_type
#         ).values_list('team__team_name').annotate(count=Count('availability_count'))
# 	print slots_data

# import ipdb;ipdb.set_trace()

#import ipdb;ipdb.set_trace()
#availabl = Availability.objects.filter(team__in=default_teams, date_in_utc__range=[date, today]).values('team_id').annotate(count=Count('availability_count'))

#availabl = Availability.objects.filter(team__in=default_teams, date_in_utc__range=[date, today]).values('team_id').annotate(total=Sum('availability_count'))


# booked_count = Availability.objects.filter(team__in=default_teams, date_in_utc__range=[date, today]).values('booked_count', 'team_id')
# print "booked-count", booked_count

# dictf = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), availabl)

# print "all sum avaialable ", dictf

# import ipdb;ipdb.set_trace()
# for data in availabl:
# 	print data

from datetime import datetime, timedelta
from main.models import UserDetails
from leads.models import Timezone, RegalixTeams, Location, TimezoneMapping, Leads, WPPLeads, CodeType
from representatives.models import (
    Availability,
    ScheduleLog,
    AvailabilityForTAT
)
from reports.report_services import DownloadLeads
from lib.salesforce import SalesforceApi
from lib.helpers import send_mail
from django.template.loader import get_template
from django.db.models import Sum
from django.template import Context
from django.db.models import Count
from collections import OrderedDict
#import datetime
from datetime import timedelta, datetime

def available_counts_booked_specific(process_type):
	""" taking values from today 2AM to previous 3AM exclude_north_america"""
	from datetime import datetime
	today_morning = datetime.today()
	today = today_morning.replace(hour=2, minute=00, second=00)
	print "exclude north america"
	print today
	previous_day_time = today_morning - timedelta(days=1)
	previous_day = previous_day_time.replace(hour=3, minute=00, second=00)
	print previous_day
	time_zone = 'IST'
	#print "exclude na",today ,previous_day
	exclude_north_america = ['default team', 'TAG - SPLATAM - Spanish', 'TAG - SPLATAM - Portuguese', 'TAG - NA - Spanish', 'TAG - NA - English', 'SHOPPING - SPLATAM - Spanish', 'SHOPPING - SPLATAM - Portuguese', 'SHOPPING - NA - English']
	selected_tzone = Timezone.objects.get(zone_name=time_zone)
	from_utc_date = SalesforceApi.get_utc_date(previous_day, selected_tzone.time_value)
	to_utc_date = SalesforceApi.get_utc_date(today, selected_tzone.time_value)
	default_teams = RegalixTeams.objects.filter(process_type__in=process_type, is_active=True).exclude(team_name__in=exclude_north_america)
	print default_teams
	available_counts_teams = default_teams.values('team_name')
	available_counts_booked = Availability.objects.exclude(team__team_name='default team' ).filter(team__in=default_teams, date_in_utc__range=[from_utc_date, to_utc_date]).values('team__team_name').annotate(Availability_count=Sum('availability_count'), booked_count=Sum('booked_count'))
	#available_counts_booked = Availability.objects.exclude(team__team_name='default team' ).filter(team__in=default_teams, date_in_utc__range=[previous_day, today]).values('team__team_name').annotate(Availability_count=Sum('availability_count'), booked_count=Sum('booked_count'))
	print available_counts_booked

	#for listvalue in exclude_north_america:
	for item in available_counts_teams:
		item['Availability Count'] = 0
		item['Ratio'] = 0
		item['Booked Count'] = 0

	for ele in available_counts_teams:
		if ele['Booked Count'] > 0:
			value = (float(ele['Booked Count'])/ele['Availability Count'])*100
			ele['Ratio'] = ("%.2f" % value)
			
	for item in available_counts_booked:
		for item2 in available_counts_teams:
			if item2['team_name'] == item['team__team_name']:
				item2['Availability Count'] = item['Availability_count']
				item2['Booked Count'] = item['booked_count']

	return available_counts_teams

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def available_counts_booked_specific_in_na(process_type):
	""" 7.00PM to nextday 7.30AM only for north america   """
	from datetime import datetime
	today_morning = datetime.today()
	today = today_morning.replace(hour=19, minute=00, second=00)
	print "include north america"
	print today
	next_day_time = today_morning + timedelta(days=1)
	next_day = next_day_time.replace(hour=7, minute=30, second=00)
	print next_day
	time_zone = 'IST'
	
	selected_tzone = Timezone.objects.get(zone_name=time_zone)
	from_utc_date = SalesforceApi.get_utc_date(today, selected_tzone.time_value)
	to_utc_date = SalesforceApi.get_utc_date(next_day, selected_tzone.time_value)
	only_north_america = ['TAG - SPLATAM - Spanish', 'TAG - SPLATAM - Portuguese', 'TAG - NA - Spanish', 'TAG - NA - English', 'SHOPPING - SPLATAM - Spanish', 'SHOPPING - SPLATAM - Portuguese', 'SHOPPING - NA - English']
	
	default_teams = RegalixTeams.objects.filter(process_type__in=process_type, is_active=True, team_name__in=only_north_america).exclude(team_name='default team' )
	print default_teams
	available_counts_booked = Availability.objects.exclude(team__team_name='default team' ).filter(team__in=default_teams, date_in_utc__range=[from_utc_date, to_utc_date]).values('team__team_name').annotate(Availability_count=Sum('availability_count'), booked_count=Sum('booked_count'))
	#available_counts_booked = Availability.objects.exclude(team__team_name='default team' ).filter(team__in=default_teams, date_in_utc__range=[today, next_day]).values('team__team_name').annotate(Availability_count=Sum('availability_count'), booked_count=Sum('booked_count'))

	available_counts_teams = default_teams.values('team_name')
	for item in available_counts_teams:
		item['Availability Count'] = 0
		item['Ratio'] = 0
		item['Booked Count'] = 0

	for item in available_counts_booked:
		for item2 in available_counts_teams:
			if item2['team_name'] == item['team__team_name']:
				item2['Availability Count'] = item['Availability_count']
				item2['Booked Count'] = item['booked_count']

	for ele in available_counts_teams:
		if ele['Booked Count'] > 0:
			value = (float(ele['Booked Count'])/ele['Availability Count'])*100
			ele['Ratio'] = ("%.2f" % value)


	return available_counts_teams

def slots_open_booked():
	tag_bookings_exclude_na = available_counts_booked_specific(['TAG'])
	shopping_bookings_exclude_na = available_counts_booked_specific(['SHOPPING'])
	tag_bookings_in_na = available_counts_booked_specific_in_na(['TAG'])
	shopping_bookings_in_na = available_counts_booked_specific_in_na(['SHOPPING'])

	tag_all = list()
	shopping_all = list()

	for data in tag_bookings_in_na:
		tag_all.append(data)

	for data in shopping_bookings_in_na:
		shopping_all.append(data)

	for data in tag_bookings_exclude_na:
		tag_all.append(data)

	for data in shopping_bookings_exclude_na:
		shopping_all.append(data)

	tag_final = list()
	for ordering in tag_all:
		keyorder = {k:v for v, k in enumerate(['team_name', 'Availability Count', 'Booked Count', 'Ratio'])}
		each_one = OrderedDict(sorted(ordering.items(), key=lambda i:keyorder.get(i[0])))
		tag_final.append(each_one)

	shopping_final = list()
	for ordering in shopping_all:
		keyorder = {k:v for v, k in enumerate(['team_name', 'Availability Count', 'Booked Count', 'Ratio'])}
		each_one = OrderedDict(sorted(ordering.items(), key=lambda i:keyorder.get(i[0])))
		shopping_final.append(each_one)

	tag_total_sum = dict()
	tag_total_sum['Availability_count'] =  sum(item['Availability Count'] for item in tag_all)
	tag_total_sum['Booked Count'] = sum(item['Booked Count'] for item in tag_all)

	shopping_total_sum = dict()
	shopping_total_sum['Availability_count'] =  sum(item['Availability Count'] for item in shopping_all)
	shopping_total_sum['Booked Count'] = sum(item['Booked Count'] for item in shopping_all)

	all_bookings = zip(tag_final,shopping_final)

	#mailing functyonaliteis
	from datetime import datetime
	import logging
	from django.template.loader import get_template
	from django.template import Context
	from lib.helpers import send_mail
	specific_date = datetime.today()
	specific_date = datetime(specific_date.year, specific_date.month, specific_date.day)
	specific_date = specific_date.date()
	logging.info("Implemeted Leads Count Mail Details sending")
	mail_subject = "count availabel and booked slots"
	mail_body = get_template('reports/email_templates/slots_detail.html').render(Context({'all_bookings':all_bookings, 'tag_total_sum':tag_total_sum, 'shopping_total_sum':shopping_total_sum }))
	mail_from = 'mashraf@regalix-inc.com'
	mail_to = ['mashraf@regalix-inc.com', 'gtracktesting@gmail.com']
	bcc = set([])
	attachments = list()
	send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)



slots_open_booked()
