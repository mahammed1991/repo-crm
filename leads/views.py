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
from leads.models import (Leads, Location, Team, CodeType, ChatMessage, Language, ContactPerson,
                          AgencyDetails, LeadFormAccessControl
                          )
from main.models import UserDetails
from lib.helpers import (get_quarter_date_slots, send_mail, get_count_of_each_lead_status_by_rep,
                         is_manager, get_user_list_by_manager, get_manager_by_user)
from icalendar import Calendar, Event, vCalAddress, vText
from django.core.files import File
from django.contrib.auth.models import User
from reports.report_services import ReportService, DownloadLeads
from lib.helpers import date_range_by_quarter, get_previous_month_start_end_days, first_day_of_month
from django.db.models import Q
from random import randint
from lib.sf_lead_ids import SalesforceLeads
from reports.models import Region


# Create your views here.
@login_required
@csrf_exempt
def lead_form(request):

    """
    Lead Submission to Salesforce
    """
    if request.method == 'POST':
        if settings.SFDC == 'STAGE':
            sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
            oid = '00DZ000000MipUa'
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
                tag_data[tag_leads[rbid_key]] = request.POST.get(rbid_key)
                tag_data[tag_leads[rbudget_key]] = request.POST.get(rbudget_key)
                tag_data[tag_leads[ga_setup_key]] = request.POST.get(ga_setup_key)

            # Split Tag Contact Person Name to First and Last Name
            if request.POST.get('tag_contact_person_name'):
                full_name = request.POST.get('tag_contact_person_name')
            else:
                full_name = request.POST.get('advertiser_name')
            tag_data['first_name'] = full_name.rsplit(' ', 1)[0]  # Primary Contact Name
            tag_data['last_name'] = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else ''
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
                first_name = full_name.rsplit(' ', 1)[0]
                last_name = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else ''
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
    lead_args = get_basic_lead_data()
    lead_args['PORTAL_MAIL_ID'] = settings.PORTAL_MAIL_ID
    return render(
        request,
        'leads/lead_form.html',
        lead_args
    )


@login_required
@csrf_exempt
def wpp_lead_form(request):

    """
    Lead Submission to Salesforce
    """
    # Check The Rep Status and redirect
    if request.method == 'POST':
        if settings.SFDC == 'STAGE':
            sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
            basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
            oid = '00DZ000000MipUa'
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
            wpp_data[value] = request.POST.get(key)

        submit_lead_to_sfdc(sf_api_url, wpp_data)

        return redirect(ret_url)

    # Get all location, teams codetypes
    lead_args = get_basic_lead_data()
    return render(
        request,
        'leads/wpp_lead_form.html',
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
    lead_args = get_basic_lead_data()
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
    if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00DZ000000MipUa'
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
            if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
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
            tag_data[tag_leads['ga_setup1']] = request.POST.get('gasetup_sameAgency')

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
            if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
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
            # if int(indx) == 1:
            #     shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')
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
    if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00DZ000000MipUa'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    else:
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00Dd0000000fk18'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')

    agency_diff_tag_count = request.POST.get('agency_diff_tag_count')
    agency_diff_shop_count = request.POST.get('agency_diff_shop_count')
    total_leads = int(agency_diff_tag_count) + int(agency_diff_shop_count)
    is_appointment_used = False
    for indx in range(1, total_leads + 1):
        indx = str(indx)
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
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
            if not is_appointment_used:
                is_appointment_used = True
                tag_data[tag_leads['tag_datepick']] = request.POST.get('tag_datepick')
            # tag fields
            tag_data[tag_leads['ctype1']] = ctype
            tag_data[basic_leads['cid']] = request.POST.get('cid' + indx)
            tag_data[tag_leads['url1']] = request.POST.get('url' + indx)
            tag_data[tag_leads['comment1']] = request.POST.get('comment' + indx)
            tag_data[tag_leads['ga_setup1']] = request.POST.get('ga_setup' + indx)

            # If Dynamic Remarketing tags
            tag_data[tag_leads['rbid1']] = request.POST.get('rbid' + indx)
            tag_data[tag_leads['rbudget1']] = request.POST.get('rbudget' + indx)
            submit_lead_to_sfdc(sf_api_url, tag_data)
        elif ctype == 'Google Shopping Setup':
            # Get Shop lead fields
            shop_data = basic_data
            # if int(indx) == 1:
            #     shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')
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
    if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00DZ000000MipUa'
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
            if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
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
            tag_data[tag_leads['ga_setup1']] = request.POST.get('ga_setupSamecustomer')

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
            if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
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
            # if int(indx) == 1:
            #     shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')

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
    if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
        sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00DZ000000MipUa'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
    else:
        sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
        oid = '00Dd0000000fk18'
        basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')

    customer_diff_tag_count = request.POST.get('customer_diff_tag_count')
    customer_diff_shop_count = request.POST.get('customer_diff_shop_count')
    total_leads = int(customer_diff_tag_count) + int(customer_diff_shop_count)
    is_appointment_used = False
    for indx in range(1, total_leads + 1):
        indx = str(indx)
        # Get Basic/Common form field data
        if settings.SFDC == 'STAGE' and not request.user.groups.filter(name='AGENCY'):
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
            if not is_appointment_used:
                is_appointment_used = True
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

            # If Dynamic Remarketing tags
            tag_data[tag_leads['rbid1']] = request.POST.get('rbid' + indx)
            tag_data[tag_leads['rbudget1']] = request.POST.get('rbudget' + indx)
            submit_lead_to_sfdc(sf_api_url, tag_data)
        elif ctype == 'Google Shopping Setup':
            shop_data = basic_data
            shop_data[basic_leads['agency_poc']] = ''
            # if int(indx) == 1:
            #     shop_data[shop_leads['setup_datepick']] = request.POST.get('setup_datepick')

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
def agency_form(request):
    """ Agency Form """
    template_args = dict()

    # Get all location, teams codetypes
    lead_args = get_basic_lead_data()
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
def agent_bulk_upload(request, agency_name, pid):
    """ Agency Bulk Upload """
    template_args = dict()
    locations = Location.objects.filter(is_active=True)
    teams = Team.objects.filter(is_active=True)
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
        loc_name = str(loc.location_name)
        time_zone_for_region[loc_name] = [{'zone_name': str(tz[
            'zone_name']), 'time_value': str(tz['time_value'])} for tz in loc.time_zone.values()]
        language_for_location[loc_name] = [{'language_name': str(lang[
            'language_name'])} for lang in loc.language.values() if lang['language_name'] != loc.primary_language.language_name]
        if language_for_location[loc_name]:
            language_for_location[loc_name].insert(0, {'language_name': str(loc.primary_language.language_name)})
        else:
            language_for_location[loc_name].append({'language_name': str(loc.primary_language.language_name)})

    code_types = CodeType.objects.filter(is_active=True)
    template_args.update({'code_types': code_types, 'locations': all_locations, 'teams': teams,
                          'time_zone_for_region': time_zone_for_region, 'language_for_location': language_for_location})

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

            remaining = len(data_list) + 11
            template_args.update({'data': data_list, 'code_types': code_types, 'is_csv': True, 'agency_name': agency_name, 'pid': pid,
                                  'remaining': range(len(data_list) + 1, remaining)})
            return render(request, 'leads/agent_bulk_form.html', template_args)

        if 'paramcounts' in request.POST:
            if settings.SFDC == 'STAGE':
                sf_api_url = 'https://test.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
                basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('sandbox')
                oid = '00DZ000000MipUa'
            elif settings.SFDC == 'PRODUCTION':
                sf_api_url = 'https://www.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8'
                basic_leads, tag_leads, shop_leads = get_all_sfdc_lead_ids('production')
                oid = '00Dd0000000fk18'

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
                    'email': goggle_rep.email,                   # Rep Email
                    'manager_name': goggle_rep.profile.user_manager_name,  # Manager Name
                    'manager_email': goggle_rep.profile.user_manager_email,  # Manager Email
                    'team': goggle_rep.profile.team.team_name if goggle_rep.profile.team else '',  # Team
                    'service_segment': None,  # Service Segment
                    'g_cases_id': None,  # G Cases Id
                    'country': location,  # Country

                    'advertiser_name': '',  # Advertiser Email
                    'phone': '',  # Advertiser Phone
                    'company': '',    # Advertiser Company
                    'cid': customer_id,  # Customer ID

                    'language': poc.agency.language.language_name,  # Language
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

            template_args.update({'is_csv': True})
    return render(request, 'leads/agent_bulk_form.html', template_args)


# Create your views here.
@login_required
@csrf_exempt
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

    lead_args = get_basic_lead_data()
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
        oid = '00DZ000000MipUa'
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

        tag_data[tag_leads.get('rbid' + str(indx))] = post_data.get('rbid_campaign' + str(cindx))  # Recommended Bid
        tag_data[tag_leads.get('rbudget' + str(indx))] = post_data.get('rbudget_campaign' + str(cindx))  # Recommended Budget

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
    first_name = full_name.rsplit(' ', 1)[0]
    last_name = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else ''
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
    }

    if redirect_page in redirect_page_source.keys():
        redirect_page = redirect_page_source[redirect_page]

    if str(lead_category) == '4':
        template = 'leads/thankyou_wpp.html'
    else:
        template = 'leads/thankyou.html'

    return render(request, template, {'return_link': redirect_page, 'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID})


@login_required
def lead_error(request):
    """ Error message fail to submitting salesforce """
    redirect_page = request.GET.get('n', reverse('main.views.home'))
    redirect_page_source = {
        '1': reverse('leads.views.lead_form'),
        '2': reverse('leads.views.bundle_lead_form'),
        '3': reverse('leads.views.agency_lead_form'),
    }

    if redirect_page in redirect_page_source.keys():
        redirect_page = redirect_page_source[redirect_page]

    return render(request, 'leads/lead_error.html', {'return_link': redirect_page, 'PORTAL_MAIL_ID': settings.PORTAL_MAIL_ID})


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
    if not leads:
        return HttpResponse(json.dumps(lead), content_type='application/json')

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


def send_calendar_invite_to_advertiser(advertiser_details, is_attachment):
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
        str(advertiser_details['email']),
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
def get_lead_summary(request, lid=None):
    """ Lead Status page """

    lead_status = settings.LEAD_STATUS
    email = request.user.email
    if request.user.groups.filter(name='SUPERUSER'):
        # start_date, end_date = first_day_of_month(datetime.utcnow()), last_day_of_month(datetime.utcnow())
        # start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        # start_date, end_date = get_previous_month_start_end_days(datetime.utcnow())
        start_date = first_day_of_month(datetime.utcnow())
        end_date = datetime.utcnow()
        query = {'lead_status__in': lead_status, 'created_date__gte': start_date, 'created_date__lte': end_date}
        leads = Leads.objects.filter(**query)
        lead_status_dict = get_count_of_each_lead_status_by_rep(email, 'normal', start_date=start_date, end_date=end_date)
    else:
        if is_manager(email):
            email_list = get_user_list_by_manager(email)
        else:
            email_list = [email]

        if 'regalix' in email:
            leads = Leads.objects.filter(lead_status__in=lead_status, lead_owner_email__in=email_list)
        elif 'google' in email:
            leads = Leads.objects.filter(lead_status__in=lead_status, google_rep_email__in=email_list)

        lead_status_dict = get_count_of_each_lead_status_by_rep(email, 'normal', start_date=None, end_date=None)
    return render(request, 'leads/lead_summary.html', {'leads': leads, 'lead_status_dict': lead_status_dict, 'lead_id': lid})


@login_required
def get_wpp_lead_summary(request, lid=None):
    """Lead status and summary of wpp leads"""

    lead_status = settings.WPP_LEAD_STATUS
    email = request.user.email
    if request.user.groups.filter(name='SUPERUSER'):
        # start_date, end_date = first_day_of_month(datetime.utcnow()), last_day_of_month(datetime.utcnow())
        # start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        # start_date, end_date = get_previous_month_start_end_days(datetime.utcnow())
        start_date = first_day_of_month(datetime.utcnow())
        end_date = datetime.utcnow()
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        lead_status_dict = get_count_of_each_lead_status_by_rep(email, 'wpp', start_date=start_date, end_date=end_date)
        query = {'type_1': 'WPP', 'lead_status__in': lead_status, 'created_date__gte': start_date, 'created_date__lte': end_date}
        leads = Leads.objects.filter(**query)
    else:
        if is_manager(email):
            email_list = get_user_list_by_manager(email)
        else:
            email_list = [email]

        if 'regalix' in email:
            leads = Leads.objects.filter(lead_status__in=lead_status, lead_owner_email__in=email_list)
        elif 'google' in email:
            leads = Leads.objects.filter(lead_status__in=lead_status, google_rep_email__in=email_list)

        lead_status_dict = get_count_of_each_lead_status_by_rep(email, 'wpp', start_date=None, end_date=None)
    return render(request, 'leads/wpp_lead_summary.html', {'leads': leads, 'lead_status_dict': lead_status_dict, 'lead_id': lid})


@login_required
def get_lead_status_by_cid(request):
    """ Lead summary for given CID """
    if request.is_ajax:
        cid = request.GET.get('cid')
        leads = Leads.objects.filter(customer_id=cid)
        lead_list = list()
        for l in leads:
            lead = convert_lead_to_dict(l)
            lead_list.append(lead)
        mimetype = 'application/json'
        return HttpResponse(json.dumps({'lead_list': lead_list}), mimetype)
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
        lead_status = ['In Queue', 'Attempting Contact', 'In Progress', 'In Active', 'Implemented']
        user_id = request.GET['user_id']
        user = User.objects.get(id=user_id)
        leads = Leads.objects.filter(Q(google_rep_email=user.email) | Q(lead_owner_email=user.email))
        leads = leads.filter(lead_status__in=lead_status)
        lead_list = list()
        for l in leads:
            lead = convert_lead_to_dict(l)
            lead_list.append(lead)
        lead_status_dict = get_count_of_each_lead_status_by_rep(user.email, 'normal', start_date=None, end_date=None)
        mimetype = 'application/json'
        ldap_dict = dict()
        ldap_dict['manager'] = user.profile.user_manager_name
        ldap_dict['program'] = user.profile.team.team_name if user.profile.team else 'N/A'
        ldap_dict['region'] = user.profile.location.location_name if user.profile.location else 'N/A'
        return HttpResponse(json.dumps({'lead_list': lead_list, 'lead_status_dict': lead_status_dict, 'ldap_dict': ldap_dict}), mimetype)
    # return render(request, 'leads/get_lead_summary_ldap.html', {})
    return render(request, 'leads/lead_summary.html', {})


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
        lead['appointment_time'] = datetime.strftime(model.appointment_date, "%m/%d/%Y %I:%M %p")
    else:
        lead['appointment_time'] = ''
    if model.date_of_installation:
        lead['date_of_installation'] = datetime.strftime(model.date_of_installation, "%m/%d/%Y")
    else:
        lead['date_of_installation'] = ''
    lead['regalix_comment'] = model.regalix_comment
    lead['lead_status'] = model.lead_status
    return lead


def get_basic_lead_data():
    """ Get Basic Lead data for submit Leads """

    lead_args = dict()
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
        loc_name = str(loc.location_name)
        time_zone_for_region[loc_name] = [{'zone_name': str(tz[
            'zone_name']), 'time_value': str(tz['time_value']), 'id': str(tz['id'])} for tz in loc.time_zone.values()]
        language_for_location[loc_name] = [{'language_name': str(lang[
            'language_name'])} for lang in loc.language.values() if lang['language_name'] != loc.primary_language.language_name]
        if language_for_location[loc_name]:
            language_for_location[loc_name].insert(0, {'language_name': str(loc.primary_language.language_name), 'id': str(loc.primary_language.id)})
        else:
            language_for_location[loc_name].append({'language_name': str(loc.primary_language.language_name), 'id': str(loc.primary_language.id)})

    teams = Team.objects.filter(is_active=True)
    code_types = CodeType.objects.filter(is_active=True)
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
    try:
        requests.post(url=sf_api_url, data=lead_data)
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

    return agency_details


def split_fullname(full_name):
    """ Split Full Name as First and Last name """
    first_name = ''
    last_name = ''
    if full_name:
        first_name = full_name.rsplit(' ', 1)[0]
        last_name = full_name.rsplit(' ', 1)[1] if len(full_name.rsplit(' ', 1)) > 1 else ' '

    return first_name, last_name


def get_lead_form_for_rep(user):
    """ Check the user and redirect based on reps programs and locations """

    l_form = 'Lead From'

    if user.groups.filter(name='AGENCY'):
        return 'Agency Form'

    access_controls = LeadFormAccessControl.objects.all()
    for control in access_controls:
        teams = [t.team_name for t in control.programs.filter()]
        locations = [l.location_name for l in control.target_location.filter()]
        emails = [usr.email for usr in control.google_rep.filter()]

        if user.profile.team and user.profile.location:
            print user.profile.team.team_name, user.profile.location.location_name
            if user.profile.team.team_name in teams and user.profile.location.location_name in locations:
                return control.lead_form.name
            elif user.email in emails:
                return control.lead_form.name
        elif user.email in emails:
            return control.lead_form.name
        else:
            continue

    return l_form
