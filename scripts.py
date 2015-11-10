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

from reports.report_services import ReportService
from django.conf import settings
from datetime import datetime, timedelta
import logging
from lib.salesforce import SalesforceApi
from leads.models import Leads, SfdcUsers, WPPLeads, PicassoLeads
from django.core.exceptions import ObjectDoesNotExist
import pytz
from representatives.models import GoogeRepresentatives, RegalixRepresentatives
from oauth2client.client import SignedJwtAssertionCredentials
from reports.models import CallLogAccountManager
from datetime import datetime


def create_or_update_picasso_leads(records, sf):
    """ Create a new leads or update existing lead for picasso"""
    logging.info("Start saving leads to our DB")
    total_leads = 0
    new_lead_saved = 0
    new_lead_failed = 0
    exist_lead_saved = 0
    exist_lead_failed = 0
    is_new_lead = True
    owners_list = {u.user_id: {'name': u.full_name, 'email': u.email} for u in SfdcUsers.objects.all()}
    for rec in records:
        total_leads += 1
        sf_lead_id = rec.get('Id')
        type_1 = rec.get('Code_Type__c')
        try:
            # check for existing lead
            lead = PicassoLeads.objects.get(sf_lead_id=sf_lead_id)
            is_new_lead = False
        except ObjectDoesNotExist:
            # create new lead
            is_new_lead = True
            lead = PicassoLeads()
        lead.lead_status = rec.get('Picasso_Lead_Stage__c')
        lead.type_1 = type_1

        # Google Representative email and name
        rep_email = rec.get('Email')
        rep_name = rec.get('Google_Rep__c')

        # Lead owner name
        owner_id = rec.get('OwnerId')
        if owner_id and owner_id in owners_list:
            details = owners_list.get(owner_id)
            lead_owner_name = details.get('name')
            lead_owner_email = details.get('email')
        else:
            try:
                user_details = sf.User.get(owner_id)
                lead_owner_name = user_details.get('Name')
                lead_owner_email = user_details.get('Email')
            except ObjectDoesNotExist:
                lead_owner_name = "%s %s" % (settings.DEFAULT_LEAD_OWNER_FNAME, settings.DEFAULT_LEAD_OWNER_LNAME)
                lead_owner_email = settings.DEFAULT_LEAD_OWNER_EMAIL

        # Team
        team = rec.get('Team__c') if rec.get('Team__c') else ''

        # Below information will be created if its a new lead or else the information will be updated
        lead.google_rep_name = rep_name
        lead.google_rep_email = rep_email if rep_email else settings.DEFAULT_LEAD_OWNER_EMAIL

        if rep_email and rep_name:
            # Save Google representatives information to Database
            try:
                GoogeRepresentatives.objects.get(email=rep_email)
            except ObjectDoesNotExist:
                google_rep = GoogeRepresentatives()
                rep_name = rep_name.split(' ')
                google_rep.first_name = unicode(rep_name[0])
                google_rep.last_name = unicode((' ').join(rep_name[1:]))
                google_rep.email = unicode(rep_email)
                google_rep.team = team
                google_rep.save()

        # Save Regalix representatives information to Database
        if lead_owner_email and lead_owner_name:
            try:
                RegalixRepresentatives.objects.get(email=lead_owner_email)
            except ObjectDoesNotExist:
                regalix_rep = RegalixRepresentatives()
                regalix_rep.name = lead_owner_name
                regalix_rep.email = lead_owner_email
                regalix_rep.team = team
                regalix_rep.save()

        # check if column is formatted to date type
        # if it is of date type, convert to datetime object
        created_date = rec.get('CreatedDate')
        created_date = SalesforceApi.salesforce_date_to_datetime_format(created_date)
        if not created_date:
            created_date = datetime.utcnow()

        lead.created_date = created_date

        lead.lead_owner_name = lead_owner_name if lead_owner_name else "%s %s" % (settings.DEFAULT_LEAD_OWNER_FNAME,
                                                                                  settings.DEFAULT_LEAD_OWNER_LNAME)
        lead.lead_owner_email = lead_owner_email if lead_owner_email else settings.DEFAULT_LEAD_OWNER_EMAIL
        lead.company = unicode(rec.get('Company'))
        lead.country = rec.get('Location__c')

        cid = rec.get('Customer_ID__c')
        internal_cid = rec.get('Internal_CID_1__c')  # for live we have to change
        if type(cid) is float:
            lead.customer_id = int(cid)
        else:
            lead.customer_id = cid

        lead.internal_cid = internal_cid
        lead.first_name = unicode(rec.get('FirstName'))
        lead.last_name = unicode(rec.get('LastName'))
        lead.phone = unicode(rec.get('Phone'))

        # check if column is formatted to date type
        # if it is of date type, convert to datetime object
        date_of_installation = rec.get('Date_of_installation__c')
        date_of_installation = SalesforceApi.salesforce_date_to_datetime_format(date_of_installation)
        lead.date_of_installation = date_of_installation

        lead.regalix_comment = unicode(rec.get('All_Regalix_Comments__c')).encode('unicode_escape')
        lead.google_comment = unicode(rec.get('Google_Comment__c')).encode('unicode_escape')

        lead.code_1 = rec.get('Code__c') if rec.get('Code__c') else ''
        lead.url_1 = rec.get('URL__c') if rec.get('URL__c') else ''
        lead.type_1 = rec.get('Code_Type__c') if rec.get('Code_Type__c') else ''
        lead.comment_1 = rec.get('Comment_1__c') if rec.get('Comment_1__c') else ''

        lead.team = team
        lead.sf_lead_id = sf_lead_id
        lead.picasso_objective = rec.get('Picasso_Objective__c') if rec.get('Picasso_Objective__c') else ''
        lead.picasso_multiple_objectives = (rec.get('Picasso_Objective__c')).replace(';', ',') if rec.get('Picasso_Objective__c') else '' #replace(';', ',')
        lead.pod_name = rec.get('POD_Name__c') if rec.get('POD_Name__c') else ''

        try:
            lead.save()
            if is_new_lead:
                new_lead_saved += 1
            else:
                exist_lead_saved += 1
        except Exception as e:
            print lead.sf_lead_id, e
            if is_new_lead:
                new_lead_failed += 1
            else:
                exist_lead_failed += 1

    logging.info("**********************************************************")
    logging.info("Total Picasso leads saved to our DB: %s" % (total_leads))
    logging.info("New Picasso Leads count: %s" % (new_lead_saved))
    logging.info("New Picasso Leads Failed Count: %s" % (new_lead_failed))
    logging.info("Exist Picasso leads updated Count: %s" % (exist_lead_saved))
    logging.info("Exist Picasso lead failed to update: %s" % (exist_lead_failed))

end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
start_date = end_date - timedelta(days=1)
start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
sf = SalesforceApi.connect_salesforce()
select_items = settings.SFDC_FIELDS
tech_team_id = settings.TECH_TEAM_ID
code_type = 'Picasso'
where_clause_picasso = "WHERE (LastModifiedDate >= %s AND LastModifiedDate <= %s) AND LastModifiedById != '%s' AND Code_Type__c = '%s'" % (start_date, end_date, tech_team_id, code_type)
sql_query_picasso = "select %s from Lead %s" % (select_items, where_clause_picasso)
try:
    picasso_leads = sf.query_all(sql_query_picasso)
    import ipdb; ipdb.set_trace()
    create_or_update_picasso_leads(picasso_leads['records'], sf)
except Exception as e:
    print e
    logging.info("Fail to get updated leads from %s to %s" % (start_date, end_date))
    logging.info("%s" % (e))
