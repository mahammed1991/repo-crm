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
from django.contrib.auth.models import User

from django.conf import settings

from lib.helpers import send_mail, manager_info_required

from main.models import UserDetails, Feedback, FeedbackComment, CustomerTestimonials, ContectList, Notification
from leads.models import Location, Leads, Team, Language
from django.db.models import Count
from lib.helpers import (get_week_start_end_days, first_day_of_month, get_user_profile, get_quarter_date_slots,
                         last_day_of_month, previous_quarter, get_count_of_each_lead_status_by_rep,
                         is_manager, get_user_list_by_manager, get_user_under_manager)
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from forum.models import *
from django.utils.html import strip_tags
from reports.report_services import ReportService


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
    title = "Leads %s Summary - %s to %s %s" % (current_quarter, datetime.strftime(start_date, '%b'), datetime.strftime(end_date, '%b'), datetime.strftime(start_date, '%Y'))
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

    # feedback summary end here
    return render(request, 'main/index.html', {'customer_testimonials': customer_testimonials, 'lead_status_dict': lead_status_dict,
                                               'user_profile': user_profile, 'question_list': question_list,
                                               'top_performer': top_performer, 'report_summary': report_summary, 'title': title,
                                               'feedback_list': feedback_list})


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


def get_top_performer_by_date_range(start_date, end_date):
    topper_list = Leads.objects.exclude(lead_owner_email='').filter(
        created_date__gte=start_date,
        created_date__lte=end_date).values('lead_owner_email').annotate(submitted=Count('sf_lead_id')).order_by('-submitted')

    toppers = dict()
    indx = 0
    topper_limit = 3
    for topper in topper_list:
        indx = indx + 1
        key = topper['submitted']

        if indx > topper_limit:
            if topper['submitted'] in toppers:
                toppers[key].append(topper['lead_owner_email'])
            else:
                break
        elif key not in toppers:
            toppers[key] = [topper['lead_owner_email']]
        else:
            toppers[key].append(topper['lead_owner_email'])

    # Get toppers from the list
    topper_email = list()
    for k in sorted(toppers.keys(), reverse=True):
        if len(toppers[k]) == 1:
            topper_email.append(toppers[k][0])
        else:
            top_list = list()
            for email in toppers[k]:
                latest_lead = dict()
                last_lead_submitted = Leads.objects.filter(lead_owner_email=email,
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
    locations = Location.objects.all()
    teams = Team.objects.all()
    if request.method == 'POST':
        try:
            user_details = UserDetails.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            user_details = UserDetails()
            user_details.user = request.user

        user_details.team_id = request.POST.get('user_team', None)
        user_details.user_manager_name = request.POST.get('user_manager_name', None)
        user_details.user_manager_email = request.POST.get('user_manager_email', None)
        user_details.location_id = request.POST.get('user_location', None)
        user_details.save()
        # return redirect('main.views.home')
    return render(request, 'main/edit_profile_info.html', {'locations': locations, 'teams': teams})


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
    first_resolved_comments = list()
    second_resolved_comments = list()

    try:
        feedback = Feedback.objects.get(id=id)
        if feedback.resolved_date:
            normal_comments = FeedbackComment.objects.filter(feedback__id=id, created_date__lte=feedback.resolved_date)
            if feedback.second_resolved_date:
                second_resolved_exist = True
                first_resolved_comments = FeedbackComment.objects.filter(feedback__id=id,
                                                                         created_date__gt=feedback.resolved_date,
                                                                         created_date__lte=feedback.second_resolved_date)
            else:
                first_resolved_comments = FeedbackComment.objects.filter(feedback__id=id, created_date__gte=feedback.resolved_date)
                second_resolved_exist = False

            if second_resolved_exist:
                if feedback.third_resolved_date:
                    second_resolved_comments = FeedbackComment.objects.filter(feedback__id=id,
                                                                              created_date__gte=feedback.second_resolved_date,
                                                                              created_date__lte=feedback.third_resolved_date)
                else:
                    second_resolved_comments = FeedbackComment.objects.filter(feedback__id=id, created_date__gt=feedback.second_resolved_date)
        else:
            normal_comments = FeedbackComment.objects.filter(feedback__id=id)
    except ObjectDoesNotExist:
        feedback = None

    can_resolve = True
    if request.user.email == feedback.lead_owner.email:
        can_resolve = False
    return render(request, 'main/view_feedback.html', {'feedback': feedback,
                                                       'comments': normal_comments,
                                                       'first_resolved_comments': first_resolved_comments,
                                                       'second_resolved_comments': second_resolved_comments,
                                                       'can_resolve': can_resolve,
                                                       'media_url': settings.MEDIA_URL + 'feedback/'})


@login_required
@manager_info_required
def list_feedback(request):
    """ List all feedbacks """
    manager_is = is_manager(request.user.email)
    feedback_type = 'TeamFeedback'
    if request.method == 'POST':
        user_list = get_user_under_manager(request.user.email)
        email_list = list()
        if request.POST['feedback_type'] == 'IndividualFeedback':
            feedback_type = request.POST['feedback_type']
            email_list.append(request.user.email)
            feedbacks = Feedback.objects.filter(user__email__in=email_list)
        else:
            feedback_type = request.POST['feedback_type']
            userids = request.POST['userids']
            email_list = get_user_list_by_manager(request.user.email)
            feedbacks = Feedback.objects.filter(user__id__in=userids)
    else:
        user_list = list()
        if is_manager(request.user.email):
            user_list = get_user_under_manager(request.user.email)

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
                                                       'feedback_list': feedback_list, 'is_manager': manager_is,
                                                       'rep_list': user_list, 'feedback_type': feedback_type})


@login_required
@manager_info_required
def create_feedback(request, lead_id=None):
    """ Create feed back """
    locations = Location.objects.all()
    programs = Team.objects.all()
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
        # feedback_details = notify_feedback_activity(request, feedback_details)

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
                'feedback_url': feedback_url
            })
        )
    elif is_resolved:
        mail_body = get_template('main/feedback_mail/resolved.html').render(
            Context({
                'feedback': feedback,
                'user_info': request.user,
                'feedback_url': feedback_url
            })
        )
    else:
        mail_body = get_template('main/feedback_mail/new_feedback.html').render(
            Context({
                'feedback': feedback,
                'feedback_url': feedback_url
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
        team = Team.objects.get(team_name=lead.team)
        feedback_details.program_id = team.id
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
        feedback_details = notify_feedback_activity(request, feedback_details)

        # return 'SUCCESS'
        return HttpResponse(json.dumps('SUCCESS'))


@login_required
@manager_info_required
def resolve_feedback(request, id):
    feedback = Feedback.objects.get(id=id)
    feedback.status = 'RESOLVED'
    if feedback.resolved_count == 0:
        feedback.resolved_count += 1
        feedback.resolved_by = request.user
        feedback.resolved_date = datetime.utcnow()
    elif feedback.resolved_count == 1:
        feedback.resolved_count += 1
        feedback.second_resolved_by = request.user
        feedback.second_resolved_date = datetime.utcnow()
    elif feedback.resolved_count == 2:
        feedback.resolved_count += 1
        feedback.third_resolved_by = request.user
        feedback.third_resolved_date = datetime.now()
    # notify_feedback_activity(request, feedback, is_resolved=True)
    feedback.save()
    return redirect('main.views.view_feedback', id=id)


@login_required
@manager_info_required
def reopen_feedback(request, id):
    feedback = Feedback.objects.get(id=id)
    feedback.status = 'IN PROGRESS'
    comment = FeedbackComment()
    comment.feedback = feedback
    comment.comment = request.POST['reopencomment']
    comment.comment_by = request.user
    comment.created_date = datetime.utcnow()
    comment.save()
    # notify_feedback_activity(request, feedback, is_resolved=True)

    feedback.save()
    return redirect('main.views.view_feedback', id=id)


@login_required
@manager_info_required
def comment_feedback(request, id):
    """ Comment on a feedback """
    feedback = Feedback.objects.get(id=id)

    comment = FeedbackComment()
    comment.feedback = feedback
    comment.comment = request.POST['comment']
    comment.comment_by = request.user
    # comment.created_date = datetime.utcnow()
    comment.save()

    feedback.status = 'IN PROGRESS'

    # notify_feedback_activity(request, feedback, comment)
    feedback.save()

    return redirect('main.views.view_feedback', id=id)


def get_contacts(request):
    """ Get team contacts information """
    contact_list = ContectList.objects.filter()
    contacts = {'management': list(),
                'representatives': list()
                }
    for cnt in contact_list:
        contact = dict()
        contact['name'] = "%s %s" % (cnt.first_name, cnt.last_name)
        contact['email'] = cnt.email
        contact['phone'] = cnt.phone_number
        contact['skype'] = cnt.skype_id
        contact['picture'] = cnt.profile_photo.name.split('/')[-1]
        contact['photo_url'] = get_profile_avatar_by_email(cnt.email)
        if cnt.position_type == 'MGMT':
            contacts['management'].append(contact)
        else:
            contacts['representatives'].append(contact)
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
    locations = Location.objects.exclude(phone__isnull=True).filter()
    location = list()
    for loc in locations:
        loc_dict = dict()
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
        user_loc = {'loc_name': '',
                    'loc_id': '',
                    'loc_phone': '',
                    'loc_flag': ''}

    return HttpResponse(dumps({'location': location, 'user_loc': user_loc}), content_type='application/json')


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
