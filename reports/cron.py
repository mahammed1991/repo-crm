import kronos
from reports.report_services import ReportService
from django.conf import settings
from datetime import datetime
from lib.helpers import get_quarter_date_slots
from reports.models import LeadSummaryReports
import logging
from lib.salesforce import connect_salesforce
from leads.models import Leads
from django.core.exceptions import ObjectDoesNotExist

logging.basicConfig(filename='/tmp/cronjob.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%d/%b/%Y %H:%M:%S',
                    level=logging.DEBUG)


@kronos.register('0 * * * *')
def get_current_quarter_summary():
    logging.info("Initializing kronos")
    # Get all teams
    teams = ReportService.get_all_teams()

    # get all code types
    code_types = ReportService.get_all_code_type()

    # get all lead status
    lead_status = settings.LEAD_STATUS
    lead_status.extend(['Pending QC - DEAD LEAD', 'Pending QC - WIN', 'Rework Required', 'Appointment Set (GS)'])

    # get current quarter
    dt = datetime.now()
    start_date, end_date = get_quarter_date_slots(dt)
    logging.info("Get Current Quarter Report from %s to %s" % (datetime.strftime(start_date, "%d %b %Y"), datetime.strftime(end_date, "%d %b %Y")))

    # get all locations
    locations = ReportService.get_all_locations()
    reports = ReportService.get_summary_by_code_types_and_status('all', code_types, lead_status,
                                                                 start_date, end_date, teams, locations)
    code_type = reports.keys()
    for k in code_type:
        current_quarter = LeadSummaryReports.objects.filter(code_type=k)
        if current_quarter:
            current_quarter.code_type = k
            current_quarter.total_leads = reports[k]['total_leads']
            current_quarter.win = reports[k]['wins']
            current_quarter.implemented = reports[k]['Implemented']
            if 'In Queue' in reports[k]:
                current_quarter.in_queue = reports[k]['In Queue'] + reports[k].get('Appointment Set (GS)', 0)
            else:
                current_quarter.in_queue = 0

            if 'In Progress' in reports[k]:
                current_quarter.in_progress = reports[k]['In Progress'] + reports[k].get('Pending QC - DEAD LEAD', 0) \
                    + reports[k].get('Pending QC - WIN', 0) + reports[k].get('Rework Required', 0)
            else:
                current_quarter.in_progress = 0
            current_quarter.tat_implemented = reports[k]['tat_implemented']
            current_quarter.tat_first_contacted = reports[k]['tat_first_contacted']
            current_quarter.start_date = start_date
            current_quarter.end_date = end_date
            current_quarter.update()
        else:
            current_quarter = LeadSummaryReports()
            current_quarter.code_type = k
            current_quarter.total_leads = reports[k]['total_leads']
            current_quarter.win = reports[k]['wins']
            current_quarter.implemented = reports[k]['Implemented']
            if 'In Queue' in reports[k]:
                current_quarter.in_queue = reports[k]['In Queue'] + reports[k].get('Appointment Set (GS)', 0)
            else:
                current_quarter.in_queue = 0

            if 'In Progress' in reports[k]:
                current_quarter.in_progress = reports[k]['In Progress'] + reports[k].get('Pending QC - DEAD LEAD', 0) \
                    + reports[k].get('Pending QC - WIN', 0) + reports[k].get('Rework Required', 0)
            else:
                current_quarter.in_progress = 0
            current_quarter.tat_implemented = reports[k]['tat_implemented']
            current_quarter.tat_first_contacted = reports[k]['tat_first_contacted']
            current_quarter.start_date = start_date
            current_quarter.end_date = end_date
            current_quarter.save()
    logging.info("Cron job done")


@kronos.register('0 * * * *')
def get_leads_from_sfdc():
    """ Get Leads from SFDC """
    """
    # get SFDC Connection
    sf = connect_salesforce()

    lead_fields = ['Id', 'LastName', 'FirstName', 'Name', 'Company', 'Phone', 'Email', 'Description',
                   'Status', 'OwnerId', 'CreatedDate', 'LastModifiedDate', 'gm_email__c', 'X1st_Contact_on__c',
                   'Customer_ID__c', 'First_Name_optional__c', 'Last_Name_optional__c', 'Phone_optional__c',
                   'Email_optional__c', 'Code__c', 'URL__c', 'Code_Type__c', 'Regalix_Comment__c', 'Rescheduled_Appointments__c',
                   'Time_Zone__c', 'Google_Comment__c', 'Code_2__c', 'Code_3__c', 'Code_4__c', 'Code_5__c',
                   'URL_2__c', 'URL_3__c', 'URL_4__c', 'URL_5__c', 'Comment_2__c', 'Comment_3__c', 'Comment_4__c'
                   'Comment_5__c', 'Type_2__c', 'Type_3__c', 'Type_4__c', 'Type_5__c', 'Appointment_Date__c', 'Lead_Sub_Status__c',
                   'qbdialer__Dials__c', 'Comment_1__c', 'E_commerce__c', 'Location__c', 'Primary_Contact_Email__c', 'Google_Rep__c',
                   'Date_of_installation__c', 'Team__c', 'Type_Of_Installation__c', 'Lead_Implemented_Date_Time__c']

    select_items = ", ".join(lead_fields)
    where_clause = "where CreatedDate >= '2015-03-01' and CreatedDate <= '2015-03-25'"
    sql_query = "select %s from Lead %s" % (select_items, where_clause)
    # get_leads = sf.query(sql_query)
    get_leads = sf.query("select Id, LastName, FirstName, Name, Company, Phone, Email, Description, Status, CreatedDate,\
        gm_email__c, Customer_ID__c, First_Name_optional__c, Last_Name_optional__c, Phone_optional__c, Email_optional__c,\
        Code__c, URL__c, Code_Type__c, Regalix_Comment__c, Google_Comment__c, Code_2__c, Code_3__c, Code_4__c, Code_5__c,\
        URL_2__c, URL_3__c, URL_4__c, URL_5__c, Comment_2__c, Comment_3__c, Comment_4__c, Comment_5__c, Type_2__c, Type_3__c,\
        Type_4__c, Type_5__c, Appointment_Date__c, qbdialer__Dials__c, Comment_1__c, E_commerce__c, Location__c, X1st_Contact_on__c,\
        Primary_Contact_Email__c, Google_Rep__c, Date_of_installation__c, Team__c, Type_Of_Installation__c, Lead_Implemented_Date_Time__c\
        Rescheduled_Appointments__c, Time_Zone__c, Lead_Sub_Status__c from Lead")

    for rec in get_leads['records']:
        sf_lead_id = rec.get('Id')

        try:
            # check for existing lead
            lead = Leads.objects.get(sf_lead_id=sf_lead_id)
        except ObjectDoesNotExist:
            # create new lead
            lead = Leads()

        # Google Representative email and name
        rep_email = rec.get('Email')
        rep_name = rec.get('Google_Rep__c')

        # Lead owner name
        lead_owner_name = rec.get('Name')
        lead_owner_email = rec.get('gm_email__c')

        # Team
        team = rec.get('Team__c')

        # Below information will be created if its a new lead or else the information will be updated
        lead.google_rep_name = rep_name
        lead.google_rep_email = rep_email

        # if rep_email:
        #     # Save Google representatives information to Database
        #     try:
        #         GoogeRepresentatives.objects.get(email=rep_email)
        #     except ObjectDoesNotExist:
        #         google_rep = GoogeRepresentatives()
        #         rep_name = rep_name.split(' ')
        #         google_rep.first_name = unicode(rep_name[0])
        #         google_rep.last_name = unicode((' ').join(rep_name[1:]))
        #         google_rep.email = unicode(rep_email)
        #         google_rep.team = team
        #         google_rep.save()

        # # Save Regalix representatives information to Database
        # try:
        #     RegalixRepresentatives.objects.get(email=lead_owner_email)
        # except ObjectDoesNotExist:
        #     regalix_rep = RegalixRepresentatives()
        #     regalix_rep.name = lead_owner_name
        #     regalix_rep.email = lead_owner_email
        #     regalix_rep.team = team
        #     regalix_rep.save()

        # check if column is formatted to date type
        # if it is of date type, convert to datetime object
        created_date = rec.get('CreateDate')
        created_date = get_valid_date(created_date)
        if not created_date:
            created_date = datetime.utcnow()

        lead.created_date = created_date

        try:
            lead.ecommerce = int(rec.get('E-commerce'))
        except Exception:
            lead.ecommerce = 0

        lead.lead_owner_name = lead_owner_name
        lead.lead_owner_email = lead_owner_email
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
        date_of_installation = get_valid_date(date_of_installation)
        lead.date_of_installation = date_of_installation

        appointment_date = rec.get('Appointment_Date__c')
        appointment_date = get_valid_date(appointment_date)
        lead.appointment_date = appointment_date

        first_contacted_on = rec.get('X1st_Contact_on__c')
        first_contacted_on = get_valid_date(first_contacted_on)
        lead.first_contacted_on = first_contacted_on

        # Rescheduled Appointments
        rescheduled_appointment = rec.get('Rescheduled_Appointments__c')
        rescheduled_appointment = get_valid_date(rescheduled_appointment)
        lead.rescheduled_appointment = rescheduled_appointment

        try:
            lead.dials = int(rec.get('qbdialer__Dials__c'))
        except Exception:
            lead.dials = 0

        lead.lead_sub_status = rec.get('Lead_Sub_Status__c')

        lead.time_zone = rec.get('Time_Zone__c')

        lead.regalix_comment = unicode(rec.get('Regalix_Comment__c')).encode('unicode_escape')
        lead.google_comment = unicode(rec.get('Google_Comment__c')).encode('unicode_escape')

        lead.code_1 = rec.get('Code__c')
        lead.url_1 = rec.get('URL__c')
        lead.type_1 = rec.get('Type__c')
        lead.comment_1 = rec.get('Comment_1__c')

        lead.team = team
        lead.sf_lead_id = sf_lead_id
        lead.save()
    """


def get_valid_date(_date):
    """ Get Formatted date to save in db """

    date_format = None
    if _date:
        try:
            date_format = datetime.strptime(_date, '%m/%d/%Y %I:%M %p')
        except Exception:
            try:
                date_format = datetime.strptime(_date, '%m/%d/%Y')
            except Exception:
                date_format = None
    else:
        date_format = None

    return date_format
