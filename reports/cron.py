import kronos
from reports.report_services import ReportService
from django.conf import settings
from datetime import datetime, timedelta
from lib.helpers import get_quarter_date_slots, first_day_of_month, last_day_of_month
from reports.models import LeadSummaryReports
import logging
from lib.salesforce import SalesforceApi
from leads.models import Leads, SfdcUsers
from django.core.exceptions import ObjectDoesNotExist
from lib.helpers import get_week_start_end_days
import time
import pytz
from representatives.models import GoogeRepresentatives, RegalixRepresentatives

logging.basicConfig(filename='/tmp/cronjob.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%d/%b/%Y %H:%M:%S',
                    level=logging.DEBUG)


# @kronos.register('0 * * * *')
# def get_current_quarter_summary():
#     logging.info("Initializing kronos")
#     # Get all teams
#     teams = ReportService.get_all_teams()

#     # get all code types
#     code_types = ReportService.get_all_code_type()

#     # get all lead status
#     lead_status = settings.LEAD_STATUS
#     lead_status.extend(['Pending QC - DEAD LEAD', 'Pending QC - WIN', 'Rework Required', 'Appointment Set (GS)'])

#     # get current quarter
#     dt = datetime.now()
#     start_date, end_date = get_quarter_date_slots(dt)
#     logging.info("Get Current Quarter Report from %s to %s" % (datetime.strftime(start_date, "%d %b %Y"), datetime.strftime(end_date, "%d %b %Y")))

#     # get all locations
#     locations = ReportService.get_all_locations()
#     reports = ReportService.get_summary_by_code_types_and_status('all', code_types, lead_status,
#                                                                  start_date, end_date, teams, locations)
#     code_type = reports.keys()
#     for k in code_type:
#         current_quarter = LeadSummaryReports.objects.filter(code_type=k)
#         if current_quarter:
#             current_quarter.code_type = k
#             current_quarter.total_leads = reports[k]['total_leads']
#             current_quarter.win = reports[k]['wins']
#             current_quarter.implemented = reports[k]['Implemented']
#             if 'In Queue' in reports[k]:
#                 current_quarter.in_queue = reports[k]['In Queue'] + reports[k].get('Appointment Set (GS)', 0)
#             else:
#                 current_quarter.in_queue = 0

#             if 'In Progress' in reports[k]:
#                 current_quarter.in_progress = reports[k]['In Progress'] + reports[k].get('Pending QC - DEAD LEAD', 0) \
#                     + reports[k].get('Pending QC - WIN', 0) + reports[k].get('Rework Required', 0)
#             else:
#                 current_quarter.in_progress = 0
#             current_quarter.tat_implemented = reports[k]['tat_implemented']
#             current_quarter.tat_first_contacted = reports[k]['tat_first_contacted']
#             current_quarter.start_date = start_date
#             current_quarter.end_date = end_date
#             current_quarter.update()
#         else:
#             current_quarter = LeadSummaryReports()
#             current_quarter.code_type = k
#             current_quarter.total_leads = reports[k]['total_leads']
#             current_quarter.win = reports[k]['wins']
#             current_quarter.implemented = reports[k]['Implemented']
#             if 'In Queue' in reports[k]:
#                 current_quarter.in_queue = reports[k]['In Queue'] + reports[k].get('Appointment Set (GS)', 0)
#             else:
#                 current_quarter.in_queue = 0

#             if 'In Progress' in reports[k]:
#                 current_quarter.in_progress = reports[k]['In Progress'] + reports[k].get('Pending QC - DEAD LEAD', 0) \
#                     + reports[k].get('Pending QC - WIN', 0) + reports[k].get('Rework Required', 0)
#             else:
#                 current_quarter.in_progress = 0
#             current_quarter.tat_implemented = reports[k]['tat_implemented']
#             current_quarter.tat_first_contacted = reports[k]['tat_first_contacted']
#             current_quarter.start_date = start_date
#             current_quarter.end_date = end_date
#             current_quarter.save()
#     logging.info("Cron job done")


@kronos.register('5 * * * *')
def current_day_leads():
    """ Get Leads from SFDC """
    current_day = datetime.utcnow()
    start_date = datetime(current_day.year, current_day.month, current_day.day, 0, 0, 0)
    end_date = datetime(current_day.year, current_day.month, current_day.day, 23, 59, 59)
    logging.info("Current Day Leads %s to %s " % (start_date, end_date))
    get_leads_from_sfdc(start_date, end_date)


@kronos.register('0 * * * *')
def current_week_leads():
    """ Get Leads from SFDC """
    week = int(time.strftime("%W")) + 1
    year = int(time.strftime("%Y"))
    start_date, end_date = get_week_start_end_days(year, week)
    logging.info("Get Week leads by %s to %s " % (start_date, end_date))
    get_leads_from_sfdc(start_date, end_date)


@kronos.register('0 6 * * *')
def current_month_leads():
    """ Get Leads from SFDC """

    start_date = first_day_of_month(datetime.utcnow())
    end_date = last_day_of_month(datetime.utcnow())
    logging.info("Current Month Leads by from %s to %s" % (start_date, end_date))
    get_leads_from_sfdc(start_date, end_date)


@kronos.register('0 7 * * *')
def current_quarter_leads():
    """ Get Leads from SFDC """

    start_date, end_date = get_quarter_date_slots(datetime.utcnow())
    logging.info("Current Quarted Leads from %s to %s" % (start_date, end_date))
    get_leads_from_sfdc(start_date, end_date)


@kronos.register('30 0 * * *')
def get_updated_leads():
    """ Get Current Quarter updated Leads from SFDC """
    end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
    start_date = end_date - timedelta(days=2)
    logging.info("Current Quarted Updated Leads from %s to %s" % (start_date, end_date))
    logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
    sf = SalesforceApi.connect_salesforce()
    logging.info("Connect Successfully")
    leads = sf.Lead.updated(start_date, end_date)
    ids = [str(lid) for lid in leads['ids']]
    ids = tuple(ids)
    select_items = settings.SFDC_FIELDS
    where_clause = "WHERE Id IN %s" % (str(ids))
    sql_query = "select %s from Lead %s" % (select_items, where_clause)
    try:
        all_leads = sf.query_all(sql_query)
        create_or_update_leads(all_leads['records'], sf)
    except Exception as e:
        print e
        logging.info("Fail to get leads from %s to %s" % (start_date, end_date))
        logging.info("%s" % (e))


def get_leads_from_sfdc(start_date, end_date):
    """ Get Leads from SFDC """
    # get SFDC Connection
    logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
    sf = SalesforceApi.connect_salesforce()

    logging.info("Connect Successfully")
    # import ipdb; ipdb.set_trace()
    start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
    end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
    select_items = settings.SFDC_FIELDS
    where_clause = "WHERE CreatedDate >= %s AND CreatedDate <= %s" % (start_date, end_date)
    sql_query = "select %s from Lead %s" % (select_items, where_clause)
    try:
        all_leads = sf.query_all(sql_query)
        logging.info("No of Leads from %s to %s is: %s" % (start_date, end_date, len(all_leads['records'])))
        create_or_update_leads(all_leads['records'], sf)
    except Exception as e:
        print e
        logging.info("Fail to get leads from %s to %s" % (start_date, end_date))
        logging.info("%s" % (e))


def create_or_update_leads(records, sf):
    """ Create a new leads or update existing lead """
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

        try:
            # check for existing lead
            lead = Leads.objects.get(sf_lead_id=sf_lead_id)
            is_new_lead = False
        except ObjectDoesNotExist:
            # create new lead
            is_new_lead = True
            lead = Leads()

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
                user_details = sf.User.get('owner_id')
                lead_owner_name = user_details.get('Email')
                lead_owner_email = user_details.get('Name')
            except ObjectDoesNotExist:
                lead_owner_name = "%s %s" % (settings.DEFAULT_LEAD_OWNER_FNAME, settings.DEFAULT_LEAD_OWNER_LNAME)
                lead_owner_email = settings.DEFAULT_LEAD_OWNER_EMAIL

        # Team
        team = rec.get('Team__c') if rec.get('Team__c') else ''

        # Below information will be created if its a new lead or else the information will be updated
        lead.google_rep_name = rep_name
        lead.google_rep_email = rep_email

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

        try:
            lead.ecommerce = int(rec.get('E-commerce'))
        except Exception:
            lead.ecommerce = 0

        lead.lead_owner_name = lead_owner_name if lead_owner_name else 'Raju K R'
        lead.lead_owner_email = lead_owner_email if lead_owner_email else 'rajuk@regalix-inc.com'
        lead.company = unicode(rec.get('Company'))
        lead.lead_status = rec.get('Status')
        lead.country = rec.get('Location__c')

        cid = rec.get('Customer_ID__c')
        if type(cid) is float:
            lead.customer_id = int(cid)
        else:
            lead.customer_id = cid

        lead.first_name = unicode(rec.get('FirstName'))
        lead.last_name = unicode(rec.get('LastName'))
        lead.phone = unicode(rec.get('Phone'))

        lead.first_name_optional = unicode(rec.get('First_Name_optional__c'))
        lead.last_name_optional = unicode(rec.get('Last_Name_optional__c'))
        lead.phone_optional = unicode(rec.get('Phone_optional__c'))
        lead.email_optional = unicode(rec.get('Email_optional__c'))

        # check if column is formatted to date type
        # if it is of date type, convert to datetime object
        date_of_installation = rec.get('Date_of_installation__c')
        date_of_installation = SalesforceApi.salesforce_date_to_datetime_format(date_of_installation)
        lead.date_of_installation = date_of_installation

        appointment_date = rec.get('Appointment_Date__c')
        appointment_date = SalesforceApi.salesforce_date_to_datetime_format(appointment_date)
        lead.appointment_date = appointment_date

        first_contacted_on = rec.get('X1st_Contact_on__c')
        first_contacted_on = SalesforceApi.salesforce_date_to_datetime_format(first_contacted_on)
        lead.first_contacted_on = first_contacted_on

        # Rescheduled Appointments
        rescheduled_appointment = rec.get('Rescheduled_Appointments__c')
        rescheduled_appointment = SalesforceApi.salesforce_date_to_datetime_format(rescheduled_appointment)
        lead.rescheduled_appointment = rescheduled_appointment

        try:
            lead.dials = int(rec.get('qbdialer__Dials__c'))
        except Exception:
            lead.dials = 0

        lead.lead_sub_status = rec.get('Lead_Sub_Status__c')

        lead.time_zone = rec.get('Time_Zone__c') if rec.get('Time_Zone__c') else ''

        lead.regalix_comment = unicode(rec.get('Regalix_Comment__c')).encode('unicode_escape')
        lead.google_comment = unicode(rec.get('Google_Comment__c')).encode('unicode_escape')

        lead.code_1 = rec.get('Code__c') if rec.get('Code__c') else ''
        lead.url_1 = rec.get('URL__c') if rec.get('URL__c') else ''
        lead.type_1 = rec.get('Code_Type__c') if rec.get('Code_Type__c') else ''
        lead.comment_1 = rec.get('Comment_1__c') if rec.get('Comment_1__c') else ''

        lead.team = team
        lead.sf_lead_id = sf_lead_id
        if lead.type_1 == 'WPP':
            lead.lead_status = rec.get('WPP_Lead_Status__c')

        # Calculate TAT for each lead
        tat = 0
        if lead.lead_status == 'Implemented':
            if lead.team in settings.SERVICES:
                tat = ReportService.get_tat_by_implemented_for_service(
                    lead.date_of_installation, lead.created_date)
            else:
                tat = ReportService.get_tat_by_implemented(
                    lead.date_of_installation, lead.appointment_date, lead.created_date)
        else:
            tat = ReportService.get_tat_by_first_contacted_on(
                lead.first_contacted_on, lead.appointment_date, lead.created_date)
        lead.tat = tat
        try:
            lead.save()
            if is_new_lead:
                new_lead_saved += 1
            else:
                exist_lead_saved += 1
        except Exception as e:
            print lead, e
            if is_new_lead:
                new_lead_failed += 1
            else:
                exist_lead_failed += 1

    logging.info("**********************************************************")
    logging.info("Total leads saved to our DB: %s" % (total_leads))
    logging.info("New Leads count: %s" % (new_lead_saved))
    logging.info("New Leads Failed Count: %s" % (new_lead_failed))
    logging.info("Exist leads updated Count: %s" % (exist_lead_saved))
    logging.info("Exist lead failed to update: %s" % (exist_lead_failed))
    logging.info("**********************************************************")


@kronos.register('0 10 * * *')
def get_salesforce_users():
    """ Get all Users from SFDC """

    logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
    sf = SalesforceApi.connect_salesforce()
    logging.info("Connect Successfully")
    user_details = sf.query_all("Select Id, Email, Name, Username from User")
    users = user_details.get('records')
    for user in users:
        details = {
            'user_id': user.get('Id'),
            'full_name': user.get('Name'),
            'email': user.get('Email'),
            'username': user.get('Username')
        }

        create_sfdc_user(details)


def create_sfdc_user(details):
    """ Create users in to db """

    try:
        user = SfdcUsers.objects.get(user_id=details.get('user_id'))
    except ObjectDoesNotExist:
        user = SfdcUsers()
    user.user_id = details.get('user_id')
    user.full_name = details.get('full_name')
    user.email = details.get('email')
    user.username = details.get('username')
    user.save()
