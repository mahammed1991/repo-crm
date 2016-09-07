from json import dumps
from datetime import datetime, timedelta, date
from collections import OrderedDict
import time
import os
import operator
import json
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from requests import request as request_call
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse
from forum.models import *
from django.contrib.auth.models import User, Group

from django.conf import settings

from lib.helpers import send_mail, manager_info_required, wpp_user_required, check_lead_submitter_for_empty

from main.models import (UserDetails, Feedback, FeedbackComment, CustomerTestimonials, ContectList, WPPMasterList,
                         Notification, PortalFeedback, ResourceFAQ, PicassoEligibilityMasterUpload)
from leads.models import Location, Leads, Team, Language, TreatmentType, WPPLeads, PicassoLeads, WhiteListedAuditCID
from django.db.models import Count
from lib.helpers import (get_week_start_end_days, first_day_of_month, get_user_profile, get_quarter_date_slots,
                         last_day_of_month, previous_quarter, get_count_of_each_lead_status_by_rep, get_rep_details_from_leads,
                         is_manager, get_user_list_by_manager, get_user_under_manager, date_range_by_quarter, tag_user_required,
                         get_previous_month_start_end_days, create_new_user, convert_excel_data_into_list)
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from leads.models import BuildsBoltEligibility
from lib.helpers import save_file

import csv

from xlrd import open_workbook, XL_CELL_DATE, xldate_as_tuple
from django.utils.html import strip_tags
from reports.report_services import ReportService, DownloadLeads
from reports.models import Region, CSATReport
import re
from lib.salesforce import SalesforceApi


def home(request):
    """ Application landing view """
    # check if user logged in
    if not request.user.is_authenticated():
        return redirect('auth.views.user_login')

    return redirect('main.views.main_home')


@manager_info_required
def main_home(request):
    """ Google Portal Home/Index Page
        1. Current User/Rep LEADS SUMMARY
        2. Leads Current Quarter Summary
        3. Feedback Summary
        4. Q&A Forum
        5. Important Resources
        6. Testimonials

    """
    user_profile = get_user_profile(request.user)
    start_date, end_date = get_quarter_date_slots(datetime.utcnow())
    current_quarter = ReportService.get_current_quarter(datetime.utcnow())
    title = "Activity Summary for %s - %s to %s %s" % (current_quarter, datetime.strftime(start_date, '%b'), datetime.strftime(end_date, '%b'), datetime.strftime(start_date, '%Y'))

    if 'wpp' not in request.get_host():

        lead_status = settings.LEAD_STATUS
        if request.user.groups.filter(name='SUPERUSER'):
            start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
            # start_date, end_date = get_previous_month_start_end_days(datetime.utcnow())
            # start_date = first_day_of_month(datetime.utcnow())
            # end_date = datetime.utcnow()
            lead_status_dict = {'total_leads': 0,
                                'implemented': 0,
                                'in_progress': 0,
                                'attempting_contact': 0,
                                'in_queue': 0,
                                'in_active': 0,
                                'in_progress': 0,
                                }
            lead_status_dict['total_leads'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(
                lead_status__in=lead_status, created_date__gte=start_date, created_date__lte=end_date).count()

            total_rr_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(lead_status='Rework Required',
                                                                                  created_date__gte=start_date,
                                                                                  created_date__lte=end_date).count()

            lead_status_dict['in_progress'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(
                lead_status__in=settings.LEAD_STATUS_DICT['In Progress'], created_date__gte=start_date, created_date__lte=end_date).count()
            lead_status_dict['attempting_contact'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(
                lead_status__in=settings.LEAD_STATUS_DICT['Attempting Contact'], created_date__gte=start_date, created_date__lte=end_date).count()
            lead_status_dict['in_queue'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(
                lead_status__in=settings.LEAD_STATUS_DICT['In Queue'], created_date__gte=start_date, created_date__lte=end_date).count()

            rr_inactive_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(
                lead_status='Rework Required', lead_sub_status='RR - Inactive', created_date__gte=start_date, created_date__lte=end_date).count()

            rr_implemented_leads = total_rr_leads - rr_inactive_leads

            lead_status_dict['implemented'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(
                lead_status__in=settings.LEAD_STATUS_DICT['Implemented'], created_date__gte=start_date, created_date__lte=end_date).count() + rr_implemented_leads

            lead_status_dict['in_active'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(
                lead_status__in=settings.LEAD_STATUS_DICT['In Active'], created_date__gte=start_date, created_date__lte=end_date).count() + rr_inactive_leads

        else:
            # 1. Current User/Rep LEADS SUMMARY
            # Get Lead status count by current user
            lead_status_dict = get_count_of_each_lead_status_by_rep(request.user.email, 'normal', start_date=None, end_date=None)
        # Customer Testimonials
        # customer_testimonials = CustomerTestimonials.objects.all().order_by('-created_date')

        # Q&A Forum
        # Get Top 3 Q&A by most voted
        # questions_by_voted = Node.objects.filter(node_type='question').order_by('-score')[:3]
        # question_list = list()
        # for q in questions_by_voted:
        #     question = dict()
        #     question['votes'] = q.score
        #     question['views'] = q.extra_count
        #     answer_count = Node.objects.filter(node_type='answer', parent_id=q.id, abs_parent_id=q.id).count()
        #     question['answer'] = answer_count
        #     question['author_id'] = q.last_activity_by_id
        #     user = User.objects.get(id=q.last_activity_by_id)
        #     question['author_name'] = user.username
        #     question['title'] = q.title
        #     question['body'] = strip_tags(q.body)
        #     question['last_activity_at'] = q.last_activity_at
        #     question_list.append(question)

        # Leads Current Quarter Summary
        # Get Leads report for Current Quarter Summary
        # by default should be current Quarter
        report_summary = dict()

        total_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(created_date__gte=start_date, created_date__lte=end_date).count()
        rr_implemented_leads = Leads.objects.exclude(type_1__in=['WPP', ''], lead_sub_status='RR - Inactive').filter(created_date__gte=start_date,
                                                                                                                     created_date__lte=end_date,
                                                                                                                     lead_status__in=['Rework Required']).count()
        implemented_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(created_date__gte=start_date,
                                                                                 created_date__lte=end_date,
                                                                                 lead_status__in=settings.LEAD_STATUS_DICT['Implemented']).count()
        report_summary.update({'total_leads': total_leads,
                               'implemented_leads': implemented_leads + rr_implemented_leads,
                               'total_win': ReportService.get_conversion_ratio(implemented_leads, total_leads)})

        total_tag_leads = Leads.objects.exclude(type_1__in=['Existing Datafeed Optimization', 'Google Shopping Migration',
                                                            'Google Shopping Setup', '', 'WPP']).filter(created_date__gte=start_date,
                                                                                                        created_date__lte=end_date).count()

        rr_implemented_tag_leads = Leads.objects.exclude(type_1__in=['Existing Datafeed Optimization', 'Google Shopping Migration', 'Google Shopping Setup', '', 'WPP'],
                                                         lead_sub_status='RR - Inactive').filter(created_date__gte=start_date,
                                                                                                 created_date__lte=end_date,
                                                                                                 lead_status__in=['Rework Required']).count()

        implemented_tag_leads = Leads.objects.exclude(type_1__in=['Existing Datafeed Optimization', 'Google Shopping Migration',
                                                                  'Google Shopping Setup', '', 'WPP']).filter(created_date__gte=start_date,
                                                                                                              created_date__lte=end_date,
                                                                                                              lead_status__in=settings.LEAD_STATUS_DICT['Implemented']).count()
        report_summary.update({'total_tag_leads': total_tag_leads,
                               'implemented_tag_leads': implemented_tag_leads + rr_implemented_tag_leads,
                               'tag_win': ReportService.get_conversion_ratio(implemented_tag_leads, total_tag_leads)})

        total_shopping_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(created_date__gte=start_date,
                                                                                    created_date__lte=end_date,
                                                                                    type_1='Google Shopping Setup').count()
        implemented_shopping_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(created_date__gte=start_date, created_date__lte=end_date,
                                                                                          lead_status__in=settings.LEAD_STATUS_DICT['Implemented'],
                                                                                          type_1='Google Shopping Setup').count()

        rr_implemented_shopping_leads = Leads.objects.exclude(type_1__in=['WPP', ''],
                                                              lead_sub_status='RR - Inactive').filter(created_date__gte=start_date,
                                                                                                      created_date__lte=end_date,
                                                                                                      lead_status__in=['Rework Required'],
                                                                                                      type_1='Google Shopping Setup').count()
        report_summary.update({'total_shopping_leads': total_shopping_leads,
                               'implemented_shopping_leads': implemented_shopping_leads + rr_implemented_shopping_leads,
                               'shopping_win': ReportService.get_conversion_ratio(implemented_shopping_leads, total_shopping_leads)})

        # Top Lead Submitter by LAST QUARTER, LAST MONTH and LAST WEEK
        current_date = datetime.utcnow()
        top_performer = get_top_performer_list(current_date, 'NORMAL')

        # Get Feedback Details
        # feedback summary
        feedback_list = dict()
        feedbacks, feedback_list = get_feedbacks(request.user, 'NORMAL')
        # print feedbacks, feedback_list

        # Notification Section
        # notifications = Notification.objects.filter(is_visible=True)
        user = UserDetails.objects.get(user=request.user)
        notifications = list()
        
        current_date = datetime.utcnow().strftime("%Y-%m-%d")
        if user.location:
            user_region = user.location.region_set.get()
            notifications = Notification.objects.filter(Q(region=user_region) | Q(target_location=user.location), is_visible=True, from_date__isnull=False, to_date__isnull=False, to_date__gte=current_date).order_by('-created_date')
        else:
            notifications = Notification.objects.filter(region=None, target_location=None, is_visible=True,from_date__isnull=True,to_date__isnull=True, to_date__gte=current_date).order_by('-created_date')

        customer_testimonials = CustomerTestimonials.objects.all().order_by('-created_date')
        # feedback summary end here
        return render(request, 'main/tag_index.html', {'customer_testimonials': customer_testimonials, 'lead_status_dict': lead_status_dict,
                                                       'user_profile': user_profile, 'no_leads': check_lead_submitter_for_empty(top_performer), # 'question_list': question_list,
                                                       'top_performer': top_performer, 'report_summary': report_summary, 'title': title,
                                                       'feedback_list': feedback_list, 'notifications': notifications})

    else:
        if request.user.groups.filter(name='SUPERUSER'):
            # start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
            start_date = datetime(2015, 01, 01)
            end_date = datetime.now()

            wpp_details = ReportService.get_wpp_report_details_for_filters(start_date, end_date, list())
            nominated_leads = WPPLeads.objects.exclude(type_1='WPP').filter(created_date__gte=start_date,
                                                                            created_date__lte=end_date,
                                                                            type_1='WPP - Nomination').count()
        else:
            start_date = datetime(2014, 01, 01)
            end_date = datetime.now()
            wpp_details = ReportService.get_wpp_report_details_for_filters(start_date, end_date, [request.user.email])
            nominated_leads = WPPLeads.objects.exclude(type_1='WPP').filter(created_date__gte=start_date,
                                                                            created_date__lte=end_date,
                                                                            google_rep_email__in=[request.user.email],
                                                                            type_1='WPP - Nomination').count()
        current_date = datetime.utcnow()
        wpp_top_performer = get_top_performer_list(current_date, 'WPP')

        wpp_feedbacks, wpp_feedback_list = get_feedbacks(request.user, 'WPP')

        wpp_report = {key: (wpp_details['wpp_treatment_type_analysis'][key]['06. Implementation'] / wpp_details['wpp_treatment_type_analysis'][key]['TOTAL']) * 100 if wpp_details['wpp_treatment_type_analysis'][key]['TOTAL'] else 0 for key in wpp_details['wpp_treatment_type_analysis'].keys()}
        wpp_report['TOTAL'] = (wpp_details['wpp_lead_status_analysis']['06. Implementation'] / wpp_details['wpp_lead_status_analysis']['TOTAL']) * 100 if wpp_details['wpp_lead_status_analysis']['TOTAL'] else 0

        # print wpp_details['wpp_lead_status_analysis']

        key_dict = {'TOTAL': 'total','01. UI/UX': 'in_ui_ux', '02. Design': 'in_design', '03. Development': 'in_development', '04. Testing': 'in_testing', '05. Staging': 'in_staging', '06. Implementation': 'in_implementation', '07. Self Development': 'in_self_development'}


        wpp_lead_dict = dict()
        for key, value in key_dict.items():
            wpp_lead_dict[value] = wpp_details['wpp_lead_status_analysis'][key]

        wpp_lead_dict['nominated_leads'] = nominated_leads

        wpp_treatment_type_report = {key.replace(' ', ''): value for key, value in wpp_report.items()}

        return render(request, 'main/wpp_index.html', {'wpp_lead_dict': wpp_lead_dict, 'user_profile': user_profile,
                                                       'wpp_feedback_list': wpp_feedback_list, 'wpp_report': wpp_report,
                                                       'wpp_top_performer': wpp_top_performer, 'title': title, 'no_leads':check_lead_submitter_for_empty(wpp_top_performer),
                                                       'wpp_treatment_type_report': wpp_treatment_type_report})


def get_feedbacks(user, feedback_type):
    """ List Feedbacks by user """
    if user.groups.filter(name='FEEDBACK'):
        if feedback_type == 'WPP':
            feedbacks = Feedback.objects.filter(code_type='WPP').order_by('-created_date')
        elif feedback_type == 'PICASSO':
            feedbacks = Feedback.objects.filter(code_type='PICASSO').order_by('-created_date')
        else:
            feedbacks = Feedback.objects.exclude(code_type__in=['WPP', 'PICASSO']).filter().order_by('-created_date')
    else:
        if feedback_type == 'WPP':
            feedbacks = Feedback.objects.filter(code_type='WPP')
            feedbacks = feedbacks.filter(
                Q(user__email=user.email)
                | Q(user__profile__user_manager_email=user.email)
                | Q(lead_owner__email=user.email)
                | Q(lead_owner__profile__user_manager_email=user.email)
            ).order_by('-created_date')
        elif feedback_type == 'PICASSO':
            feedbacks = Feedback.objects.filter(code_type='PICASSO')
            feedbacks = feedbacks.filter(
                Q(user__email=user.email)
                | Q(user__profile__user_manager_email=user.email)
                | Q(lead_owner__email=user.email)
                | Q(lead_owner__profile__user_manager_email=user.email)
            ).order_by('-created_date')
        else:
            feedbacks = Feedback.objects.exclude(code_type__in=['WPP', 'PICASSO']).filter(
                Q(user__email=user.email)
                | Q(user__profile__user_manager_email=user.email)
                | Q(lead_owner__email=user.email)
                | Q(lead_owner__profile__user_manager_email=user.email)
            ).order_by('-created_date')
    feedback_list = dict()
    feedback_list['new'] = feedbacks.filter(status='NEW').count()
    feedback_list['in_progress'] = feedbacks.filter(status='IN PROGRESS').count()
    feedback_list['resolved'] = feedbacks.filter(status='RESOLVED').count()
    feedback_list['fixed'] = feedbacks.filter(status='FIXED').count()
    feedback_list['total'] = feedbacks.count()
    return feedbacks, feedback_list


def get_top_performer_list(current_date, lead_type):
    top_performer_list = {'weekly': [], 'monthly': [], 'quarterly': []}

    # Get Top 3 performers by previous week of current week
    prev_week = int(time.strftime("%W"))
    start_date, end_date = get_week_start_end_days(current_date.year, prev_week)
    top_performer_list['weekly'] = get_top_performer_by_date_range(start_date, end_date, lead_type)

    # Get Top 3 performers by previous month of current month
    prev_month = date.today().replace(day=1) - timedelta(days=1)
    start_date = first_day_of_month(prev_month)
    end_date = last_day_of_month(prev_month)
    top_performer_list['monthly'] = get_top_performer_by_date_range(start_date, end_date, lead_type)

    # Get Top 3 performers by previous quarter of current quarter
    prev_quarter = previous_quarter(current_date)
    start_date = datetime(prev_quarter.year, prev_quarter.month - 2, 1)
    end_date = prev_quarter
    top_performer_list['quarterly'] = get_top_performer_by_date_range(start_date, end_date, lead_type)
    return top_performer_list


def top_30_cms(request):
    """ Get top 30 CMS """
    return render(request, 'main/top_30_cms.html')


def get_top_performer_by_date_range(start_date, end_date, lead_type):

    if lead_type == 'NORMAL':
        topper_list = Leads.objects.exclude(google_rep_email__contains='regalix-inc').filter(
            created_date__gte=start_date,
            created_date__lte=end_date).values('google_rep_email').annotate(submitted=Count('sf_lead_id')).order_by('-submitted')
    elif lead_type == 'PICASSO':
        topper_list = PicassoLeads.objects.exclude(google_rep_email__contains='regalix').filter(
            created_date__gte=start_date,
            created_date__lte=end_date).values('google_rep_email').annotate(submitted=Count('sf_lead_id')).order_by('-submitted')
    else:
        topper_list = WPPLeads.objects.exclude(google_rep_email__contains='regalix').filter(
            created_date__gte=start_date,
            created_date__lte=end_date).values('google_rep_email').annotate(submitted=Count('sf_lead_id')).order_by('-submitted')
    toppers = dict()
    indx = 0
    topper_limit = 3
    for topper in topper_list:
        indx = indx + 1
        key = topper['submitted']

        if indx > topper_limit:
            if topper['submitted'] in toppers:
                toppers[key].append(topper['google_rep_email'])
            else:
                break
        elif key not in toppers:
            toppers[key] = [topper['google_rep_email']]
        else:
            toppers[key].append(topper['google_rep_email'])

    # Get toppers from the list
    topper_email = list()
    for k in sorted(toppers.keys(), reverse=True):
        if len(toppers[k]) == 1:
            topper_email.append(toppers[k][0])
        else:
            top_list = list()
            for email in toppers[k]:
                latest_lead = dict()
                if lead_type == 'NORMAL':
                    last_lead_submitted = Leads.objects.filter(google_rep_email=email,
                                                               created_date__gte=start_date,
                                                               created_date__lte=end_date).order_by('-created_date')[:1]
                elif lead_type == 'PICASSO':
                    last_lead_submitted = PicassoLeads.objects.filter(google_rep_email=email,
                                                                      created_date__gte=start_date,
                                                                      created_date__lte=end_date).order_by('-created_date')[:1]
                else:
                    last_lead_submitted = WPPLeads.objects.filter(google_rep_email=email,
                                                                  created_date__gte=start_date,
                                                                  created_date__lte=end_date).order_by('-created_date')[:1]
                latest_lead.update({'email': email, 'created_date': last_lead_submitted[0].created_date})
                top_list.append(latest_lead)
            top_list.sort(key=operator.itemgetter('created_date'))
            created_dates = list()
            for tpr in top_list:
                created_dates.append(str(tpr['created_date']))
                if len(topper_email) != topper_limit:
                    topper_email.append(tpr['email'])
                # Check if rep has submitted lead on same date, Created has only day, month and year
                elif created_dates and created_dates[len(created_dates) - 1] == str(tpr['created_date']):
                    topper_email.append(tpr['email'])
                else:
                    break

    topper_list = list()
    topper_email[:topper_limit]
    for rep_email in topper_email:
        rep = dict()
        location = ''
        rep.update({'google_rep_name': rep_email.split('@')[0]})
        try:
            # Get user details
            user = User.objects.get(email=rep_email)
            full_name = "%s %s" % (user.first_name, user.last_name)
            rep.update({'google_rep_name': full_name})
            try:
                user_profile = UserDetails.objects.get(user_id=user.id)
                location = user_profile.location.location_name if user_profile.location else ''
            except ObjectDoesNotExist:
                location = ''
        except ObjectDoesNotExist:
            location = ''
        avatar_url = get_profile_avatar_by_email(rep_email)
        rep.update({'image_url': avatar_url, 'location': location})
        topper_list.append(rep)
    return topper_list


@login_required
@csrf_exempt
def edit_profile_info(request):
    """ Profile information for user """
    picasso_header = False
    referer = request.META.get('HTTP_REFERER', None)
    if referer:
        if 'picasso' in referer or 'smb' in referer:
            picasso_header = True
    locations = Location.objects.filter(is_active=True)
    if 'google.com' in request.user.email:
        tag_teams = Team.objects.exclude(belongs_to__in=['WPP', 'PICASSO']).filter(is_active=True)
        teams = tag_teams.exclude(team_name__in=['Help Center Task', 'Help Centre Follow-ups', 'AdWords Front End (AWFE)', 'Help Centre Tasks - Inbound'])
    else:
        teams = Team.objects.exclude(belongs_to__in=['WPP', 'PICASSO']).filter(is_active=True)
    managers = User.objects.values_list('email', flat=True)
    managers = [str(m) for m in managers]
    users = User.objects.all()
    manager_details = dict()
    locations = Location.objects.filter(is_active=True)
    regions = Region.objects.all()
    all_regions = list()
    region_locations = dict()
    podname = UserDetails.objects.get(user_id=request.user.id)
    for rgn in regions:
        for loc in rgn.location.all():
            region_locations[int(rgn.id)] = [int(loc.id) for loc in rgn.location.filter()]
        region_dict = dict()
        region_dict['id'] = int(rgn.id)
        region_dict['name'] = str(rgn.name)
        all_regions.append(region_dict)

    all_locations = list()
    for loc in locations:
        l = {'id': int(loc.id), 'name': str(loc.location_name)}
        all_locations.append(l)

    for user in users:
        if user.first_name or user.last_name:
            full_name = "%s %s" % (user.first_name, user.last_name)
            try:
                full_name = str(full_name)
            except Exception:
                full_name = ''
            manager_details[str(user.email)] = str(full_name)

    if request.method == 'POST':
        next_url = request.POST.get('next_url', None)
        if next_url != 'home':
            user_full_name = request.POST.get('user_full_name', None)
            if user_full_name:
                request.user.first_name = user_full_name.rsplit(' ')[0]
                request.user.last_name = user_full_name.rsplit(' ')[1]
                request.user.save()
        try:
            user_details = UserDetails.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            user_details = UserDetails()
            user_details.user = request.user

        user_details.phone = request.POST.get('user_phone', None)
        user_details.user_manager_name = request.POST.get('user_manager_name', None)
        user_details.user_manager_email = request.POST.get('user_manager_email', None)
        user_details.pod_name = request.POST.get('pod_name', None)

        if '@google.com' in request.user.email:
            user_details.team_id = request.POST.get('user_team', None)
            if request.POST.get('region', None) == '0':
                user_details.region_id = None
            else:
                user_details.region_id = request.POST.get('region', None)
            user_details.location_id = request.POST.get('user_location', None)

        user_details.rep_location = request.POST.get('rep_location', None)
        user_details.save()

        if next_url == 'home':
            return redirect('main.views.home')
    api_key = settings.API_KEY
    return render(request, 'main/edit_profile_info.html', {'podname': podname, 'locations': locations, 'managers': managers, 'regions': regions, 'api_key': api_key,
                                                           'all_locations': all_locations, 'region_locations': region_locations, 'teams': teams, 'manager_details': manager_details, 'picasso_header' : picasso_header})


@login_required
@csrf_exempt
def get_started(request):
    """ Get Initial information from user """
    locations = Location.objects.filter(is_active=True)
    if 'google.com' in request.user.email:
        tag_teams = Team.objects.exclude(belongs_to__in=['WPP', 'PICASSO']).filter(is_active=True)
        teams = tag_teams.exclude(team_name__in=['Help Center Task', 'Help Centre Follow-ups', 'AdWords Front End (AWFE)', 'Help Centre Tasks - Inbound'])
    else:
        teams = Team.objects.exclude(belongs_to__in=['WPP', 'PICASSO']).filter(is_active=True)
    managers = User.objects.values_list('email', flat=True)
    managers = [str(m) for m in managers]
    users = User.objects.all()
    user_details = dict()

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

    all_locations = list()
    for loc in locations:
        l = {'id': int(loc.id), 'name': str(loc.location_name)}
        all_locations.append(l)

    for user in users:
        if user.first_name or user.last_name:
            full_name = "%s %s" % (user.first_name, user.last_name)
            try:
                full_name = str(full_name)
            except Exception:
                full_name = ''
            user_details[str(user.email)] = str(full_name)
    # regalix_team = RegalixTeams.objects.filter(is_active=True)
    api_key = settings.API_KEY
    return render(request, 'main/get_started.html', {'locations': locations, 'regions': regions, 'api_key': api_key,
                                                     'all_locations': all_locations, 'region_locations': region_locations,
                                                     'teams': teams, 'managers': managers, 'user_details': user_details})


@login_required
@manager_info_required
@tag_user_required
def team(request):
    contacts_list, cnt = get_contacts(request)
    return render(request, 'main/team.html', {'contacts_list': contacts_list, 'cnt': cnt})


@login_required
@manager_info_required
def view_feedback(request, id):
    """ Detail view of a feedback """
    normal_comments = list()
    try:
        feedback = Feedback.objects.get(id=id)
    except Feedback.DoesNotExist:
        return redirect('main.views.main_home')
    normal_comments = FeedbackComment.objects.filter(feedback__id=id)
    resolved_count = FeedbackComment.objects.filter(feedback__id=id, feedback_status='resolved').count()
    can_resolve = True

    if request.user.email == feedback.lead_owner.email:
        can_resolve = False

    if feedback.code_type in ['PICASSO', 'Picasso']:
        return render(request, 'main/view_feedback.html', {'feedback': feedback,
                                                       'comments': normal_comments,
                                                       'can_resolve': can_resolve,
                                                       'resolved_count': resolved_count,
                                                       'media_url': settings.MEDIA_URL + 'feedback/',
                                                       'picasso': True})
    else:
        return render(request, 'main/view_feedback.html', {'feedback': feedback,
                                                       'comments': normal_comments,
                                                       'can_resolve': can_resolve,
                                                       'resolved_count': resolved_count,
                                                       'media_url': settings.MEDIA_URL + 'feedback/'})


@login_required
@manager_info_required
@tag_user_required
def list_feedback(request):
    """ List all feedbacks """

    feedbacks, feedback_list = get_feedbacks(request.user, 'NORMAL')

    return render(request, 'main/list_feedback.html', {'feedbacks': feedbacks,
                                                       'media_url': settings.MEDIA_URL + 'feedback/',
                                                       'feedback_list': feedback_list, 'type': 'NORMAL'
                                                       })


@login_required
@manager_info_required
@wpp_user_required
def list_feedback_wpp(request):
    """ List all WPP feedbacks """

    feedbacks, feedback_list = get_feedbacks(request.user, 'WPP')

    return render(request, 'main/list_feedback.html', {'feedbacks': feedbacks,
                                                       'media_url': settings.MEDIA_URL + 'feedback/',
                                                       'feedback_list': feedback_list, 'type': 'WPP'
                                                       })


@login_required
@manager_info_required
def list_feedback_picasso(request):
    """ List all PICASSO feedbacks"""

    feedbacks, feedback_list = get_feedbacks(request.user, 'PICASSO')

    return render(request, 'main/list_feedback.html', {'feedbacks': feedbacks,
                                                       'media_url': settings.MEDIA_URL + 'feedback/',
                                                       'feedback_list': feedback_list, 'type': 'PICASSO', 'picasso': True
                                                       })


@login_required
@manager_info_required
def create_feedback(request, lead_id=None):
    """ Create feed back """
    if request.method == 'POST':
        feedback_details = Feedback()
        feedback_details.user = request.user
        feedback_details.title = request.POST['title']
        if request.POST['code_type'] in ['PICASSO', 'Picasso']:
            feedback_details.cid = request.POST['enter_cid']
        else:
            feedback_details.cid = request.POST['cid']
        feedback_details.advertiser_name = request.POST['advertiser']
        if request.POST.get('language'):
            language = Language.objects.get(id=request.POST['language'])
            feedback_details.language = language.language_name
        else:
            feedback_details.language = '-'

        # picasso has no location, so we are saving India as default for picasso because location is foriegn key in feedback
        feedback_location = Location.objects.get(location_name=request.POST['location'])
        feedback_details.location = feedback_location

        feedback_details.feedback_type = request.POST['feedbackType']
        feedback_details.description = request.POST['description']
        feedback_details.program_id = request.POST['program']
        feedback_details.sf_lead_id = request.POST['sf_type']
        feedback_details.code_type = request.POST['code_type']
        owner_email = request.POST['lead_owner']
        try:
            # if lead owner not exist, assign lead to default user
            lead_owner = User.objects.get(email=owner_email)
            feedback_details.lead_owner = lead_owner
        except ObjectDoesNotExist:
            if owner_email:
                lead_owner = create_new_user(owner_email)
                feedback_details.lead_owner = lead_owner

        manager_email = request.POST['google_acManager_name']
        try:
            google_account_manager = User.objects.get(email=manager_email)
            feedback_details.google_account_manager = google_account_manager
        except ObjectDoesNotExist:
            if manager_email:
                google_account_manager = create_new_user(manager_email)
                feedback_details.google_account_manager = google_account_manager

        if request.FILES:
            feedback_details.attachment = request.FILES['attachment_name']

        feedback_details.save()
        feedback_details = notify_feedback_activity(request, feedback_details, comment=None, fixed=None)

        if request.POST['code_type'] == 'WPP':
            return redirect('main.views.list_feedback_wpp')
        elif request.POST['code_type'] in ['PICASSO', 'Picasso']:
            return redirect('main.views.list_feedback_picasso')
        else:
            return redirect('main.views.list_feedback')

    # Feedback Form
    feedback_type = request.GET.get('type')

    lead = None
    if lead_id:
        try:
            if feedback_type and feedback_type == 'WPP':
                lead = WPPLeads.objects.get(id=lead_id)
            else:
                lead = Leads.objects.get(id=lead_id)
                feedback_type = 'NORMAL'
        except Leads.ObjectDoesNotExist:
            lead = None
    if feedback_type == 'WPP':
        programs = Team.objects.exclude(belongs_to='TAG').filter()
        locations = Location.objects.filter(location_name__in=['United States', 'AU/NZ'])
        languages = Language.objects.filter(language_name='English')
        return render(request, 'main/feedback_mail/wpp_feedback_form.html', {'locations': locations,
                                                                             'programs': programs, 'lead': lead, 'languages': languages,
                                                                             'feedback_type': feedback_type})
    elif feedback_type == "PICASSO":
        programs = Team.objects.filter(belongs_to__in=['PICASSO', 'BOTH'], is_active=True)
        return render(request, 'main/feedback_mail/picasso_feedback_form.html', {'picasso': True, 'programs': programs, 'feedback_type': feedback_type, 'lead': lead})
    else:
        programs = Team.objects.filter(is_active=True)
        locations = Location.objects.all()
        languages = Language.objects.all()
        return render(request, 'main/feedback_mail/feedback_form.html', {'locations': locations,
                                                                         'programs': programs, 'lead': lead, 'languages': languages,
                                                                         'feedback_type': feedback_type})


def notify_feedback_activity(request, feedback, comment=None, fixed=None, is_resolved=None):
    feedback_url = request.build_absolute_uri(reverse('main.views.view_feedback', kwargs={'id': feedback.id}))
    if feedback.code_type != 'WPP':
        signature = 'Tag Team'
    else:
        signature = 'WPP Team'
    bcc = set()

    if is_resolved:
        mail_subject = "Customer Feedback ["+feedback.feedback_type+" - "+ feedback.cid+"] Status - Resolved"
        mail_from = "Google Feedback <" + request.user.email +">"
        mail_body = get_template('main/feedback_mail/resolved.html').render(
            Context({
                'feedback': feedback,
                'user_info': request.user,
                'feedback_url': feedback_url,
                'cid': feedback.cid,
                'type': feedback.feedback_type,
                'feedback_title': feedback.title,
                'description': feedback.description,
                'comment':comment,
                'signature': signature
            })
        )
        fb_su = []
        feedback_super_user_group = User.objects.filter(groups__name='FEEDBACK-SUPER-USER')
        for user in feedback_super_user_group:
            fb_su.append(user.email)
        assignee = Feedback.objects.get(id=feedback.id)
        mail_to = [  
                 assignee.assigned_to.email, feedback.lead_owner.email, feedback.user.email,
                 'sabinaa@google.com','rwieker@google.com', 'g-crew@regalix-inc.com',]
        mail_to.extend(fb_su)
        mail_to = set(mail_to)
    elif comment:
        mail_subject = "Customer Feedback ["+feedback.feedback_type+" - "+ feedback.cid+"] Status - New comment added"
        mail_from = "Google Feedback <" + request.user.email +">"
        mail_body = get_template('main/feedback_mail/new_comment.html').render(
            Context({
                'feedback': feedback,
                'comment': comment,
                'feedback_url': feedback_url,
                'feedback_owner': request.user.first_name + request.user.last_name,
                'signature': signature
            })
        )
        fb_su = []
        feedback_super_user_group = User.objects.filter(groups__name='FEEDBACK-SUPER-USER')
        for user in feedback_super_user_group:
            fb_su.append(user.email)
        assignee = Feedback.objects.get(id=feedback.id)
        first_comment_count = FeedbackComment.objects.filter(feedback=feedback.id)
        first_comment_count = first_comment_count.filter(comment_type="U").count()

        if first_comment_count == 0:
            mail_to = [ assignee.assigned_to.email, 'g-crew@regalix-inc.com', 'sabinaa@google.com',
                        'rwieker@google.com', feedback.lead_owner.email ]
            mail_to.extend(fb_su)
            mail_to = set(mail_to)
        else:
            mail_to = [assignee.assigned_to.email, feedback.user.email, feedback.lead_owner.email]
            mail_to.extend(fb_su)
            mail_to = set(mail_to)
    else:
        # New Feedback mailing
        mail_subject = "Customer Feedback ["+feedback.feedback_type+" - "+ feedback.cid+"] Status - Assign Owner"
        mail_from = "Google Feedback <" + request.user.email +">"
        mail_subject = "Customer Feedback ["+feedback.feedback_type+" - "+ feedback.cid+"] Status - Assign Owner"
        mail_body = get_template('main/feedback_mail/new_feedback.html').render(
            Context({
                'feedback': feedback,
                'user_info': request.user,
                'feedback_url': feedback_url,
                'cid': feedback.cid,
                'type': feedback.feedback_type,
                'feedback_title': feedback.title,
                'feedback_body': feedback.description,
                'signature': signature
            })
        )
        fb_su = []
        feedback_super_user_group = User.objects.filter(groups__name='FEEDBACK-SUPER-USER')
        for user in feedback_super_user_group:
            fb_su.append(user.email)
        mail_to = [
                'g-crew@regalix-inc.com', 'rwieker@google.com',
                'sabinaa@google.com', 'vsharan@regalix-inc.com',
                'babla@regalix-inc.com','khengg@google.com',
                'portalsupport@regalix-inc.com', request.user.email,
                feedback.user.email, feedback.lead_owner.email,
                 ]
        mail_to.extend(fb_su)
        mail_to = set(mail_to)
    attachments = list()
    if feedback.attachment:
        attachments.append(feedback.attachment)

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

    return feedback

def notify_feedback_fixed(request, feedback, comment=None ):
    mail_subject = "Customer Feedback ["+feedback.feedback_type+" - "+ feedback.cid+"] Status- Response Submitted: Request to Closure"
    feedback_url = request.build_absolute_uri(reverse('main.views.view_feedback', kwargs={'id': feedback.id}))
    issue_fixedby = request.user.first_name + ' ' + request.user.last_name
    assignee = Feedback.objects.get(id=feedback.id)
    mail_body = get_template('main/feedback_mail/feedback_fixed_mail_tosuperuser.html').render(
        Context({
            'feedback': feedback,
            'user_info': request.user,
            'feedback_url': feedback_url,
            'cid': feedback.cid,
            'type': feedback.feedback_type,
            'feedback_title': feedback.title,
            'description': feedback.description,
            'issue_fixedby':issue_fixedby,
            'comment':comment,
        })
    )
    fb_su = []
    feedback_super_user_group = User.objects.filter(groups__name='FEEDBACK-SUPER-USER')
    for user in feedback_super_user_group:
        fb_su.append(user.email)
    mail_to = [ assignee.assigned_to.email,]
    mail_to.extend(fb_su)
    mail_to = set(mail_to)
    mail_from = "Google Feedback <" + request.user.email +">"
    attachments = list()
    bcc = list()
    if feedback.attachment:
        attachments.append(feedback.attachment)
    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)
    return feedback

@login_required
def create_feedback_from_lead_status(request):
    """ Create feed back """
    if request.is_ajax():

        lead_id = request.GET.get('lead_id')
        lead_type = request.GET.get('lead_type')
        feedback_details = Feedback()

        if lead_type == 'wpp':
            lead = WPPLeads.objects.get(id=lead_id)
            feedback_details.code_type = 'WPP'
        else:
            lead = Leads.objects.get(id=lead_id)

        feedback_details.user = request.user
        feedback_details.title = request.GET.get('title')
        feedback_details.feedback_type = request.GET.get('type')
        feedback_details.description = request.GET.get('comment')

        feedback_details.cid = lead.customer_id
        feedback_details.advertiser_name = lead.first_name + ' ' + lead.last_name
        feedback_details.language = 'English'
        feedback_location = Location.objects.get(location_name=lead.country)
        feedback_details.location = feedback_location

        try:
            team = Team.objects.get(team_name=lead.team)
            feedback_details.program_id = team.id
        except ObjectDoesNotExist:
            feedback_details.program = None
        feedback_details.created_date = datetime.utcnow()

        owner_email = lead.lead_owner_email
        try:
            # if lead owner not exist, assign lead to default user
            lead_owner = User.objects.get(email=owner_email)
            feedback_details.lead_owner = lead_owner
        except ObjectDoesNotExist:
            if owner_email:
                lead_owner = create_new_user(owner_email)
                feedback_details.lead_owner = lead_owner

        manager_email = lead.google_rep_email
        try:
            google_account_manager = User.objects.get(email=manager_email)
            feedback_details.google_account_manager = google_account_manager
        except ObjectDoesNotExist:
            if manager_email:
                google_account_manager = create_new_user(manager_email)
                feedback_details.google_account_manager = google_account_manager

        feedback_details.save()
        feedback_details = notify_feedback_activity(request, feedback_details)

        # return 'SUCCESS'
        return HttpResponse(json.dumps('SUCCESS'))


@login_required
@manager_info_required
def reopen_feedback(request, id):
    """ Reopen Comment """
    feedback = Feedback.objects.get(id=id)
    feedback.status = 'IN PROGRESS'
    comment = FeedbackComment()
    comment.feedback = feedback
    comment.comment = request.POST.get('reopencomment')
    comment.comment_by = request.user
    comment.feedback_status = 'IN PROGRESS'
    comment.created_date = datetime.utcnow()
    # If assigining we add the comment in Table, so just to know who added the comment.
    # We use comment_type 'S' == System comment, 'U' == User comment
    comment.comment_type = 'U'
    comment.save()
    feedback.save()
    comment_for_reopen = request.POST.get('reopencomment')

    mail_subject = "Customer Feedback ["+feedback.feedback_type+" - "+ feedback.cid+"] Status - Reopened"
    feedback_url = request.build_absolute_uri(reverse('main.views.view_feedback', kwargs={'id': feedback.id}))
    reopenedby = request.user.first_name + ' ' + request.user.last_name
    mail_body = get_template('main/feedback_mail/reopened_feedback.html').render(
        Context({
            'reopenedby': reopenedby,
            'description':feedback.description,
            'feedback_url': feedback_url,
            'cid': feedback.cid,
            'type': feedback.feedback_type,
            'feedback_title': feedback.title,
            'comment_for_reopen':comment_for_reopen,
        })
    )
    fb_su = []
    feedback_super_user_group = User.objects.filter(groups__name='FEEDBACK-SUPER-USER')
    mail_to = feedback_super_user_group
    mail_from = "Google Feedback <" + request.user.email +">"
    for user in feedback_super_user_group:
        fb_su.append(user.email)
    mail_to = [ 'rwieker@google.com',
                'g-crew@regalix-inc.com',
                'sabinaa@google.com',
                feedback.lead_owner.email,
                feedback.user.email,]
    mail_to.extend(fb_su)
    mail_to = set(mail_to)
    attachments = list()
    bcc = list()
    if feedback.attachment:
        attachments.append(feedback.attachment)
    mail_subject = "Customer Feedback ["+feedback.feedback_type+" - "+ feedback.cid+"] Status - Reopened"
    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

    return redirect('main.views.view_feedback', id=id)


@login_required
@manager_info_required
def comment_feedback(request, id):
    """ Comment on a feedback """
    action_type = request.POST.get('feedback_action')
    feedback = Feedback.objects.get(id=id)
    comment = FeedbackComment()
    comment.feedback = feedback
    comment.comment = request.POST.get('comment')
    comment.comment_by = request.user
    # If assigining we add the comment in Table, so just to know who added the comment.
    # We use comment_type 'S' == System comment, 'U' == User comment
    comment.comment_type = 'U'

    if action_type == 'Resolved':
        comment.feedback_status = 'RESOLVED'
        comment.save()
        feedback.status = 'RESOLVED'

        resolved_count = FeedbackComment.objects.filter(feedback__id=id, feedback_status='resolved').count()
        if resolved_count == 1:
            feedback.resolved_by = request.user
            feedback.resolved_date = datetime.utcnow()
        elif resolved_count == 2:
            feedback.second_resolved_by = request.user
            feedback.second_resolved_date = datetime.utcnow()
        elif resolved_count == 3:
            feedback.third_resolved_by = request.user
            feedback.third_resolved_date = datetime.utcnow()

    elif action_type == 'FIXED':
        comment.feedback_status = 'FIXED'
        feedback.status = 'FIXED'
        comment.save()

    else:
        comment.feedback_status = 'IN PROGRESS'
        feedback.status = 'IN PROGRESS'
        comment.save()

    feedback.save()

    if action_type == 'Resolved':
        notify_feedback_activity(request, feedback, comment, is_resolved=True)
    elif action_type == 'FIXED':
        notify_feedback_fixed(request, feedback, comment)
    else:
        # Here comment is the event
        notify_feedback_activity(request, feedback, comment, is_resolved=False)
    return redirect('main.views.view_feedback', id=id)


def get_contacts(request):
    """ Get team contacts information """
    contact_list = ContectList.objects.filter(is_active=True)
    keyorder = {k: v for v, k in enumerate(['The implementation team', 'Training/ SME/ Tech', 'QUALITY', 'MIS / WFM', 'OPERATIONS', 'MANAGEMENT'])}
    your_team = {'The implementation team': list(), 'Training/ SME/ Tech': list(), 'MANAGEMENT': list(), 'OPERATIONS': list(), 'QUALITY': list(), 'MIS / WFM': list()}
    other_team = {'The implementation team': list(), 'Training/ SME/ Tech': list(), 'MANAGEMENT': list(), 'OPERATIONS': list(), 'QUALITY': list(), 'MIS / WFM': list()}
    contacts = dict()
    ur_team_cnt = 0
    for cnt in contact_list:
        contact = dict()
        contact['name'] = "%s %s" % (cnt.first_name, cnt.last_name)
        contact['email'] = cnt.email
        contact['phone'] = cnt.phone_number
        contact['skype'] = cnt.skype_id
        contact['picture'] = cnt.profile_photo.name.split('/')[-1]
        contact['photo_url'] = get_profile_avatar_by_email(cnt.email)
        contact['position_type'] = cnt.position_type
        contact['ldap'] = str(cnt.google_id.split('@')[0])
        contact['support_hrs'] = cnt.supporting_hours

        # if cnt.region_id == request.user.profile.location_id:
        locations = [l.id for l in cnt.target_location.filter()]
        if request.user.profile.location_id in locations:
            if cnt.position_type in ['TAG', 'SHOPPING']:
                ur_team_cnt += 1
                your_team['The implementation team'].append(contact)
            elif cnt.position_type in ['TECH/SME', 'DESIGN/DEV']:
                ur_team_cnt += 1
                your_team['Training/ SME/ Tech'].append(contact)
            elif cnt.position_type in ['MANAGEMENT']:
                ur_team_cnt += 1
                your_team['MANAGEMENT'].append(contact)
            elif cnt.position_type in ['OPERATIONS']:
                ur_team_cnt += 1
                your_team['OPERATIONS'].append(contact)
            elif cnt.position_type in ['QUALITY']:
                ur_team_cnt += 1
                your_team['QUALITY'].append(contact)
            elif cnt.position_type in ['MIS', 'POD']:
                ur_team_cnt += 1
                your_team['MIS / WFM'].append(contact)
        else:
            if cnt.position_type in ['TAG', 'SHOPPING']:
                other_team['The implementation team'].append(contact)
            elif cnt.position_type in ['TECH/SME', 'DESIGN/DEV']:
                other_team['Training/ SME/ Tech'].append(contact)
            elif cnt.position_type in ['MANAGEMENT']:
                other_team['MANAGEMENT'].append(contact)
            elif cnt.position_type in ['OPERATIONS']:
                other_team['OPERATIONS'].append(contact)
            elif cnt.position_type in ['QUALITY']:
                other_team['QUALITY'].append(contact)
            elif cnt.position_type in ['MIS', 'POD']:
                other_team['MIS / WFM'].append(contact)

    contacts['You Work With...'] = OrderedDict(sorted(your_team.items(), key=lambda i: keyorder.get(i[0])))
    contacts['The Rest of Us!!!'] = OrderedDict(sorted(other_team.items(), key=lambda i: keyorder.get(i[0])))
    contact_keyorder = {k: v for v, k in enumerate(['You Work With...', 'The Rest of Us!!!'])}
    contacts = OrderedDict(sorted(contacts.items(), key=lambda i: contact_keyorder.get(i[0])))
    return contacts, ur_team_cnt


def get_profile_avatar_by_email(email):
    """ Get Profile Avatar """

    avatar_url = 'images/avtar-big.jpg'
    try:
        try:
            user = User.objects.get(email=email)
            try:
                user_profile = UserDetails.objects.get(user_id=user.id)
                if user_profile.profile_photo_url:
                    avatar_url = user_profile.profile_photo_url
                else:
                    username = email.split('@')[0]
                    os_path = settings.STATIC_FOLDER + '/images/GTeam/' + username
                    # Check if profile picture exist
                    if os.path.isfile(os_path + '.png') or os.path.isfile(os_path + '.png.gz'):
                        avatar_url = 'images/GTeam/' + username + '.png'
            except ObjectDoesNotExist:
                avatar_url = 'images/avtar-big.jpg'
        except Exception:
            avatar_url = 'images/avtar-big.jpg'
    except ObjectDoesNotExist:
        if email:
            username = email.split('@')[0]
            os_path = settings.STATIC_FOLDER + '/images/GTeam/' + username
            # Check if profile picture exist
            if os.path.isfile(os_path + '.png') or os.path.isfile(os_path + '.png.gz'):
                avatar_url = 'images/GTeam/' + username + '.png'
    return avatar_url


# @login_required
# def resources(request):
#     video_url = settings.MEDIA_URL + 'TaggingWins_06_18_2015.mp4'
#     return render(request, 'main/resources.html', {'video_url': video_url})


@login_required
@tag_user_required
def resources(request):
    if request.is_ajax():
        resfaq = ResourceFAQ()
        resfaq.task_type = request.GET.get('tasktype')
        resfaq.task_question = request.GET.get('task_question')
        resfaq.submited_by = request.user
        try:
            resfaq.save()
            resfaq = notify_faq(request, resfaq)
            return HttpResponse(json.dumps('SUCCESS'))
        except Exception:
            return HttpResponse(json.dumps('FAILURE'))
    customer_testimonials = CustomerTestimonials.objects.all().order_by('-created_date')
    mp4_url = settings.MEDIA_URL + 'TaggingWins_11_13_2015.mp4'
    ogg_url = settings.MEDIA_URL + 'TaggingWins_11_13_2015.ogg'
    return render(request, 'main/new_resources.html', {'customer_testimonials': customer_testimonials, 'mp4_url': mp4_url, 'ogg_url': ogg_url})


@login_required
def notify_faq(request, resfaq):
    mail_subject = resfaq.task_type + "Portal FAQs"
    mail_body = get_template('main/portal_faqs/faq.html').render(
        Context({
            'resfaq': resfaq,
            'user_info': request.user,
            'type': resfaq.task_type,
            'faq_question': resfaq.task_question
        })
    )

    bcc = set([])

    mail_to = set([
        'abraham@regalix-inc.com',
        'asarkar@regalix-inc.com'
    ])

    mail_from = request.user.email
    attachments = list()

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

    return resfaq


@login_required
def get_inbound_locations(request):
    """ Get all In-Bound Locations """
    if request.user.groups.filter(name='WPP'):
        locations = Location.objects.exclude(flag_image__isnull=True).exclude(phone__isnull=True).filter(location_name__in=['United States', 'AU/NZ'])
    else:
        locations = Location.objects.exclude(flag_image__isnull=True).exclude(phone__isnull=True).filter()

    location = list()
    for loc in locations:
        loc_dict = dict()
        if loc.phone and loc.flag_image.name:
            loc_dict['id'] = loc.id
            loc_dict['name'] = loc.location_name
            loc_dict['phone'] = loc.phone
            loc_dict['url'] = settings.MEDIA_URL + '' + loc.flag_image.name if loc.flag_image.name else ""
            location.append(loc_dict)

    if request.user.profile.location:
        user_loc = {'loc_name': request.user.profile.location.location_name,
                    'loc_id': request.user.profile.location.id,
                    'loc_phone': request.user.profile.location.phone,
                    'loc_flag': settings.MEDIA_URL + '' + request.user.profile.location.flag_image.name if request.user.profile.location.flag_image else "",
                    }
    else:
        us_locations = Location.objects.filter(Q(location_name__iexact='United States') | Q(location_name__iexact='US'))
        user_loc = {'loc_name': us_locations[0].location_name,
                    'loc_id': us_locations[0].id,
                    'loc_phone': us_locations[0].phone,
                    'loc_flag': settings.MEDIA_URL + '' + us_locations[0].flag_image.name if us_locations[0].flag_image else ''}

    return HttpResponse(dumps({'location': location, 'user_loc': user_loc}), content_type='application/json')


@login_required
def sales_tasks(request):
    """ Sales Tasks Page """

    return render(request, 'main/sales_tasks.html')


@login_required
def rep_details_download(request):
    ''' Google Rep Detials for Mailing '''
    if request.method == 'POST':
        # time_line = request.POST['rep_date'].split(',')
        # start_date = re.search(r'\d{4}-\d{2}-\d{2}', time_line[0]).group()
        # end_date = re.search(r'\d{4}-\d{2}-\d{2}', time_line[1]).group()
        # start_date = datetime.strptime(start_date, '%Y-%m-%d')
        # end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

        start_date = datetime(2015, 01, 01)
        end_date = datetime(2015, 04, 01)

        reps = list(Leads.objects.filter(created_date__gte=start_date,
                                         created_date__lte=end_date,
                                         google_rep_email__contains='@google.com').values_list('google_rep_email', flat=True).distinct().order_by('google_rep_email'))

        rep_details = get_rep_details_from_leads(reps, start_date, end_date)
        filename = 'basava'
        path = "/tmp/%s.csv" % (filename)
        # code_types = list(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date).values_list('type_1', flat=True).distinct())
        selected_fields = ['profile_photo_url', 'location__location_name', 'code_types', 'implemented_leads', 'monthly_lead_status',
                           'user__first_name', 'user__last_name', 'total_leads', 'user__email', 'team__team_name']
        # selected_fields.extend(code_types)
        DownloadLeads.conver_to_csv(path, rep_details, selected_fields)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response

    return render(request, 'main/rep_details_download.html')


@login_required
def get_notifications(request):
    """ Get all Notifications """
    # Notifications list
    user = UserDetails.objects.get(user=request.user)
    notification = list()
    if 'wpp' not in request.get_host():
        if user.location:
            user_region = user.location.region_set.get()
            #notifications = Notification.objects.filter(Q(region=user_region) | Q(target_location=user.location), is_visible=True).order_by('-created_date')
            notifications = Notification.objects.filter(Q(region=user_region) | Q(target_location=user.location), is_visible=True).order_by('-created_date')
        else:
            notifications = Notification.objects.filter(region=None, target_location=None, is_visible=True).order_by('-created_date')

        for notif in notifications:
            notif_dict = dict()
            notif_dict['id'] = notif.id
            notif_dict['text'] = notif.text
            notification.append(notif_dict)

    return HttpResponse(dumps(notification), content_type='application/json')


@csrf_exempt
@login_required
@manager_info_required
def create_portal_feedback(request):
    """ Create feed back """
    if request.method == 'POST':
        feedback_details = PortalFeedback()
        feedback_details.user = request.user
        feedback_details.feedback_type = str(request.POST['type'])
        feedback_details.description = str(request.POST['comment'])
        if request.FILES:
            feedback_details.attachment = request.FILES['attachmentfile']

        feedback_details.save()
        feedback_details = notify_portal_feedback_activity(request, feedback_details)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('main.views.main_home')

def report_a_bug(request):
    if request.is_ajax():
        feedback_details = PortalFeedback()
        feedback_details.user = request.user
        feedback_details.feedback_type = str(request.POST['type'])
        feedback_details.description = str(request.POST['comment'])
        feedback_details.bug_report_url = str(request.POST.get('bug_url'))
        if request.FILES:
            feedback_details.attachment = request.FILES['attachmentfile']

        feedback_details.save()
        feedback_details = notify_portal_feedback_activity(request, feedback_details)
        return HttpResponse("success")
    else:
        return HttpResponse("error")



def notify_portal_feedback_activity(request, feedback):
    mail_subject = feedback.feedback_type + " Portal Feedback"
    mail_body = get_template('main/portal_feedback/portal_feedback_mail.html').render(
        Context({
            'feedback': feedback,
            'user_info': request.user,
            'type': feedback.feedback_type,
            'bug_report_url':feedback.bug_report_url,
            'feedback_body': feedback.description,
        })
    )

    # get feedback user manager and lead owner managers information
    bcc = set([])

    mail_to = set([
        
        'g-crew@regalix-inc.com',
        'portalsupport@regalix-inc.com'
        
    ])

    mail_from = request.user.email

    attachments = list()
    if feedback.attachment:
        attachments.append(feedback.attachment)

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)
    return feedback


# @login_required
# def master_data_upload(request):
#     """ upload and load leads to view """
#     template_args = dict()
#     if request.method == 'POST':
#         if request.FILES:
#             excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
#             if not os.path.exists(excel_file_save_path):
#                 os.makedirs(excel_file_save_path)
#             excel_file = request.FILES['file']
#             # excel sheet data
#             excel_data = list()

#             # Check file extension type
#             # require only .xlsx file
#             if excel_file.name.split('.')[1] != 'xls':
#                 template_args.update({'excel_data': [], 'excel_file': excel_file.name, 'error': 'Please upload .xlsx file'})
#                 return render(request, 'main/master_upload.html', template_args)

#             file_name = 'master_data.xlsx'
#             excel_file_path = excel_file_save_path + file_name
#             with open(excel_file_path, 'wb+') as destination:
#                 for chunk in excel_file.chunks():
#                     destination.write(chunk)
#                 destination.close()

#             try:
#                 workbook = open_workbook(excel_file_path)
#             except Exception as e:
#                 template_args.update({'excel_data': [], 'excel_file': excel_file.name, 'error': e})
#                 return render(request, 'main/master_upload.html', template_args)

#             sheet = workbook.sheet_by_index(0)

#             for row_index in range(sheet.nrows):
#                 # read each row
#                 excel_row_data = list()
#                 for col_index in range(sheet.ncols):
#                     # check each column for date type
#                     cell_type = sheet.cell_type(row_index, col_index)
#                     cell_value = sheet.cell_value(row_index, col_index)

#                     # if column is formatted as datetype, convert to datetime object
#                     # otherwise show column as is
#                     if cell_type == XL_CELL_DATE:
#                         dt_tuple = xldate_as_tuple(cell_value, workbook.datemode)
#                         cell_dt = datetime(dt_tuple[0], dt_tuple[1], dt_tuple[2], dt_tuple[3], dt_tuple[4], dt_tuple[5])
#                         cell_dt = datetime.strftime(cell_dt, '%m/%d/%Y')
#                         excel_row_data.append(cell_dt)
#                     else:
#                         excel_row_data.append(cell_value)

#                 # append row data to excel sheet data
#                 excel_data.append(excel_row_data)

#             template_args.update({'excel_data': excel_data, 'excel_file': file_name})
#     return render(request, 'main/master_upload.html', template_args)


@csrf_exempt
def migrate_user_data(request):
    """ Update leads to server Database from uploaded file """

    excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
    excel_file = request.POST['file']
    excel_file_path = excel_file_save_path + excel_file
    workbook = open_workbook(excel_file_path)
    sheet = workbook.sheet_by_index(0)

    users = User.objects.all()
    user_dict = dict()
    for user in users:
        if user.first_name or user.last_name:
            full_name = "%s %s" % (user.first_name, user.last_name)
            try:
                full_name = str(full_name)
            except Exception:
                full_name = ''
            user_dict[str(user.email)] = str(full_name)

    number_of_records = sheet.nrows - 1
    number_of_saved_records = 0
    number_of_unsaved_records = 0
    new_programs = list()
    new_locations = list()
    new_region = list()
    failed_rows = list()
    tag_wpp = Group.objects.get(name='TAG-AND-WPP')
    for r_i in range(1, sheet.nrows):
        region = None
        rep_email = sheet.cell(r_i, get_col_index(sheet, 'username')).value
        google_rep_email = rep_email + '@google.com'
        google_manager = sheet.cell(r_i, get_col_index(sheet, 'manager')).value
        program = sheet.cell(r_i, get_col_index(sheet, 'program')).value
        google_manager_email = str(google_manager) + '@google.com' if google_manager else ''
        #region = sheet.cell(r_i, get_col_index(sheet, 'region')).value
        country = sheet.cell(r_i, get_col_index(sheet, 'market')).value
        country1 = sheet.cell(r_i, get_col_index(sheet, 'country')).value
        podname = sheet.cell(r_i, get_col_index(sheet, 'podname')).value
        if valid_string(program) and valid_string(country):
            try:
                user = User.objects.get(email=google_rep_email)
                tag_wpp.user_set.add(user)
            except ObjectDoesNotExist:
                user = User()
                user.email = google_rep_email
                user.username = rep_email
                user.save()
                tag_wpp.user_set.add(user)
            try:
                user_details = UserDetails.objects.get(user_id=user.id)
            except ObjectDoesNotExist:
                user_details = UserDetails()
                user_details.user_id = user.id

            user_details.pod_name = podname
            user_details.user_manager_email = google_manager_email
            user_details.user_manager_name = user_dict.get(google_manager_email, '')
            try:
                program = Team.objects.get(team_name=program)
                user_details.team_id = program.id
            except ObjectDoesNotExist:
                program = Team(team_name=program, is_active=False)
                program.save()
                new_programs.append(program.team_name)
                user_details.team_id = program.id

            if region:
                try:
                    region = Region.objects.get(name=region)
                    user_details.region_id = region.id
                except ObjectDoesNotExist:
                    region = Region(name=region)
                    region.save()
                    new_region.append(region.name)
                    user_details.region_id = region.id
            from django.db import IntegrityError
            try:
                location = Location.objects.get(location_name=country)
                location.location_name = country1
                location.save()
            except IntegrityError:
                location.delete()
                location = Location.objects.get(location_name=country1)
            except ObjectDoesNotExist:
                location = Location(location_name=country1, is_active=False)
                try:
                    location.save()
                except IntegrityError:
                    print country1
                    pass

            user_details.location_id = location.id
            '''try:
                from django.db import IntegrityError
                location = Location.objects.get(location_name=country)
                location.location_name = country1
                try:
                    location.save()
                except IntegrityError:
                    location.delete()
                    location = Location.objects.get(location_name=country1)
                user_details.location_id = location.id
            except ObjectDoesNotExist:
                location = Location(location_name=country, is_active=False)
                location.save()
                new_locations.append(country)
                user_details.location_id = location.id'''

            user_details.save()
            number_of_saved_records = number_of_saved_records + 1

        else:
            number_of_unsaved_records = number_of_unsaved_records + 1
            failed_rec = {}
            failed_rec['Google Account Manager ldap (Google Rep)'] = rep_email
            failed_rec['Google Manager'] = google_manager
            # failed_rec['r.quarter'] = r_quarter
            failed_rec['Program'] = program
            failed_rec['Country'] = country
            #failed_rec['Region'] = region
            failed_rows.append(failed_rec)

    path = "/tmp/Unsaved_Records.csv"

    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(excel_file_path):
        os.remove(excel_file_path)
    if len(failed_rows) > 0:
        filename = "Unsaved_Records"
        path = "/tmp/%s.csv" % (filename)
        DownloadLeads.conver_to_csv(path, failed_rows, failed_rows[0].keys())
    template_args = {'number_of_saved_records': number_of_saved_records if number_of_saved_records else 0,
                     'number_of_unsaved_records': number_of_unsaved_records if number_of_unsaved_records else 0,
                     'total_record': number_of_records, 'new_region': new_region, 'new_locations': new_locations,
                     'new_programs': new_programs, 'upload_target': 'normal_master_list', 'result': True}

    return render(request, 'main/upload_file.html', template_args)


def rep_details_upload(request):
    if request.method == 'POST':
        if request.FILES:
            excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
            if not os.path.exists(excel_file_save_path):
                os.makedirs(excel_file_save_path)
            excel_file = request.FILES['file']
            # excel sheet data
            file_name = 'rep_data.xlsx'
            excel_file_path = excel_file_save_path + file_name
            with open(excel_file_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)
                destination.close()

    return render(request, 'main/rep_details_upload.html')


def download_failed_records(request):
    path = "/tmp/Unsaved_Records.csv"
    response = DownloadLeads.get_downloaded_file_response(path)
    return response


def get_col_index(sheet, col_name):
    for col_index in range(sheet.ncols):
        col_val = sheet.cell(0, col_index).value
        if col_name == col_val:
            return col_index


def valid_string(col_val):
    if type(col_val) in [int, float]:
        return False
    elif not col_val:
        return False
    else:
        return True

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

@csrf_exempt
@login_required
def upload_file_handling(request):
    template_args = dict()
    if request.method == 'POST':
        if request.FILES:
            file_name, file_extension = request.FILES['attachment_name'].name.split('.')
            upload_target = request.POST['uploadTarget']
            
            if upload_target == 'whitelist_audit_permission_csv':
                if file_extension == "csv":
                    file_path = settings.MEDIA_ROOT + '/csv/'
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    csv_file = request.FILES['attachment_name']
                    file_path = file_path + csv_file.name
                    file_path = save_file(csv_file, file_path)
                    required_headers = ['External Customer Id', 'Opportunity Type']

                    with open(file_path, 'rb') as csvfile:
                        csv_object = csv.reader(csvfile, delimiter=',')
                        uploaded_column_headers = csv_object.next()
                        if required_headers[0] == uploaded_column_headers[0] and required_headers[1] == uploaded_column_headers[1]:
                            for row in csv_object:
                                s = str(row[2])
                                cid = s[:3] + '-' + s[3:6] + '-' + s[6:]
                                whitelist = WhiteListedAuditCID.objects.filter(external_customer_id=cid).first()
                                if whitelist:
                                    whitelist.external_customer_id = s[:3] + '-' + s[3:6] + '-' + s[6:]
                                    whitelist.opportunity_type = row[4]
                                    whitelist.save()
                                else:
                                    whitelist = WhiteListedAuditCID()
                                    whitelist.external_customer_id = cid
                                    whitelist.opportunity_type = row[4]
                                    whitelist.save()
                        else:
                            template_args.update({'csv_file': file_name, 'error': 'File headers mismatch. Please upload correct .csv file', 'upload_target': upload_target})

                    os.unlink(file_path)
                    template_args.update({'csv_file': csv_file.name, 'msg': "File Upload Done Successfully" + " WhiteList Added", 'upload_target': upload_target})
                else:
                    template_args.update({'csv_file': file_name, 'error': 'Please upload .csv file', 'upload_target': upload_target})
                return render(request, 'main/upload_file.html', template_args)


            if upload_target == 'bolt_permission_csv':
                if file_extension == "csv":
                    file_path = settings.MEDIA_ROOT + '/csv/'
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    csv_file = request.FILES['attachment_name']
                    file_path = file_path + csv_file.name
                    file_path = save_file(csv_file, file_path)
                    with open(file_path, 'rb') as csvfile:
                        csv_object = csv.reader(csvfile, delimiter=',')
                        user_email_list = []
                        for row in csv_object:
                            user_email_list.append(row[0])
                        users = User.objects.filter(email__in=user_email_list)
                        group = Group.objects.get(name='PICASSO-BOLT')
                        for user in users:
                             user.groups.add(group)
                    os.unlink(file_path)
                    template_args.update({'csv_file': csv_file.name, 'msg': str(len(users)) + " Users added to Picasso Bolt Group", 'upload_target': upload_target})
                else:
                    template_args.update({'csv_file': file_name, 'error': 'Please upload .csv file', 'upload_target': upload_target})
                return render(request, 'main/upload_file.html', template_args)

            # Bellow elif code is for uploading master csv file of picasso workflow master data upload
            elif upload_target == 'picasso_build_eligible_csv':

                if file_extension == "csv":
                    file_path = settings.MEDIA_ROOT + '/csv/'
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    csv_file = request.FILES['attachment_name']
                    csv_file_path = file_path + file_name
                    file_path = save_file(csv_file, csv_file_path)
                    file_name = csv_file.name

                    default_column_headers = ['Url', 'Date Assessed', 'Assessment Type', 'Pages', 'Framework', 
                                'Mobile Responsive', 'Priority', 'Comments', 'Builds Eligible', 
                                'Development Time', 'Priority Number', 'Highest Priority Number', 
                                'Is Highest Priority', 'Is Duplicate']


                    with open(file_path, 'rb') as csvfile:
                        csv_object = csv.reader(csvfile, delimiter=',')
                        uploaded_column_headers = csv_object.next()
                        for element in default_column_headers:
                            if element not in uploaded_column_headers:
                                template_args.update({'default_headers':default_column_headers, 'error':'Column Headers are not matching/not in order as fallow. Miss matched column is '+element})
                                return render(request, 'main/upload_file.html', template_args)
                        if cmp(default_column_headers, uploaded_column_headers) == 0:
                            row_count = 1
                            for each_line in csv_object:
                                row_count = row_count + 1
                                check_url = each_line[0]
                                checkdata = PicassoEligibilityMasterUpload.objects.filter(url=check_url)
                                if checkdata:
                                    pass
                                else:
                                    value = PicassoEligibilityMasterUpload()
                                    if each_line[0] == '':
                                        upload_break_msg = "Url is Mandatory and it is not given in the row "+str (row_count)+" please upload again with adding url"
                                        template_args.update({'upload_break_msg':upload_break_msg})
                                        return render(request, 'main/upload_file.html', template_args) 
                                    else:
                                        value.url = each_line[0]
                                    
                                    if each_line[1] == '':
                                        value.date_assess = 'date is not given'
                                    else:
                                        value.date_assess = each_line[1]
                                    
                                    if each_line[2] == '':
                                        value.assesment_type = 'not given'
                                    else:
                                        value.assesment_type = each_line[2]
                                    
                                    if each_line[3] == '':
                                        value.pages = 0
                                    else:
                                        value.pages = each_line[3]
                                    
                                    if each_line[4] == '':
                                        value.framework = "not given"
                                    else:
                                        value.framework =each_line[4]
                                    
                                    if each_line[5] == '':
                                         value.mobile_responsivenes = "not given"
                                    else:
                                        value.mobile_responsivenes = each_line[5]
                                    
                                    if each_line[6] == '':
                                        value.priority = 'not given'
                                    else:
                                        value.priority = each_line[6]
                                    
                                    if each_line[7] == '':
                                        value.comments = 'comments not given'
                                    else:
                                        value.comments = each_line[7]
                                    
                                    if each_line[8] == '':
                                        value.buildeligible == 'not given'
                                    else:
                                        value.buildeligible = each_line[8]
                                    
                                    if each_line[9] == '':
                                         value.development_time = 'not specified'
                                    else:
                                        value.development_time = each_line[9]
                                    
                                    if each_line[10] == '':
                                        value.priority_number = 0
                                    else:
                                        value.priority_number = each_line[10]
                                    
                                    if each_line[11] == '':
                                        value.highest_priority_number = 0
                                    else: 
                                        value.highest_priority_number = each_line[11]
                                    
                                    if each_line[12] == '':
                                        value.is_highest_priority = 'not given'
                                    else:
                                        value.is_highest_priority = each_line[12]
                                    
                                    if each_line[13] == '':
                                        value.is_duplicate = 'not given'
                                    else:
                                        value.is_duplicate = each_line[13]
                                    value.save()
                            template_args.update({'success':'File uploaded succesfully !!! '})
                            return render(request, 'main/upload_file.html', template_args)
                        else:
                            template_args.update({'error':'Please falolw the order as', 'default_headers':default_column_headers, })
                            return render(request, 'main/upload_file.html', template_args)
                else:
                    template_args.update({'csv_file': file_name, 'error': 'Please upload .csv file', 'upload_target': upload_target})
                    return render(request, 'main/upload_file.html', template_args)
                    # Bellow elif code is for uploading master csv file of picasso workflow master data upload
            elif upload_target == 'wpp_speed_optimization_csv':

                if file_extension == "csv":
                    file_path = settings.MEDIA_ROOT + '/csv/'
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    csv_file = request.FILES['attachment_name']
                    csv_file_path = file_path + file_name
                    file_path = save_file(csv_file, csv_file_path)
                    file_name = csv_file.name

                    required_headers = ['CID', 'URL', 'Builds Eligible?', 'Date Assessed']

                    with open(file_path, 'rb') as csvfile:
                        csv_object = csv.reader(csvfile, delimiter=',')
                        uploaded_column_headers = csv_object.next()
                        missing_headers = []
                        for element in required_headers:
                            if element not in uploaded_column_headers:
                                missing_headers.append(element)
                        if missing_headers:
                            template_args.update({'default_headers': missing_headers,
                                                      'error': 'Missing Headers '+ str(missing_headers)})
                            return render(request, 'main/upload_file.html', template_args)

                        row_count = 0
                        from leads.views import url_filter
                        errors = []
                        for row in csv_object:
                            skip = False
                            error = {}
                            row_count += 1
                            cid = row[0]
                            if not cid:
                                skip = True
                                error["row_count"] = row_count
                                error["missing_data"] = ["CID"]

                            url = row[1]
                            if not url:
                                skip = True
                                error["row_count"] = row_count
                                err = error.get("missing_data", False)
                                if not err:
                                    error["missing_data"] = ['URL']
                                else:
                                    err.append(url)

                            domain = url_filter(url)

                            last_assessed_date = row[2]
                            if len(last_assessed_date) > 0:
                                try:
                                    last_assessed_date = datetime.strptime(last_assessed_date, "%m/%d/%Y")
                                except:
                                    skip = True
                                    error["row_count"] = row_count
                                    err = error.get("missing_data", False)
                                    if not err:
                                        error["Invalid Date Format"] = ["LAST ASSESSED DATE"]
                                    else:
                                        err.append(last_assessed_date)
                            else:
                                last_assessed_date = datetime.now()

                            bolt_eligible = row[9]
                            if not bolt_eligible:
                                bolt_eligible = False
                            else:
                                bolt_eligible = bolt_eligible.lower()
                                if bolt_eligible == "y":
                                    bolt_eligible = True
                                elif bolt_eligible == "n":
                                    bolt_eligible = False
                            if not skip:
                                bolt_object = BuildsBoltEligibility.objects.filter(cid=cid, domain=domain).order_by('-last_assessed_date')
                                if bolt_object:
                                    bolt_object = bolt_object[0]
                                    bolt_object.last_assessed_date = last_assessed_date
                                    bolt_object.bolt_eligible = bolt_eligible
                                    bolt_object.cid = cid
                                    bolt_object.save()
                                else:
                                    bolt_object = BuildsBoltEligibility()
                                    bolt_object.last_assessed_date = last_assessed_date
                                    bolt_object.bolt_eligible = bolt_eligible
                                    bolt_object.cid = cid
                                    bolt_object.url = url
                                    bolt_object.domain = domain
                                    bolt_object.save()
                            else:
                                errors.append(error)
                        if errors:
                            template_args.update({'success': 'File uploaded succesfully !!! ', 'error':errors})
                        else:
                            template_args.update({'success': 'File uploaded succesfully !!! '})
                        return render(request, 'main/upload_file.html', template_args)
                else:
                    template_args.update({'success': 'Invalid file format'})
                    return render(request, 'main/upload_file.html', template_args)
            else:
                excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
                if not os.path.exists(excel_file_save_path):
                    os.makedirs(excel_file_save_path)
                excel_file = request.FILES['attachment_name']
                upload_target = request.POST['uploadTarget']

                if excel_file.name.split('.')[1] not in ['xls', 'xlsx']:
                    template_args.update({'excel_data': [], 'excel_file': excel_file.name, 'error': 'Please upload .xlsx file', 'upload_target': upload_target})
                    return render(request, 'main/upload_file.html', template_args)

                file_name = excel_file.name
                excel_file_path = excel_file_save_path + file_name
                file_path = save_file(excel_file, excel_file_path)

                try:
                    workbook = open_workbook(excel_file_path)
                except Exception as e:
                    template_args.update({'excel_data': [], 'excel_file': excel_file.name, 'error': e, 'upload_target': upload_target})
                    return render(request, 'main/upload_file.html', template_args)

                sheet = workbook.sheet_by_index(0)
                uploaded_headers = [str(cell.value) for cell in sheet.row(0)]

                if upload_target == 'wpp_master_list':
                    default_headers = ['CID', 'Provisional Assignee', 'URL', 'Server', 'Framework', 'CMS', 'Ecommerce', 'Priority', 'Treatment Type', 'Notes']
                    if len(default_headers) == len(uploaded_headers):
                        if cmp(default_headers, uploaded_headers) != 0:
                            template_args.update({'excel_data': [], 'default_headers': default_headers, 'excel_file': excel_file.name, 'error': 'Sheet Header Mis Match, please follow these header', 'upload_target': upload_target})
                            return render(request, 'main/upload_file.html', template_args)
                        else:
                            # print default_headers, uploaded_headers
                            excel_data = convert_excel_data_into_list(workbook)
                            template_args.update({'excel_data': excel_data, 'excel_file': excel_file.name, 'upload_target': upload_target})
                            return render(request, 'main/upload_file.html', template_args)

                elif upload_target == 'normal_master_list':
                    default_headers = ['manager', 'username', 'market served', 'program', 'region', 'podname']
                    for element in default_headers:
                        if element not in uploaded_headers:
                            template_args.update({'excel_data': [], 'default_headers': default_headers, 'excel_file': excel_file.name, 'error': 'Sheet Header Mis Match, please follow these header', 'upload_target': upload_target})
                            return render(request, 'main/upload_file.html', template_args)
                        else:
                            excel_data = convert_excel_data_into_list(workbook)
                            template_args.update({'excel_data': excel_data, 'excel_file': excel_file.name, 'upload_target': upload_target})
                            return render(request, 'main/upload_file.html', template_args)
                elif upload_target == 'csat_report_data':
                    default_headers = ['Date', 'Time', 'Category', 'Language', 'CID', 'CLI', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5']
                    for element in default_headers:
                        if element not in uploaded_headers:
                            template_args.update({'excel_data': [], 'default_headers': default_headers, 'excel_file': excel_file.name, 'error': 'Sheet Header Mis Match, please follow these header', 'upload_target': upload_target})
                            return render(request, 'main/upload_file.html', template_args)
                        else:
                            sheet = workbook.sheet_by_index(0)
                            get_survey_data_from_excel(workbook, sheet, request.POST.get('survey_channel'))
                            return render(request, 'main/upload_file.html')
    return render(request, 'main/upload_file.html')


def map_leads(leads):
    if len(leads) > 1:
        return leads[0]
    elif len(leads) == 1:
        return leads[0]
    else:
        pass


def find_leads(cid, process, survey_date):
    query = dict()
    if process == 'TAG':
        query['customer_id'] = cid
        query['date_of_installation'] = survey_date
        shopping_code_types = ['Google Shopping Setup', 'Existing Datafeed Optimization', 'Google Shopping Migration']
        day_leads = Leads.objects.exclude(type_1__in=shopping_code_types).filter(**query)

        if not day_leads:
            _dt_start = survey_date - timedelta(7)
            _dt_end = survey_date
            del query['date_of_installation']
            query['date_of_installation__range'] = (_dt_start, _dt_end)
            week_leads = Leads.objects.exclude(type_1__in=shopping_code_types).filter(**query)

            if not week_leads:
                _dt_start = survey_date - timedelta(30)
                _dt_end = survey_date
                query['date_of_installation__range'] = (_dt_start, _dt_end)
                month_leads = Leads.objects.exclude(type_1__in=shopping_code_types).filter(**query)

                if not month_leads:
                    del query['date_of_installation__range']
                    all_leads = Leads.objects.exclude(type_1__in=shopping_code_types).filter(**query)

                    if not all_leads:
                        print 'lead_is_unmapped'
                        return None
                    else:
                        lead = map_leads(all_leads)

                else:
                    lead = map_leads(month_leads)
            else:
                lead = map_leads(week_leads)
        else:
            lead = map_leads(day_leads)
    else:
        query['type_1__in'] = ['Google Shopping Setup', 'Existing Datafeed Optimization', 'Google Shopping Migration']
        query['customer_id'] = cid
        query['date_of_installation'] = survey_date
        day_leads = Leads.objects.filter(**query)
        if not day_leads:
            del query['date_of_installation']
            all_leads = Leads.objects.filter(**query)

            if not all_leads:
                print 'shopping_lead_is_unmapped'
                return None
            else:
                lead = map_leads(all_leads)
        else:
            lead = map_leads(day_leads)

    return lead


def get_survey_data_from_excel(workbook, sheet, survey_channel):
    for r_i in range(1, sheet.nrows):
        if survey_channel == 'Phone':
            str_cid = str(int(sheet.cell(r_i, get_col_index(sheet, 'CID')).value))
            cid = '%s-%s-%s' % (str_cid[:3], str_cid[3:6], str_cid[6:])
        else:
            cid = sheet.cell(r_i, get_col_index(sheet, 'CID')).value

        lead_date = sheet.cell(r_i, get_col_index(sheet, 'Date')).value
        lead_time = sheet.cell(r_i, get_col_index(sheet, 'Time')).value
        process = sheet.cell(r_i, get_col_index(sheet, 'Category')).value

        survey_date_tuple = xldate_as_tuple(lead_date + lead_time, workbook.datemode)
        # survey_date = datetime(survey_date_tuple[0], survey_date_tuple[1], survey_date_tuple[2], survey_date_tuple[3], survey_date_tuple[4], survey_date_tuple[5])
        survey_date = datetime(survey_date_tuple[0], survey_date_tuple[1], survey_date_tuple[2], survey_date_tuple[3])
        try:
            csat_record = CSATReport.objects.get(customer_id=cid, survey_date=survey_date, process=process)
        except ObjectDoesNotExist:
            csat_record = CSATReport()

        csat_record.region = ''
        csat_record.program = ''
        csat_record.code_type = ''
        csat_record.lead_owner = ''
        csat_record.sf_lead_id = ''
        if survey_channel == 'Phone':
            csat_record.channel = 'PHONE'
            csat_record.cli = int(sheet.cell(r_i, get_col_index(sheet, 'CLI')).value)
        else:
            csat_record.channel = 'EMAIL'
            csat_record.cli = 0
        csat_record.customer_id = cid
        csat_record.survey_date = survey_date
        csat_record.process = process
        csat_record.q1 = int(sheet.cell(r_i, get_col_index(sheet, 'Q1')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q1')).value else 0
        csat_record.q2 = int(sheet.cell(r_i, get_col_index(sheet, 'Q2')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q2')).value else 0
        csat_record.q3 = int(sheet.cell(r_i, get_col_index(sheet, 'Q3')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q3')).value else 0
        csat_record.q4 = int(sheet.cell(r_i, get_col_index(sheet, 'Q4')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q4')).value else 0
        csat_record.q5 = int(sheet.cell(r_i, get_col_index(sheet, 'Q5')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q5')).value else 0

        lead = find_leads(cid, process, survey_date)
        if lead:
            csat_record.sf_lead_id = lead.sf_lead_id
            csat_record.region = lead.country
            csat_record.program = lead.team
            csat_record.code_type = lead.type_1
            csat_record.lead_owner = lead.lead_owner_email
            csat_record.mapped_lead_created_date = lead.created_date
            csat_record.lead_owner_name = lead.lead_owner_name
            csat_record.lead_owner_email = lead.lead_owner_email
            csat_record.language = lead.language if lead.language else sheet.cell(r_i, get_col_index(sheet, 'Language')).value
            csat_record.category = 'MAPPED'
        else:
            csat_record.category = 'UNMAPPED'
            csat_record.language = sheet.cell(r_i, get_col_index(sheet, 'Language')).value

        try:
            csat_record.save()
        except Exception as e:
            print e, cid

@csrf_exempt
def migrate_table_data(request):
    template_args = dict()
    excel_file_save_path = settings.MEDIA_ROOT + '/excel/'
    excel_file = request.POST['file']
    excel_file_path = excel_file_save_path + excel_file
    workbook = open_workbook(excel_file_path)
    sheet = workbook.sheet_by_index(0)
    upload_target = request.POST['target_upload']
    treatment_type_dict = {t_type.name: t_type.id for t_type in TreatmentType.objects.all()}
    number_of_records = 0
    number_of_saved_records = 0
    number_of_updated_records = 0
    if upload_target == 'wpp_master_list':
        number_of_records = sheet.nrows - 1
        for r_i in range(1, sheet.nrows):
            data = dict()
            data['customer_id'] = sheet.cell(r_i, get_col_index(sheet, 'CID')).value
            data['provisional_assignee'] = sheet.cell(r_i, get_col_index(sheet, 'Provisional Assignee')).value
            data['url'] = sheet.cell(r_i, get_col_index(sheet, 'URL')).value
            data['server'] = sheet.cell(r_i, get_col_index(sheet, 'Server')).value
            data['framework'] = sheet.cell(r_i, get_col_index(sheet, 'Framework')).value
            data['cms'] = sheet.cell(r_i, get_col_index(sheet, 'CMS')).value
            data['ecommerce'] = sheet.cell(r_i, get_col_index(sheet, 'Ecommerce')).value
            try:
                priority = int(sheet.cell(r_i, get_col_index(sheet, 'Priority')).value)
                data['priority'] = priority
            except Exception:
                data['priority'] = 1
            treatment_type = sheet.cell(r_i, get_col_index(sheet, 'Treatment Type')).value
            data['treatment_type_id'] = treatment_type_dict.get(treatment_type, None)
            data['notes'] = sheet.cell(r_i, get_col_index(sheet, 'Notes')).value
            data['year'] = datetime.now().year
            month = datetime.now().month
            if month <= 3:
                data['quarter'] = 'Q1'
            elif month > 3 and month <= 6:
                data['quarter'] = 'Q2'
            elif month > 6 and month <= 9:
                data['quarter'] = 'Q3'
            elif month > 9 and month <= 12:
                data['quarter'] = 'Q4'
            try:
                wpp_record = WPPMasterList.objects.get(customer_id=data['customer_id'], quarter=data['quarter'], year=data['year'])
                number_of_updated_records += 1
                wpp_rec = WPPMasterList(id=wpp_record.id, **data)
                wpp_rec.created_date = wpp_record.created_date
            except ObjectDoesNotExist:
                wpp_rec = WPPMasterList(**data)
                number_of_saved_records += 1
            wpp_rec.save()

        if os.path.isfile(excel_file_path):
            os.remove(excel_file_path)
        template_args.update({'result': 'WPP Master List', 'number_of_saved_records': number_of_saved_records, 'number_of_records': number_of_records,
                              'number_of_records': number_of_records, 'number_of_updated_records': number_of_updated_records})
        return render(request, 'main/upload_file.html', template_args)


@login_required
def picasso_home(request):
    user_profile = get_user_profile(request.user)
    query = dict()
    picasso_objective_dict = dict()
    start_date, end_date = get_quarter_date_slots(datetime.utcnow())
    current_quarter = ReportService.get_current_quarter(datetime.utcnow())
    title = "Activity Summary for %s - %s to %s %s" % (current_quarter, datetime.strftime(start_date, '%b'), datetime.strftime(end_date, '%b'), datetime.strftime(start_date, '%Y'))
    query['created_date__gte'] = start_date
    query['created_date__lte'] = end_date
    objectives = ['Engage with your Content', 'Become a Fan', 'Buy Online', 'Form Entry', 'Call your Business']
    if request.user.groups.filter(name='SUPERUSER'):
        end_date = datetime.utcnow()
        start_date = datetime(2015, 01, 01)
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        # start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        picasso_lead_status = get_count_of_each_lead_status_by_rep(list(), 'picasso', start_date=start_date, end_date=end_date)
        picasso_objective_counts = PicassoLeads.objects.filter(**query).values('picasso_objective').annotate(count=Count('pk'))
    else:
        picasso_lead_status = get_count_of_each_lead_status_by_rep(request.user.email, 'picasso', start_date=None, end_date=None)
        picasso_objective_counts = PicassoLeads.objects.filter(**query).values('picasso_objective').annotate(count=Count('pk'))

    picasso_status_dict = {'Buy Online': 0, 'Engage with your Content': 0, 'Call your Business': 0, 'Form Entry': 0, 'Become a Fan': 0}
    for each_objective in picasso_objective_counts:
        picasso_status_dict[each_objective['picasso_objective']] = each_objective.get('count')
    picasso_objective_total = sum([picasso_dict.get('count') for picasso_dict in picasso_objective_counts])

    for key, value in picasso_status_dict.iteritems():
        if key in objectives:
            picasso_objective_dict[key.replace(' ', '_')] = value

    current_date = datetime.utcnow()
    picasso_top_performer = get_top_performer_list(current_date, 'PICASSO')

    feedback_list = dict()
    feedbacks, feedback_list = get_feedbacks(request.user, 'PICASSO')
    return render(request, 'main/picasso_index.html', {'feedback_list': feedback_list, 'picasso': True, 'user_profile': user_profile,
                                                        'title': title,
                                                        'picasso_lead_status': picasso_lead_status,
                                                        'picasso_objective_dict': picasso_objective_dict,
                                                        'picasso_objective_total': picasso_objective_total,
                                                        'picasso_top_performer': picasso_top_performer,
                                                        'no_leads': check_lead_submitter_for_empty(picasso_top_performer)})


@login_required
def export_feedback(request):
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        from_date = datetime.strptime(str(date_from), '%m/%d/%Y')
        to_date = datetime.strptime(str(date_to), '%m/%d/%Y')

        get_feedbacks = Feedback.objects.filter(created_date__gte=from_date, created_date__lte=to_date)

        collattr = ['ID', 'Title', 'CID', 'Advertiser Name', 'Location', 'Language', 'Feedback Type', 'Description', 'Status', 'Lead Owner', 'Google Account Manager', 'Program', 'Code Type', 'Created Date', 'Resolved By', 'Resolved By Date', 'Second Resolved By', 'Second Resolved Date', 'Third Resolved By', 'Third Resolved Date', 'SF Lead ID', 'Comments']
        feedback_list = list()

        for feedback in get_feedbacks:

            feedback_dict = dict()
            feedback_dict['ID'] = feedback.id
            feedback_dict['Title'] = feedback.title
            feedback_dict['CID'] = feedback.cid
            feedback_dict['Advertiser Name'] = feedback.advertiser_name
            feedback_dict['Location'] = feedback.location.location_name
            feedback_dict['Language'] = feedback.language
            feedback_dict['Feedback Type'] = feedback.feedback_type
            feedback_dict['Description'] = feedback.description
            feedback_dict['Status'] = feedback.status
            feedback_dict['Lead Owner'] = feedback.lead_owner.username
            try:
                if feedback.google_account_manager:
                    feedback_dict['Google Account Manager'] = feedback.google_account_manager.username
            except ObjectDoesNotExist:
                feedback_dict['Google Account Manager'] = ''

            if feedback.code_type and feedback.program:
                feedback_dict['Code Type'] = feedback.code_type
                feedback_dict['Program'] = feedback.program.team_name
            else:
                if feedback.sf_lead_id:
                    program_name = Leads.objects.get(sf_lead_id=feedback.sf_lead_id)
                    feedback_dict['Program'] = program_name.team
                    feedback_dict['Code Type'] = program_name.type_1
                else:
                    feedback_dict['Program'] = ""
                    feedback_dict['Code Type'] = ""

            feedback_dict['Created Date'] = datetime.strftime(feedback.created_date, '%m/%d/%Y')
            feedback_dict['Resolved By'] = feedback.resolved_by.username if feedback.resolved_by  else ''
            feedback_dict['Resolved By Date'] = datetime.strftime(feedback.resolved_date, '%m/%d/%Y') if feedback.resolved_date else ''
            feedback_dict['Second Resolved By'] = feedback.second_resolved_by.username if feedback.second_resolved_by else ''
            feedback_dict['Second Resolved Date'] = datetime.strftime(feedback.second_resolved_date, '%m/%d/%Y') if feedback.second_resolved_date else ''
            feedback_dict['Third Resolved By'] = feedback.third_resolved_by.username if feedback.third_resolved_by else ''
            feedback_dict['Third Resolved Date'] = datetime.strftime(feedback.third_resolved_date, '%m/%d/%Y') if feedback.third_resolved_date else ''
            feedback_dict['SF Lead ID'] = feedback.sf_lead_id

            get_feedback_comments = FeedbackComment.objects.filter(feedback=feedback.id).values('comment', 'comment_by__username', 'feedback_status')
            comments = list()
            for data in get_feedback_comments:
                for key, val in data.iteritems():
                    comments.append(key + ":" + val)
            comments = ', '.join(comments)
            feedback_dict['Comments'] = comments

            feedback_list.append(feedback_dict)

        filename = "feedbacks"
        path = write_appointments_to_csv(feedback_list, collattr, filename)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response
    return render(request, 'main/export_feedback.html', {})


def write_appointments_to_csv(result, collumn_attr, filename):
    path = "/tmp/%s.csv" % (filename)
    DownloadLeads.conver_to_csv(path, result, collumn_attr)
    return path

@login_required
def rlsa_limitations(request):
    return render(request, 'main/rlsa_limitations.html', {})


def get_regalix_emails(request):
    if request.is_ajax():
        search_keyword = request.GET.get('search_key')
        all_email = User.objects.filter(email__icontains = search_keyword)[:20]
        regalix_email_list = list()
        for email in all_email:
            if 'regalix-inc.com' in email.email:
                regalix_email_list.append(email.email)
        response = {'success':True, 'message':'Emails Fetched', 'data':regalix_email_list}
        return HttpResponse(json.dumps(response))
    response = {'success':False, 'message':'failed to fetch email id or no email id in db'}
    return HttpResponse(json.dumps(response))


def assign_feedback(request):
    if request.is_ajax():
        assignee = request.GET.get('assignee_mail')
        title = request.GET.get('assign_feedback_title')
        cid = request.GET.get('assign_feedback_cid')
        feedback_type = request.GET.get('assign_feedback_type')
        loaction = request.GET.get('feedback_location_name')
        created_date = request.GET.get('assign_feedback_createddate')
        feedback_id = request.GET.get('feedback_id');
        feedback_description = request.GET.get('feedback_description')

        user = User.objects.get(email=assignee)
        if user:
            try:
                Feedback.objects.select_for_update().filter(id=feedback_id).update(assigned_to = user)
                # mailing functionolities
                feedback_url = request.build_absolute_uri(reverse('main.views.view_feedback', kwargs={'id': feedback_id}))
                mail_from = str(request.user.first_name)+' '+str(request.user.last_name)
                fb_su = []
                feedback_super_user_group = User.objects.filter(groups__name='FEEDBACK-SUPER-USER')
                
                for user in feedback_super_user_group:
                    fb_su.append(user.email)

                if feedback_super_user_group:

                    description = "The following customer feedback is assigned to "+str(assignee)+" for action by " + request.user.first_name + " " + request.user.last_name
                    #mail_subject = "Lead Feedback is assigned to you to resolve " + str(datetime.today().date())
                    mail_subject = "Customer Feedback ["+feedback_type+" - "+cid+"] Status- Submit Response and/or Initiate Closure"
                    mail_body = get_template('main/feedback_mail/feedback_assigning_mail.html').render(Context({
                                            'title': title, 'cid':cid, 'feedbacktype':feedback_type, 
                                            'loaction':loaction,'url_link':feedback_url, 'created_date':created_date, 'feedback_description':feedback_description, 'description' : description}))
                    bcc = set()
                    attachments = list()
                    send_mail(mail_subject, mail_body, mail_from, fb_su, list(bcc),  attachments, template_added=True)

                if assignee:
                    description = "The following customer feedback is assigned to you for action. Please submit appropriate response and/ or initiate closure in a timely manner."

                    mail_to = [ str(assignee)]
                    #mail_subject = "Lead Feedback is assigned to you to resolve " + str(datetime.today().date())
                    mail_subject = "Customer Feedback ["+feedback_type+" - "+cid+"] Status- Submit Response and/or Initiate Closure"
                    mail_body = get_template('main/feedback_mail/feedback_assigning_mail.html').render(Context({
                                            'title': title, 'cid':cid, 'feedbacktype':feedback_type, 
                                            'loaction':loaction,'url_link':feedback_url, 'created_date':created_date, 'feedback_description':feedback_description, 'description' : description}))
                    bcc = set()
                    attachments = list()
                    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc),  attachments, template_added=True)
                
                assiging_feedback(request, assignee, id=feedback_id) # saving assigning process
                response = {'success': True, 'msg':'Succesfully assigned'}
                return HttpResponse(json.dumps(response))
            except ObjectDoesNotExist, e:
                print e
                response = {'success': False,'msg':'failed to assign'}
                return HttpResponse(json.dumps(response))
    response = {'success': False,'msg':'failed to assign. Server error please try after sometime.'}
    return HttpResponse(json.dumps(response))

        
def assiging_feedback(request, assignee, id):
    assigned_by = str(request.user.first_name)+' '+str(request.user.last_name)
    feedback = Feedback.objects.get(id=id)
    feedback_assigning_ascomment = FeedbackComment()
    feedback_assigning_ascomment.feedback = feedback
    feedback_assigning_ascomment.comment = "This Feedback has been assigned to "+str(assignee)+" to fix. Assigned by "+str(assigned_by)
    feedback_assigning_ascomment.comment_by = request.user
    # If assigining we add the comment in Table, so just to know who added the comment.
    # We use comment_type 'S' == System comment, 'U' == User comment
    feedback_assigning_ascomment.comment_type = 'S'
    feedback_assigning_ascomment.save()
    #return redirect('main.views.view_feedback', id=id)
    return True


@csrf_exempt
# Notification Manager
def notification_manager(request):
    region = Region.objects.all()
    location = Location.objects.all()   
    if request.method == "GET":
        notification = request.GET.get('notifications', False)
        if notification:
            data = []
            records = Notification.objects.all()
            for rec in records:
                notify_status = ''
                display_on_form_status = ''
                modified_by = ''

                if rec.is_visible:
                    notify_status = 'Published'
                elif rec.is_draft:
                    notify_status = 'Drafted'
                else:
                    notify_status = 'Expired'

                if rec.display_on_form:
                    display_on_form_status = 'Yes'
                else:
                    display_on_form_status = 'No'
                
                created_on = rec.created_date
                if created_on:
                    created_on = time.mktime(created_on.timetuple())

                start_date = rec.from_date
                if start_date:
                    start_date = time.mktime(start_date.timetuple())

                end_date = rec.to_date
                if end_date:
                    end_date = time.mktime(end_date.timetuple())
                
                region_list = []
                location_list = []
                for i in rec.region.all():
                    region_list.append('  '+str(i.name))

                for i in rec.target_location.all():
                    location_list.append('  '+str(i.location_name))

                if rec.modified_by:
                    modified_by = str(rec.modified_by.first_name) + ' ' + str(rec.modified_by.last_name)
                else:
                    modified_by = ''
                da = {
                    'created_on': created_on,
                    'content': rec.text,
                    'countries': location_list,
                    'regions': region_list,
                    'status': notify_status,
                    'display_on_form': display_on_form_status,
                    'start_date': start_date,
                    'end_date': end_date,
                    'modified_by': modified_by,
                    'id': rec.id,
                }
                data.append(da)
            resp = {'success': True, 'data': data}
            return HttpResponse(json.dumps(resp), content_type='application/json')
        return render(request, 'main/notification_manager.html',{'locations':location,'regions':region})

    elif request.method == "POST":
        data = json.loads(request.body)
        text = data['text']
        locations =  data['location']
        if data['f_date'] and data['f_date'] != '/-/':
            from_date = datetime.strptime(str(data['f_date']), '%m/%d/%Y')
        else:
            from_date = None

        if data['t_date'] and data['t_date'] != '/-/': 
            to_date = datetime.strptime(str(data['t_date']), '%m/%d/%Y')
        else:
            to_date = None

        regions =  data['region']
        
        on_form =  data['on_form']

        region = Region.objects.filter(name__in=regions)
        location = Location.objects.filter(location_name__in=locations)
        
        email = request.user.username

        try:
            user = User.objects.get(email=email)
        except:
            user = None

        update = request.GET.get('id')

        if update == '0':
            notification = Notification()
            notification.text = text

            if data['draft']:
                notification.is_visible = False
                notification.is_draft = True
            else:
                notification.is_visible = True
                notification.is_draft = False
            notification.from_date = from_date
            notification.to_date = to_date
            notification.display_on_form = on_form
            notification.modified_by = user
            notification.save()

            for reg in region:
                notification.region.add(reg)
            for loc in location:
                notification.target_location.add(loc)

        else:
            notification = Notification.objects.get(id=update)
            notification.text = text

            if data['draft']:
                notification.is_visible = False
                notification.is_draft = True
            else:
                notification.is_visible = True
                notification.is_draft = False
            notification.from_date = from_date
            notification.to_date = to_date
            notification.display_on_form = on_form
            notification.modified_by = user
            notification.region.clear()
            notification.target_location.clear()
            notification.save()

            for reg in region:
                notification.region.add(reg)
            for loc in location:
                notification.target_location.add(loc)

        created_on = notification.created_date
        if created_on:
            created_on = time.mktime(created_on.timetuple())

        start_date = notification.from_date
        if start_date:
            start_date = time.mktime(start_date.timetuple())

        end_date = notification.to_date
        if end_date:
            end_date = time.mktime(end_date.timetuple())


        notify_status = ''
        display_on_form_status = ''
        if notification.is_visible:
            notify_status = 'Published'
        elif notification.is_draft:
            notify_status = 'Drafted'

        if notification.display_on_form:
            display_on_form_status = 'Yes'
        else:
            display_on_form_status = 'No'


        region_list = []
        location_list = []
        for i in notification.region.all():
            region_list.append('  '+str(i.name))

        for i in notification.target_location.all():
            location_list.append('  '+str(i.location_name))



        resp = {'success': True,
        'id':notification.id,
        'content':notification.text,
        'countries':location_list,
        'regions':region_list,
        'display_on_form':display_on_form_status,
        'modified_by':str(notification.modified_by.first_name) + ' ' + str(notification.modified_by.last_name),
        'start_date':start_date,
        'end_date':end_date,
        'created_date':created_on,
        'status':notify_status,
        }
        return HttpResponse(json.dumps(resp), content_type='application/json')
    elif request.method == 'PUT':
        row_id = request.GET.get('id')
        notification = Notification.objects.get(id=row_id)
        if notification:
            notification.is_visible = False
            notification.display_on_form = False
            notification.save()
            resp = {'success': True}
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            from django.core import exceptions
            raise exceptions.PermissionDenied
    
    else:
        from django.core import exceptions
        raise exceptions.PermissionDenied

    return render(request, 'main/notification_manager.html', {'locations':location,'regions':region})



