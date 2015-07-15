import kronos
from reports.report_services import ReportService
from django.conf import settings
from datetime import datetime, timedelta
from lib.helpers import first_day_of_month, last_day_of_month
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


# @kronos.register('*/25 * * * *')
# def current_day_leads():
#     """ Get Leads from SFDC """
#     end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
#     start_date = end_date - timedelta(minutes=30)
#     logging.info("Current Day Leads %s to %s " % (start_date, end_date))
#     get_leads_from_sfdc(start_date, end_date)


# @kronos.register('0 * * * *')
# def current_week_leads():
#     """ Get Leads from SFDC """
#     week = int(time.strftime("%W")) + 1
#     year = int(time.strftime("%Y"))
#     start_date, end_date = get_week_start_end_days(year, week)
#     logging.info("Get Week leads by %s to %s " % (start_date, end_date))
#     get_leads_from_sfdc(start_date, end_date)


# @kronos.register('0 6 * * *')
# def current_month_leads():
#     """ Get Leads from SFDC """

#     start_date = first_day_of_month(datetime.utcnow())
#     end_date = last_day_of_month(datetime.utcnow())
#     logging.info("Current Month Leads by from %s to %s" % (start_date, end_date))
#     get_leads_from_sfdc(start_date, end_date)


# @kronos.register('0 7 * * *')
# def current_quarter_leads():
#     """ Get Leads from SFDC """
#     end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
#     start_date = end_date - timedelta(days=75)
#     end_date = end_date + timedelta(days=15)
#     # start_date, end_date = get_quarter_date_slots(datetime.utcnow())
#     logging.info("Current Quarted Leads from %s to %s" % (start_date, end_date))
#     get_leads_from_sfdc(start_date, end_date)


@kronos.register('*/10 * * * *')
def get_updated_leads():
    """ Get Current Quarter updated Leads from SFDC """
    end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
    start_date = end_date - timedelta(minutes=10)
    start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
    end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
    logging.info("Current Quarted Updated Leads from %s to %s" % (start_date, end_date))
    logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
    sf = SalesforceApi.connect_salesforce()
    logging.info("Connect Successfully")
    select_items = settings.SFDC_FIELDS
    tech_team_id = settings.TECH_TEAM_ID
    where_clause = "WHERE (LastModifiedDate >= %s AND LastModifiedDate <= %s) AND LastModifiedById != '%s'" % (start_date, end_date, tech_team_id)
    sql_query = "select %s from Lead %s" % (select_items, where_clause)
    try:
        all_leads = sf.query_all(sql_query)
        logging.info("Updating Leads count: %s " % (len(all_leads['records'])))
        create_or_update_leads(all_leads['records'], sf)
        update_sfdc_leads(all_leads['records'], sf)
    except Exception as e:
        print e
        logging.info("Fail to get updated leads from %s to %s" % (start_date, end_date))
        logging.info("%s" % (e))


# @kronos.register('*/45 * * * *')
# def get_appointment_leads():
#     """ Get Current day Leads from SFDC """
#     end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
#     start_date = end_date - timedelta(minutes=50)
#     start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
#     end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
#     logging.info("Current day Leads from %s to %s" % (start_date, end_date))
#     logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
#     sf = SalesforceApi.connect_salesforce()
#     logging.info("Connect Successfully")
#     select_items = settings.SFDC_FIELDS
#     tech_team_id = settings.TECH_TEAM_ID
#     where_clause = "WHERE (Rescheduled_Appointments__c != null OR Appointment_Date__c != null) AND (LastModifiedDate >= %s AND LastModifiedDate <= %s) AND Status != 'Implemented' AND LastModifiedById != '%s'" % (start_date, end_date, tech_team_id)
#     sql_query = "select %s from Lead %s" % (select_items, where_clause)
#     try:
#         all_leads = sf.query_all(sql_query)
#         logging.info("Updating Leads count: %s " % (len(all_leads['records'])))
#         create_or_update_leads(all_leads['records'], sf)
#         update_sfdc_leads(all_leads['records'], sf)
#     except Exception as e:
#         print e
#         logging.info("Fail to get updated leads from %s to %s" % (start_date, end_date))
#         logging.info("%s" % (e))


@kronos.register('55 0 * * *')
def get_deleted_leads():
    """ Get Current Quarter updated Leads from SFDC """
    end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
    start_date = end_date - timedelta(days=29)
    logging.info("Current Quarted Deleted Leads from %s to %s" % (start_date, end_date))
    logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
    sf = SalesforceApi.connect_salesforce()
    if sf:
        logging.info("Connect Successfully")
        logging.info("Get Deleted leads form %s to %s" % (start_date, end_date))
        leads = sf.Lead.deleted(start_date, end_date)
        if leads:
            ids = [str(lid.get('id')) for lid in leads['deletedRecords']]
            ids = tuple(ids)
            logging.info("Deleted Lead Id's %s, Total = %s" % (ids, len(ids)))
            Leads.objects.filter(sf_lead_id__in=ids).delete()
            logging.info("Deleted Successfully")
        # start_date, end_date = get_quarter_date_slots(datetime.utcnow())
        # start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
        # end_date = end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        # portal_lead_ids = list(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date).values_list(
        #     'sf_lead_id', flat=True).distinct())
        # logging.info("No of Portal Leads on Current Quarter %s" % (len(portal_lead_ids)))
        # start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
        # end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
        # where_clause = "WHERE CreatedDate >= %s AND CreatedDate <= %s" % (start_date, end_date)
        # sql_query = "select Id from Lead %s" % (where_clause)
        # try:
        #     all_leads = sf.query_all(sql_query)
        #     logging.info("No of Lead Ids from %s to %s is: %s" % (start_date, end_date, len(all_leads['records'])))
        #     sf_lead_ids = [sf_id.get('Id') for sf_id in all_leads['records']]
        #     logging.info("No of Salesforce Leads on Current Quarter %s" % (len(sf_lead_ids)))
        #     if len(portal_lead_ids) > len(sf_lead_ids):
        #         extra_leads = set(portal_lead_ids) - set(sf_lead_ids)
        #         logging.info("No of Current Quarter leads deleted on portal %s" % (len(extra_leads)))
        #         Leads.objects.filter(sf_lead_id__in=list(extra_leads)).delete()
        # except Exception as e:
        #     print e
        #     logging.info("Fail to get leads from %s to %s" % (start_date, end_date))
        #     logging.info("%s" % (e))


def get_leads_from_sfdc(start_date, end_date):
    """ Get Leads from SFDC """
    # get SFDC Connection
    logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
    sf = SalesforceApi.connect_salesforce()

    logging.info("Connect Successfully")
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

        try:
            lead.ecommerce = int(rec.get('E-commerce'))
        except Exception:
            lead.ecommerce = 0

        lead.lead_owner_name = lead_owner_name if lead_owner_name else "%s %s" % (settings.DEFAULT_LEAD_OWNER_FNAME,
                                                                                  settings.DEFAULT_LEAD_OWNER_LNAME)
        lead.lead_owner_email = lead_owner_email if lead_owner_email else settings.DEFAULT_LEAD_OWNER_EMAIL
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

        # Rescheduled Appointments in IST
        rescheduled_appointment_in_ist = rec.get('Reschedule_IST__c')
        rescheduled_appointment_in_ist = SalesforceApi.salesforce_date_to_datetime_format(rescheduled_appointment_in_ist)
        lead.rescheduled_appointment_in_ist = rescheduled_appointment_in_ist

        time_zone = rec.get('Time_Zone__c') if rec.get('Time_Zone__c') else ''
        lead.time_zone = time_zone

        try:
            lead.dials = int(rec.get('qbdialer__Dials__c'))
        except Exception:
            lead.dials = 0

        lead.lead_sub_status = rec.get('Lead_Sub_Status__c')

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
            lead.wpp_treatment_type = rec.get('Treatment_Type__c') if rec.get('Treatment_Type__c') else 'Regalix Website Build Treatment'

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
            print lead.sf_lead_id, e
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


@kronos.register('30 * * * *')
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


# @kronos.register('*/30 * * * *')
# def get_appointment_and_rescheduled_leads():
#     """ Get appointment and rescheduled leads from SFDC """
#     end_date = datetime.now(pytz.UTC)    # we need to use UTC as salesforce API requires this
#     start_date = end_date - timedelta(days=20)
#     end_date = end_date + timedelta(days=7)
#     start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
#     end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
#     logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
#     sf = SalesforceApi.connect_salesforce()
#     if sf:
#         logging.info("Connect Successfully")
#         logging.info("Get Appointment and Rescheduled leads form %s to %s" % (start_date, end_date))
#         select_items = settings.SFDC_FIELDS
#         # select_items = "Id, Location__c, Time_Zone__c, Rescheduled_Appointments__c, Date_of_installation__c, Status"
#         where_clause = "WHERE (Rescheduled_Appointments__c != null OR Appointment_Date__c != null) AND (CreatedDate >= %s AND CreatedDate <= %s)"\
#             % (start_date, end_date)
#         sql_query = "select %s from Lead %s" % (select_items, where_clause)
#         try:
#             all_leads = sf.query_all(sql_query)
#             logging.info("No of Leads from %s to %s is: %s" % (start_date, end_date, len(all_leads['records'])))
#             update_sfdc_leads(all_leads['records'], sf)
#         except Exception as e:
#             print e
#             logging.info("Fail to get leads from %s to %s" % (start_date, end_date))
#             logging.info("%s" % (e))


def update_sfdc_leads(records, sf):
    """ Update Appointment and Rescheduled Appointment IN IST Time """
    sf.headers.update({"Sforce-Auto-Assign": 'FALSE'})
    logging.info("Updating Leads count on SFDC: %s" % (len(records)))
    for lead in records:
        location = lead.get('Location__c')
        time_zone = lead.get('Time_Zone__c')
        appointment_date = lead.get('Appointment_Date__c')
        appointment_in_ist = lead.get('IST_TIME_N__c')
        appointment_in_pst = lead.get('Appointment_Time_in_PST__c')
        rescheduled_appointment = lead.get('Rescheduled_Appointments__c')
        reschedule_in_ist = lead.get('Reschedule_IST_Time__c')
        sf_lead_id = lead.get('Id')
        appointment_date = SalesforceApi.salesforce_date_to_datetime_format(appointment_date)
        timezone = SalesforceApi.get_current_timezone_by_location(appointment_date, location, time_zone)
        appointment_in_ist = SalesforceApi.convert_appointment_to_timezone(appointment_date, timezone, 'IST')
        tz = SalesforceApi.get_current_timezone_of_salesforce()
        appointment_in_pst = SalesforceApi.convert_appointment_to_timezone(appointment_date, timezone, tz.zone_name)

        rescheduled_appointment = SalesforceApi.salesforce_date_to_datetime_format(rescheduled_appointment)
        timezone = SalesforceApi.get_current_timezone_by_location(rescheduled_appointment, location, time_zone)
        reschedule_in_ist = SalesforceApi.convert_appointment_to_timezone(rescheduled_appointment, timezone, 'IST')

        try:
            sf.Lead.update(sf_lead_id, {'Reschedule_IST__c': reschedule_in_ist,
                                        'IST_TIME_N__c': appointment_in_ist,
                                        'Appointment_Time_in_PST__c': appointment_in_pst})
        except Exception as e:
            print e
