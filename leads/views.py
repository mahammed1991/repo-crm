import os
import json
from datetime import datetime, timedelta
import requests

from xlrd import open_workbook, XL_CELL_DATE, xldate_as_tuple
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from django.conf import settings
from representatives.models import (
    GoogeRepresentatives,
    RegalixRepresentatives
)
from leads.models import Leads, Location, Team
from main.models import UserDetails
from lib.helpers import get_quarter_date_slots, send_mail, get_count_of_each_lead_status_by_rep
from icalendar import Calendar, Event, vCalAddress, vText
from django.core.files import File
#from django.db.models import Q


# Create your views here.
@login_required
@csrf_exempt
def lead_form(request):
    if request.method == 'POST':
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'

        # Get Basic/Common form filed data
        basic_data = get_common_lead_data(request.POST)
        basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None

        tag_data = basic_data
        tag_data['00Nd0000005WYhJ'] = request.POST.get('00Nd0000005WYhJ')  # Code Type
        tag_data['00Nd0000005WYhE'] = request.POST.get('00Nd0000005WYhE')  # URL1
        tag_data['00Nd0000005WYh9'] = request.POST.get('00Nd0000005WYh9')  # Code
        tag_data['00Nd0000005WZIe'] = request.POST.get('00Nd0000005WZIe')  # Comments

        tag_data['00Nd0000005WYkS'] = request.POST.get('00Nd0000005WYkS')  # Optional Code type
        tag_data['00Nd0000005WYi9'] = request.POST.get('00Nd0000005WYi9')  # Optional URL
        tag_data['00Nd0000005WYiv'] = request.POST.get('00Nd0000005WYiv')  # Optional Code
        tag_data['00Nd0000005WYjy'] = request.POST.get('00Nd0000005WYjy')  # Optional Comments
        tag_data['00Nd0000005WYlL'] = request.POST.get('tag_datepick')  # Appointment Date

        requests.request('POST', url=sf_api_url, data=tag_data)

        # Create Icallender (*.ics) file for send mail
        advirtiser_details = {'first_name': request.POST.get('first_name'),
                              'last_name': request.POST.get('last_name'),
                              'email': request.POST.get('00Nd0000005WcNw'),
                              'role': request.POST.get('00Nd0000005WayR'),
                              'customer_id': request.POST.get('00Nd0000005WYgV'),
                              'country': request.POST.get('00Nd0000005WYga'),
                              'appointment_date': request.POST.get('tag_datepick')
                              }
        if advirtiser_details.get('appointment_date'):
            create_icalendar_file(advirtiser_details)
            send_calendar_invite_to_advertiser(advirtiser_details)

        if request.POST.get('setup_lead_check'):
            setup_data = basic_data
            setup_data['00Nd0000005WYhJ'] = 'Google Shopping Setup',  # Code Type
            setup_data['00Nd00000077T9o'] = request.POST.get('00Nd00000077T9o')  # MC-ID
            setup_data['00Nd00000077T9t'] = request.POST.get('00Nd00000077T9t')  # Web Inventory
            setup_data['00Nd00000077T9y'] = request.POST.get('00Nd00000077T9y')  # Recommended Bid
            setup_data['00Nd00000077TA3'] = request.POST.get('00Nd00000077TA3')  # Recommended Budget
            setup_data['00Nd00000077TA8'] = request.POST.get('00Nd00000077TA8')  # Recommended Mobile Bid Modifier
            setup_data['00Nd0000005WYlL'] = request.POST.get('setup_datepick')  # Appointment Date

            requests.request('POST', url=sf_api_url, data=setup_data)

            # Create Icallender (*.ics) file for send mail
            advirtiser_details.update({'appointment_date': request.POST.get('setup_datepick')})
            if advirtiser_details.get('appointment_date'):
                create_icalendar_file(advirtiser_details)
                send_calendar_invite_to_advertiser(advirtiser_details)

        return redirect(basic_data['retURL'])

    locations = Location.objects.all()
    time_zone_for_region = dict()
    for loc in locations:
        time_zone_for_region[loc.location_name] = [{'zone_name': tz[
            'zone_name'], 'time_value': tz['time_value']} for tz in loc.time_zone.values()]

    teams = Team.objects.all()

    return render(
        request,
        'leads/lead_form.html',
        {'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID,
         'locations': locations,
         'teams': teams,
         'time_zone_for_region': json.dumps(time_zone_for_region)}
    )


@login_required
@csrf_exempt
def shopping_campaign_setup_lead_form(request):

    if request.method == 'POST':
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'

        # Get Basic/Common form filed data
        basic_data = get_common_lead_data(request.POST)
        basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None

        setup_data = basic_data
        setup_data['00Nd0000005WYhJ'] = 'Google Shopping Setup',  # Code Type
        setup_data['00Nd00000077T9o'] = request.POST.get('00Nd00000077T9o')  # MC-ID
        setup_data['00Nd00000077T9t'] = request.POST.get('00Nd00000077T9t')  # Web Inventory
        setup_data['00Nd00000077T9y'] = request.POST.get('00Nd00000077T9y')  # Recommended Bid
        setup_data['00Nd00000077TA3'] = request.POST.get('00Nd00000077TA3')  # Recommended Budget
        setup_data['00Nd00000077TA8'] = request.POST.get('00Nd00000077TA8')  # Recommended Mobile Bid Modifier
        setup_data['00Nd0000005WYlL'] = request.POST.get('00Nd0000005WYlL')  # Appointment Date

        requests.request('POST', url=sf_api_url, data=setup_data)

        # Create Icallender (*.ics) file for send mail
        advirtiser_details = {'first_name': request.POST.get('first_name'),
                              'last_name': request.POST.get('last_name'),
                              'phone': request.POST.get('phone'),
                              'email': request.POST.get('00Nd0000005WcNw'),
                              'role': request.POST.get('00Nd0000005WayR'),
                              'customer_id': request.POST.get('00Nd0000005WYgV'),
                              'country': request.POST.get('00Nd0000005WYga'),
                              'language': request.POST.get('00Nd0000007clUn'),
                              'time_zone': request.POST.get('00Nd0000005WYhT'),
                              'appointment_date': request.POST.get('00Nd0000005WYlL')
                              }
        if advirtiser_details.get('appointment_date'):
            create_icalendar_file(advirtiser_details)
            send_calendar_invite_to_advertiser(advirtiser_details)

    locations = Location.objects.all()
    time_zone_for_region = dict()
    for loc in locations:
        time_zone_for_region[loc.location_name] = [{'zone_name': tz[
            'zone_name'], 'time_value': tz['time_value']} for tz in loc.time_zone.values()]

    return render(
        request,
        'leads/pla_lead_form.html',
        {'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID,
         'locations': locations,
         'process_type': 'SHOPPING',
         'time_zone_for_region': json.dumps(time_zone_for_region)}
    )


def get_common_lead_data(post_data):
    """ Get basic data from both lead forms """

    basic_data = {
        '00Nd0000005WYgk': post_data.get('00Nd0000005WYgk'),  # Full Name
        'email': post_data.get('email'),                      # Rep Email
        '00Nd00000075Crj': post_data.get('00Nd00000075Crj'),  # Manager Name
        '00Nd00000077r3s': post_data.get('00Nd00000077r3s'),  # Manager Email
        '00Nd0000005WYgV': post_data.get('00Nd0000005WYgV'),  # Customer ID
        '00Nd0000005WaHr': post_data.get('00Nd0000005WaHr'),  # E-commerce
        'company': post_data.get('company'),  # Company
        '00Nd0000005XIWB': post_data.get('00Nd0000005XIWB'),  # Team
        '00Nd0000007e2AF': post_data.get('00Nd0000007e2AF'),  # Service Segment
        '00Nd0000005WYga': post_data.get('00Nd0000005WYga'),  # Country
        '00Nd0000007clUn': post_data.get('00Nd0000007clUn'),  # Language
        '00Nd0000005WYhT': post_data.get('00Nd0000005WYhT'),  # Time Zone
        'first_name': post_data.get('first_name'),  # First Name
        'last_name': post_data.get('last_name'),  # Last Name
        'phone': post_data.get('phone'),  # Phone
        '00Nd0000005WcNw': post_data.get('00Nd0000005WcNw'),  # Mandatory Email
        '00Nd0000005WayR': post_data.get('00Nd0000005WayR'),  # Role
        '00Nd0000005Wayb': post_data.get('00Nd0000005Wayb'),  # Established Contact
        '00Nd0000005WYgp': post_data.get('00Nd0000005WYgp'),  # Optional First Name
        '00Nd0000005WYgu': post_data.get('00Nd0000005WYgu'),  # Optional Last Name
        '00Nd0000005WYgz': post_data.get('00Nd0000005WYgz'),  # Optional Phone
        '00Nd0000005WYh4': post_data.get('00Nd0000005WYh4'),  # Optional Email
        '00Nd0000005WayW': post_data.get('00Nd0000005WayW'),  # Optional Role
        '00Nd0000005Wayg': post_data.get('00Nd0000005Wayg'),  # Optional Establised Contact
        'description': post_data.get('description'),
        'Campaign_ID': post_data.get('Campaign_ID'),
        'oid': post_data.get('oid'),
        '__VIEWSTATE': post_data.get('__VIEWSTATE'),
    }

    return basic_data


@login_required
def shopping_campaign_lead_form(request):
    return redirect('main.views.home')


@login_required
def leads_list(request):
    """ List All leads form Database """
    users = GoogeRepresentatives.objects.all().values_list(
        'first_name',
        'last_name',
        'email',
        flat=False
    ).distinct().order_by('first_name')

    return render(request, 'leads/lead_status.html', {'users': users})


@login_required
def leads_report(request):
    """ List selected leads report form Database """
    rep_email = request.POST.get('rep_email')
    quarter_start_date, quarter_end_date = get_quarter_date_slots(datetime.utcnow())

    # get all leads for user for the current quarter
    leads = Leads.objects.filter(google_rep_email=rep_email, created_date__range=(quarter_start_date, quarter_end_date))
    leads_count = Leads.objects.filter(
        google_rep_email=rep_email,
        created_date__range=(quarter_start_date, quarter_end_date)).values('lead_status').annotate(lcount=Count('lead_status'))
    return render(request, 'leads/leads_report.html', {'leads': leads, 'leads_count': leads_count})


@login_required
def thankyou(request):
    """ Thank user after sucessful submitting form to salesforce """
    redirect_page = request.GET.get('n', reverse('main.views.home'))
    redirect_page_source = {
        '1': reverse('leads.views.lead_form'),
        '2': reverse('leads.views.shopping_campaign_setup_lead_form'),
    }

    if redirect_page in redirect_page_source.keys():
        redirect_page = redirect_page_source[redirect_page]

    return render(request, 'leads/thankyou.html', {'return_link': redirect_page, 'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID})


@login_required
def day_light_changes(request):
    return render(request, 'leads/day_light_change.html')


@login_required
def manage_leads(request):
    """ upload and load leads to view """
    template_args = dict({'migrate_type': None})
    if request.method == 'POST':
        migrate_type = request.POST.get('migrate_type')
        if request.FILES:
            excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
            if not os.path.exists(excel_file_save_path):
                os.makedirs(excel_file_save_path)
            excel_file = request.FILES['file']
            # excel sheet data
            excel_data = list()

            # Check file extension type
            # require only .xlsx file
            if excel_file.name.split('.')[1] != 'xlsx':
                template_args.update({'excel_data': [], 'excel_file': excel_file.name, 'error': 'Please upload .xlsx file'})
                return render(request, 'leads/manage_leads.html', template_args)

            file_name = 'leads_data.xls'
            excel_file_path = excel_file_save_path + file_name
            with open(excel_file_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)
                destination.close()

            workbook = open_workbook(excel_file_path)

            sheet = workbook.sheet_by_index(0)

            for row_index in range(sheet.nrows):
                # read each row
                excel_row_data = list()
                for col_index in range(sheet.ncols):
                    # check each column for date type
                    cell_type = sheet.cell_type(row_index, col_index)
                    cell_value = sheet.cell_value(row_index, col_index)

                    # if column is formatted as datetype, convert to datetime object
                    # otherwise show column as is
                    if cell_type == XL_CELL_DATE:
                        dt_tuple = xldate_as_tuple(cell_value, workbook.datemode)
                        cell_dt = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
                        cell_dt = datetime.strftime(cell_dt, '%m/%d/%Y')
                        excel_row_data.append(cell_dt)
                    else:
                        excel_row_data.append(cell_value)

                # append row data to excel sheet data
                excel_data.append(excel_row_data)

            template_args.update({'excel_data': excel_data, 'excel_file': file_name, 'migrate_type': migrate_type})
    return render(request, 'leads/manage_leads.html', template_args)


def get_col_index(sheet, col_name):
    for col_index in range(sheet.ncols):
        col_val = sheet.cell(0, col_index).value
        if col_name == col_val:
            return col_index


@login_required
def upload_leads(request):
    """ save leads to server Database from uploaded file"""
    excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
    excel_file = request.POST['file']
    excel_file_path = excel_file_save_path + excel_file

    workbook = open_workbook(excel_file_path)
    sheet = workbook.sheet_by_index(0)

    for r_i in range(1, sheet.nrows):

        # Google Representative email and name
        rep_email = sheet.cell(r_i, get_col_index(sheet, 'Email')).value
        rep_name = unicode(sheet.cell(r_i, get_col_index(sheet, 'Google Account Manager')).value)

        # Lead owner name
        lead_owner_name = unicode(sheet.cell(r_i, get_col_index(sheet, 'Lead Owner')).value)
        lead_owner_email = unicode(sheet.cell(r_i, get_col_index(sheet, 'Regalix E-mails')).value)

        # Team
        team = sheet.cell(r_i, get_col_index(sheet, 'Team')).value

        sf_lead_id = sheet.cell(r_i, get_col_index(sheet, 'Lead ID')).value
        try:
            # check for existing lead
            lead = Leads.objects.get(sf_lead_id=sf_lead_id)
        except ObjectDoesNotExist:
            # create new lead
            lead = Leads()

        # Below information will be created if its a new lead or else the information will be updated
        lead.google_rep_name = rep_name
        lead.google_rep_email = rep_email

        if rep_email:
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
        col_type = sheet.cell_type(r_i, get_col_index(sheet, 'Create Date'))
        col_value = sheet.cell_value(r_i, get_col_index(sheet, 'Create Date'))
        if col_type == XL_CELL_DATE:
            dt_tuple = xldate_as_tuple(col_value, workbook.datemode)
            col_value = datetime(dt_tuple[0],
                                 dt_tuple[1],
                                 dt_tuple[2],
                                 dt_tuple[3],
                                 dt_tuple[4],
                                 dt_tuple[5]
                                 )
        else:
            try:
                col_value = datetime.strptime(col_value, '%m/%d/%Y')
            except Exception:
                col_value = datetime.utcnow()

        lead.created_date = col_value

        try:
            lead.ecommerce = int(sheet.cell(r_i, get_col_index(sheet, 'E-commerce')).value)
        except Exception:
            lead.ecommerce = 0

        lead.lead_owner_name = lead_owner_name
        lead.lead_owner_email = lead_owner_email
        lead.company = unicode(sheet.cell(r_i, get_col_index(sheet, 'Company / Account')).value)
        lead.lead_status = sheet.cell(r_i, get_col_index(sheet, 'Lead Status')).value
        lead.country = sheet.cell(r_i, get_col_index(sheet, 'Location')).value

        cid_index = get_col_index(sheet, 'Customer ID')
        if type(sheet.cell(r_i, cid_index).value) is float:
            lead.customer_id = int(sheet.cell(r_i, cid_index).value)
        else:
            lead.customer_id = sheet.cell(r_i, cid_index).value
        lead.first_name = unicode(sheet.cell(r_i, get_col_index(sheet, 'First Name')).value)
        lead.last_name = unicode(sheet.cell(r_i, get_col_index(sheet, 'Last Name')).value)
        lead.phone = sheet.cell(r_i, get_col_index(sheet, 'Phone')).value

        lead.first_name_optional = sheet.cell(r_i, get_col_index(sheet, 'First Name - optional')).value
        lead.last_name_optional = sheet.cell(r_i, get_col_index(sheet, 'Last Name - optional')).value
        lead.phone_optional = sheet.cell(r_i, get_col_index(sheet, 'Phone - optional')).value
        lead.email_optional = sheet.cell(r_i, get_col_index(sheet, 'Email - optional')).value

        # check if column is formatted to date type
        # if it is of date type, convert to datetime object
        doi_index = get_col_index(sheet, 'Date of installation')
        doi_type = sheet.cell_type(r_i, doi_index)
        doi_value = sheet.cell_value(r_i, doi_index)
        if doi_type == XL_CELL_DATE:
            dt_tuple = xldate_as_tuple(doi_value, workbook.datemode)
            doi_value = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
        else:
            try:
                doi_value = datetime.strptime(doi_value, '%m/%d/%Y')
            except Exception:
                doi_value = None

        lead.date_of_installation = doi_value

        appointment_index = get_col_index(sheet, 'Appointment Date')
        appointment_type = sheet.cell_type(r_i, appointment_index)
        appointment_value = sheet.cell_value(r_i, appointment_index)
        if appointment_type == XL_CELL_DATE:
            dt_tuple = xldate_as_tuple(appointment_value, workbook.datemode)
            appointment_value = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
        else:
            try:
                appointment_value = datetime.strptime(appointment_value, '%m/%d/%Y %I:%M %p')
            except Exception:
                appointment_value = None

        lead.appointment_date = appointment_value

        fco_index = get_col_index(sheet, '1st Contacted on')
        fco_type = sheet.cell_type(r_i, fco_index)
        fco_value = sheet.cell_value(r_i, fco_index)
        if fco_type == XL_CELL_DATE:
            dt_tuple = xldate_as_tuple(fco_value, workbook.datemode)
            fco_value = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
        else:
            try:
                fco_value = datetime.strptime(fco_value, '%m/%d/%Y %I:%M %p')
            except Exception:
                fco_value = None

        lead.first_contacted_on = fco_value

        # Rescheduled Appointments
        r_apppintment_index = get_col_index(sheet, 'Rescheduled Appointments')
        r_apppintment_type = sheet.cell_type(r_i, r_apppintment_index)
        r_apppintment_value = sheet.cell_value(r_i, r_apppintment_index)
        if r_apppintment_type == XL_CELL_DATE:
            dt_tuple = xldate_as_tuple(r_apppintment_value, workbook.datemode)
            r_apppintment_value = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
        else:
            try:
                r_apppintment_value = datetime.strptime(r_apppintment_value, '%m/%d/%Y %I:%M %p')
            except Exception:
                r_apppintment_value = None

        lead.rescheduled_appointment = r_apppintment_value
        try:
            lead.dials = int(sheet.cell(r_i, get_col_index(sheet, 'Dials')).value)
        except Exception:
            lead.dials = 0
        lead.lead_sub_status = sheet.cell(r_i, get_col_index(sheet, 'Lead Sub-Status')).value

        lead.time_zone = sheet.cell(r_i, get_col_index(sheet, 'Time Zone')).value

        lead.regalix_comment = unicode(sheet.cell(r_i, get_col_index(sheet, 'Regalix Comment')).value).encode('unicode_escape')
        lead.google_comment = unicode(sheet.cell(r_i, get_col_index(sheet, 'Google Comment')).value).encode('unicode_escape')

        lead.code_1 = sheet.cell(r_i, get_col_index(sheet, 'Code')).value
        lead.url_1 = sheet.cell(r_i, get_col_index(sheet, 'URL')).value
        lead.type_1 = sheet.cell(r_i, get_col_index(sheet, 'Code Type')).value
        lead.comment_1 = sheet.cell(r_i, get_col_index(sheet, 'Comment 1')).value

        lead.team = team
        lead.sf_lead_id = sf_lead_id
        lead.save()

    return redirect('leads.views.manage_leads')


def get_lead(request, cid):
    """ Get lead information """
    lead = {'status': 'FAILED', 'details': None}
    leads = Leads.objects.filter(customer_id=cid)
    team = Team.objects.get(team_name=leads[0].team)
    if leads:
        lead['status'] = 'SUCCESS'

        lead['details'] = {
            'name': leads[0].first_name + ' ' + leads[0].last_name,
            'email': leads[0].lead_owner_email,
            'location': leads[0].country,
            'team': team.team_name,
            'team_id': team.id
        }
    return HttpResponse(json.dumps(lead), content_type='application/json')


# Data migration
def migrate_leads(request):
    """ Update leads to server Database from uploaded file """
    excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
    excel_file = request.POST['file']
    migrate_type = request.POST['migrate_type']
    excel_file_path = excel_file_save_path + excel_file

    workbook = open_workbook(excel_file_path)
    sheet = workbook.sheet_by_index(0)

    for r_i in range(1, sheet.nrows):

        sf_lead_id = sheet.cell(r_i, get_col_index(sheet, 'Lead ID')).value
        try:
            # check for existing lead
            lead = Leads.objects.get(sf_lead_id=sf_lead_id)

            if migrate_type == 'reshedule':
                # Rescheduled Appointments
                r_apppintment_index = get_col_index(sheet, 'Rescheduled Appointments')
                r_apppintment_type = sheet.cell_type(r_i, r_apppintment_index)
                r_apppintment_value = sheet.cell_value(r_i, r_apppintment_index)
                if r_apppintment_type == XL_CELL_DATE:
                    dt_tuple = xldate_as_tuple(r_apppintment_value, workbook.datemode)
                    r_apppintment_value = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
                else:
                    try:
                        r_apppintment_value = datetime.strptime(r_apppintment_value, '%m/%d/%Y %I:%M %p')
                    except Exception:
                        r_apppintment_value = None
                try:
                    lead.dials = int(sheet.cell(r_i, get_col_index(sheet, 'Dials')).value)
                except Exception:
                    lead.dials = 0
                lead.lead_sub_status = sheet.cell(r_i, get_col_index(sheet, 'Lead Sub-Status')).value
                lead.rescheduled_appointment = r_apppintment_value
                lead.save()

        except ObjectDoesNotExist:
            continue

    return redirect('leads.views.manage_leads')


def create_icalendar_file(advirtiser_details):
    """ Create Calender ICS file for appointment slot """

    cal = Calendar()

    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', 'Appointment Slot')

    # Appointment slot Date formate: "11/20/2014 10:00 AM"
    appointment_date = datetime.strptime(advirtiser_details['appointment_date'], "%m/%d/%Y %H:%M %p")
    event.add('dtstart', appointment_date)
    event.add('dtend', appointment_date + timedelta(minutes=30))
    event.add('dtstamp', appointment_date)
    event['location'] = vText(advirtiser_details['country'])
    event['uid'] = advirtiser_details['customer_id']

    organizer = vCalAddress('MAILTO:rajuk@regalix-inc.com.com')
    organizer.params['cn'] = vText('Regalix')
    organizer.params['ROLE'] = vText('REQ-PARTICIPANT')
    event.add('organizer', organizer)

    attendee = vCalAddress('MAILTO:%s' % (advirtiser_details['email']))
    attendee.params['cn'] = vText("%s %s" % (advirtiser_details['first_name'], advirtiser_details['last_name']))
    attendee.params['role'] = vText(advirtiser_details['role'])
    event.add('attendee', attendee, encode=0)

    cal.add_component(event)

    cal.to_ical()

    ics_file_save_path = settings.MEDIA_ROOT + '/icallender_files/'
    if not os.path.exists(ics_file_save_path):
        os.makedirs(ics_file_save_path)
    ics_file_path = ics_file_save_path + 'appointment.ics'
    f = open(ics_file_path, 'wb')
    f.write(cal.to_ical())
    f.close()


def send_calendar_invite_to_advertiser(advertiser_details):
    mail_subject = "Google Tag Implementation Support Appointment Confirmation"

    mail_body = get_template('leads/advertiser_mail/appointment_confirmation.html').render(
        Context({
            'text': "Google Tag Implementation Support Appointment Confirmation",
            'first_name': advertiser_details.get('first_name'),
            'last_name': advertiser_details.get('last_name')
        })
    )

    bcc = set()

    mail_to = set([
        advertiser_details['email'],
    ])

    mail_from = "implementation-support@google.com"

    ics_file = open(settings.MEDIA_ROOT + '/icallender_files/appointment.ics', 'r')

    appointment_file = File(ics_file)
    appointment_file.name = 'appointment.ics'

    attachments = list()

    attachments.append(appointment_file)

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

    return 'Success'


@login_required
def get_lead_summary(request):
    """ Lead Status page """

    lead_status = ['In Queue', 'Attempting Contact', 'In Progress', 'In Active', 'Implemented']
    email = request.user.email
    email = 'bhavinb@google.com'
    if 'regalix' in email:
        leads = Leads.objects.filter(lead_status__in=lead_status, lead_owner_email=email)
    elif 'google' in email:
        leads = Leads.objects.filter(lead_status__in=lead_status, google_rep_email=email)

    lead_status_dict = get_count_of_each_lead_status_by_rep(email, start_date=None, end_date=None)

    return render(request, 'leads/lead_summary.html', {'leads': leads, 'lead_status_dict': lead_status_dict})
