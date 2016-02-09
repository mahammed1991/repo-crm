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
from lib.salesforce import SalesforceApi
from leads.models import (Leads, Location, Team, CodeType, ChatMessage, Language, ContactPerson, TreatmentType,
                          AgencyDetails, LeadFormAccessControl, RegalixTeams, Timezone, WPPLeads, PicassoLeads
                          )
from main.models import UserDetails
from lib.helpers import (get_unique_uuid, get_quarter_date_slots, send_mail, get_count_of_each_lead_status_by_rep, wpp_lead_status_count_analysis, get_tat_for_picasso,
                         is_manager, get_user_list_by_manager, get_manager_by_user, date_range_by_quarter, tag_user_required, wpp_user_required, get_picasso_count_of_each_lead_status_by_rep)
from icalendar import Calendar, Event, vCalAddress, vText
from django.core.files import File
from django.contrib.auth.models import User
from reports.report_services import ReportService, DownloadLeads
from django.db.models import Q
from random import randint
from lib.sf_lead_ids import SalesforceLeads
from reports.models import Region
import operator
import collections


# Create your views here.
@login_required
@csrf_exempt
@tag_user_required
def lead_form(request):

    """
    Lead Submission to Salesforce
    """
    if request.method == 'POST':
        if settings.SFDC == 'STAGE':
            sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
            # oid = '00DZ000000MjkJO'
            oid = '00D7A0000008nBH'
        elif settings.SFDC == 'PRODUCTION':
            sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
            oid = '00Dd0000000fk18'

        ret_url = ''
        # error_url = ''
        if request.POST.get('is_tag_lead') == 'yes':
            # Get Basic/Common form field data
            if settings.SFDC == 'STAGE':
                basic_data = get_common_sandbox_lead_data(request.POST)
            else:
                basic_data = get_common_salesforce_lead_data(request.POST)
            basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
            basic_data['errorURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
            basic_data['oid'] = oid
            ret_url = basic_data['retURL']
            # error_url = basic_data['errorURL']

            tag_data = basic_data
            for key, value in tag_leads.items():
                tag_data[value] = request.POST.get(key)

            for i in range(1, 6):
                i = str(i)
                rbid_key = 'rbid' + i
                rbudget_key = 'rbudget' + i
                ga_setup_key = 'ga_setup' + i
                analytics_code_key = 'analytics_code' + i
                call_extension_key = 'call_extension' + i
                product_behaviour_key = 'product_behaviour' + i
                cartpage_behaviour_key = 'cartpage_behaviour' + i
                checkout_process_key = 'checkout_process' + i
                transaction_behaviour_key = 'transaction_behaviour' + i

                user_list_id_key = 'user_list_id' + i
                rsla_bid_adjustment_key = 'rsla_bid_adjustment' + i
                rlsa_internal_cid_key = 'internal_cid' + i
                campaign_ids_key = 'campaign_ids' + i
                create_new_bid_modifiers_key = 'create_new_bid_modifiers' + i
                overwrite_existing_bid_modifiers_key = 'overwrite_existing_bid_modifiers' + i
                # rsla_policies_key = 'rsla_policies' + i

                tag_data[tag_leads[rbid_key]] = request.POST.get(rbid_key)
                tag_data[tag_leads[rbudget_key]] = request.POST.get(rbudget_key)
                tag_data[tag_leads[ga_setup_key]] = request.POST.get(ga_setup_key)
                tag_data[tag_leads[analytics_code_key]] = request.POST.get(analytics_code_key)
                tag_data[tag_leads[call_extension_key]] = request.POST.get(call_extension_key)
                tag_data[tag_leads[product_behaviour_key]] = request.POST.get(product_behaviour_key)
                tag_data[tag_leads[cartpage_behaviour_key]] = request.POST.get(cartpage_behaviour_key)
                tag_data[tag_leads[checkout_process_key]] = request.POST.get(checkout_process_key)
                tag_data[tag_leads[transaction_behaviour_key]] = request.POST.get(transaction_behaviour_key)

                tag_data[tag_leads[user_list_id_key]] = request.POST.get(user_list_id_key)
                tag_data[tag_leads[rsla_bid_adjustment_key]] = request.POST.get(rsla_bid_adjustment_key)
                tag_data[tag_leads[rlsa_internal_cid_key]] = request.POST.get(rlsa_internal_cid_key)
                tag_data[tag_leads[campaign_ids_key]] = request.POST.get(campaign_ids_key)
                tag_data[tag_leads[create_new_bid_modifiers_key]] = request.POST.get(create_new_bid_modifiers_key)
                tag_data[tag_leads[overwrite_existing_bid_modifiers_key]] = request.POST.get(overwrite_existing_bid_modifiers_key)
                # tag_data[tag_leads[rsla_policies_key]] = request.POST.get(rsla_policies_key)

            # Split Tag Contact Person Name to First and Last Name
            if request.POST.get('tag_contact_person_name'):
                full_name = request.POST.get('tag_contact_person_name')
            else:
                full_name = request.POST.get('advertiser_name')
            first_name, last_name = split_fullname(full_name)
            tag_data['first_name'] = first_name
            tag_data['last_name'] = last_name
            submit_lead_to_sfdc(sf_api_url, tag_data)

        basic_data = dict()
        if request.POST.get('is_shopping_lead') == 'yes':
            # Get Basic/Common form field data
            if settings.SFDC == 'STAGE':
                basic_data = get_common_sandbox_lead_data(request.POST)
            else:
                basic_data = get_common_salesforce_lead_data(request.POST)
            basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
            basic_data['errorURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
            basic_data['oid'] = oid
            ret_url = basic_data['retURL']
            # error_url = basic_data['errorURL']

            setup_data = basic_data
            for key, value in shop_leads.items():
                setup_data[value] = request.POST.get(key)

            # Split Shopping Contact Person Name to First and Last Name
            if request.POST.get('shop_contact_person_name'):
                full_name = request.POST.get('shop_contact_person_name')
                first_name, last_name = split_fullname(full_name)
                setup_data['first_name'] = first_name  # Primary Contact First Name
                setup_data['last_name'] = last_name  # Primary Contact Last Name
            setup_data[shop_leads['ctype1']] = 'Google Shopping Setup'
            submit_lead_to_sfdc(sf_api_url, setup_data)

        return redirect(ret_url)

    # Check The Rep Status and redirect
    if request.user.groups.filter(name='AGENCY'):
        return redirect('leads.views.agency_lead_form')
    form_name = get_lead_form_for_rep(request.user)

    if 'Bundle' in form_name:
        return redirect('leads.views.bundle_lead_form')
    elif 'Agency' in form_name:
        return redirect('leads.views.agency_lead_form')

    # Get all location, teams codetypes
    lead_args = get_basic_lead_data(request)
    lead_args['PORTAL_MAIL_ID'] = settings.PORTAL_MAIL_ID
    return render(
        request,
        'leads/lead_form.html',
        lead_args
    )


@login_required
@wpp_user_required
@csrf_exempt
def wpp_lead_form(request, ref_id=None):

    """
    Lead Submission to Salesforce
    """
    # Check The Rep Status and redirect
    if request.method == 'POST':
        if settings.SFDC == 'STAGE':
            sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
            oid = '00D7A0000008nBH'
        elif settings.SFDC == 'PRODUCTION':
            sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
            oid = '00Dd0000000fk18'

        ret_url = ''
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)
        basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
        basic_data['errorURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
        basic_data['oid'] = oid
        basic_data['Campaign_ID'] = None
        ret_url = basic_data['retURL']
        wpp_data = basic_data
        for key, value in tag_leads.items():
            if key == 'picasso_objective_list[]':
                wpp_data[value] = (';').join(request.POST.getlist('picasso_objective_list[]'))
            elif key == 'unique_ref_id':
                wpp_data[value] = get_unique_uuid('Wpp')
            else:
                wpp_data[value] = request.POST.get(key)
        submit_lead_to_sfdc(sf_api_url, wpp_data)
        advirtiser_details = get_advertiser_details(sf_api_url, wpp_data)
        send_calendar_invite_to_advertiser(advirtiser_details, False)

        return redirect(ret_url)

    # Get all location, teams codetypes
    lead_args = get_basic_lead_data(request)
    lead_args['teams'] = Team.objects.exclude(belongs_to__in=['TAG', 'PICASSO']).filter(is_active=True)
    lead_args['treatment_type'] = [str(t_type.name) for t_type in TreatmentType.objects.all().order_by('id')]

    user_groups = [group.name for group in request.user.groups.all()]
    if 'TAG-AND-WPP' not in user_groups and 'WPP' not in user_groups:
        lead_args['whitelisted_user'] = 'Yes'

    if ref_id:
        try:
            ref_lead = WPPLeads.objects.get(ref_uuid=ref_id)
            lead_args['ref_lead'] = ref_lead
        except:
            return redirect('leads.views.wpp_lead_form')

    wpp_locations = list()
    for loc in lead_args['locations']:
        if loc['name'] in ['AU/NZ', 'United States', 'Canada', 'UK/I']:
            wpp_locations.append(loc)
    lead_args.update({'wpp_locations': wpp_locations})
    wpp_loc = list()
    regalix_team = RegalixTeams.objects.filter(process_type='WPP', is_active=True)
    for tm in regalix_team:
        for loc in tm.location.all():
            wpp_loc.append(loc)
    lead_args.update({'wpp_loc': wpp_loc})
    return render(
        request,
        'leads/wpp_lead_form.html',
        lead_args
    )


@login_required
@csrf_exempt
def picasso_lead_form(request):

    """
    Picasso Lead Submission to Salesforce
    """
    # Check The Rep Status and redirect
    if request.method == 'POST':
        if settings.SFDC == 'STAGE':
            sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
            oid = '00D7A0000008nBH'
        elif settings.SFDC == 'PRODUCTION':
            sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
            oid = '00Dd0000000fk18'

        ret_url = ''
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)
        basic_data['retURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
        basic_data['errorURL'] = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
        basic_data['oid'] = oid
        basic_data['Campaign_ID'] = None
        ret_url = basic_data['retURL']
        picasso_data = basic_data

        estimated_tat = ""
        tat_dict = get_tat_for_picasso('portal')
        if tat_dict['estimated_date']:
            estimated_tat = tat_dict['estimated_date'].date()
            request.session[str(request.user.email) + 'estimated_tat'] = estimated_tat
            request.session[str(request.user.email) + 'no_of_inqueue_leads'] = tat_dict['no_of_inqueue_leads']

        for key, value in tag_leads.items():
            if key == 'picasso_objective_list[]':
                picasso_data[value] = (';').join(request.POST.getlist('picasso_objective_list[]'))
            elif key == 'unique_ref_id':
                picasso_data[value] = get_unique_uuid('Picasso')
            elif key == 'picasso_tat':
                picasso_data[value] = datetime.strftime(estimated_tat, '%m/%d/%Y')
            else:
                picasso_data[value] = request.POST.get(key)

        response = submit_lead_to_sfdc(sf_api_url, picasso_data)
        advirtiser_details = get_advertiser_details(sf_api_url, picasso_data)
        # send_calendar_invite_to_advertiser(advirtiser_details, False)
        if response.status_code == 200:
            ret_url = basic_data['retURL']
        else:
            ret_url = basic_data['errorURL']
        return redirect(ret_url)

    # Get all location, teams codetypes
    lead_args = get_basic_lead_data(request)
    # lead_args['teams'] = Team.objects.filter(is_active=True)
    lead_args['teams'] = Team.objects.filter(belongs_to__in=['BOTH', 'PICASSO', 'WPP']).order_by('team_name')
    lead_args['picasso'] = True
    tat_dict = get_tat_for_picasso('portal')
    if tat_dict['estimated_date']:
        lead_args['estimated_tat'] = tat_dict['estimated_date'].date()
        lead_args['no_of_inqueue_leads'] = tat_dict['no_of_inqueue_leads']
    return render(
        request,
        'leads/picasso_lead_form.html',
        lead_args
    )


@login_required
@csrf_exempt
def wpp_nomination_form(request):

    """
    Nomination Form To WPP
    """
    # Check The Rep Status and redirect
    # Get all location, teams codetypes
    lead_args = get_basic_lead_data(request)
    lead_args['teams'] = Team.objects.exclude(belongs_to__in=['TAG', 'PICASSO']).filter(is_active=True)
    lead_args['treatment_type'] = [str(t_type.name) for t_type in TreatmentType.objects.all().order_by('id')]

    wpp_locations = list()
    for loc in lead_args['locations']:
        if loc['name'] in ['AU/NZ', 'United States', 'Canada', 'UK/I']:
            wpp_locations.append(loc)
    lead_args.update({'wpp_locations': wpp_locations})
    wpp_loc = list()
    regalix_team = RegalixTeams.objects.filter(process_type='WPP', is_active=True)
    for tm in regalix_team:
        for loc in tm.location.all():
            wpp_loc.append(loc)
    lead_args.update({'wpp_loc': wpp_loc})
    return render(
        request,
        'leads/wpp_nomination_form.html',
        lead_args
    )


def get_common_sandbox_lead_data(post_data):
    """ Get basic data from both lead forms """
    basic_data = dict()
    for key, value in SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.items():
        basic_data[value] = post_data.get(key)

    if post_data.get('advertiser_name'):     # Advertiser Name
        first_name, last_name = split_fullname(post_data.get('advertiser_name'))
        basic_data['first_name'] = first_name
        basic_data['last_name'] = last_name   # Last Name

    return basic_data


def get_common_salesforce_lead_data(post_data):
    """ Get basic data from both lead forms """
    basic_data = dict()
    for key, value in SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.items():
        basic_data[value] = post_data.get(key)

    if post_data.get('advertiser_name'):     # Advertiser Name
        first_name, last_name = split_fullname(post_data.get('advertiser_name'))
        basic_data['first_name'] = first_name
        basic_data['last_name'] = last_name   # Last Name

    return basic_data


@login_required
@csrf_exempt
def agency_lead_form(request):
    """ New Agency Lead Form """

    template_args = dict()

    # Get all location, teams codetypes
    lead_args = get_basic_lead_data(request)
    template_args.update(lead_args)

    template_args.update({'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID})

    if request.method == 'POST':
        # Get the Who submit the lead
        is_google_rep = request.POST.get('is_google_rep')
        is_google_rep = True

        # Check the type of user
        customer_type = request.POST.get('customer_type')
        task_type = request.POST.get('task_type')
        agency_bundle = "%s-%s" % (request.user.email.split('@')[0], randint(0, 99999))

        ret_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
        # error_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None

        if is_google_rep:
            if customer_type == "agency":
                # get Agency related lead values
                if task_type == "same_task":
                    submit_agency_same_tasks(request, agency_bundle)
                elif task_type == 'diff_task':
                    # Agency Different Task submission
                    submit_agency_different_tasks(request, agency_bundle)
            elif customer_type == 'end_customer':
                if task_type == 'same_task':
                    submit_customer_lead_same_tasks(request, agency_bundle)
                elif task_type == 'diff_task':
                    # Customer Different Task submission
                    submit_customer_lead_different_tasks(request, agency_bundle)

            return redirect(ret_url)

    # Check The Rep Status and redirect
    form_name = get_lead_form_for_rep(request.user)

    if 'Lead' in form_name:
        return redirect('leads.views.lead_form')
    elif 'Bundle' in form_name:
        return redirect('leads.views.bundle_lead_form')

    return render(
        request,
        'leads/agent_lead_form.html',
        template_args
    )


# ######################## Agency Lead Functions ##################################
def submit_agency_same_tasks(request, agency_bundle):
    """ Agency Same Tasks Submission to SFDC """

    ret_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
    error_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
    if settings.SFDC == 'STAGE':
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00D7A0000008nBH'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    else:
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00Dd0000000fk18'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
    same_task_ctype = request.POST.get('same_task_ctype')
    if same_task_ctype != "Google Shopping Setup":
        # Get Tag lead fields
        agency_same_tag_count = request.POST.get('agency_same_tag_count')
        agency_same_tag_count = int(agency_same_tag_count) if agency_same_tag_count else 0

        for indx in range(1, agency_same_tag_count + 1):
            # Get Basic/Common form field data
            indx = str(indx)
            if settings.SFDC == 'STAGE':
                basic_data = get_common_sandbox_lead_data(request.POST)
            else:
                basic_data = get_common_salesforce_lead_data(request.POST)
            basic_data['retURL'] = ret_url
            basic_data['errorURL'] = error_url
            basic_data['oid'] = oid
            full_name = request.POST.get('contact_person_name')
            basic_data[basic_leads['agency_bundle']] = agency_bundle
            if full_name:
                first_name, last_name = split_fullname(full_name)
                basic_data['first_name'] = first_name
                basic_data['last_name'] = last_name
            tag_data = basic_data
            if int(indx) == 1:
                tag_data[tag_leads['tag_datepick']] = request.POST.get('tag_datepick')
            # tag fields
            tag_data[tag_leads['ctype1']] = same_task_ctype
            tag_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            tag_data[tag_leads['url1']] = request.POST.get('url' + indx)
            tag_data[tag_leads['comment1']] = request.POST.get('comment' + indx)
            tag_data[tag_leads['ga_setup1']] = request.POST.get('ga_setup' + indx)
            if str(request.POST.get('ga_setup' + indx)) == '1':
                tag_data[tag_leads['analytics_code1']] = request.POST.get('analytics_code' + indx)

            tag_data[tag_leads['call_extension1']] = request.POST.get('call_extension' + indx)
            tag_data[tag_leads['product_behaviour1']] = request.POST.get('product_behaviour' + indx)
            tag_data[tag_leads['cartpage_behaviour1']] = request.POST.get('cartpage_behaviour' + indx)
            tag_data[tag_leads['checkout_process1']] = request.POST.get('checkout_process' + indx)
            tag_data[tag_leads['transaction_behaviour1']] = request.POST.get('transaction_behaviour' + indx)

            tag_data[tag_leads['user_list_id1']] = request.POST.get('user_list_id' + indx)
            tag_data[tag_leads['rsla_bid_adjustment1']] = request.POST.get('rsla_bid_adjustment' + indx)
            tag_data[tag_leads['internal_cid1']] = request.POST.get('internal_cid' + indx)
            tag_data[tag_leads['campaign_ids1']] = request.POST.get('campaign_ids' + indx)
            tag_data[tag_leads['create_new_bid_modifiers1']] = request.POST.get('create_new_bid_modifiers' + indx)
            tag_data[tag_leads['overwrite_existing_bid_modifiers1']] = request.POST.get('overwrite_existing_bid_modifiers' + indx)
            # tag_data[tag_leads['rsla_policies1']] = request.POST.get('rsla_policies' + indx)

            # If Dynamic Remarketing tags
            tag_data[tag_leads['rbid1']] = request.POST.get('rbid' + indx)
            tag_data[tag_leads['rbudget1']] = request.POST.get('rbudget' + indx)
            submit_lead_to_sfdc(sf_api_url, tag_data)
    else:
        # Get Shop lead fields
        agency_same_shop_count = request.POST.get('agency_same_shop_count')
        agency_same_shop_count = int(agency_same_shop_count) if agency_same_shop_count else 0
        for indx in range(1, agency_same_shop_count + 1):
            indx = str(indx)
            # Get Basic/Common form field data
            if settings.SFDC == 'STAGE':
                basic_data = get_common_sandbox_lead_data(request.POST)
            else:
                basic_data = get_common_salesforce_lead_data(request.POST)

            basic_data['retURL'] = ret_url
            basic_data['errorURL'] = error_url
            basic_data['oid'] = oid
            basic_data[basic_leads['agency_bundle']] = agency_bundle
            full_name = request.POST.get('contact_person_name')
            if full_name:
                first_name, last_name = split_fullname(full_name)
                basic_data['first_name'] = first_name
                basic_data['last_name'] = last_name
            shop_data = basic_data
            if int(indx) == 1:
                shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')
            # Shop fields
            shop_data[shop_leads['ctype1']] = same_task_ctype
            shop_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            shop_data[shop_leads['shopping_url']] = request.POST.get('url' + indx)
            shop_data[shop_leads['comment1']] = request.POST.get('comment' + indx)
            shop_data[shop_leads['rbid']] = request.POST.get('rbid' + indx)
            shop_data[shop_leads['rbudget']] = request.POST.get('rbudget' + indx)
            shop_data[shop_leads['rbidmodifier']] = request.POST.get('rbidmodifier' + indx)
            shop_data[shop_leads['web_client_inventory']] = request.POST.get('web_client_inventory')
            shop_data[shop_leads['mc_id']] = request.POST.get('mc_id' + indx)
            submit_lead_to_sfdc(sf_api_url, shop_data)


def submit_agency_different_tasks(request, agency_bundle):
    """ Agency Differrnt Tasks Submission to SFDC """

    ret_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
    error_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
    if settings.SFDC == 'STAGE':
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00D7A0000008nBH'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    else:
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00Dd0000000fk18'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')

    agency_diff_tag_count = request.POST.get('agency_diff_tag_count')
    agency_diff_shop_count = request.POST.get('agency_diff_shop_count')
    total_leads = int(agency_diff_tag_count) + int(agency_diff_shop_count)
    is_tag_appointment_used = False
    is_shop_appointment_used = False
    for indx in range(1, total_leads + 1):
        indx = str(indx)
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)
        basic_data['retURL'] = ret_url
        basic_data['errorURL'] = error_url
        basic_data['oid'] = oid
        basic_data[basic_leads['agency_bundle']] = agency_bundle
        full_name = request.POST.get('contact_person_name')
        if full_name:
            first_name, last_name = split_fullname(full_name)
            basic_data['first_name'] = first_name
            basic_data['last_name'] = last_name
        tag_data = basic_data
        ctype = request.POST.get('diff_ctype' + indx)
        if ctype != 'Google Shopping Setup':
            if not is_tag_appointment_used:
                is_tag_appointment_used = True
                tag_data[tag_leads['tag_datepick']] = request.POST.get('tag_datepick')
            # tag fields
            tag_data[tag_leads['ctype1']] = ctype
            tag_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            tag_data[tag_leads['url1']] = request.POST.get('url' + indx)
            tag_data[tag_leads['comment1']] = request.POST.get('comment' + indx)
            tag_data[tag_leads['ga_setup1']] = request.POST.get('ga_setup' + indx)
            if str(request.POST.get('ga_setup' + indx)) == '1':
                tag_data[tag_leads['analytics_code1']] = request.POST.get('analytics_code' + indx)

            tag_data[tag_leads['call_extension1']] = request.POST.get('call_extension' + indx)
            tag_data[tag_leads['product_behaviour1']] = request.POST.get('product_behaviour' + indx)
            tag_data[tag_leads['cartpage_behaviour1']] = request.POST.get('cartpage_behaviour' + indx)
            tag_data[tag_leads['checkout_process1']] = request.POST.get('checkout_process' + indx)
            tag_data[tag_leads['transaction_behaviour1']] = request.POST.get('transaction_behaviour' + indx)

            tag_data[tag_leads['user_list_id1']] = request.POST.get('user_list_id' + indx)
            tag_data[tag_leads['rsla_bid_adjustment1']] = request.POST.get('rsla_bid_adjustment' + indx)
            tag_data[tag_leads['internal_cid1']] = request.POST.get('internal_cid' + indx)
            tag_data[tag_leads['campaign_ids1']] = request.POST.get('campaign_ids' + indx)
            tag_data[tag_leads['create_new_bid_modifiers1']] = request.POST.get('create_new_bid_modifiers' + indx)
            tag_data[tag_leads['overwrite_existing_bid_modifiers1']] = request.POST.get('overwrite_existing_bid_modifiers' + indx)
            # tag_data[tag_leads['rsla_policies1']] = request.POST.get('rsla_policies' + indx)

            # If Dynamic Remarketing tags
            tag_data[tag_leads['rbid1']] = request.POST.get('rbid' + indx)
            tag_data[tag_leads['rbudget1']] = request.POST.get('rbudget' + indx)
            submit_lead_to_sfdc(sf_api_url, tag_data)
        elif ctype == 'Google Shopping Setup':
            # Get Shop lead fields
            shop_data = basic_data
            if not is_shop_appointment_used:
                is_shop_appointment_used = True
                shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')

            shop_data[shop_leads['ctype1']] = ctype
            shop_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            shop_data[shop_leads['shopping_url']] = request.POST.get('url' + indx)
            shop_data[shop_leads['comment1']] = request.POST.get('comment' + indx)
            shop_data[shop_leads['rbid']] = request.POST.get('rbid' + indx)
            shop_data[shop_leads['rbudget']] = request.POST.get('rbudget' + indx)
            shop_data[shop_leads['rbidmodifier']] = request.POST.get('rbidmodifier' + indx)
            shop_data[shop_leads['web_client_inventory']] = request.POST.get('web_client_inventory')
            shop_data[shop_leads['mc_id']] = request.POST.get('mc_id' + indx)
            submit_lead_to_sfdc(sf_api_url, shop_data)


def submit_customer_lead_same_tasks(request, agency_bundle):
    """ Customer Same Tasks Submission to SFDC """

    ret_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
    error_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
    if settings.SFDC == 'STAGE':
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00D7A0000008nBH'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    else:
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00Dd0000000fk18'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')

    same_task_cust_type = request.POST.get('same_task_cust_type')
    if same_task_cust_type != "Google Shopping Setup":
        # Get Tag lead fields
        customer_same_tag_count = request.POST.get('customer_same_tag_count')
        customer_same_tag_count = int(customer_same_tag_count) if customer_same_tag_count else 0
        for indx in range(1, customer_same_tag_count + 1):
            indx = str(indx)
            # Get Basic/Common form field data
            if settings.SFDC == 'STAGE':
                basic_data = get_common_sandbox_lead_data(request.POST)
            else:
                basic_data = get_common_salesforce_lead_data(request.POST)
            basic_data['retURL'] = ret_url
            basic_data['errorURL'] = error_url
            basic_data['oid'] = oid
            basic_data[basic_leads['agency_bundle']] = agency_bundle
            full_name = request.POST.get('contact_person_name')
            if full_name:
                first_name, last_name = split_fullname(full_name)
                basic_data['first_name'] = first_name
                basic_data['last_name'] = last_name
            tag_data = basic_data
            tag_data[basic_leads['agency_poc']] = ''
            if int(indx) == 1:
                tag_data[tag_leads['tag_datepick']] = request.POST.get('tag_datepick')

            # Get End Customer Name details
            tag_data[basic_leads['advertiser_name']] = request.POST.get('advertiser_name' + indx)
            tag_data[basic_leads['aemail']] = request.POST.get('aemail' + indx)
            tag_data[basic_leads['phone']] = request.POST.get('phone' + indx)

            # tag fields
            tag_data[tag_leads['ctype1']] = same_task_cust_type
            tag_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            tag_data[tag_leads['url1']] = request.POST.get('url' + indx)
            tag_data[tag_leads['comment1']] = request.POST.get('comment' + indx)
            tag_data[tag_leads['ga_setup1']] = request.POST.get('ga_setup' + indx)
            if str(request.POST.get('ga_setup' + indx)) == '1':
                tag_data[tag_leads['analytics_code1']] = request.POST.get('analytics_code' + indx)

            tag_data[tag_leads['call_extension1']] = request.POST.get('call_extension' + indx)
            tag_data[tag_leads['product_behaviour1']] = request.POST.get('product_behaviour' + indx)
            tag_data[tag_leads['cartpage_behaviour1']] = request.POST.get('cartpage_behaviour' + indx)
            tag_data[tag_leads['checkout_process1']] = request.POST.get('checkout_process' + indx)
            tag_data[tag_leads['transaction_behaviour1']] = request.POST.get('transaction_behaviour' + indx)

            tag_data[tag_leads['user_list_id1']] = request.POST.get('user_list_id' + indx)
            tag_data[tag_leads['rsla_bid_adjustment1']] = request.POST.get('rsla_bid_adjustment' + indx)
            tag_data[tag_leads['internal_cid1']] = request.POST.get('internal_cid' + indx)
            tag_data[tag_leads['campaign_ids1']] = request.POST.get('campaign_ids' + indx)
            tag_data[tag_leads['create_new_bid_modifiers1']] = request.POST.get('create_new_bid_modifiers' + indx)
            tag_data[tag_leads['overwrite_existing_bid_modifiers1']] = request.POST.get('overwrite_existing_bid_modifiers' + indx)
            # tag_data[tag_leads['rsla_policies1']] = request.POST.get('rsla_policies' + indx)

            # If Dynamic Remarketing tags
            tag_data[tag_leads['rbid1']] = request.POST.get('rbid' + indx)
            tag_data[tag_leads['rbudget1']] = request.POST.get('rbudget' + indx)
            submit_lead_to_sfdc(sf_api_url, tag_data)
    else:
        # Get Shop lead fields
        customer_same_shop_count = request.POST.get('customer_same_shop_count')
        customer_same_shop_count = int(customer_same_shop_count) if customer_same_shop_count else 0
        for indx in range(1, customer_same_shop_count + 1):
            indx = str(indx)
            # Get Basic/Common form field data
            if settings.SFDC == 'STAGE':
                basic_data = get_common_sandbox_lead_data(request.POST)
            else:
                basic_data = get_common_salesforce_lead_data(request.POST)
            basic_data['retURL'] = ret_url
            basic_data['errorURL'] = error_url
            basic_data['oid'] = oid
            basic_data[basic_leads['agency_bundle']] = agency_bundle
            full_name = request.POST.get('contact_person_name')
            if full_name:
                first_name, last_name = split_fullname(full_name)
                basic_data['first_name'] = first_name
                basic_data['last_name'] = last_name
            shop_data = basic_data
            shop_data[basic_leads['agency_poc']] = ''
            if int(indx) == 1:
                shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')

            # Get End Customer Name details
            shop_data[basic_leads['advertiser_name']] = request.POST.get('advertiser_name' + indx)
            shop_data[basic_leads['aemail']] = request.POST.get('aemail' + indx)
            shop_data[basic_leads['phone']] = request.POST.get('phone' + indx)

            # Shop fields
            shop_data[shop_leads['ctype1']] = same_task_cust_type
            shop_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            shop_data[shop_leads['shopping_url']] = request.POST.get('url' + indx)
            shop_data[shop_leads['comment1']] = request.POST.get('comment' + indx)
            shop_data[shop_leads['rbid']] = request.POST.get('rbid' + indx)
            shop_data[shop_leads['rbudget']] = request.POST.get('rbudget' + indx)
            shop_data[shop_leads['rbidmodifier']] = request.POST.get('rbidmodifier' + indx)
            shop_data[shop_leads['web_client_inventory']] = request.POST.get('web_client_inventory')
            shop_data[shop_leads['mc_id']] = request.POST.get('mc_id' + indx)
            submit_lead_to_sfdc(sf_api_url, shop_data)


def submit_customer_lead_different_tasks(request, agency_bundle):
    """ Customer Different Tasks Submission to SFDC """

    ret_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
    error_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
    if settings.SFDC == 'STAGE':
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00D7A0000008nBH'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    else:
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00Dd0000000fk18'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')

    customer_diff_tag_count = request.POST.get('customer_diff_tag_count')
    customer_diff_shop_count = request.POST.get('customer_diff_shop_count')
    total_leads = int(customer_diff_tag_count) + int(customer_diff_shop_count)
    is_tag_appointment_used = False
    is_shop_appointment_used = False
    for indx in range(1, total_leads + 1):
        indx = str(indx)
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)
        basic_data['retURL'] = ret_url
        basic_data['errorURL'] = error_url
        basic_data['oid'] = oid
        basic_data[basic_leads['agency_bundle']] = agency_bundle
        full_name = request.POST.get('contact_person_name')
        if full_name:
            first_name, last_name = split_fullname(full_name)
            basic_data['first_name'] = first_name
            basic_data['last_name'] = last_name
        tag_data = basic_data
        tag_data[basic_leads['agency_poc']] = ''
        ctype = request.POST.get('diff_cust_type' + indx)

        if ctype != 'Google Shopping Setup':
            if not is_tag_appointment_used:
                is_tag_appointment_used = True
                tag_data[tag_leads['tag_datepick']] = request.POST.get('tag_datepick')
            # Get End Customer Name details
            tag_data[basic_leads['advertiser_name']] = request.POST.get('advertiser_name' + indx)
            tag_data[basic_leads['aemail']] = request.POST.get('aemail' + indx)
            tag_data[basic_leads['phone']] = request.POST.get('phone' + indx)

            # tag fields
            tag_data[tag_leads['ctype1']] = ctype
            tag_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            tag_data[tag_leads['url1']] = request.POST.get('url' + indx)
            tag_data[tag_leads['comment1']] = request.POST.get('comment' + indx)
            tag_data[tag_leads['ga_setup1']] = request.POST.get('ga_setup' + indx)
            if str(request.POST.get('ga_setup' + indx)) == '1':
                tag_data[tag_leads['analytics_code1']] = request.POST.get('analytics_code' + indx)

            tag_data[tag_leads['call_extension1']] = request.POST.get('call_extension' + indx)
            tag_data[tag_leads['product_behaviour1']] = request.POST.get('product_behaviour' + indx)
            tag_data[tag_leads['cartpage_behaviour1']] = request.POST.get('cartpage_behaviour' + indx)
            tag_data[tag_leads['checkout_process1']] = request.POST.get('checkout_process' + indx)
            tag_data[tag_leads['transaction_behaviour1']] = request.POST.get('transaction_behaviour' + indx)

            tag_data[tag_leads['user_list_id1']] = request.POST.get('user_list_id' + indx)
            tag_data[tag_leads['rsla_bid_adjustment1']] = request.POST.get('rsla_bid_adjustment' + indx)
            tag_data[tag_leads['internal_cid1']] = request.POST.get('internal_cid' + indx)
            tag_data[tag_leads['campaign_ids1']] = request.POST.get('campaign_ids' + indx)
            tag_data[tag_leads['create_new_bid_modifiers1']] = request.POST.get('create_new_bid_modifiers' + indx)
            tag_data[tag_leads['overwrite_existing_bid_modifiers1']] = request.POST.get('overwrite_existing_bid_modifiers' + indx)
            # tag_data[tag_leads['rsla_policies1']] = request.POST.get('rsla_policies' + indx)

            # If Dynamic Remarketing tags
            tag_data[tag_leads['rbid1']] = request.POST.get('rbid' + indx)
            tag_data[tag_leads['rbudget1']] = request.POST.get('rbudget' + indx)
            submit_lead_to_sfdc(sf_api_url, tag_data)
        elif ctype == 'Google Shopping Setup':
            shop_data = basic_data
            shop_data[basic_leads['agency_poc']] = ''

            if not is_shop_appointment_used:
                is_shop_appointment_used = True
                shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')

            # Get End Customer Name details
            shop_data[basic_leads['advertiser_name']] = request.POST.get('advertiser_name' + indx)
            shop_data[basic_leads['aemail']] = request.POST.get('aemail' + indx)
            shop_data[basic_leads['phone']] = request.POST.get('phone' + indx)

            # Get Shop lead fields
            shop_data[shop_leads['ctype1']] = ctype
            shop_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            shop_data[shop_leads['shopping_url']] = request.POST.get('url' + indx)
            shop_data[shop_leads['comment1']] = request.POST.get('comment' + indx)
            shop_data[shop_leads['rbid']] = request.POST.get('rbid' + indx)
            shop_data[shop_leads['rbudget']] = request.POST.get('rbudget' + indx)
            shop_data[shop_leads['rbidmodifier']] = request.POST.get('rbidmodifier' + indx)
            shop_data[shop_leads['web_client_inventory']] = request.POST.get('web_client_inventory')
            shop_data[shop_leads['mc_id']] = request.POST.get('mc_id' + indx)
            submit_lead_to_sfdc(sf_api_url, shop_data)
            # requests.post(url=sf_api_url, data=shop_data)

# ######################## Agency Lead Functions Ends ##############################


@login_required
@csrf_exempt
def agency_introduction_form(request):
    """ Agency Form """
    template_args = dict()

    # Get all location, teams codetypes
    lead_args = get_basic_lead_data(request)
    template_args.update(lead_args)

    agencies = AgencyDetails.objects.filter(google_rep_id=request.user.id)

    template_args.update({'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID,
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
@login_required
def agent_bulk_upload(request):
    """ Agency Bulk Upload """
    template_args = dict()
    lead_args = get_basic_lead_data(request)
    template_args = lead_args
    code_types = CodeType.objects.filter(is_active=True)
    template_args.update({'google_rep': request.user})

    # try:
    #     poc_details = ContactPerson.objects.get(person_id=pid)
    #     template_args['poc_details'] = poc_details
    # except ObjectDoesNotExist:
    #     template_args.update({'status': 'fail', 'error': 'Invalid POC'})
    #     return render(request, 'leads/agent_bulk_form.html', template_args)
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

            remaining = len(data_list) + 11
            template_args.update({'data': data_list, 'code_types': code_types, 'is_csv': True,
                                  'remaining': range(len(data_list) + 1, remaining)})
            return render(request, 'leads/agent_bulk_form.html', template_args)

        if 'paramcounts' in request.POST:
            if settings.SFDC == 'STAGE':
                sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
                basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
                oid = '00D7A0000008nBH'
            elif settings.SFDC == 'PRODUCTION':
                sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
                basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
                oid = '00Dd0000000fk18'

            params_count = request.POST.get('paramcounts')
            google_rep_id = request.POST.get('google_rep_id')
            # poc_id = request.POST.get('poc_id')

            ret_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None

            try:
                goggle_rep = User.objects.get(id=int(google_rep_id))
            except ObjectDoesNotExist:
                pass

            # try:
            #     poc = ContactPerson.objects.get(id=poc_id)
            # except ObjectDoesNotExist:
            #     pass
            for i in range(1, int(params_count) + 1):
                customer_id = request.POST.get('customer_id_' + str(i))
                location = request.POST.get('location_' + str(i))
                timezone = request.POST.get('timezone_' + str(i))
                agency_name = request.POST.get('agency_name_' + str(i))
                agency_phone = request.POST.get('agency_phone_' + str(i))
                agency_email = request.POST.get('agency_email_' + str(i))
                code_type = request.POST.get('code_type_' + str(i))
                url = request.POST.get('url_' + str(i))
                special_instructions = request.POST.get('special_instructions_' + str(i))

                first_name, last_name = split_fullname(agency_name)

                basic_lead_args = {
                    # Google Rep Information
                    'gref': goggle_rep.first_name + ' ' + goggle_rep.last_name,  # Full Name
                    'emailref': goggle_rep.email,                   # Rep Email
                    'manager_name': goggle_rep.profile.user_manager_name,  # Manager Name
                    'manager_email': goggle_rep.profile.user_manager_email,  # Manager Email
                    'team': goggle_rep.profile.team.team_name if goggle_rep.profile.team else '',  # Team
                    'service_segment': None,  # Service Segment
                    'g_cases_id': None,  # G Cases Id
                    'country': location,  # Country
                    'lead_type': 'Agency Bulk Lead',

                    'advertiser_name': '',  # Advertiser Email
                    'phone': '',  # Advertiser Phone
                    'company': '',    # Advertiser Company
                    'cid': customer_id,  # Customer ID

                    # 'language': poc.agency.language.language_name,  # Language
                    'language': '',  # Language
                    'tzone': timezone,  # Time Zone

                    # Advertiser Details
                    'advertiser_name': '',  # Advertiser Name
                    'first_name': first_name,  # First Name
                    'last_name': last_name,  # Last Name
                    'advertiser_location': '',  # Advertiser Location
                    'aemail': '',  # Advertiser Email
                    'phone': '',  # Advertiser phone
                    'company': '',  # Advertiser Company

                    # Webmaster Details
                    'fopt': '',  # Webmaster First Name
                    'lopt': '',  # Webmaster Last Name
                    'webmaster_name': '',    # Webmaster Name
                    'web_access': '',  # Web Access
                    'web_master_email': '',  # Webmaster Email
                    'popt': '',  # Webmaster Phone
                    'change_lead_owner': '1',    # Default value for Change Lead Owner

                    # Agency Details
                    'agency_name': agency_name,
                    'agency_email': agency_email,
                    'agency_phone': agency_phone,
                    'agency_poc': '',

                    'rep_location': '',
                    'Campaign_ID': None,
                    'oid': request.POST.get('oid'),
                    '__VIEWSTATE': request.POST.get('__VIEWSTATE'),
                }

                tag_data = {
                    'tag_datepick': '',  # TAG Appointment Date
                    'tag_primary_role': '',  # Role
                    # Code Type 1 Details
                    'ctype1': code_type,  # Code Type1
                    'url1': url,   # URL1
                    'code1': '',   # Code1
                    'comment1': special_instructions,  # Comments1
                    'rbid1': '',  # Recommended Bid1
                    'rbudget1': '',  # Recommended Budget1
                    'ga_setup1': '',  # Is GS Setup1
                }

                lead_args = dict()
                for key, value in basic_leads.items():
                    lead_args[value] = basic_lead_args.get(key)

                for key, value in tag_leads.items():
                    lead_args[value] = tag_data.get(key)
                lead_args['oid'] = oid
                lead_args['create_date'] = datetime.utcnow()  # Created Date
                # Post Lead data to SalesForce
                try:
                    submit_lead_to_sfdc(sf_api_url, lead_args)
                except Exception as e:
                    print e
            return redirect(ret_url)
            template_args.update({'is_csv': True})
    data_list = list()
    each_rec = dict()
    each_rec['customer_id'] = ''
    each_rec['code_type'] = ''
    each_rec['url'] = ''
    each_rec['special_instructions'] = ''
    data_list.append(each_rec)
    template_args.update({'data': data_list})
    return render(request, 'leads/agent_bulk_form.html', template_args)


# Create your views here.
@login_required
@csrf_exempt
@tag_user_required
def bundle_lead_form(request):

    """
    Bundle Lead Form
    Combination of 3 Code Types
    """
    if request.method == 'POST':

        return_url = bundle_lead_to_salesforce(request)
        return redirect(return_url)

    # Check the rep status and redirect
    form_name = get_lead_form_for_rep(request.user)

    if 'Lead' in form_name:
        return redirect('leads.views.lead_form')
    elif 'Agency' in form_name:
        return redirect('leads.views.agency_lead_form')

    lead_args = get_basic_lead_data(request)
    lead_args['PORTAL_MAIL_ID'] = settings.PORTAL_MAIL_ID
    return render(
        request,
        'leads/bundle_lead_form.html',
        lead_args
    )


def bundle_lead_to_salesforce(request):
    """ Bundle Lead to Sandbox  """
    complex_code_type = ['Google Shopping Setup']

    code_type1 = request.POST.get('ctype1')
    code_type2 = request.POST.get('ctype2')
    code_type3 = request.POST.get('ctype3')
    code_types = list()
    ctypes = ''
    if code_type1:
        ctypes += get_codetype_abbreviation(code_type1)
    if code_type2:
        ctypes += "+" + get_codetype_abbreviation(code_type2)
    if code_type3:
        ctypes += "+" + get_codetype_abbreviation(code_type3)

    # Get Basic/Common form filed data
    basic_data = dict()
    ret_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('retURL') if request.POST.get('retURL') else None
    error_url = request.META['wsgi.url_scheme'] + '://' + request.POST.get('errorURL') if request.POST.get('errorURL') else None
    lead_bundle = "%s-%s/%s/%s/%s" % (ctypes, randint(0, 99999), request.user.email.split('@')[0], datetime.utcnow().day, datetime.utcnow().month)
    if settings.SFDC == 'STAGE':
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
        oid = '00D7A0000008nBH'
    elif settings.SFDC == 'PRODUCTION':
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
        oid = '00Dd0000000fk18'

    if code_type1 in complex_code_type:
        basic_data = dict()
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)

        basic_data['retURL'] = ret_url
        basic_data['errorURL'] = error_url
        basic_data['oid'] = oid
        basic_data[basic_leads['bundle_bundle']] = lead_bundle

        if code_type1 != 'Google Shopping Setup':
            post_tag_lead_to_sf(request, request.POST, basic_data, [1])
        else:
            post_shopping_lead_to_sf(request, request.POST, basic_data, 1)
    elif code_type1:
        code_types.append(1)

    if code_type2 in complex_code_type:
        basic_data = dict()
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)
        basic_data['retURL'] = ret_url
        basic_data['errorURL'] = error_url
        basic_data['oid'] = oid
        basic_data[basic_leads['bundle_bundle']] = lead_bundle

        if code_type2 != 'Google Shopping Setup':
            post_tag_lead_to_sf(request, request.POST, basic_data, [2])
        else:
            post_shopping_lead_to_sf(request, request.POST, basic_data, 2)
    elif code_type2:
        code_types.append(2)

    if code_type3 in complex_code_type:
        basic_data = dict()
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)
        basic_data['retURL'] = ret_url
        basic_data['errorURL'] = error_url
        basic_data['oid'] = oid
        basic_data[basic_leads['bundle_bundle']] = lead_bundle

        if code_type3 != 'Google Shopping Setup':
            post_tag_lead_to_sf(request, request.POST, basic_data, [3])
        else:
            post_shopping_lead_to_sf(request, request.POST, basic_data, 3)
    elif code_type3:
        code_types.append(3)

    if code_types:
        basic_data = dict()
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE':
            basic_data = get_common_sandbox_lead_data(request.POST)
        else:
            basic_data = get_common_salesforce_lead_data(request.POST)
        basic_data['retURL'] = ret_url
        basic_data['errorURL'] = error_url
        basic_data['oid'] = oid
        basic_data[basic_leads['bundle_bundle']] = lead_bundle

        post_tag_lead_to_sf(request, request.POST, basic_data, code_types)

    return basic_data['retURL']


def post_tag_lead_to_sf(request, post_data, basic_data, code_types):
    """ Post Tag Lead to Salesforce """
    if settings.SFDC == 'STAGE':
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    elif settings.SFDC == 'PRODUCTION':
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')

    tag_data = dict()
    tag_data = basic_data

    if post_data.get('tag_contact_person_name1'):
        full_name = post_data.get('tag_contact_person_name1')
    else:
        full_name = post_data.get('advertiser_name')
    if full_name:
        first_name, last_name = split_fullname(full_name)
        tag_data['first_name'] = first_name
        tag_data['last_name'] = last_name

    tag_data[tag_leads.get('tag_primary_role')] = post_data.get('tag_primary_role') if post_data.get('tag_primary_role') else post_data.get('shop_primary_role')  # Role
    tag_data[tag_leads.get('tag_datepick')] = post_data.get('tag_datepick')  # TAG Appointment Date

    for indx in range(1, len(code_types) + 1):
        cindx = code_types[indx - 1]
        # Code Type 1 Details
        tag_data[tag_leads.get('ctype' + str(indx))] = post_data.get('ctype' + str(cindx))  # Code Type1
        tag_data[tag_leads.get('url' + str(indx))] = post_data.get('url' + str(cindx))  # URL1
        tag_data[tag_leads.get('comment' + str(indx))] = post_data.get('comment' + str(cindx))  # Comments1

        tag_data[tag_leads.get('ga_setup' + str(indx))] = post_data.get('ga_setup' + str(cindx))  # Comments1
        tag_data[tag_leads.get('analytics_code' + str(indx))] = post_data.get('analytics_code' + str(cindx))  # Recommended Budget

        tag_data[tag_leads.get('rbid' + str(indx))] = post_data.get('rbid_campaign' + str(cindx))  # Recommended Bid
        tag_data[tag_leads.get('rbudget' + str(indx))] = post_data.get('rbudget_campaign' + str(cindx))  # Recommended Budget

        tag_data[tag_leads.get('call_extension' + str(indx))] = post_data.get('call_extension' + str(cindx))
        tag_data[tag_leads.get('product_behaviour' + str(indx))] = post_data.get('product_behaviour' + str(cindx))
        tag_data[tag_leads.get('cartpage_behaviour' + str(indx))] = post_data.get('cartpage_behaviour' + str(cindx))
        tag_data[tag_leads.get('checkout_process' + str(indx))] = post_data.get('checkout_process' + str(cindx))
        tag_data[tag_leads.get('transaction_behaviour' + str(indx))] = post_data.get('transaction_behaviour' + str(cindx))

        tag_data[tag_leads.get('user_list_id' + str(indx))] = post_data.get('user_list_id' + str(cindx))
        tag_data[tag_leads.get('rsla_bid_adjustment' + str(indx))] = post_data.get('rsla_bid_adjustment' + str(cindx))
        tag_data[tag_leads.get('internal_cid' + str(indx))] = post_data.get('internal_cid' + str(cindx))
        tag_data[tag_leads.get('campaign_ids' + str(indx))] = post_data.get('campaign_ids' + str(cindx))
        tag_data[tag_leads.get('create_new_bid_modifiers' + str(indx))] = post_data.get('create_new_bid_modifiers' + str(cindx))
        tag_data[tag_leads.get('overwrite_existing_bid_modifiers' + str(indx))] = post_data.get('overwrite_existing_bid_modifiers' + str(cindx))
        # tag_data[tag_leads.get('rsla_policies' + str(indx))] = post_data.get('rsla_policies' + str(cindx))

        # elif indx == 2:
        #     # Code Type 2 Details
        #     tag_data[tag_leads.get('ctype' + str(indx))] = post_data.get('ctype' + str(indx))  # Code Type1
        #     tag_data[tag_leads.get('url' + str(indx))] = post_data.get('url' + str(indx))  # URL1
        #     tag_data[tag_leads.get('comment' + str(indx))] = post_data.get('comment' + str(indx))  # Comments1

        #     tag_data[tag_leads.get('ga_setup' + str(indx))] = post_data.get('ga_setup' + str(indx))  # Comments1

        #     if post_data.get('rbid_campaign' + str(indx)) and post_data.get('rbudget_campaign' + str(indx)):
        #         tag_data[tag_leads.get('rbid' + str(indx))] = post_data.get('rbid_campaign' + str(indx))  # Recommended Bid
        #         tag_data[tag_leads.get('rbudget' + str(indx))] = post_data.get('rbudget_campaign' + str(indx))  # Recommended Budget

        # elif indx == 3:
        #     # Code Type 3 Details
        #     tag_data[tag_leads.get('ctype' + str(indx))] = post_data.get('ctype' + str(indx))  # Code Type1
        #     tag_data[tag_leads.get('url' + str(indx))] = post_data.get('url' + str(indx))  # URL1
        #     tag_data[tag_leads.get('comment' + str(indx))] = post_data.get('comment' + str(indx))  # Comments1

        #     tag_data[tag_leads.get('ga_setup' + str(indx))] = post_data.get('ga_setup' + str(indx))  # Comments1

        #     if post_data.get('rbid_campaign' + str(indx)) and post_data.get('rbudget_campaign' + str(indx)):
        #         tag_data[tag_leads.get('rbid' + str(indx))] = post_data.get('rbid_campaign' + str(indx))  # Recommended Bid
        #         tag_data[tag_leads.get('rbudget' + str(indx))] = post_data.get('rbudget_campaign' + str(indx))  # Recommended Budget

    # Sandbox ID for TAD VIA GTM
    tag_data[tag_leads.get('tag_via_gtm')] = post_data.get('tag_via_gtm')  # Tag Via  GTM
    # requests.post(url=sf_api_url, data=tag_data)
    submit_lead_to_sfdc(sf_api_url, tag_data)


def post_shopping_lead_to_sf(request, post_data, basic_data, indx):
    """ Post Tag Lead to SandBox """

    if settings.SFDC == 'STAGE':
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    elif settings.SFDC == 'PRODUCTION':
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')

    setup_data = dict()
    setup_data = basic_data

    # if post_data.get('setup_datepick1') and indx == 1:
    #     setup_data[shop_leads.get('setup_datepick')] = post_data.get('setup_datepick1'),  # TAG Appointment Date
    if post_data.get('shop_contact_person_name1'):
        full_name = post_data.get('shop_contact_person_name1')
    else:
        full_name = post_data.get('advertiser_name')
    first_name, last_name = split_fullname(full_name)
    setup_data['first_name'] = first_name  # Primary Contact First Name
    setup_data['last_name'] = last_name  # Primary Contact Last Name

    setup_data[shop_leads.get('shop_primary_role')] = post_data.get('shop_primary_role') if post_data.get('shop_primary_role') else post_data.get('tag_primary_role')  # Role
    setup_data[shop_leads.get('ctype1')] = u'Google Shopping Setup'  # Code Type
    setup_data[shop_leads.get('mc_id')] = post_data.get('mc_id' + str(indx))  # MC-ID
    setup_data[shop_leads.get('web_client_inventory')] = post_data.get('web_client_inventory')  # Web Inventory
    setup_data[shop_leads.get('rbid')] = post_data.get('rbid' + str(indx))  # Recommended Bid
    setup_data[shop_leads.get('rbudget')] = post_data.get('rbudget' + str(indx))  # Recommended Budget
    setup_data[shop_leads.get('rbidmodifier')] = post_data.get('rbidmodifier' + str(indx))  # Recommended Mobile Bid Modifier
    setup_data[tag_leads.get('url1')] = post_data.get('url' + str(indx))  # Shopping URL

    # SandBox ID for IS SHOPPING POLICIES
    setup_data[shop_leads.get('is_shopping_policies')] = post_data.get('is_shopping_policies')  # Shopping Policies
    # requests.post(url=sf_api_url, data=setup_data)
    submit_lead_to_sfdc(sf_api_url, setup_data)


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
    lead_category = redirect_page
    redirect_page_source = {
        '1': reverse('leads.views.lead_form'),
        '2': reverse('leads.views.bundle_lead_form'),
        '3': reverse('leads.views.agency_lead_form'),
        '4': reverse('leads.views.wpp_lead_form'),
        '5': reverse('leads.views.agent_bulk_upload'),
        '6': reverse('leads.views.picasso_lead_form'),
        # '7': reverse('leads.views.picasso_build_wpp_form'),
        '8': reverse('leads.views.wpp_nomination_form'),
    }

    if redirect_page in redirect_page_source.keys():
        redirect_page = redirect_page_source[redirect_page]

    template_args = {'return_link': redirect_page, 'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID}

    if str(lead_category) == '4':
        template_args.update({'lead_type': 'WPP'})
    elif str(lead_category) == '6':
        estimated_tat = request.session.get(str(request.user.email)+'estimated_tat')
        no_of_inqueue_leads = request.session.get(str(request.user.email)+'no_of_inqueue_leads')
        template_args.update({'lead_type': 'Mobile Site Request', 'picasso': True, 'PORTAL_MAIL_ID': 'projectpicasso@regalix-inc.com', 'estimated_tat': estimated_tat, 'no_of_inqueue_leads': no_of_inqueue_leads})
    elif str(lead_category) == '8':
        template_args.update({'lead_type': 'Picasso Build Nomination Request', 'nomination': True})
    else:
        template_args.update({'lead_type': 'Implementation lead'})

    return render(request, 'leads/thankyou.html', template_args)


@login_required
def lead_error(request):
    """ Error message fail to submitting salesforce """
    redirect_page = request.GET.get('n', reverse('main.views.home'))
    redirect_page_key = redirect_page
    redirect_page_source = {
        '1': reverse('leads.views.lead_form'),
        '2': reverse('leads.views.bundle_lead_form'),
        '3': reverse('leads.views.agency_lead_form'),
        '4': reverse('leads.views.wpp_lead_form'),
        '5': reverse('leads.views.agent_bulk_upload'),
        '6': reverse('leads.views.picasso_lead_form'),
        # '7': reverse('leads.views.picasso_build_wpp_form'),
        '8': reverse('leads.views.wpp_nomination_form'),
    }

    if redirect_page in redirect_page_source.keys():
        redirect_page = redirect_page_source[redirect_page]

    template_args = {'return_link': redirect_page, 'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID}
    if str(redirect_page_key) == '6':
        template_args.update({'picasso': True})

    return render(request, 'leads/lead_error.html', template_args)


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


def get_lead(request, cid, feedback_type):
    """ Get lead information """
    lead = {'status': 'FAILED', 'details': None}
    if feedback_type == 'NORMAL':
        leads = Leads.objects.filter(customer_id=cid)
    elif feedback_type == 'PICASSO':
        leads = PicassoLeads.objects.filter(customer_id=cid)
    else:
        leads = WPPLeads.objects.filter(customer_id=cid)
    if not leads:
        return HttpResponse(json.dumps(lead), content_type='application/json')

    if len(leads) > 1:
        leads = leads
        adv_list = []
        if feedback_type == 'PICASSO':
            for each_lead in leads:
                details = {'name': each_lead.company, 'l_id': each_lead.sf_lead_id}
                adv_list.append(details)
        else:
            for each_lead in leads:
                details = {'name': each_lead.first_name + ' ' + each_lead.last_name, 'l_id': each_lead.sf_lead_id}
                adv_list.append(details)
        lead['status'] = "MULTIPLE"
        lead['details'] = adv_list
        return HttpResponse(json.dumps(lead), content_type='application/json')

    else:
        leads = leads[0]

    try:
        team = Team.objects.get(team_name=leads.team)
    except ObjectDoesNotExist:
        team = None

    try:
        location = Location.objects.get(location_name=leads.country)
        languages = location.language.all()
    except ObjectDoesNotExist:
        languages = None
        location = None

    if not languages:
        languages = Language.objects.all()
    languages_list = list()
    for lang in languages:
        languages_list.append({'l_id': lang.id, 'language_name': lang.language_name})
    if leads:
        lead['status'] = 'SUCCESS'

        if feedback_type == 'PICASSO':
            lead['details'] = {
            'name': leads.company,
            'email': leads.lead_owner_email,
            'google_rep_email': leads.google_rep_email,
            'loc': location.location_name if location else 0,
            'team': team.team_name if team else '',
            'team_id': team.id if team else 0,
            'languages_list': languages_list,
            'code_type': leads.type_1,
            'l_id': leads.sf_lead_id,
            }
        else:
            lead['details'] = {
                'name': leads.first_name + ' ' + leads.last_name,
                'email': leads.lead_owner_email,
                'google_rep_email': leads.google_rep_email,
                'loc': location.location_name if location else 0,
                'team': team.team_name if team else '',
                'team_id': team.id if team else 0,
                'languages_list': languages_list,
                'code_type': leads.type_1,
                'l_id': leads.sf_lead_id,
            }
    return HttpResponse(json.dumps(lead), content_type='application/json')


def get_lead_by_lid(request, lid, feedback_type):
    """ Get lead information """
    lead = {'status': 'FAILED', 'details': None}
    if feedback_type == 'NORMAL':
        leads = Leads.objects.get(sf_lead_id=lid)
    elif feedback_type == 'PICASSO':
        leads = PicassoLeads.objects.get(sf_lead_id=lid)
    else:
        leads = WPPLeads.objects.get(sf_lead_id=lid)
    try:
        team = Team.objects.get(team_name=leads.team)
    except ObjectDoesNotExist:
        team = None

    try:
        location = Location.objects.get(location_name=leads.country)
        languages = location.language.all()
    except ObjectDoesNotExist:
        languages = None
        location = None

    if not languages:
        languages = Language.objects.all()
    languages_list = list()
    for lang in languages:
        languages_list.append({'l_id': lang.id, 'language_name': lang.language_name})
    if leads:
        lead['status'] = 'SUCCESS'

        if feedback_type == 'PICASSO':
            lead['details'] = {
            'name': leads.company,
            'email': leads.lead_owner_email,
            'google_rep_email': leads.google_rep_email,
            'loc': location.location_name if location else 0,
            'team': team.team_name if team else '',
            'team_id': team.id if team else 0,
            'languages_list': languages_list,
            'code_type': leads.type_1,
            'l_id': leads.sf_lead_id,

        }
        else:
            lead['details'] = {
            'name': leads.first_name + ' ' + leads.last_name,
            'email': leads.lead_owner_email,
            'google_rep_email': leads.google_rep_email,
            'loc': location.location_name if location else 0,
            'team': team.team_name if team else '',
            'team_id': team.id if team else 0,
            'languages_list': languages_list,
            'code_type': leads.type_1,
            'l_id': leads.sf_lead_id,

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


def send_calendar_invite_to_advertiser(advertiser_details, is_attachment):

    mail_body = get_template('leads/advertiser_mail/appointment_confirmation.html').render(
        Context({
            'text': "Google Tag Implementation Support Appointment Confirmation",
            'lead_details': advertiser_details,
        })
    )

    bcc = set()

    if advertiser_details['code_type'] == 'WPP':
        mail_subject = "WPP Customer ID: %s PICASSO Build(WPP) Implementation Lead" % (advertiser_details['cid_std'])
        mail_to = set([
            # str(advertiser_details['email']),
            'asarkar@regalix-inc.com',
            'skumar@regalix-inc.com',
            'sprasad@regalix-inc.com',
            'abraham@regalix-inc.com',
            'gedward@regalix-inc.com',
            'anusha.panchikala@regalix-inc.com',
            'michelle.fernandes@regalix-inc.com',
        ])
    else:
        mail_subject = "WPP - Nomination CID: %s " % (advertiser_details['cid_std'])
        mail_to = set([
            # str(advertiser_details['email']),
            'asarkar@regalix-inc.com',
            'skumar@regalix-inc.com',
            'sprasad@regalix-inc.com',
            'gedward@regalix-inc.com',
            'vreguri@regalix-inc.com',
            'asarkar@regalix-inc.com',

        ])

    mail_from = "implementation-support@google.com"
    attachments = list()

    if is_attachment:
        ics_file = open(settings.MEDIA_ROOT + '/icallender_files/appointment.ics', 'r')
        appointment_file = File(ics_file)
        appointment_file.name = 'appointment.ics'
        attachments.append(appointment_file)

    # send_welcome_mail(mail_from, list(mail_to), mail_subject, mail_body, attachments)

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

    return 'Success'


@login_required
@tag_user_required
def get_lead_summary(request, lid=None, page=None):
    """ Lead Status page """

    lead_status = settings.LEAD_STATUS
    email = request.user.email
    if request.user.groups.filter(name='SUPERUSER'):
        # start_date, end_date = first_day_of_month(datetime.utcnow()), last_day_of_month(datetime.utcnow())
        start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        # start_date, end_date = get_previous_month_start_end_days(datetime.utcnow())
        # start_date = first_day_of_month(datetime.utcnow())
        # end_date = datetime.utcnow()
        query = {'lead_status__in': lead_status, 'created_date__gte': start_date, 'created_date__lte': end_date}
        leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(**query).order_by('-rescheduled_appointment_in_ist')[:1000]
        lead_ids = Leads.objects.values_list('id', flat=True).exclude(type_1__in=['WPP', '']).filter(**query).order_by('-rescheduled_appointment_in_ist')
        # lead_status_dict = get_count_of_each_lead_status_by_rep(email, 'normal', start_date=start_date, end_date=end_date)
        lead_status_dict = ReportService.get_leads_status_summary(lead_ids)
        del lead_status_dict['TAT']
    else:
        if is_manager(email):
            email_list = get_user_list_by_manager(email)
            email_list.append(email)
        else:
            email_list = [email]

        # prev_quarter_start_date, prev_quarter_end_date = prev_quarter_date_range(datetime.utcnow())
        cur_qtr_start_date, cur_qtr_end_date = get_quarter_date_slots(datetime.utcnow())
        leads = Leads.objects.exclude(type_1='WPP').filter(Q(google_rep_email__in=email_list) | Q(lead_owner_email__in=email_list),
                                                           lead_status__in=lead_status, created_date__gte=cur_qtr_start_date).order_by('-rescheduled_appointment_in_ist')

        lead_status_dict = get_count_of_each_lead_status_by_rep(email, 'normal', start_date=None, end_date=None)

    return render(request, 'leads/lead_summary.html', {'leads': leads, 'lead_status_dict': lead_status_dict, 'lead_id': lid})


@login_required
@wpp_user_required
def get_wpp_lead_summary(request, lid=None):
    """Lead status and summary of wpp leads"""
    treatment_types = [str(t_type.name) for t_type in TreatmentType.objects.all()]
    return render(request, 'leads/wpp_lead_summary.html', {'treatment_types': treatment_types, 'lead_id': lid})


@login_required
def get_wpp_lead_summary_by_treatment(request):
    """Lead status and summary of wpp leads"""
    lead_status = settings.WPP_LEAD_STATUS
    email = request.user.email
    treatment_type = request.GET.get('treatment_type')
    if treatment_type == 'all':
        treatment_type_list = [str(t_type.name) for t_type in TreatmentType.objects.all()]
    else:
        treatment_type_list = [treatment_type]
    if request.user.groups.filter(name='SUPERUSER'):
        # start_date, end_date = first_day_of_month(datetime.utcnow()), last_day_of_month(datetime.utcnow())
        # start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        # start_date, end_date = get_previous_month_start_end_days(datetime.utcnow())
        # start_date = first_day_of_month(datetime.utcnow())
        end_date = datetime.utcnow()
        start_date = datetime(2015, 01, 01)
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        status_count = wpp_lead_status_count_analysis(email, treatment_type_list, start_date, end_date)
        query = {'lead_status__in': lead_status, 'created_date__gte': start_date, 'created_date__lte': end_date}
        leads = WPPLeads.objects.filter(**query).order_by('-created_date')
        leads_list = [convert_lead_to_dict(lead) for lead in leads]
    else:
        if is_manager(email):
            email_list = get_user_list_by_manager(email)
            email_list.append(email)
        else:
            email_list = [email]

        mylist = [Q(google_rep_email__in=email_list), Q(lead_owner_email__in=email_list)]
        query = {'lead_status__in': lead_status}
        status_count = wpp_lead_status_count_analysis(email, treatment_type_list, start_date=None, end_date=None)
        leads = WPPLeads.objects.filter(reduce(operator.or_, mylist), **query).order_by('-created_date')
        leads_list = [convert_lead_to_dict(lead) for lead in leads]

    return HttpResponse(json.dumps({'leads_list': leads_list, 'status_count': status_count}))


@login_required
def get_lead_status_by_cid(request):
    """ Lead summary for given CID """
    if request.is_ajax:
        cid = request.GET.get('cid', None)
        leads = Leads.objects.exclude(type_1__in=['', 'WPP']).filter(customer_id=cid)
        lead_ids = [lead.id for lead in leads]
        lead_list = list()
        lead_status_dict = ReportService.get_leads_status_summary(lead_ids)
        for l in leads:
            lead = convert_lead_to_dict(l)
            lead_list.append(lead)
        mimetype = 'application/json'
        lead_list.sort(key=lambda item: item['rescheduled_appointment_in_ist'], reverse=True)
        return HttpResponse(json.dumps({'lead_list': lead_list, 'lead_status_dict': lead_status_dict}), mimetype)
    return render(request, 'leads/lead_summary.html', {})


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
        user_id = request.GET['user_id']
        user = User.objects.get(id=user_id)
        lead_status = settings.LEAD_STATUS
        leads_ids = Leads.objects.values_list(
            'id', flat=True).exclude(team__in=['', 'WPP']).filter(Q(google_rep_email=user.email) | Q(lead_owner_email=user.email), lead_status__in=lead_status)
        leads = Leads.objects.filter(id__in=leads_ids).order_by('-rescheduled_appointment_in_ist')
        lead_status_dict = ReportService.get_leads_status_summary(leads_ids)
        lead_list = list()
        for l in leads:
            lead = convert_lead_to_dict(l)
            lead_list.append(lead)
        # lead_status_dict = get_count_of_each_lead_status_by_rep(user.email, 'normal', start_date=None, end_date=None)
        mimetype = 'application/json'
        ldap_dict = dict()
        ldap_dict['manager'] = user.profile.user_manager_name
        ldap_dict['program'] = user.profile.team.team_name if user.profile.team else 'N/A'
        ldap_dict['region'] = user.profile.location.location_name if user.profile.location else 'N/A'
        lead_list.sort(key=lambda item: item['rescheduled_appointment_in_ist'], reverse=True)
        return HttpResponse(json.dumps({'lead_list': lead_list, 'lead_status_dict': lead_status_dict, 'ldap_dict': ldap_dict}), mimetype)
    # return render(request, 'leads/get_lead_summary_ldap.html', {})
    return render(request, 'leads/lead_summary.html', {})


@login_required
def lead_history(request, lid):
    template_args = dict()
    lead_status = collections.OrderedDict()
    lead_status['Open'] = {'title': 'Just received, studying requirements'}
    lead_status['In UI/UX Review'] = {'title': 'Awaiting response from advertiser on files/instructions'}
    lead_status['On Hold'] = {'title': 'On Hold'}
    lead_status['In Mockup'] = {'title': 'Regalix team designing the Mock Up'}
    lead_status['Mockup Review'] = {'title': 'Google CSRs &amp; Advertisers reviewing mock up'}
    lead_status['In Development'] = {'title': 'Regalix team coding the website'}
    lead_status['In Stage'] = {'title': 'On a staging server for feedback from the advertiser'}
    lead_status['In Stage - Adv Implementation'] = {'title': 'In Stage advance to Implementation'}
    lead_status['In A/B Test'] = {'title': 'A/B Test launched on Analytics/Adwords'}
    lead_status['Implemented'] = {'title': 'New website launched'}
    lead = None
    try:
        lead = WPPLeads.objects.get(sf_lead_id=lid)
        is_ab_test = lead.is_ab_test
        lead_status[lead.lead_status].update({'status': 'PROGRESS'})
        template_args['lead'] = lead
    except ObjectDoesNotExist:
        template_args['error'] = 'Lead does not exist'

    tat_by_status = collections.OrderedDict()
    for key, value in lead_status.iteritems():
        tat_by_status[key] = {'tat': '-'}

    # Get Lead History by WPP Lead Status
    field = 'WPP_Lead_Status__c'
    try:
        sf = SalesforceApi.connect_salesforce()
    except Exception:
        template_args['error'] = 'History Not exist'
    history = sf.query("SELECT Id, LeadID, Field, OldValue, NewValue, CreatedDate from LeadHistory WHERE LeadID = '%s' AND Field = '%s' ORDER BY CreatedDate ASC" % (lid, field))
    if lead:
        last_modified_date = lead.created_date
        tat_my_dict = collections.defaultdict(int)

        for i in range(0, len(history['records'])):
            old_status = history['records'][i]['OldValue']
            #  new_status = history['records'][i]['NewValue']
            status_modified_date = history['records'][i]['CreatedDate']
            status_modified_date = SalesforceApi.salesforce_date_to_datetime_format(status_modified_date)
            status_tat = tat_by_dates(last_modified_date, status_modified_date)
            tat_my_dict[old_status] += status_tat
            last_modified_date = status_modified_date

    if history['records']:
        final_new_status = history['records'][-1]['NewValue']
        final_prev_status = history['records'][-1]['OldValue']

        if final_new_status == 'On Hold':
            lead_status[final_prev_status].update({'status': 'PAUSE'})
            indx = lead_status.keys().index(final_prev_status)
        else:
            indx = lead_status.keys().index(final_new_status)
            lead_status[lead_status.keys()[indx]].update({'status': 'PROGRESS'})
    else:
        indx = lead_status.keys().index('Open')

    for i in range(0, indx):
        lead_status[lead_status.keys()[i]].update({'status': 'DONE'})
    for i in range(indx + 1, len(lead_status.keys())):
        lead_status[lead_status.keys()[i]].update({'status': 'FUTURE'})

    for key, value in tat_my_dict.iteritems():
        tat_by_status[key]['tat'] = value

    del lead_status['On Hold']

    if is_ab_test != 'Yes':
        del lead_status['In A/B Test']
        del tat_by_status['In A/B Test']

    template_args['tat_by_status'] = tat_by_status.iteritems()
    template_args['lead_status'] = lead_status.iteritems()

    if template_args['lead'].company:
        if 'http' in template_args['lead'].company:
            template_args['company_url'] = template_args['lead'].company
        else:
            template_args['company_url'] = 'http://' + template_args['lead'].company
    else:
        template_args['company_url'] = 'N/A'

    return render(request, 'leads/lead_history.html', template_args)


def tat_by_dates(start_date, end_date):
    """ Difference b/w 2 dates in days"""

    diff = max([start_date, end_date]) - min([start_date, end_date])
    return diff.days


def convert_lead_to_dict(model):
    lead = {}
    lead['lead_id'] = model.id
    lead['sf_lead_id'] = model.sf_lead_id
    lead['company'] = model.company
    lead['url'] = model.url_1
    lead['cid'] = model.customer_id
    lead['code_type'] = model.type_1
    lead['google_rep'] = model.google_rep_name
    lead['regalix_rep'] = model.lead_owner_name
    if model.created_date:
        lead['date_created'] = datetime.strftime(model.created_date, "%m/%d/%Y")
    else:
        lead['date_created'] = ''
    if model.appointment_date:
        lead['appointment_time'] = datetime.strftime(model.appointment_date, "%m/%d/%Y %I:%M %p")
    else:
        lead['appointment_time'] = ''
    if model.date_of_installation:
        lead['date_of_installation'] = datetime.strftime(model.date_of_installation, "%m/%d/%Y")
    else:
        lead['date_of_installation'] = ''
    if model.rescheduled_appointment:
        lead['rescheduled_appointment'] = datetime.strftime(model.rescheduled_appointment, "%m/%d/%Y %I:%M %p")
    else:
        lead['rescheduled_appointment'] = ''
    if model.rescheduled_appointment_in_ist:
        lead['rescheduled_appointment_in_ist'] = datetime.strftime(model.rescheduled_appointment_in_ist, "%m/%d/%Y %I:%M %p")
    else:
        lead['rescheduled_appointment_in_ist'] = ''
    lead['regalix_comment'] = model.regalix_comment
    lead['lead_status'] = model.lead_status
    if model.type_1 == 'WPP':
        lead['treatment_type'] = model.treatment_type
    return lead


def get_basic_lead_data(request):
    """ Get Basic Lead data for submit Leads """

    lead_args = dict()
    locations = Location.objects.filter(is_active=True)
    new_locations = list()
    all_locations = list()
    time_zone_for_region = dict()
    language_for_location = dict()
    for loc in locations:
        is_daylight_savings = False
        l = {'id': int(loc.id), 'name': str(loc.location_name)}
        all_locations.append(l)
        loc_name = str(loc.location_name)
        if loc.daylight_start and loc.daylight_end:
            daylight_start = datetime(loc.daylight_start.year, loc.daylight_start.month, loc.daylight_start.day, 0, 0, 0)
            daylight_end = datetime(loc.daylight_end.year, loc.daylight_end.month, loc.daylight_end.day, 11, 59, 59)
            if datetime.utcnow() >= daylight_start and datetime.utcnow() <= daylight_end:
                is_daylight_savings = True
            else:
                is_daylight_savings = False

        if is_daylight_savings:
            time_zone_for_region[loc_name] = [{'zone_name': str(tz[
                'zone_name']), 'time_value': str(tz['time_value']), 'id': str(tz['id'])} for tz in loc.ds_time_zone.values()]
        else:
            time_zone_for_region[loc_name] = [{'zone_name': str(tz[
                'zone_name']), 'time_value': str(tz['time_value']), 'id': str(tz['id'])} for tz in loc.time_zone.values()]
        language_for_location[loc_name] = [{'language_name': str(lang[
            'language_name'])} for lang in loc.language.values() if lang['language_name'] != loc.primary_language.language_name]
        if language_for_location[loc_name]:
            language_for_location[loc_name].insert(0, {'language_name': str(loc.primary_language.language_name), 'id': str(loc.primary_language.id)})
        else:
            language_for_location[loc_name].append({'language_name': str(loc.primary_language.language_name), 'id': str(loc.primary_language.id)})

    if 'google.com' in request.user.email:
        tag_teams = Team.objects.exclude(belongs_to__in=['WPP', 'PICASSO']).filter(is_active=True)
        teams = tag_teams.exclude(team_name__in=['Help Center Task', 'Help Centre Follow-ups', 'AdWords Front End (AWFE)', 'Help Centre Tasks - Inbound'])
    else:
        teams = Team.objects.exclude(belongs_to__in=['WPP', 'PICASSO']).filter(is_active=True)

    code_types = CodeType.objects.filter(is_active=True).values_list('name', flat=True)
    code_types = [str(ctype) for ctype in code_types]
    programs = ReportService.get_all_teams()
    programs = [str(pgm) for pgm in programs]

    regions = Region.objects.all()
    all_regions = list()
    region_locations = dict()
    for rgn in regions:
        for loc in rgn.location.all():
            region_locations[int(rgn.id)] = [int(loc.id) for loc in rgn.location.filter()]
        region_dict = dict()
        region_dict['id'] = int(rgn.id)
        region_dict['name'] = str(rgn.name)
        all_regions.append(region_dict)

    lead_args['locations'] = all_locations
    lead_args['new_locations'] = new_locations
    lead_args['teams'] = teams
    lead_args['code_types'] = code_types
    lead_args['programs'] = programs
    lead_args['time_zone_for_region'] = json.dumps(time_zone_for_region)
    lead_args['language_for_location'] = json.dumps(language_for_location)
    lead_args['programs'] = programs
    lead_args['regions'] = all_regions
    lead_args['region_locations'] = region_locations

    return lead_args


def get_all_sfdc_lead_ids(sfdc_type):
    """ Get all SFDC lead Ids """
    basic_leads = dict()
    tag_leads = dict()
    shop_leads = dict()
    if sfdc_type == 'sandbox':
        for key, value in SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.items():
            basic_leads[key] = value
        for key, value in SalesforceLeads.SANDBOX_TAG_LEAD_ARGS.items():
            tag_leads[key] = value
        for key, value in SalesforceLeads.SANDBOX_SHOPPING_ARGS.items():
            shop_leads[key] = value
    elif sfdc_type == 'production':
        for key, value in SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.items():
            basic_leads[key] = value
        for key, value in SalesforceLeads.PRODUCTION_TAG_LEADS_ARGS.items():
            tag_leads[key] = value
        for key, value in SalesforceLeads.PRODUCTION_SHOPPING_ARGS.items():
            shop_leads[key] = value
    return basic_leads, tag_leads, shop_leads


def submit_lead_to_sfdc(sf_api_url, lead_data):
    """ Submit lead to Salesforce """
    if "www" in sf_api_url:
        time_zone = lead_data.get(SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.get('tzone'))
        appointment_in_ist_key = SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.get('appointment_in_ist')
        appointment_in_pst_key = SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.get('appointment_in_pst')
        appointment_date = lead_data.get(SalesforceLeads.PRODUCTION_TAG_LEADS_ARGS.get('tag_datepick'))
        code_type = lead_data.get(SalesforceLeads.PRODUCTION_TAG_LEADS_ARGS.get('ctype1'))
        country = lead_data.get(SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.get('country'))
        team = lead_data.get(SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.get('team'))
        cid = lead_data.get(SalesforceLeads.PRODUCTION_BASIC_LEADS_ARGS.get('cid'))
    else:
        time_zone = lead_data.get(SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.get('tzone'))
        appointment_in_ist_key = SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.get('appointment_in_ist')
        appointment_in_pst_key = SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.get('appointment_in_pst')
        appointment_date = lead_data.get(SalesforceLeads.SANDBOX_TAG_LEAD_ARGS.get('tag_datepick'))
        code_type = lead_data.get(SalesforceLeads.SANDBOX_TAG_LEAD_ARGS.get('ctype1'))
        country = lead_data.get(SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.get('country'))
        team = lead_data.get(SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.get('team'))
        cid = lead_data.get(SalesforceLeads.SANDBOX_BASIC_LEADS_ARGS.get('cid'))
    if code_type and country and cid:
        appointment_in_ist = None
        appointment_in_pst = None
        if appointment_date:
            # Appointment date format Ex: 05/14/2015 10:30 AM
            appointment_date = datetime.strptime(appointment_date, "%m/%d/%Y %I:%M %p")

            # Convert Appointment to IST
            if time_zone == 'IST':
                appointment_in_ist = appointment_date
            else:
                tz = Timezone.objects.get(zone_name=time_zone)
                utc_date = SalesforceApi.get_utc_date(appointment_date, tz.time_value)

                tz_ist = Timezone.objects.get(zone_name='IST')
                appointment_in_ist = SalesforceApi.convert_utc_to_timezone(utc_date, tz_ist.time_value)

            appointment_in_ist = datetime.strftime(appointment_in_ist, '%m/%d/%Y %I:%M %p')

            # Convert Appointment to PST/PDT
            sf_timezone = SalesforceApi.get_current_timezone_of_salesforce()
            if time_zone == sf_timezone.zone_name:
                appointment_in_pst = appointment_date
            else:
                tz = Timezone.objects.get(zone_name=time_zone)
                utc_date = SalesforceApi.get_utc_date(appointment_date, tz.time_value)

                tz_ist = Timezone.objects.get(zone_name=sf_timezone.zone_name)
                appointment_in_pst = SalesforceApi.convert_utc_to_timezone(utc_date, tz_ist.time_value)
            appointment_in_pst = datetime.strftime(appointment_in_pst, '%m/%d/%Y %I:%M %p')
        lead_data[appointment_in_ist_key] = appointment_in_ist
        lead_data[appointment_in_pst_key] = appointment_in_pst
        sf_resp = None
        try:
            sf_resp = requests.post(url=sf_api_url, data=lead_data)
            # Get Advertiser Details
            advirtiser_details = get_advertiser_details(sf_api_url, lead_data)

            # Create Icallender (*.ics) file for send mail
            if advirtiser_details.get('appointment_date'):
                # create_icalendar_file(advirtiser_details)
                is_attachment = True
                # send_calendar_invite_to_advertiser(advirtiser_details, is_attachment)
            else:
                # Send Welcome email
                is_attachment = False
                # send_calendar_invite_to_advertiser(advirtiser_details, is_attachment)
        except Exception as e:
            print e
        return sf_resp


def get_codetype_abbreviation(code_type):
    """ Get Short cut Abbrevation for Code Type """

    if 'Analytics' in code_type:
        return 'GA'
    elif 'Shopping Setup' in code_type:
        return 'GS'
    else:
        return 'AW'


def get_advertiser_details(sf_api_url, lead_data):
    """ Get Agency Details with appointment date """
    agency_details = dict()
    if 'www' in sf_api_url:
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
    else:
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')

    agency_details['appointment_date'] = lead_data.get(tag_leads.get('tag_datepick'))
    agency_details['customer_id'] = lead_data.get(basic_leads.get('cid'))
    agency_details['country'] = lead_data.get(basic_leads.get('country'))
    if lead_data.get(basic_leads.get('aemail')):
        agency_details['email'] = lead_data.get(basic_leads.get('aemail'))
    else:
        agency_details['email'] = lead_data.get(basic_leads.get('agency_email'))
    agency_details['role'] = lead_data.get(tag_leads.get('tag_primary_role'))
    agency_details['code_type'] = lead_data.get(tag_leads.get('ctype1'))
    agency_details['cid_std'] = agency_details.get('customer_id').rsplit("-", 1)[0] + '-xxxx'

    first_name = lead_data.get(basic_leads.get('first_name'))
    last_name = lead_data.get(basic_leads.get('last_name'))

    if not first_name and not last_name:
        full_name = lead_data.get(basic_leads.get('advertiser_name'))

        if full_name:
            first_name, last_name = split_fullname(full_name)
            agency_details['first_name'] = first_name
            agency_details['last_name'] = last_name
        else:
            full_name = lead_data.get(basic_leads.get('agency_name'))
            first_name, last_name = split_fullname(full_name)
            agency_details['first_name'] = first_name
            agency_details['last_name'] = last_name
            agency_details['email'] = lead_data.get(basic_leads.get('agency_email'))
    else:
        agency_details['first_name'] = first_name
        agency_details['last_name'] = last_name

    if agency_details['code_type'] == 'WPP':
        agency_details['additional_notes'] = lead_data.get(basic_leads.get('additional_notes'))
        agency_details['email'] = lead_data.get(basic_leads.get('wpp_aemail'))
        agency_details['role'] = lead_data.get(basic_leads.get('advertiser_role'))
        agency_details['treatment_type'] = lead_data.get(basic_leads.get('treatment_type'))
        if agency_details['role'] == 'Other':
            agency_details['role_other'] = lead_data.get(basic_leads.get('role_other'))

    agency_details['telephone'] = lead_data.get(basic_leads.get('phone'))
    agency_details['google_rep_name'] = lead_data.get(basic_leads.get('gref'))
    agency_details['google_rep_email'] = lead_data.get(basic_leads.get('emailref'))
    agency_details['program'] = lead_data.get(basic_leads.get('team'))
    agency_details['website'] = lead_data.get(tag_leads.get('url1'))
    agency_details['ab_testing'] = lead_data.get(basic_leads.get('ab_testing'))
    agency_details['conversion_goal'] = lead_data.get(basic_leads.get('conversion_goal'))
    agency_details['timezone'] = lead_data.get(basic_leads.get('tzone'))
    # agency_details['comment'] = lead_data.get(tag_leads.get('comment1'))

    return agency_details


def split_fullname(full_name):
    """ Split Full Name as First and Last name """
    first_name = ''
    last_name = ''
    if full_name:
        first_name = full_name.rsplit(' ', 1)[0]
        last_name = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else '.'

    return first_name, last_name


def get_lead_form_for_rep(user):
    """ Check the user and redirect based on reps programs and locations """

    l_form = 'Lead From'

    if user.groups.filter(name='AGENCY'):
        return 'Agency Form'

    try:
        user_lead_form = LeadFormAccessControl.objects.get(google_rep__email=user.email)
        return user_lead_form.lead_form.name
    except ObjectDoesNotExist:
        access_controls = LeadFormAccessControl.objects.all()
        for control in access_controls:
            teams = [t.team_name for t in control.programs.filter()]
            locations = [l.location_name for l in control.target_location.filter()]
            emails = [usr.email for usr in control.google_rep.filter()]

            if user.email in emails:
                return control.lead_form.name
            elif user.profile.team and user.profile.location:
                if user.profile.team.team_name in teams and user.profile.location.location_name in locations:
                    return control.lead_form.name
                elif user.email in emails:
                    return control.lead_form.name
            else:
                continue

    return l_form


def get_pagination_lead_summary(request):
    ''' Gives paginated data for lead summary page'''
    if request.is_ajax:
        if request.user.groups.filter(name='SUPERUSER'):
            from_leads = request.GET.get('from')
            upto_leads = request.GET.get('to')
            start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
            query = {'lead_status__in': settings.LEAD_STATUS, 'created_date__gte': start_date, 'created_date__lte': end_date}
            leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(**query).order_by('-rescheduled_appointment_in_ist')[from_leads:upto_leads]
            lead_list = list()
            for l in leads:
                lead = convert_lead_to_dict(l)
                lead_list.append(lead)
            return HttpResponse(json.dumps(lead_list))
        else:
            return HttpResponse(json.dumps({'msg': 'Not a Superuser'}))


@login_required
def check_url_priority(request):
    """ Check priority for WPP URL """
    if request.is_ajax():
        url = request.GET.get('name')
        post_url = 'http://lp.wppperformance.com/wg/xp.php'
        data = {'url': url}
        res = requests.post(post_url, data=data)
        return HttpResponse(json.dumps({'json': res.json(), 'status': res.ok}))
    else:
        return HttpResponse('FAIL')


@login_required
def priority_check(request):
    """ Website priority Checker LP """
    template_args = dict()
    return render(request, 'leads/website_priority_checker.html', template_args)


@login_required
def report_team(request):
    """ Send/Report status code to WPP Team """
    url = request.GET.get('url')
    status_code = request.GET.get('status_code')
    mail_subject = "WPP Priority check inquiry"

    mail_body = get_template('leads/advertiser_mail/report_team.html').render(
        Context({
            'url': url,
            'status_code': status_code,
        })
    )

    bcc = set()

    mail_to = set([
        'skumar@regalix-inc.com',
        'sprasad@regalix-inc.com',
        'akumar@regalix-inc.com'
    ])

    mail_from = "implementation-support@google.com"
    attachments = list()

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)
    return HttpResponse(json.dumps('SUCCESS'))


@login_required
def get_picasso_lead_summary(request):
    if request.is_ajax():
        lead_status = settings.PICASSO_LEAD_STATUS
        email = request.user.email
        query = {'lead_status__in': lead_status}
        objective_type = request.GET.get('objective_type')
        if objective_type != 'all':
            query['picasso_objective'] = objective_type

        if request.user.groups.filter(name='SUPERUSER'):
            end_date = datetime.utcnow()
            start_date = datetime(2015, 01, 01)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            status_count = get_picasso_count_of_each_lead_status_by_rep(list(), objective_type, start_date, end_date)
            query['created_date__gte'] = start_date
            query['created_date__lte'] = end_date
            leads = PicassoLeads.objects.filter(**query).order_by('-created_date')
            leads_list = [convert_picasso_lead_to_dict(lead) for lead in leads]
        else:
            if is_manager(email):
                email_list = get_user_list_by_manager(email)
                email_list.append(email)
            else:
                email_list = [email]

            mylist = [Q(google_rep_email__in=email_list), Q(lead_owner_email__in=email_list)]
            status_count = get_picasso_count_of_each_lead_status_by_rep(email, objective_type, start_date=None, end_date=None)
            leads = PicassoLeads.objects.filter(reduce(operator.or_, mylist), **query).order_by('-created_date')
            leads_list = [convert_picasso_lead_to_dict(lead) for lead in leads]

        return HttpResponse(json.dumps({'leads_list': leads_list, 'status_count': status_count}))
    return render(request, 'leads/picasso_lead_summary.html', {'picasso': True})


def convert_picasso_lead_to_dict(model):
    lead = {}
    lead['lead_id'] = model.id
    lead['sf_lead_id'] = model.sf_lead_id
    lead['company'] = model.company
    lead['url'] = model.url_1
    lead['cid'] = model.customer_id
    lead['code_type'] = model.type_1
    lead['google_rep'] = model.google_rep_name
    lead['regalix_rep'] = model.lead_owner_name
    if model.created_date:
        lead['date_created'] = datetime.strftime(model.created_date, "%m/%d/%Y")
    else:
        lead['date_created'] = ''
    if model.date_of_installation:
        lead['date_of_installation'] = datetime.strftime(model.date_of_installation, "%m/%d/%Y")
    else:
        lead['date_of_installation'] = ''
    lead['regalix_comment'] = model.regalix_comment
    lead['lead_status'] = model.lead_status
    lead['pod_name'] = model.pod_name
    lead['picasso_objective'] = model.picasso_objective
    return lead


def get_eligible_picasso_leads(request):
    """ Eligible picasso lead as WPP Lead
        1. Lead should be build Eligible.
        2. Lead's program name should be in WPP programs list.

    """
    if request.is_ajax():
        lead = {'status': 'FAILED', 'details': None}
        cid = request.GET.get('cid')
        if '-' in cid:
            cid = cid
        elif len(cid) == 10:
            cid = '%s-%s-%s' % (cid[:3], cid[3:6], cid[6:])
        wpp_teams = [team.team_name for team in Team.objects.filter(belongs_to__in=['WPP', 'BOTH'])]
        leads = WPPLeads.objects.filter(customer_id=cid, team__in=wpp_teams, type_1='WPP - Nomination')
        if leads:
            lead_type = 'nomination'
        else:
            leads = PicassoLeads.objects.filter(customer_id=cid, team__in=wpp_teams, is_build_eligible=True)
            if leads:
                lead_type = 'picasso'
            else:
                return HttpResponse(json.dumps(lead), content_type='application/json')

        if len(leads) > 1:
            leads = leads
            url_list = []
            for each_lead in leads:
                details = dict()
                details['lead_details'] = {
                    'l_id': each_lead.sf_lead_id,
                    'url': each_lead.url_1,
                }
                url_list.append(details)
            lead['status'] = "MULTIPLE"
            lead['details'] = url_list
            return HttpResponse(json.dumps(lead), content_type='application/json')

        else:
            leads = leads[0]

        try:
            team = Team.objects.get(team_name=leads.team)
        except ObjectDoesNotExist:
            team = None

        if leads:
            lead['status'] = 'SUCCESS'

            lead['details'] = {
                'name': leads.first_name + ' ' + leads.last_name,
                'email': leads.lead_owner_email,
                'google_rep_email': leads.google_rep_email,
                'team': team.team_name if team else '',
                'code_type': leads.type_1,
                'l_id': leads.sf_lead_id,
                'url': leads.url_1,
                'treatment_type': leads.treatment_type,
            }
        if lead_type == 'nomination':
            # Objectives in Wpp stored in comment_5 field since we are not using this
            lead['details']['picasso_objectives'] = leads.comment_5.split(',')
            lead['details']['pod_name'] = leads.url_5
            lead['details']['country'] = leads.country
        else:
            lead['details']['pod_name'] = leads.pod_name
            lead['details']['picasso_objectives'] = leads.picasso_objective.split(',')
    return HttpResponse(json.dumps(lead), content_type='application/json')


def get_eligible_picasso_lead_by_lid(request):
    """Get Specific Lead from mulitple elegible leads with same CID by using lead id"""
    if request.is_ajax():
        lead = {'status': 'FAILED', 'details': None}
        lid = request.GET.get('lid')

        leads = WPPLeads.objects.filter(sf_lead_id=lid)
        if leads:
            leads = leads[0]
            lead_type = 'nomination'
        else:
            leads = PicassoLeads.objects.filter(sf_lead_id=lid)
            if leads:
                leads = leads[0]
                lead_type = 'picasso'

        try:
            team = Team.objects.get(team_name=leads.team)
        except ObjectDoesNotExist:
            team = None

        lead['status'] = 'SUCCESS'

        lead['details'] = {
            'name': leads.first_name + ' ' + leads.last_name,
            'email': leads.lead_owner_email,
            'google_rep_email': leads.google_rep_email,
            'team': team.team_name if team else '',
            'code_type': leads.type_1,
            'l_id': leads.sf_lead_id,
            'url': leads.url_1,
            'treatment_type': leads.treatment_type,

        }
        if lead_type == 'nomination':
            # Objectives in Wpp stored in comment_5 field since we are not using this
            lead['details']['picasso_objectives'] = leads.comment_5.split(',')
            lead['details']['pod_name'] = leads.url_5
            lead['details']['country'] = leads.country
        else:
            lead['details']['pod_name'] = leads.pod_name
            lead['details']['picasso_objectives'] = leads.picasso_objective.split(',')

    return HttpResponse(json.dumps(lead), content_type='application/json')


def searh_leads(request):
    """
    From Lead status field Searching the leads with matching search text
    """
    if request.is_ajax:
        start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        search_text = request.GET.get('search-text', None)
        lead_type = request.GET.get('lead-type', None)
        if search_text:
            fieldnames = ['lead_owner_name', 'lead_owner_email', 'google_rep_name', 'google_rep_email', 'customer_id', 'company', 'team', 'type_1']
            qgroup = reduce(operator.or_, (Q(**{fieldname + '%s' % ('__icontains'): search_text}) for fieldname in fieldnames))
            if 'TAG' in lead_type:
                leads = Leads.objects.filter(qgroup, created_date__gte=start_date, created_date__lte=end_date)
            else:
                leads = WPPLeads.objects.filter(qgroup)

        lead_ids = [lead.id for lead in leads]
        lead_list = list()
        lead_status_dict = ReportService.get_leads_status_summary(lead_ids)
        for l in leads:
            lead = convert_lead_to_dict(l)
            lead_list.append(lead)
        mimetype = 'application/json'
        lead_list.sort(key=lambda item: item['rescheduled_appointment_in_ist'], reverse=True)
        return HttpResponse(json.dumps({'lead_list': lead_list, 'lead_status_dict': lead_status_dict}), mimetype)
    if 'TAG' in lead_type:
        return render(request, 'leads/lead_summary.html', {})
    else:
        return render(request, 'leads/wpp_lead_summary.html', {})


def wpp_whitelist_request(request):
    if request.is_ajax():
        user = UserDetails.objects.get(user=request.user)
        notes = request.GET.get('notes')
        mail_subject = "[Website Opt] Please whitelist for website performance optimization submissions"
        mail_body = get_template('leads/email_templates/whitelist_request_template.html').render(
            Context({
                'program': user.team,
                'market': user.location,
                'ldap': request.user.email,
                'pod_name': user.pod_name,
                'notes': notes,
                'signature': request.user.first_name,
            })
        )
        mail_from = 'Picasso Build Request Team'
        mail_to = ['basavaraju@regalix-inc.com', 'gtracktesting@gmail.com', 'skumar@regalix-inc.com', 'sprasad@regalix-inc.com']
        bcc = set([])
        attachments = list()
        send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)
        return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
