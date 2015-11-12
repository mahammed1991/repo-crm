from json import dumps
from datetime import datetime, timedelta, date
from collections import OrderedDict
import time
import os
import operator
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from requests import request as request_call
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse
from forum.models import *
from django.contrib.auth.models import User, Group

from django.conf import settings

from lib.helpers import send_mail, manager_info_required, wpp_user_required

from main.models import (UserDetails, Feedback, FeedbackComment, CustomerTestimonials, ContectList, WPPMasterList,
                         Notification, PortalFeedback, ResourceFAQ)
from leads.models import Location, Leads, Team, Language, TreatmentType, WPPLeads, PicassoLeads
from django.db.models import Count
from lib.helpers import (get_week_start_end_days, first_day_of_month, get_user_profile, get_quarter_date_slots,
                         last_day_of_month, previous_quarter, get_count_of_each_lead_status_by_rep, get_rep_details_from_leads,
                         is_manager, get_user_list_by_manager, get_user_under_manager, date_range_by_quarter, tag_user_required,
                         get_previous_month_start_end_days, create_new_user, convert_excel_data_into_list)
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
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

    if 'WPP' not in request.session['groups']:

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

        total_tag_leads = Leads.objects.exclude(type_1__in=['Google Shopping Migration',
                                                            'Google Shopping Setup', '', 'WPP']).filter(created_date__gte=start_date,
                                                                                                        created_date__lte=end_date).count()

        rr_implemented_tag_leads = Leads.objects.exclude(type_1__in=['Google Shopping Migration', 'Google Shopping Setup', '', 'WPP'],
                                                         lead_sub_status='RR - Inactive').filter(created_date__gte=start_date,
                                                                                                 created_date__lte=end_date,
                                                                                                 lead_status__in=['Rework Required']).count()

        implemented_tag_leads = Leads.objects.exclude(type_1__in=['Google Shopping Migration',
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
        notifications = Notification.objects.filter(is_visible=True)

        customer_testimonials = CustomerTestimonials.objects.all().order_by('-created_date')

        # feedback summary end here
        return render(request, 'main/tag_index.html', {'customer_testimonials': customer_testimonials, 'lead_status_dict': lead_status_dict,
                                                       'user_profile': user_profile,  # 'question_list': question_list,
                                                       'top_performer': top_performer, 'report_summary': report_summary, 'title': title,
                                                       'feedback_list': feedback_list, 'notifications': notifications})

    else:
        if request.user.groups.filter(name='SUPERUSER'):
            # start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
            start_date = datetime(2015, 01, 01)
            end_date = datetime.now()

            wpp_details = ReportService.get_wpp_report_details_for_filters(start_date, end_date, list())
        else:
            start_date = datetime(2014, 01, 01)
            end_date = datetime.now()
            wpp_details = ReportService.get_wpp_report_details_for_filters(start_date, end_date, [request.user.email])

        current_date = datetime.utcnow()
        wpp_top_performer = get_top_performer_list(current_date, 'WPP')

        wpp_feedback_list = dict()
        wpp_feedbacks, wpp_feedback_list = get_feedbacks(request.user, 'WPP')

        wpp_report = {key: (wpp_details['wpp_treatment_type_analysis'][key]['Implemented'] / wpp_details['wpp_treatment_type_analysis'][key]['TOTAL']) * 100 if wpp_details['wpp_treatment_type_analysis'][key]['TOTAL'] else 0 for key in wpp_details['wpp_treatment_type_analysis'].keys()}
        wpp_report['TOTAL'] = (wpp_details['wpp_lead_status_analysis']['Implemented'] / wpp_details['wpp_lead_status_analysis']['TOTAL']) * 100 if wpp_details['wpp_lead_status_analysis']['TOTAL'] else 0

        # print wpp_details['wpp_lead_status_analysis']

        key_dict = {'Open': 'open', 'On Hold': 'on_hold', 'In UI/UX Review': 'in_ui_ux_review', 'In File Transfer': 'in_file_transfer', 'In Mockup': 'in_mockup', 'TOTAL': 'total',
                    'Mockup Review': 'mockup_review', 'In Development': 'in_development', 'In Stage': 'in_statge', 'In A/B Test': 'in_ab_test', 'Implemented': 'implemented', 'Deferred': 'deferred'}

        wpp_lead_dict = dict()
        for key, value in key_dict.items():
            wpp_lead_dict[value] = wpp_details['wpp_lead_status_analysis'][key]

        wpp_treatment_type_report = {key.replace(' ', ''): value for key, value in wpp_report.items()}

        return render(request, 'main/wpp_index.html', {'wpp_lead_dict': wpp_lead_dict, 'user_profile': user_profile,
                                                       'wpp_feedback_list': wpp_feedback_list, 'wpp_report': wpp_report,
                                                       'wpp_top_performer': wpp_top_performer, 'title': title,
                                                       'wpp_treatment_type_report': wpp_treatment_type_report})


def get_feedbacks(user, feedback_type):
    """ List Feedbacks by user """

    if user.groups.filter(name='FEEDBACK'):
        if feedback_type == 'WPP':
            feedbacks = Feedback.objects.filter(code_type='WPP').order_by('-created_date')
        else:
            feedbacks = Feedback.objects.exclude(code_type='WPP').filter().order_by('-created_date')
    else:
        if feedback_type == 'WPP':
            feedbacks = Feedback.objects.filter(code_type='WPP')
            feedbacks = feedbacks.filter(
                Q(user__email=user.email)
                | Q(user__profile__user_manager_email=user.email)
                | Q(lead_owner__email=user.email)
                | Q(lead_owner__profile__user_manager_email=user.email)
            ).order_by('-created_date')
        else:
            feedbacks = Feedback.objects.exclude(code_type='WPP').filter(
                Q(user__email=user.email)
                | Q(user__profile__user_manager_email=user.email)
                | Q(lead_owner__email=user.email)
                | Q(lead_owner__profile__user_manager_email=user.email)
            ).order_by('-created_date')
    feedback_list = dict()
    feedback_list['new'] = feedbacks.filter(status='NEW').count()
    feedback_list['in_progress'] = feedbacks.filter(status='IN PROGRESS').count()
    feedback_list['resolved'] = feedbacks.filter(status='RESOLVED').count()
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
        topper_list = Leads.objects.exclude(google_rep_email='').filter(
            created_date__gte=start_date,
            created_date__lte=end_date).values('google_rep_email').annotate(submitted=Count('sf_lead_id')).order_by('-submitted')
    elif lead_type == 'PICASSO':
        topper_list = PicassoLeads.objects.exclude(google_rep_email='').filter(
            created_date__gte=start_date,
            created_date__lte=end_date).values('google_rep_email').annotate(submitted=Count('sf_lead_id')).order_by('-submitted')
    else:
        topper_list = WPPLeads.objects.exclude(google_rep_email='').filter(
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
    return render(request, 'main/edit_profile_info.html', {'locations': locations, 'managers': managers, 'regions': regions, 'api_key': api_key,
                                                           'all_locations': all_locations, 'region_locations': region_locations, 'teams': teams, 'manager_details': manager_details})


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
    feedback = Feedback.objects.get(id=id)
    normal_comments = FeedbackComment.objects.filter(feedback__id=id)
    resolved_count = FeedbackComment.objects.filter(feedback__id=id, feedback_status='resolved').count()
    can_resolve = True
    if request.user.email == feedback.lead_owner.email:
        can_resolve = False
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
def create_feedback(request, lead_id=None):
    """ Create feed back """
    if request.method == 'POST':
        feedback_details = Feedback()
        feedback_details.user = request.user
        feedback_details.title = request.POST['title']
        feedback_details.cid = request.POST['cid']
        feedback_details.advertiser_name = request.POST['advertiser']
        language = Language.objects.get(id=request.POST['language'])
        feedback_details.language = language.language_name
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
        feedback_details = notify_feedback_activity(request, feedback_details, comment=None)

        if request.POST['code_type'] == 'WPP':
            return redirect('main.views.list_feedback_wpp')
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
    else:
        programs = Team.objects.filter(is_active=True)
        locations = Location.objects.all()
        languages = Language.objects.all()
        return render(request, 'main/feedback_mail/feedback_form.html', {'locations': locations,
                                                                         'programs': programs, 'lead': lead, 'languages': languages,
                                                                         'feedback_type': feedback_type})


def notify_feedback_activity(request, feedback, comment=None, is_resolved=False):
    mail_subject = "Feedback - " + feedback.title
    feedback_url = request.build_absolute_uri(reverse('main.views.view_feedback', kwargs={'id': feedback.id}))
    if feedback.code_type != 'WPP':
        signature = 'Tag Team'
    else:
        signature = 'WPP Team'
    if comment:
        mail_body = get_template('main/feedback_mail/new_comment.html').render(
            Context({
                'feedback': feedback,
                'comment': comment,
                'feedback_url': feedback_url,
                'feedback_owner': request.user.first_name + request.user.last_name,
                'signature': signature
            })
        )
    elif is_resolved:
        mail_body = get_template('main/feedback_mail/resolved.html').render(
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
    else:
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

    # get feedback user manager and lead owner managers information
    bcc = set()

    mail_to = set([
        'g-crew@regalix-inc.com',
        'rwieker@google.com',
        'sabinaa@google.com',
        'vsharan@regalix-inc.com',
        'babla@regalix-inc.com',
        feedback.lead_owner.email,
        request.user.email
    ])

    mail_from = request.user.email

    attachments = list()
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
    comment.comment = request.POST['reopencomment']
    comment.comment_by = request.user
    comment.feedback_status = 'IN PROGRESS'
    comment.created_date = datetime.utcnow()
    comment.save()
    notify_feedback_activity(request, feedback, comment)

    feedback.save()
    return redirect('main.views.view_feedback', id=id)


@login_required
@manager_info_required
def comment_feedback(request, id):
    """ Comment on a feedback """
    action_type = request.POST['feedback_action']
    feedback = Feedback.objects.get(id=id)
    comment = FeedbackComment()
    comment.feedback = feedback
    comment.comment = request.POST['comment']
    comment.comment_by = request.user
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
    else:
        comment.feedback_status = 'IN PROGRESS'
        feedback.status = 'IN PROGRESS'
        comment.save()

    feedback.save()
    if action_type == 'Resolved':
        notify_feedback_activity(request, feedback, comment, is_resolved=True)
    else:
        notify_feedback_activity(request, feedback, comment, is_resolved=False)
    return redirect('main.views.view_feedback', id=id)


def get_contacts(request):
    """ Get team contacts information """
    contact_list = ContectList.objects.filter()
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
    mp4_url = settings.MEDIA_URL + 'TaggingWins_06_18_2015.mp4'
    ogg_url = settings.MEDIA_URL + 'TaggingWins_06_18_2015.ogg'
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
        'dkarthik@regalix-inc.com',
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
    notification = list()
    if 'WPP' not in request.session['groups']:
        notifications = Notification.objects.filter(is_visible=True).order_by('-created_date')
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

        return redirect('main.views.main_home')
    return redirect('main.views.main_home')


def notify_portal_feedback_activity(request, feedback):
    mail_subject = feedback.feedback_type + " Portal Feedback"
    mail_body = get_template('main/portal_feedback/portal_feedback_mail.html').render(
        Context({
            'feedback': feedback,
            'user_info': request.user,
            'type': feedback.feedback_type,
            'feedback_body': feedback.description
        })
    )

    # get feedback user manager and lead owner managers information
    bcc = set([])

    mail_to = set([
        'dkarthik@regalix-inc.com',
        'tkhan@regalix.com',
        'ram@regalix-inc.com',
        'rajuk@regalix-inc.com',
        'sprasad@regalix-inc.com'
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

        rep_email = sheet.cell(r_i, get_col_index(sheet, 'username')).value
        google_rep_email = rep_email + '@google.com'
        google_manager = sheet.cell(r_i, get_col_index(sheet, 'manager')).value
        program = sheet.cell(r_i, get_col_index(sheet, 'program')).value
        google_manager_email = str(google_manager) + '@google.com' if google_manager else ''
        region = sheet.cell(r_i, get_col_index(sheet, 'region')).value
        country = sheet.cell(r_i, get_col_index(sheet, 'market served')).value
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

            try:
                location = Location.objects.get(location_name=country)
                user_details.location_id = location.id
            except ObjectDoesNotExist:
                location = Location(location_name=country, is_active=False)
                location.save()
                new_locations.append(country)
                user_details.location_id = location.id

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
            failed_rec['Region'] = region
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


@csrf_exempt
@login_required
def upload_file_handling(request):
    template_args = dict()
    if request.method == 'POST':
        if request.FILES:
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
            with open(excel_file_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)
                destination.close()

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
                default_headers = ['manager', 'username', 'market served', 'program', 'region']
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


def get_survey_data_from_excel(workbook, sheet, survey_channel):
    implemented_cids = Leads.objects.exclude(lead_sub_status='RR - Inactive').filter(lead_status__in=['Implemented', 'Pending QC - WIN', 'Rework Required']).values_list('customer_id', flat=True).distinct()
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
        survey_date = datetime(survey_date_tuple[0], survey_date_tuple[1], survey_date_tuple[2], survey_date_tuple[3], survey_date_tuple[4], survey_date_tuple[5])
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
        csat_record.category = 'UNMAPPED'
        csat_record.language = sheet.cell(r_i, get_col_index(sheet, 'Language')).value

        if cid in implemented_cids:

            # survey date in ist and date_of_installation in pst but month and year will be the same
            if process == 'TAG':
                csat_lead = Leads.objects.exclude(type_1__in=['Google Shopping Setup', 'Google Shopping Migration']).filter(customer_id=cid, date_of_installation__month=survey_date.month, date_of_installation__year=survey_date.year)
            elif process == 'SHOPPING':
                csat_lead = Leads.objects.filter(customer_id=cid, date_of_installation__month=survey_date.month,
                                                 date_of_installation__year=survey_date.year, type_1__in=['Google Shopping Setup', 'Google Shopping Migration'])

            if csat_lead:
                if len(csat_lead) == 1:
                    csat_record.sf_lead_id = csat_lead[0].sf_lead_id
                    csat_record.region = csat_lead[0].country
                    csat_record.program = csat_lead[0].team
                    csat_record.code_type = csat_lead[0].type_1
                    csat_record.lead_owner = csat_lead[0].lead_owner_email
                    csat_record.language = csat_lead[0].language if csat_lead[0].language else sheet.cell(r_i, get_col_index(sheet, 'Language')).value
                    csat_record.category = 'MAPPED'
                else:
                    # csat_lead should be one but here is mutiple
                    csat_record.category = 'UNMAPPED'
                    # survey_prev_date = survey_date - datetime.timedelta(1)
                    # csat_lead = Leads.objects.filter(customer_id=cid, date_of_installation__gte=survey_prev_date, date_of_installation__lte=survey_date).order_by('-date_of_installation')

                    # us_zone = Location.objects.filter(location_name__in=['United States', 'Canada'])

                    # if csat_lead:
                    #     # Lead's date of installation is in PST,comparing it with pst or pdt timezone to convert ist
                    #     if csat_lead[0].date_of_installation >= us_zone[0].daylight_start and csat_lead[0].date_of_installation <= us_zone[0].daylight_end:
                    #         tz = Timezone.objects.get(zone_name='PDT')
                    #     else:
                    #         tz = Timezone.objects.get(zone_name='PST')
                    #     utc_date = SalesforceApi.get_utc_date(csat_lead[0].date_of_installation, tz.time_value)
                    #     ist_tz = Timezone.objects.get(zone_name='IST')
                    #     date_of_installation_in_ist = SalesforceApi.convert_utc_to_timezone(utc_date, ist_tz.time_value)
                    # else:
                    #     csat_record.sf_lead_id = ''
                    #     csat_record.category = 'UNMAPPED'

        csat_record.customer_id = cid
        csat_record.survey_date = survey_date
        csat_record.process = process
        csat_record.q1 = int(sheet.cell(r_i, get_col_index(sheet, 'Q1')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q1')).value else 0
        if csat_record.q1 == 0:
            csat_record.category = 'UNMAPPED'
        csat_record.q2 = int(sheet.cell(r_i, get_col_index(sheet, 'Q2')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q2')).value else 0
        csat_record.q3 = int(sheet.cell(r_i, get_col_index(sheet, 'Q3')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q3')).value else 0
        csat_record.q4 = int(sheet.cell(r_i, get_col_index(sheet, 'Q4')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q4')).value else 0
        csat_record.q5 = int(sheet.cell(r_i, get_col_index(sheet, 'Q5')).value) if sheet.cell(r_i, get_col_index(sheet, 'Q5')).value else 0

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


def picasso_home(request):
    user_profile = get_user_profile(request.user)
    query = dict()
    picasso_objective_dict =dict()
    start_date, end_date = get_quarter_date_slots(datetime.utcnow())
    current_quarter = ReportService.get_current_quarter(datetime.utcnow())
    title = "Activity Summary for %s - %s to %s %s" % (current_quarter, datetime.strftime(start_date, '%b'), datetime.strftime(end_date, '%b'), datetime.strftime(start_date, '%Y'))
    query['created_date__gte'] = start_date
    query['created_date__lte'] = end_date
    objectives = ['Engage with your Content', 'Become a Fan', 'Buy Online', 'Form Entry', 'Call your Business']
    if request.user.groups.filter(name='SUPERUSER'):
        start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
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
    return render(request, 'main/picasso_index.html', {'picasso': True, 'user_profile': user_profile,
                                                                        'title': title,
                                                                        'picasso_lead_status': picasso_lead_status,
                                                                        'picasso_objective_dict': picasso_objective_dict,
                                                                        'picasso_objective_total': picasso_objective_total,
                                                                        'picasso_top_performer': picasso_top_performer})
