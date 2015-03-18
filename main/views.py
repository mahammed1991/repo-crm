from json import dumps, loads
from datetime import datetime, timedelta, date
import time
import os
import operator
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from requests import request as request_call
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse
from forum.models import *
from django.contrib.auth.models import User

from django.conf import settings

from lib.helpers import send_mail, manager_info_required

from main.models import (UserDetails, Feedback, FeedbackComment, CustomerTestimonials, ContectList,
                         Notification, PortalFeedback)
from leads.models import Location, Leads, Team, Language
from django.db.models import Count
from lib.helpers import (get_week_start_end_days, first_day_of_month, get_user_profile, get_quarter_date_slots,
                         last_day_of_month, previous_quarter, get_count_of_each_lead_status_by_rep,
                         is_manager, get_user_list_by_manager, get_user_under_manager, date_range_by_quarter,
                         get_previous_month_start_end_days)
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from xlrd import open_workbook, XL_CELL_DATE, xldate_as_tuple
from django.utils.html import strip_tags
from reports.report_services import ReportService
from reports.models import Region


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
    lead_status = settings.LEAD_STATUS
    if request.user.groups.filter(name='SUPERUSER'):
        # start_date, end_date = date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))
        start_date, end_date = get_previous_month_start_end_days(datetime.utcnow())
        end_date = datetime.utcnow()
        lead_status_dict = {'total_leads': 0,
                            'implemented': 0,
                            'in_progress': 0,
                            'attempting_contact': 0,
                            'in_queue': 0,
                            'in_active': 0,
                            'in_progress': 0,
                            }
        lead_status_dict['total_leads'] = Leads.objects.filter(
            lead_status__in=lead_status, created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['implemented'] = Leads.objects.filter(
            lead_status__in=settings.LEAD_STATUS_DICT['Implemented'], created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['in_progress'] = Leads.objects.filter(
            lead_status__in=settings.LEAD_STATUS_DICT['In Progress'], created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['attempting_contact'] = Leads.objects.filter(
            lead_status__in=settings.LEAD_STATUS_DICT['Attempting Contact'], created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['in_queue'] = Leads.objects.filter(
            lead_status__in=settings.LEAD_STATUS_DICT['In Queue'], created_date__gte=start_date, created_date__lte=end_date).count()
        lead_status_dict['in_active'] = Leads.objects.filter(
            lead_status__in=settings.LEAD_STATUS_DICT['In Active'], created_date__gte=start_date, created_date__lte=end_date).count()
    else:
        # 1. Current User/Rep LEADS SUMMARY
        # Get Lead status count by current user
        lead_status_dict = get_count_of_each_lead_status_by_rep(request.user.email, start_date=None, end_date=None)

    # Customer Testimonials
    customer_testimonials = CustomerTestimonials.objects.all().order_by('-created_date')

    # Q&A Forum
    # Get Top 3 Q&A by most voted
    questions_by_voted = Node.objects.filter(node_type='question').order_by('-score')[:3]
    question_list = list()
    for q in questions_by_voted:
        question = dict()
        question['votes'] = q.score
        question['views'] = q.extra_count
        answer_count = Node.objects.filter(node_type='answer', parent_id=q.id, abs_parent_id=q.id).count()
        question['answer'] = answer_count
        question['author_id'] = q.last_activity_by_id
        user = User.objects.get(id=q.last_activity_by_id)
        question['author_name'] = user.username
        question['title'] = q.title
        question['body'] = strip_tags(q.body)
        question['last_activity_at'] = q.last_activity_at
        question_list.append(question)

    # Leads Current Quarter Summary
    # Get Leads report for Current Quarter Summary
    # by default should be current Quarter
    start_date, end_date = get_quarter_date_slots(datetime.utcnow())
    current_quarter = ReportService.get_current_quarter(datetime.utcnow())
    title = "Activity Summary for %s - %s to %s %s" % (current_quarter, datetime.strftime(start_date, '%b'), datetime.strftime(end_date, '%b'), datetime.strftime(start_date, '%Y'))
    report_summary = dict()

    total_leads = len(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date))
    implemented_leads = len(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date, lead_status='Implemented'))
    report_summary.update({'total_leads': total_leads,
                           'implemented_leads': implemented_leads,
                           'total_win': ReportService.get_conversion_ratio(implemented_leads, total_leads)})

    total_tag_leads = len(Leads.objects.exclude(type_1__in=['Google Shopping Migration',
                                                            'Google Shopping Setup']).filter(created_date__gte=start_date,
                                                                                             created_date__lte=end_date))
    implemented_tag_leads = len(Leads.objects.exclude(type_1__in=['Google Shopping Migration',
                                                                  'Google Shopping Setup']).filter(created_date__gte=start_date,
                                                                                                   created_date__lte=end_date,
                                                                                                   lead_status='Implemented'))
    report_summary.update({'total_tag_leads': total_tag_leads,
                           'implemented_tag_leads': implemented_tag_leads,
                           'tag_win': ReportService.get_conversion_ratio(implemented_tag_leads, total_tag_leads)})

    total_shopping_leads = len(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date, type_1='Google Shopping Setup'))
    implemented_shopping_leads = len(Leads.objects.filter(created_date__gte=start_date,
                                                          created_date__lte=end_date, lead_status='Implemented',
                                                          type_1='Google Shopping Setup'))

    report_summary.update({'total_shopping_leads': total_shopping_leads,
                           'implemented_shopping_leads': implemented_shopping_leads,
                           'shopping_win': ReportService.get_conversion_ratio(implemented_shopping_leads, total_shopping_leads)})

    # Top Lead Submitter by LAST QUARTER, LAST MONTH and LAST WEEK
    current_date = datetime.utcnow()
    top_performer = get_top_performer_list(current_date)

    # feedback summary
    feedback_list = dict()
    feedbacks = Feedback.objects.filter(
        Q(user__email=request.user.email)
        | Q(user__profile__user_manager_email=request.user.email)
        | Q(lead_owner__email=request.user.email)
        | Q(lead_owner__profile__user_manager_email=request.user.email)
    )
    feedback_list['new'] = feedbacks.filter(status='NEW').count()
    feedback_list['in_progress'] = feedbacks.filter(status='IN PROGRESS').count()
    feedback_list['resolved'] = feedbacks.filter(status='RESOLVED').count()
    feedback_list['total'] = feedbacks.count()

    # Notification Section
    notifications = Notification.objects.filter(is_visible=True)

    # feedback summary end here
    return render(request, 'main/index.html', {'customer_testimonials': customer_testimonials, 'lead_status_dict': lead_status_dict,
                                               'user_profile': user_profile, 'question_list': question_list,
                                               'top_performer': top_performer, 'report_summary': report_summary, 'title': title,
                                               'feedback_list': feedback_list, 'notifications': notifications})


def get_top_performer_list(current_date):
    top_performer_list = {'weekly': [], 'monthly': [], 'quarterly': []}

    # Get Top 3 performers by previous week of current week
    prev_week = int(time.strftime("%W"))
    start_date, end_date = get_week_start_end_days(current_date.year, prev_week)
    top_performer_list['weekly'] = get_top_performer_by_date_range(start_date, end_date)

    # Get Top 3 performers by previous month of current month
    prev_month = date.today().replace(day=1) - timedelta(days=1)
    start_date = first_day_of_month(prev_month)
    end_date = last_day_of_month(prev_month)
    top_performer_list['monthly'] = get_top_performer_by_date_range(start_date, end_date)

    # Get Top 3 performers by previous quarter of current quarter
    prev_quarter = previous_quarter(current_date)
    start_date = datetime(prev_quarter.year, prev_quarter.month - 2, 1)
    end_date = prev_quarter
    top_performer_list['quarterly'] = get_top_performer_by_date_range(start_date, end_date)
    return top_performer_list


def top_30_cms(request):
    """ Get top 30 CMS """
    return render(request, 'main/top_30_cms.html')


def get_top_performer_by_date_range(start_date, end_date):
    topper_list = Leads.objects.exclude(google_rep_email='').filter(
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
                last_lead_submitted = Leads.objects.filter(google_rep_email=email,
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
    teams = Team.objects.filter(is_active=True)
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
    teams = Team.objects.filter(is_active=True)
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
def team(request):
    contacts_list = get_contacts(request)
    return render(request, 'main/team.html', {'contacts_list': contacts_list})


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
def list_feedback(request):
    """ List all feedbacks """

    feedbacks = Feedback.objects.filter(
        Q(user__email=request.user.email)
        | Q(user__profile__user_manager_email=request.user.email)
        | Q(lead_owner__email=request.user.email)
        | Q(lead_owner__profile__user_manager_email=request.user.email)
    )
    feedback_list = dict()
    feedback_list['new'] = feedbacks.filter(status='NEW').count()
    feedback_list['in_progress'] = feedbacks.filter(status='IN PROGRESS').count()
    feedback_list['resolved'] = feedbacks.filter(status='RESOLVED').count()
    feedback_list['total'] = feedbacks.count()

    return render(request, 'main/list_feedback.html', {'feedbacks': feedbacks,
                                                       'media_url': settings.MEDIA_URL + 'feedback/',
                                                       'feedback_list': feedback_list,
                                                       })


@login_required
@manager_info_required
def create_feedback(request, lead_id=None):
    """ Create feed back """
    locations = Location.objects.filter(is_active=True)
    programs = Team.objects.filter(is_active=True)
    languages = Language.objects.all()
    lead = None
    if lead_id:
        try:
            lead = Leads.objects.get(id=lead_id)
        except Leads.ObjectDoesNotExist:
            lead = None

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

        feedback_details.feedback_type = request.POST['type']
        feedback_details.description = request.POST['description']
        feedback_details.program_id = request.POST['program']

        try:
            # if lead owner not exist, assign lead to default user
            lead_owner = User.objects.get(email=request.POST['lead_owner'])
            feedback_details.lead_owner = lead_owner
            google_account_manager = User.objects.get(email=request.POST['google_acManager_name'])
            feedback_details.google_account_manager = google_account_manager
        except ObjectDoesNotExist:
            pass
        if request.FILES:
            feedback_details.attachment = request.FILES['attachment_name']

        feedback_details.save()
        # feedback_details = notify_feedback_activity(request, comment=None, feedback_details)

        return redirect('main.views.list_feedback')
    return render(request, 'main/feedback_mail/feedback_form.html', {'locations': locations,
                                                                     'programs': programs, 'lead': lead, 'languages': languages})


def notify_feedback_activity(request, feedback, comment=None, is_resolved=False):
    mail_subject = "Feedback - " + feedback.title
    feedback_url = request.build_absolute_uri(reverse('main.views.view_feedback', kwargs={'id': feedback.id}))
    if comment:
        mail_body = get_template('main/feedback_mail/new_comment.html').render(
            Context({
                'feedback': feedback,
                'comment': comment,
                'feedback_url': feedback_url,
                'feedback_owner': request.user.first_name + request.user.last_name
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
                'feedback_body': feedback.description
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
                'feedback_body': feedback.description
            })
        )

    # get feedback user manager and lead owner managers information
    bcc = set()

    mail_to = set([
        feedback.lead_owner.email,
        feedback.user.email
    ])

    try:
        mail_to.add(feedback.user.profile.user_manager_email)
        mail_to.add(feedback.lead_owner.profile.user_manager_email)
    except:
        pass

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
        lead = Leads.objects.get(id=lead_id)

        feedback_details = Feedback()
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
        try:
            # if lead owner not exist, assign lead to default user
            lead_owner = User.objects.get(email=lead.lead_owner_email)
            feedback_details.lead_owner = lead_owner
            google_account_manager = User.objects.get(email=lead.google_rep_email)
            feedback_details.google_account_manager = google_account_manager
        except ObjectDoesNotExist:
            pass

        feedback_details.save()
        # feedback_details = notify_feedback_activity(request, feedback_details)

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
    # notify_feedback_activity(request, feedback, comment)

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
        comment.save()
    # comment.created_date = datetime.utcnow()
    feedback.save()
    # if action_type == 'Resolved':
    #     # notify_feedback_activity(request, feedback, comment, is_resolved=True)
    # else:
    #     notify_feedback_activity(request, feedback, comment, is_resolved=False)
    return redirect('main.views.view_feedback', id=id)


def get_contacts(request):
    """ Get team contacts information """
    contact_list = ContectList.objects.filter()
    contacts = {'management': list(),
                'representatives': list()
                }
    groups = dict()
    for cnt in contact_list:
        contact = dict()
        contact['name'] = "%s %s" % (cnt.first_name, cnt.last_name)
        contact['email'] = cnt.email
        contact['phone'] = cnt.phone_number
        contact['skype'] = cnt.skype_id
        contact['picture'] = cnt.profile_photo.name.split('/')[-1]
        contact['photo_url'] = get_profile_avatar_by_email(cnt.email)
        contact['position_type'] = cnt.position_type
        if cnt.position_type == 'MGMT':
            contacts['management'].append(contact)
        else:
            if cnt.position_type not in groups:
                groups[cnt.position_type] = [contact]
            else:
                groups[cnt.position_type].append(contact)

    contacts['representatives'].append(groups)
    return contacts


def get_profile_avatar_by_email(email):
    """ Get Profile Avatar """

    avatar_url = 'images/avtar-big.jpg'
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
    except ObjectDoesNotExist:
        if email:
            username = email.split('@')[0]
            os_path = settings.STATIC_FOLDER + '/images/GTeam/' + username
            # Check if profile picture exist
            if os.path.isfile(os_path + '.png') or os.path.isfile(os_path + '.png.gz'):
                avatar_url = 'images/GTeam/' + username + '.png'
    return avatar_url


@login_required
def resources(request):
    return render(request, 'main/resources.html')


@login_required
def get_inbound_locations(request):
    """ Get all In-Bound Locations """
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

    location.append({'id': '0', "name": 'US', 'phone': '8669997725', 'url': '/static/images/US-flag.png'})
    if request.user.profile.location:
        user_loc = {'loc_name': request.user.profile.location.location_name,
                    'loc_id': request.user.profile.location.id,
                    'loc_phone': request.user.profile.location.phone,
                    'loc_flag': settings.MEDIA_URL + '' + request.user.profile.location.flag_image.name if request.user.profile.location.flag_image else "",
                    }
    else:
        user_loc = {'loc_name': '',
                    'loc_id': '',
                    'loc_phone': '',
                    'loc_flag': ''}

    return HttpResponse(dumps({'location': location, 'user_loc': user_loc}), content_type='application/json')


@login_required
def sales_tasks(request):
    """ Sales Tasks Page """

    return render(request, 'main/sales_tasks.html')


@login_required
def get_notifications(request):
    """ Get all Notifications """
    # Notifications list
    notifications = Notification.objects.filter(is_visible=True).order_by('-created_date')
    notification = list()
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


@login_required
def master_data_upload(request):
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
                return render(request, 'main/master_upload.html', template_args)

            file_name = 'master_data.xls'
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
    return render(request, 'main/master_upload.html', template_args)


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

    for r_i in range(1, sheet.nrows):
        rep_email = sheet.cell(r_i, get_col_index(sheet, 'Google Account Manager ldap (Google Rep)')).value
        google_rep_email = rep_email + '@google.com'
        google_manager = sheet.cell(r_i, get_col_index(sheet, 'Google Manager')).value
        program = sheet.cell(r_i, get_col_index(sheet, 'Program')).value
        #rep_name = sheet.cell(r_i, get_col_index(sheet, 'Google Account Manager Name (Google Rep)')).value
        #r_quarter = sheet.cell(r_i, get_col_index(sheet, 'r.quarter')).value
        #market = sheet.cell(r_i, get_col_index(sheet, 'Market')).value
        #rep_location = sheet.cell(r_i, get_col_index(sheet, 'Rep Location')).value
        google_manager_email = str(google_manager) + '@google.com'
        region = sheet.cell(r_i, get_col_index(sheet, 'Region')).value
        country = sheet.cell(r_i, get_col_index(sheet, 'Country')).value
        try:
            user = User.objects.get(email=google_rep_email)
            user_details = UserDetails.objects.get(user_id=user.id)
            user_details.user_manager_email = google_manager_email
            user_details.user_manager_name = user_dict.get(google_manager_email, '')
            try:
                program = Team.objects.get(team_name=program)
                user_details.team_id = program.id
            except ObjectDoesNotExist:
                program = Team(team_name=program)
                program.save()
                user_details.team_id = program.id

            try:
                region = Region.objects.get(name=region)
                user_details.region_id = region.id
            except ObjectDoesNotExist:
                region = Region(name=region)
                region.save()
                user_details.region_id = region.id

            try:
                location = Location.objects.get(location_name=country)
                user_details.location_id = location.id
            except ObjectDoesNotExist:
                location = Location(location_name=country)
                location.save()
                user_details.location_id = location.id

            user_details.save()

        except ObjectDoesNotExist:
            continue

    return redirect('main.views.master_data_upload')

 
def get_col_index(sheet, col_name):
    for col_index in range(sheet.ncols):
        col_val = sheet.cell(0, col_index).value
        if col_name == col_val:
            return col_index
