import os
import json
from datetime import datetime, timedelta
import requests
import csv
from uuid import uuid4
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
from leads.models import Leads, Location, Team, CodeType, ChatMessage, Language, ContactPerson, AgencyDetails
from main.models import UserDetails
from lib.helpers import (get_quarter_date_slots, send_mail, get_count_of_each_lead_status_by_rep,
                         is_manager, get_user_list_by_manager, get_manager_by_user)
from icalendar import Calendar, Event, vCalAddress, vText
from django.core.files import File
from django.contrib.auth.models import User
from reports.report_services import ReportService, DownloadLeads
from lib.helpers import date_range_by_quarter
from django.db.models import Q
from random import randint


# Create your views here.
@login_required
@csrf_exempt
def lead_form(request):

    """
    Production OID
    <input type="hidden" value="00Dd0000000fk18" name="oid">

    Sandbox OID
    <input type=hidden name="oid" value="00Dq00000009tyR">
    """
    if request.method == 'POST':
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        # sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'

        # Get Basic/Common form filed data
        basic_data = get_common_lead_data(request.POST)
        basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None

        tag_data = basic_data
        advirtiser_details = {'first_name': request.POST.get('advertiser_name'),
                              'last_name': request.POST.get('last_name'),
                              'email': request.POST.get('aemail'),
                              'role': request.POST.get('primary_role'),
                              'customer_id': request.POST.get('cid'),
                              'country': request.POST.get('country'),
                              'cid_std': request.POST.get('cid').rsplit("-", 1)[0] + '-xxxx',
                              'code_type': request.POST.get('ctype1')
                              }

        if request.POST.get('is_tag_lead') == 'yes':

            tag_data['00Nd0000005WYlL'] = request.POST.get('tag_datepick'),  # TAG Appointment Date
            if request.POST.get('tag_contact_person_name'):
                tag_data['first_name'] = request.POST.get('tag_contact_person_name').rsplit(' ', 1)[0],  # Primary Contact Name
                tag_data['last_name'] = request.POST.get('tag_contact_person_name').rsplit(' ', 1)[1] if len(request.POST.get('tag_contact_person_name').rsplit(' ', 1)) > 1 else '',
            tag_data['00Nd0000005WayR'] = request.POST.get('tag_primary_role'),  # Role

            # Code Type 1 Details
            tag_data['00Nd0000005WYhJ'] = request.POST.get('ctype1')  # Code Type1
            tag_data['00Nd0000005WYhE'] = request.POST.get('url1')  # URL1
            tag_data['00Nd0000005WYh9'] = request.POST.get('code1')  # Code1
            tag_data['00Nd0000005WZIe'] = request.POST.get('comment1')  # Comments1

            # Code Type 2 Details
            tag_data['00Nd0000005WYkS'] = request.POST.get('ctype2')  # Code type2
            tag_data['00Nd0000005WYi9'] = request.POST.get('url2')  # URL2
            tag_data['00Nd0000005WYiv'] = request.POST.get('code2')  # Code2
            tag_data['00Nd0000005WYjy'] = request.POST.get('comment2')  # Comments2

            # Code Type 3 Details
            tag_data['00Nd0000005WYkX'] = request.POST.get('ctype3')  # Code type3
            tag_data['00Nd0000005WYjU'] = request.POST.get('url3')  # URL3
            tag_data['00Nd0000005WYj5'] = request.POST.get('code3')  # Code3
            tag_data['00Nd0000005WYjB'] = request.POST.get('comment3')  # Comments3

            # Code Type 4 Details
            tag_data['00Nd0000005WYkm'] = request.POST.get('ctype4')  # Code type4
            tag_data['00Nd0000005WYjZ'] = request.POST.get('url4')  # URL4
            tag_data['00Nd0000005WYjA'] = request.POST.get('code4')  # Code4
            tag_data['00Nd0000005WYkI'] = request.POST.get('comment4')  # Comments4

            # Code Type 5 Details
            tag_data['00Nd0000005WYl6'] = request.POST.get('ctype5')  # Code type5
            tag_data['00Nd0000005WYjo'] = request.POST.get('url5')  # URL5
            tag_data['00Nd0000005WYiw'] = request.POST.get('code5')  # Code5
            tag_data['00Nd0000005WYkN'] = request.POST.get('comment5')  # Comments5

            # Production ID for TAD VIA GTM
            # tag_data['00Nd0000007esIr'] = request.POST.get('tag_via_gtm')  # Tag Via  GTM

            # Sandbox ID for TAD VIA GTM
            tag_data['00Nq0000000eZP6'] = request.POST.get('tag_via_gtm')  # Tag Via  GTM
            requests.request('POST', url=sf_api_url, data=tag_data)

            # Create Icallender (*.ics) file for send mail
            advirtiser_details.update({'appointment_date': request.POST.get('tag_datepick')})

            # if advirtiser_details.get('appointment_date'):
            # create_icalendar_file(advirtiser_details)
            # send_calendar_invite_to_advertiser(advirtiser_details)

        if request.POST.get('is_shopping_lead') == 'yes':
            setup_data = basic_data
            if request.POST.get('shop_contact_person_name'):
                full_name = request.POST.get('shop_contact_person_name')
                first_name = full_name.rsplit(' ', 1)[0]
                last_name = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else ''
                setup_data['first_name'] = first_name  # Primary Contact First Name
                setup_data['last_name'] = last_name  # Primary Contact Last Name
            setup_data['00Nd0000005WayR'] = request.POST.get('shop_primary_role'),  # Role
            setup_data['00Nd0000005WYlL'] = request.POST.get('setup_datepick')  # Shopping Appointment Date
            setup_data['00Nd0000005WYhJ'] = u'Google Shopping Setup'  # Code Type
            setup_data['00Nd00000077T9o'] = request.POST.get('00Nd00000077T9o')  # MC-ID
            setup_data['00Nd00000077T9t'] = request.POST.get('00Nd00000077T9t')  # Web Inventory
            setup_data['00Nd00000077T9y'] = request.POST.get('rbid')  # Recommended Bid
            setup_data['00Nd00000077TA3'] = request.POST.get('rbudget')  # Recommended Budget
            setup_data['00Nd00000077TA8'] = request.POST.get('rbidmodifier')  # Recommended Mobile Bid Modifier
            setup_data['00Nd0000005WYhE'] = request.POST.get('shopping_url')  # Shopping URL

            # Production ID for IS SHOPPING POLICIES
            # setup_data['00Nd0000007esIw'] = request.POST.get('is_shopping_policies')  # Shopping Policies

            # SandBox ID for IS SHOPPING POLICIES
            setup_data['00Nq0000000eZPB'] = request.POST.get('is_shopping_policies')  # Shopping Policies

            requests.request('POST', url=sf_api_url, data=setup_data)

            # Create Icallender (*.ics) file for send mail
            # advirtiser_details.update({'appointment_date': request.POST.get('setup_datepick')})
            # if advirtiser_details.get('appointment_date'):
            # create_icalendar_file(advirtiser_details)
            # send_calendar_invite_to_advertiser(advirtiser_details)

        return redirect(basic_data['retURL'])

    locations = Location.objects.filter(is_active=True)
    new_locations = list()
    all_locations = list()
    time_zone_for_region = dict()
    language_for_location = dict()
    for loc in locations:
        l = {'id': int(loc.id), 'name': str(loc.location_name)}
        if loc.location_name in ['Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Panama']:
            new_locations.append(l)
        else:
            all_locations.append(l)
        time_zone_for_region[loc.location_name] = [{'zone_name': tz[
            'zone_name'], 'time_value': tz['time_value']} for tz in loc.time_zone.values()]
        language_for_location[loc.location_name] = [{'language_name': lang[
            'language_name']} for lang in loc.language.values()]

    teams = Team.objects.filter(is_active=True)
    code_types = CodeType.objects.filter(is_active=True)

    return render(
        request,
        'leads/lead_form.html',
        {'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID,
         'locations': all_locations,
         'new_locations': new_locations,
         'teams': teams,
         'code_types': code_types,
         'time_zone_for_region': json.dumps(time_zone_for_region),
         'language_for_location': json.dumps(language_for_location)
         }
    )


def get_common_lead_data(post_data):
    """ Get basic data from both lead forms """

    basic_data = {

        # Google Rep Information
        '00Nd0000005WYgk': post_data.get('gref'),  # Full Name
        'email': post_data.get('emailref'),                   # Rep Email
        '00Nd00000075Crj': post_data.get('manager_name'),  # Manager Name
        '00Nd00000077r3s': post_data.get('manager_email'),  # Manager Email
        '00Nd0000005XIWB': post_data.get('team'),  # Team
        '00Nd0000007e2AF': post_data.get('service_segment'),  # Service Segment
        '00Nd0000007f0fj': post_data.get('g_case_id'),  # G Cases Id
        '00Nd0000005WYga': post_data.get('country'),  # Country

        # Production ID's
        # '00Nd0000007esJ1': post_data.get('advertiser_name'),  # Advertiser Name
        # '00Nd0000007es7U': post_data.get('advertiser_location').split(',')[0] if post_data.get('advertiser_location') else post_data.get('advertiser_location'),  # Advertiser Location
        # '00Nd0000007esIm': post_data.get('web_access'),  # Web Access
        # '00Nd0000007esIh': post_data.get('web_master_email'),  # Webmaster Email
        # '00Nd0000007esIc': post_data.get('popt'),  # Webmaster Phone
        # '00Nd0000007elYB': 1,  # Default value for Change Lead Owner

        '00Nd0000005WcNw': post_data.get('aemail'),  # Advertiser Email
        '00Nd0000005WYgz': post_data.get('phone'),  # Advertiser Phone
        'company': post_data.get('company'),    # Advertiser Company
        '00Nd0000005WYgV': post_data.get('cid'),  # Customer ID

        '00Nd0000007clUn': post_data.get('language'),  # Language
        '00Nd0000005WYhT': post_data.get('tzone'),  # Time Zone


        # Sandbox ID's
        '00Nq0000000eZPG': post_data.get('advertiser_name'),  # Advertiser Name
        'first_name': post_data.get('advertiser_name').rsplit(' ', 1)[0],    # First Name
        'last_name': post_data.get('advertiser_name').rsplit(' ', 1)[1] if len(post_data.get('advertiser_name').rsplit(' ', 1)) > 1 else '',   # Last Name
        '00Nq0000000eZOS': post_data.get('advertiser_location').split(',')[0] if post_data.get('advertiser_location') else post_data.get('advertiser_location'),  # Advertiser Location
        '00Nq0000000eZOw': post_data.get('web_access'),  # Web Access
        '00Nq0000000eZOh': post_data.get('web_master_email'),  # Webmaster Email
        '00Nq0000000eZOc': post_data.get('popt'),  # Webmaster Phone

        # Webmaster Details
        '00Nd0000005WYgp': post_data.get('fopt'),  # Webmaster First Name
        '00Nd0000005WYgu': post_data.get('lopt'),  # Webmaster Last Name
        '00Nq0000000eJdW': 1,    # Default value for Change Lead Owner
        'Campaign_ID': post_data.get('Campaign_ID'),
        'oid': post_data.get('oid'),
        '__VIEWSTATE': post_data.get('__VIEWSTATE'),
    }

    return basic_data


@login_required
@csrf_exempt
def agency_form(request):
    """ Agency Form """

    template_args = dict()

    locations = Location.objects.filter(is_active=True)
    new_locations = list()
    all_locations = list()
    time_zone_for_region = dict()
    language_for_location = dict()
    for loc in locations:
        l = {'id': int(loc.id), 'name': str(loc.location_name)}
        all_locations.append(l)
        time_zone_for_region[loc.id] = [{'zone_name': tz.zone_name, 'id': tz.id, 'time_value': tz.time_value} for tz in loc.time_zone.filter()]
        language_for_location[loc.id] = [{'language_name': lang.language_name, 'id': lang.id} for lang in loc.language.filter()]

    teams = Team.objects.filter(is_active=True)
    code_types = CodeType.objects.filter(is_active=True)

    agencies = AgencyDetails.objects.filter(google_rep_id=request.user.id)

    template_args.update({'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID,
                          'locations': all_locations,
                          'new_locations': new_locations,
                          'teams': teams,
                          'code_types': code_types,
                          'time_zone_for_region': json.dumps(time_zone_for_region),
                          'language_for_location': json.dumps(language_for_location),
                          'agencies': agencies
                          })
    if request.method == 'POST':
        agency_name = request.POST.get("agency_name")
        location = request.POST.get("country")
        timezone = request.POST.get("tzone")
        language = request.POST.get("language")
        appointment_date = request.POST.get('set_appointment')
        #  02/12/2015 09:16 pm Time Formate
        appointment_date = datetime.strptime(appointment_date, "%m/%d/%Y %I:%M %p")
        print appointment_date
        try:
            agency = AgencyDetails.objects.get(google_rep=request.user, agency_name=agency_name, location_id=location,
                                               timezone_id=timezone, language_id=language)
        except ObjectDoesNotExist:
            agency = AgencyDetails(google_rep=request.user, agency_name=agency_name, location_id=location,
                                   timezone_id=timezone, language_id=language, appointment_date=appointment_date)
            agency.save()

        poc_count = int(request.POST.get('poc_count'))
        for i in range(1, poc_count + 1):
            indx = str(i)
            person_name = "contact_person_name_" + indx
            telephone = "contact_telephone_" + indx
            email = "agency_email_" + indx
            person_name = request.POST.get(person_name)
            contact_telephone = request.POST.get(telephone)
            agency_email = request.POST.get(email)
            try:
                ContactPerson.objects.get(contact_email=agency_email)
                template_args.update({'status': 'fail', 'error': "%s Email already exist" % (agency_email)})
                break
            except ObjectDoesNotExist:
                person_id = "%s-%s" % (agency_email.split('@')[0], uuid4())
                try:
                    per = ContactPerson(contact_person=person_name, contact_email=agency_email,
                                        contact_phone=contact_telephone, agency=agency, person_id=person_id)
                    per.save()
                    is_rep = "advertiser"
                    mail_notification(request, per, is_rep)
                    is_rep = "google_rep"
                    mail_notification(request, per, is_rep)
                except Exception:
                    template_args.update({'status': 'fail', 'error': "Something went wrong!"})
                    break

            template_args.update({'status': 'success'})

    return render(
        request,
        'leads/agent_form.html',
        template_args
    )


def mail_notification(request, person, is_rep):
    poc_link = request.build_absolute_uri(reverse('leads.views.agent_bulk_upload', kwargs={'agency_name': person.agency.agency_name.replace(' ', '-'),
                                                                                           'pid': person.person_id}))
    if is_rep == 'advertiser':
        mail_body = get_template('leads/advertiser_mail/advetiser_email.html').render(
            Context({
                'advertiser_name': person.contact_person,
                'poc_link': poc_link,
            })
        )
        mail_subject = " Agency Form Submission "
        mail_to = set([
            person.contact_email,
        ])

    if is_rep == 'google_rep':
        mail_body = get_template('leads/advertiser_mail/google_rep_mail.html').render(
            Context({
                'advertiser_name': person.contact_person,
                'google_account_manager': request.user.first_name,
                'poc_link': poc_link,
            })
        )
        mail_subject = " Agency Form Submission "
        mail_to = set([
            request.user.email,
        ])

    bcc = set([])

    mail_from = 'rajuk@regalix-inc.com'

    attachments = list()

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

    return "feedback"


def get_timezones(request):
    if request.is_ajax():
        loc_name = request.GET.get('loc_name')
        location = Location.objects.get(location_name=loc_name)
        timezones = location.time_zone.all()
        timezones_list = list()
        for zone in timezones:
            zone_val = "%s (UTC%s)" % (zone.zone_name, zone.time_value)
            timezones_list.append({"id": zone.zone_name, "time": zone_val})
        return HttpResponse(json.dumps(timezones_list))


def download_agency_csv(request):
    path = settings.STATIC_FOLDER + '/AGENCY.csv'
    response = DownloadLeads.get_downloaded_file_response(path)
    return response


@csrf_exempt
def agent_bulk_upload(request, agency_name, pid):
    """ Agency Bulk Upload """
    template_args = dict()
    try:
        poc_details = ContactPerson.objects.get(person_id=pid)
        template_args['poc_details'] = poc_details
    except ObjectDoesNotExist:
        template_args.update({'status': 'fail', 'error': 'Invalid POC'})
        return render(request, 'leads/agent_bulk_form.html', template_args)
    if request.method == "POST":
        if request.FILES:
            myfile = request.FILES['csvfile']
            data_list = list()
            for record in csv.DictReader(myfile.read().splitlines()):
                each_rec = dict()
                each_rec['customer_id'] = record['Customer ID']
                each_rec['code_type'] = record['Code Type']
                each_rec['url'] = record['URL']
                each_rec['special_instructions'] = record['Special Instructions']
                data_list.append(each_rec)

            locations = Location.objects.filter(is_active=True)
            new_locations = list()
            all_locations = list()
            time_zone_for_region = dict()
            language_for_location = dict()
            for loc in locations:
                l = {'id': int(loc.id), 'name': str(loc.location_name)}
                if loc.location_name in ['Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Panama']:
                    new_locations.append(l)
                else:
                    all_locations.append(l)
                time_zone_for_region[loc.location_name] = [{'zone_name': tz[
                    'zone_name'], 'time_value': tz['time_value']} for tz in loc.time_zone.values()]
                language_for_location[loc.location_name] = [{'language_name': lang[
                    'language_name']} for lang in loc.language.values()]

            code_types = ReportService.get_all_code_type()
            remaining = len(data_list) + 11
            template_args.update({'data': data_list, 'code_types': code_types, 'is_csv': True, 'agency_name': agency_name, 'pid': pid,
                                  'remaining': range(len(data_list) + 1, remaining), 'locations': all_locations,
                                  'time_zone_for_region': time_zone_for_region, 'language_for_location': language_for_location})
            print template_args
            return render(request, 'leads/agent_bulk_form.html', template_args)

        if 'paramcounts' in request.POST:
            params_count = request.POST.get('paramcounts')
            google_rep_id = request.POST.get('google_rep_id')
            poc_id = request.POST.get('poc_id')

            try:
                goggle_rep = User.objects.get(id=int(google_rep_id))
            except ObjectDoesNotExist:
                pass

            try:
                poc = ContactPerson.objects.get(id=poc_id)
            except ObjectDoesNotExist:
                pass

            basic_lead_args = {
                # Google Rep Information
                '00Nd0000005WYgk': goggle_rep.first_name + ' ' + goggle_rep.last_name,  # Full Name
                'email': goggle_rep.email,                   # Rep Email
                '00Nd00000075Crj': goggle_rep.profile.user_manager_name,  # Manager Name
                '00Nd00000077r3s': goggle_rep.profile.user_manager_email,  # Manager Email
                '00Nd0000005XIWB': goggle_rep.profile.team.team_name,  # Team
                '00Nd0000007e2AF': None,  # Service Segment
                '00Nd0000007dWIH': None,  # G Cases Id
                '00Nd0000005WYga': '',  # Country

                '00Nd0000005WcNw': '',  # Advertiser Email
                '00Nd0000005WYgz': '',  # Advertiser Phone
                'company': '',    # Advertiser Company
                '00Nd0000005WYgV': '',  # Customer ID

                '00Nd0000007clUn': poc.agency.language.language_name,  # Language
                '00Nd0000005WYhT': '',  # Time Zone


                # Sandbox ID's
                '00Nq0000000eZPG': '',  # Advertiser Name
                '00Nq0000000eZOS': '',  # Advertiser Location
                '00Nq0000000eZOw': 0,  # Web Access
                '00Nq0000000eZOh': '',  # Webmaster Email
                '00Nq0000000eZOc': '',  # Webmaster Phone

                # Webmaster Details
                '00Nd0000005WYgp': None,  # Webmaster First Name
                '00Nd0000005WYgu': None,  # Webmaster Last Name
                '00Nq0000000eJdW': 1,    # Default value for Change Lead Owner
                'Campaign_ID': None,
                'oid': request.POST.get('oid'),
                '__VIEWSTATE': request.POST.get('__VIEWSTATE'),
            }

            for i in range(1, int(params_count) + 1):
                lead_args = dict()
                customer_id = request.POST.get('customer_id_' + str(i))
                location = request.POST.get('location_' + str(i))
                timezone = request.POST.get('timezone_' + str(i))
                agency_name = request.POST.get('agency_name_' + str(i))
                agency_phone = request.POST.get('agency_phone_' + str(i))
                agency_email = request.POST.get('agency_email_' + str(i))
                code_type = request.POST.get('code_type_' + str(i))
                url = request.POST.get('url_' + str(i))
                special_instructions = request.POST.get('special_instructions_' + str(i))

                lead_args = basic_lead_args
                lead_args['00Nq0000000eZPG'] = agency_name     # Advertiser Name
                lead_args['first_name'] = agency_name.rsplit(' ', 1)[0]    # First Name
                lead_args['last_name'] = agency_name.rsplit(' ', 1)[1] if len(agency_name.rsplit(' ', 1)) > 1 else ''   # Last Name
                lead_args['00Nd0000005WcNw'] = agency_email     # Advertiser Email
                lead_args['00Nd0000005WYgz'] = agency_phone     # Advertiser Phone
                lead_args['00Nd0000005WYgV'] = customer_id     # Customer ID
                lead_args['00Nd0000005WYga'] = location     # Agency Location
                lead_args['00Nd0000005WYhT'] = timezone     # Time Zone

                # Code Type 1 Details
                lead_args['00Nd0000005WYhJ'] = code_type  # Code Type1
                lead_args['00Nd0000005WYhE'] = url  # URL1
                lead_args['00Nd0000005WYh9'] = None  # Code1
                lead_args['00Nd0000005WZIe'] = special_instructions  # Comments1

                lead_args['create_date'] = datetime.utcnow()  # Created Date
                # Post Lead data to SalesForce
                post_lead_to_sf(request, lead_args)

            template_args.update({'is_csv': True})
    return render(request, 'leads/agent_bulk_form.html', template_args)


def post_lead_to_sf(request, lead_data):
    """ Post lead to SalesForce """
    sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
    requests.request('POST', url=sf_api_url, data=lead_data)


# Create your views here.
@login_required
@csrf_exempt
def bundle_lead_form(request):

    """
    Bundle Leas Form
    Combination of 3 Code Types
    """
    if request.method == 'POST':
        complex_code_type = ['Dynamic Remarketing - Extension (non retail)', 'Google Shopping Setup',
                             'Dynamic Remarketing - Retail', 'Cross Domain Tracking']

        code_type1 = request.POST.get('ctype1')
        code_type2 = request.POST.get('ctype2')
        code_type3 = request.POST.get('ctype3')
        code_types = list()
        lead_bundle = "%s-%s-%s" % (randint(0, 99999), datetime.utcnow().month, datetime.utcnow().year)
        if code_type1 in complex_code_type:
            if code_type1 != 'Google Shopping Setup':
                # Get Basic/Common form filed data
                basic_data = dict()
                basic_data = get_common_lead_data(request.POST)
                basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
                basic_data['00Nd0000007f4St'] = lead_bundle
                post_tag_lead_to_sf(request, request.POST, basic_data, [1])
            else:
                basic_data = dict()
                basic_data = get_common_lead_data(request.POST)
                basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
                basic_data['00Nd0000007f4St'] = lead_bundle
                post_shopping_lead_to_sf(request, request.POST, basic_data, 1)
        elif code_type1:
            code_types.append(1)

        if code_type2 in complex_code_type:
            if code_type2 != 'Google Shopping Setup':
                basic_data = dict()
                basic_data = get_common_lead_data(request.POST)
                basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
                basic_data['00Nd0000007f4St'] = lead_bundle
                post_tag_lead_to_sf(request, request.POST, basic_data, [2])
            else:
                basic_data = dict()
                basic_data = get_common_lead_data(request.POST)
                basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
                basic_data['00Nd0000007f4St'] = lead_bundle
                post_shopping_lead_to_sf(request, request.POST, basic_data, 2)
        elif code_type2:
            code_types.append(2)

        if code_type3 in complex_code_type:
            if code_type3 != 'Google Shopping Setup':
                basic_data = dict()
                basic_data = get_common_lead_data(request.POST)
                basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
                basic_data['00Nd0000007f4St'] = lead_bundle
                post_tag_lead_to_sf(request, request.POST, basic_data, [3])
            else:
                basic_data = dict()
                basic_data = get_common_lead_data(request.POST)
                basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
                basic_data['00Nd0000007f4St'] = lead_bundle
                post_shopping_lead_to_sf(request, request.POST, basic_data, 3)
        elif code_type3:
            code_types.append(3)

        if code_types:
            basic_data = dict()
            basic_data = get_common_lead_data(request.POST)
            basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
            basic_data['00Nd0000007f4St'] = lead_bundle
            post_tag_lead_to_sf(request, request.POST, basic_data, code_types)

        # Create Icallender (*.ics) file for send mail
        # advirtiser_details.update({'appointment_date': request.POST.get('setup_datepick')})
        # if advirtiser_details.get('appointment_date'):
        # create_icalendar_file(advirtiser_details)
        # send_calendar_invite_to_advertiser(advirtiser_details)

        return redirect(basic_data['retURL'])

    locations = Location.objects.filter(is_active=True)
    new_locations = list()
    all_locations = list()
    time_zone_for_region = dict()
    language_for_location = dict()
    for loc in locations:
        l = {'id': int(loc.id), 'name': str(loc.location_name)}
        if loc.location_name in ['Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Panama']:
            new_locations.append(l)
        else:
            all_locations.append(l)
        time_zone_for_region[loc.location_name] = [{'zone_name': tz[
            'zone_name'], 'time_value': tz['time_value']} for tz in loc.time_zone.values()]
        language_for_location[loc.location_name] = [{'language_name': lang[
            'language_name']} for lang in loc.language.values()]

    teams = Team.objects.filter(is_active=True)
    code_types = CodeType.objects.filter(is_active=True)

    return render(
        request,
        'leads/bundle_lead_form.html',
        {'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID,
         'locations': all_locations,
         'new_locations': new_locations,
         'teams': teams,
         'code_types': code_types,
         'time_zone_for_region': json.dumps(time_zone_for_region),
         'language_for_location': json.dumps(language_for_location)
         }
    )


def post_tag_lead_to_sf(request, post_data, basic_data, code_types):
    """ Post Tag Lead to Salesforce """

    sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
    # sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
    tag_data = dict()
    tag_data = basic_data
    # advirtiser_details = {'first_name': post_data.get('advertiser_name'),
    #                       'last_name': post_dataget('advertiser_name').split(' ')[1] if len(post_data.get('advertiser_name')) > 1 else '',
    #                       'email': post_data.get('aemail'),
    #                       'role': post_data.get('primary_role'),
    #                       'customer_id': post_data.get('cid'),
    #                       'country': post_data.get('country'),
    #                       'cid_std': post_data.get('cid').rsplit("-", 1)[0] + '-xxxx'
    #                       }

    if post_data.get('tag_contact_person_name1'):
        full_name = post_data.get('tag_contact_person_name1')
    else:
        full_name = post_data.get('shop_contact_person_name1')

    tag_data['first_name'] = full_name.rsplit(' ', 1)[0] if full_name else '',  # Primary Contact Name
    tag_data['last_name'] = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else '',

    tag_data['00Nd0000005WayR'] = post_data.get('tag_primary_role') if post_data.get('tag_primary_role') else post_data.get('shop_primary_role'),  # Role

    for indx in code_types:
        if indx == 1:
            tag_data['00Nd0000005WYlL'] = post_data.get('tag_datepick1'),  # TAG Appointment Date

            # Code Type 1 Details
            tag_data['00Nd0000005WYhJ'] = post_data.get('ctype' + str(indx))  # Code Type1
            tag_data['00Nd0000005WYhE'] = post_data.get('url' + str(indx))  # URL1
            tag_data['00Nd0000005WZIe'] = post_data.get('comment' + str(indx))  # Comments1

            # if post_data.get('is_campaign_created' + str(indx)) == '0' or post_data.get('is_campaign_created' + str(indx)) == 0:
            tag_data['00Nd00000077T9y'] = post_data.get('rbid_campaign' + str(indx))  # Recommended Bid
            tag_data['00Nd00000077TA3'] = post_data.get('rbudget_campaign' + str(indx))  # Recommended Budget

        elif indx == 2:
            # Code Type 2 Details
            tag_data['00Nd0000005WYkS'] = post_data.get('ctype' + str(indx))  # Code Type2
            tag_data['00Nd0000005WYi9'] = post_data.get('url' + str(indx))  # URL2
            tag_data['00Nd0000005WYjy'] = post_data.get('comment' + str(indx))  # Comments2

            # if post_data.get('is_campaign_created' + str(indx)) == '0' or post_data.get('is_campaign_created' + str(indx)) == 0:
            tag_data['00Nd00000077T9y'] = post_data.get('rbid_campaign' + str(indx))  # Recommended Bid
            tag_data['00Nd00000077TA3'] = post_data.get('rbudget_campaign' + str(indx))  # Recommended Budget

        elif indx == 3:
            # Code Type 3 Details
            tag_data['00Nd0000005WYkX'] = post_data.get('ctype' + str(indx))  # Code Type3
            tag_data['00Nd0000005WYjU'] = post_data.get('url' + str(indx))  # URL3
            tag_data['00Nd0000005WYjB'] = post_data.get('comment' + str(indx))  # Comments3

            # if post_data.get('is_campaign_created' + str(indx)) == '0' or post_data.get('is_campaign_created' + str(indx)) == 0:
            tag_data['00Nd00000077T9y'] = post_data.get('rbid_campaign' + str(indx))  # Recommended Bid
            tag_data['00Nd00000077TA3'] = post_data.get('rbudget_campaign' + str(indx))  # Recommended Budget

    # Sandbox ID for TAD VIA GTM
    tag_data['00Nq0000000eZP6'] = post_data.get('tag_via_gtm')  # Tag Via  GTM

    requests.request('POST', url=sf_api_url, data=tag_data)


def post_shopping_lead_to_sf(request, post_data, basic_data, indx):
    """ Post Tag Lead to Salesforce """

    sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
    # sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
    setup_data = dict()
    setup_data = basic_data
    # advirtiser_details = {'first_name': post_data.get('advertiser_name'),
    #                       'last_name': post_dataget('advertiser_name').split(' ')[1] if len(post_data.get('advertiser_name')) > 1 else '',
    #                       'email': post_data.get('aemail'),
    #                       'role': post_data.get('primary_role'),
    #                       'customer_id': post_data.get('cid'),
    #                       'country': post_data.get('country'),
    #                       'cid_std': post_data.get('cid').rsplit("-", 1)[0] + '-xxxx'
    #                       }

    if post_data.get('setup_datepick1') and indx == 1:
        setup_data['00Nd0000005WYlL'] = post_data.get('setup_datepick1'),  # TAG Appointment Date
    if post_data.get('shop_contact_person_name1'):
        full_name = post_data.get('shop_contact_person_name1')
    else:
        full_name = post_data.get('tag_contact_person_name1')
    first_name = full_name.rsplit(' ', 1)[0]
    last_name = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else ''
    setup_data['first_name'] = first_name  # Primary Contact First Name
    setup_data['last_name'] = last_name  # Primary Contact Last Name
    setup_data['00Nd0000005WayR'] = post_data.get('shop_primary_role') if post_data.get('shop_primary_role') else post_data.get('tag_primary_role'),  # Role
    setup_data['00Nd0000005WYhJ'] = u'Google Shopping Setup'  # Code Type
    setup_data['00Nd00000077T9o'] = post_data.get('00Nd00000077T9o')  # MC-ID
    setup_data['00Nd00000077T9t'] = post_data.get('00Nd00000077T9t')  # Web Inventory
    setup_data['00Nd00000077T9y'] = post_data.get('rbid' + str(indx))  # Recommended Bid
    setup_data['00Nd00000077TA3'] = post_data.get('rbudget' + str(indx))  # Recommended Budget
    setup_data['00Nd00000077TA8'] = post_data.get('rbidmodifier' + str(indx))  # Recommended Mobile Bid Modifier
    setup_data['00Nd0000005WYhE'] = post_data.get('shopping_url' + str(indx))  # Shopping URL

    # Production ID for IS SHOPPING POLICIES
    # setup_data['00Nd0000007esIw'] = post_data.get('is_shopping_policies')  # Shopping Policies

    # SandBox ID for IS SHOPPING POLICIES
    setup_data['00Nq0000000eZPB'] = post_data.get('is_shopping_policies')  # Shopping Policies

    requests.request('POST', url=sf_api_url, data=setup_data)


@login_required
@csrf_exempt
def shopping_campaign_setup_lead_form(request):
    pass


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
        '3': reverse('leads.views.bundle_lead_form'),
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
    if len(leads) > 1:
        leads = leads[0]
    team = Team.objects.get(team_name=leads.team)
    location = Location.objects.get(location_name=leads.country)
    languages = location.language.all()
    if not languages:
        languages = Language.objects.all()
    languages_list = list()
    for lang in languages:
        languages_list.append({'l_id': lang.id, 'language_name': lang.language_name})
    if leads:
        lead['status'] = 'SUCCESS'

        lead['details'] = {
            'name': leads.first_name + ' ' + leads.last_name,
            'email': leads.lead_owner_email,
            'google_rep_email': leads.google_rep_email,
            'location': leads.country,
            'team': team.team_name,
            'team_id': team.id,
            'languages_list': languages_list

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
    event.add('summary', 'Google Implementation Appointment')

    # Appointment slot Date formate: "11/20/2014 10:00 AM"
    appointment_date = datetime.strptime(advirtiser_details['appointment_date'], "%m/%d/%Y %H:%M %p")
    event.add('dtstart', appointment_date)
    event.add('dtend', appointment_date + timedelta(minutes=30))
    event.add('dtstamp', appointment_date)
    event['location'] = vText(advirtiser_details['country'])
    event['uid'] = advirtiser_details['customer_id']

    organizer = vCalAddress('MAILTO:rajuk@regalix-inc.com.com')
    organizer.params['cn'] = vText('Google')
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

    mail_subject = "Customer ID: %s Authorization Email for Google Code Installation" % (advertiser_details['cid_std'])

    mail_body = get_template('leads/advertiser_mail/appointment_confirmation.html').render(
        Context({
            'text': "Google Tag Implementation Support Appointment Confirmation",
            'first_name': advertiser_details.get('first_name'),
            'last_name': advertiser_details.get('last_name'),
            'customer_id': advertiser_details.get('customer_id'),
            'code_type': advertiser_details.get('code_type'),
            'appointment_date': advertiser_details.get('appointment_date')
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
def get_lead_summary(request, lid=None):
    """ Lead Status page """

    lead_status = ['In Queue', 'Attempting Contact', 'In Progress', 'In Active', 'Implemented']
    email = request.user.email
    # email = 'tkhan@regalix-inc.com'
    if email in ['rajuk@regalix-inc.com', 'rwieker@google.com', 'winstonsingh@google.com', 'sabinaa@google.com', 'tkhan@regalix-inc.com', 'rraghav@regalix-inc.com', 'anoop@regalix-inc.com', 'dkarthik@regalix-inc.com', 'sprasad@regalix-inc.com']:
        start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        leads = Leads.objects.filter(lead_status__in=lead_status, created_date__gte=start_date, created_date__lte=end_date)
        # leads = Leads.objects.filter(google_rep_email="bhavinb@google.com")

        status = ['In Queue', 'Attempting Contact', 'In Progress', 'In Active', 'Implemented']
        lead_status_dict = {'total_leads': 0,
                            'implemented': 0,
                            'in_progress': 0,
                            'attempting_contact': 0,
                            'in_queue': 0,
                            'in_active': 0,
                            'in_progress': 0,
                            }
        start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        lead_status_dict['total_leads'] = Leads.objects.filter(lead_status__in=status, created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['implemented'] = Leads.objects.filter(lead_status='Implemented', created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['in_progress'] = Leads.objects.filter(lead_status='In Progress', created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['attempting_contact'] = Leads.objects.filter(lead_status='Attempting Contact', created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['in_queue'] = Leads.objects.filter(lead_status='In Queue', created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['in_active'] = Leads.objects.filter(lead_status='In Active', created_date__gte=start_date, created_date__lte=end_date).count()
    else:
        if is_manager(email):
            email_list = get_user_list_by_manager(email)
        else:
            email_list = [email]

        if 'regalix' in email:
            leads = Leads.objects.filter(lead_status__in=lead_status, lead_owner_email__in=email_list)
        elif 'google' in email:
            leads = Leads.objects.filter(lead_status__in=lead_status, google_rep_email__in=email_list)

        lead_status_dict = get_count_of_each_lead_status_by_rep(email, start_date=None, end_date=None)

    return render(request, 'leads/lead_summary.html', {'leads': leads, 'lead_status_dict': lead_status_dict, 'lead_id': lid})


@login_required
def create_chat_message(request):
    """ creating chat messages"""
    if request.is_ajax():
        lead_id = request.GET.get('lead_id')
        message = request.GET.get('msg')
        user_id = request.user.email

        chat = ChatMessage()
        chat.lead_id = lead_id
        chat.user_id = user_id
        chat.message = message
        chat.save()
        # notify_chat_activity(request, chat)
        messages = ChatMessage.objects.filter(lead_id=lead_id)
        message_list = list()
        for m in messages:
            message = convert_chat_message_to_dict(m)
            message_list.append(message)
        mimetype = 'application/json'
        return HttpResponse(json.dumps(message_list), mimetype)


@login_required
def get_chat_message_by_lead(request):
    """ creating chat messages"""
    if request.is_ajax():
        lead_id = request.GET.get('lead_id')
        messages = ChatMessage.objects.filter(lead_id=lead_id)
        message_list = list()
        for m in messages:
            message = convert_chat_message_to_dict(m)
            message_list.append(message)
        mimetype = 'application/json'
        return HttpResponse(json.dumps(message_list), mimetype)


def convert_chat_message_to_dict(model):
    image_url = '/static/images/default_user.png'
    message = {}
    message['lead_id'] = model.lead_id
    message['user_id'] = model.user_id
    try:
        user = User.objects.get(email=model.user_id)
        user_profile = UserDetails.objects.get(user_id=user.id)
        image_url = user_profile.profile_photo_url
    except ObjectDoesNotExist:
        image_url = '/static/images/default_user.png'
    message['message'] = model.message
    message['created_date'] = datetime.strftime(model.created_date, "%m/%d/%Y")
    message['image_url'] = image_url
    return message


def notify_chat_activity(request, chatmessage, lead_id):
    lead = Leads.objects.get(id=lead_id)

    # get chat user manager and lead owner managers information
    rgx_user_profile = get_manager_by_user(lead.lead_owner_email)
    google_user_profile = get_manager_by_user(lead.google_rep_email)

    # create mail subject
    mail_subject = "IMP - Lead Status Updates - " + lead.cid
    # CHat url
    chat_url = request.build_absolute_uri(reverse('leads.views.get_lead_summary', kwargs={'lid': chatmessage.lead_id}))
    # Chat Body
    mail_body = get_template('main/ping_chat_mail/new_chat.html').render(
        Context({
            'message': chatmessage.message,
            'message_url': chat_url,
            'rgx_rep': lead.lead_owner_name,
            'google_rep': lead.google_rep_name,
            'rgx_rep_mgr': rgx_user_profile.user_manager_name,
            'google_rep_mgr': google_user_profile.user_manager_name,
            'cid': lead.cid,
            'sender_name': request.user.name,
            'sender_email': request.user.email
        })
    )

    # mail_to.add(request.user.email)
    mail_to = set([])
    lead = Leads.objects.get(id=chatmessage.user_id)
    if 'regalix' in request.user.email:
        mail_to.add(lead.google_rep_email)
    elif 'google' in request.user.email:
        mail_to.add(lead.lead_owner_email)

    # add mail_Bcc address
    bcc = set([])
    bcc.add(rgx_user_profile.user_manager_email)
    bcc.add(google_user_profile.user_manager_email)

    mail_from = request.user.email

    attachments = list()
    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

    return chatmessage


@login_required
def create_teams(request):
    """ Create Teams by Leads Data """
    teams = ReportService.get_all_teams()
    for team in teams:
        if not Team.objects.filter(team_name=team):
            t_object = Team(team_name=team)
            t_object.save()
    return HttpResponse('Success')


@login_required
def create_codetypes(request):
    """ Create Code Types by Leads Data """
    code_types = ReportService.get_all_code_type()
    for code in code_types:
        if not CodeType.objects.filter(name=code):
            c_object = CodeType(name=code)
            c_object.save()
    return HttpResponse('Success')


@login_required
def create_locations(request):
    """ Create location by Leads Data """
    locations = ReportService.get_all_locations()
    for location in locations:
        if not Location.objects.filter(location_name=location):
            l_object = Location(location_name=location)
            l_object.save()
    return HttpResponse('Success')


@login_required
def get_lead_status_by_ldap(request):
    if request.is_ajax():
        lead_status = ['In Queue', 'Attempting Contact', 'In Progress', 'In Active', 'Implemented']
        user_id = request.GET['user_id']
        user = User.objects.get(id=user_id)
        leads = Leads.objects.filter(Q(google_rep_email=user.email) | Q(lead_owner_email=user.email))
        leads = leads.filter(lead_status__in=lead_status)
        lead_list = list()
        for l in leads:
            lead = convert_lead_to_dict(l)
            lead_list.append(lead)
        lead_status_dict = get_count_of_each_lead_status_by_rep(user.email, start_date=None, end_date=None)
        mimetype = 'application/json'
        return HttpResponse(json.dumps({'lead_list': lead_list, 'lead_status_dict': lead_status_dict}), mimetype)
    return render(request, 'leads/get_lead_summary_ldap.html', {})


def convert_lead_to_dict(model):
    lead = {}
    lead['Advertiser'] = model.company
    lead['cid'] = model.customer_id
    lead['code_type'] = model.type_1
    lead['google_rep'] = model.google_rep_name
    lead['regalix_rep'] = model.lead_owner_name
    if model.created_date:
        lead['date_created'] = datetime.strftime(model.created_date, "%m/%d/%Y")
    else:
        lead['date_created'] = ''
    if model.appointment_date:
        lead['appointment_time'] = datetime.strftime(model.appointment_date, "%m/%d/%Y")
    else:
        lead['appointment_time'] = ''
    if model.date_of_installation:
        lead['date_of_installation'] = datetime.strftime(model.date_of_installation, "%m/%d/%Y")
    else:
        lead['date_of_installation'] = ''
    lead['regalix_comment'] = model.regalix_comment
    lead['lead_status'] = model.lead_status
    return lead
