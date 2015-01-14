from json import dumps, loads
from datetime import datetime, timedelta, date
import time
import os
import operator

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

from main.models import UserDetails, Feedback, FeedbackComment, CustomerTestimonials, ContectList
from leads.models import Location, Leads, Team
from django.db.models import Count
from lib.helpers import (get_week_start_end_days, first_day_of_month, get_user_profile,
                         last_day_of_month, previous_quarter, get_count_of_each_lead_status_by_rep)
from django.http import Http404

from forum.models import *
from django.utils.html import strip_tags


def home(request):
    """ Application landing view """
    # check if user logged in
    if not request.user.is_authenticated():
        return redirect('auth.views.user_login')

    return redirect('main.views.main_home')


@manager_info_required
def main_home(request):
    """ Google Portal Home/Index Page """
    user_profile = get_user_profile(request.user)
    # Get Lead status count by current user
    lead_status_dict = get_count_of_each_lead_status_by_rep(request.user.email, start_date=None, end_date=None)
    customer_testimonials = CustomerTestimonials.objects.all().order_by('-created_date')

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

    # List all Locations/Country
    locations = Location.objects.all()

    # feedback summary
    feedback_list = dict()
    feedbacks = Feedback.objects.filter(
        Q(user__email=request.user.email)
        | Q(user__profile__user_manager_email=request.user.email)
        | Q(lead_owner__email=request.user.email)
        | Q(lead_owner__profile__user_manager_email=request.user.email)
    ).order_by('-created_date')[:3]
    feedbacks_new = Feedback.objects.filter(Q(user__email=request.user.email) | Q(user__profile__user_manager_email=request.user.email)
                                            | Q(lead_owner__email=request.user.email)
                                            | Q(lead_owner__profile__user_manager_email=request.user.email)
                                            )
    feedbacks_new = feedbacks_new.filter(status='NEW').count()
    feedbacks_in_progress = Feedback.objects.filter(Q(user__email=request.user.email) | Q(user__profile__user_manager_email=request.user.email)
                                            | Q(lead_owner__email=request.user.email)
                                            | Q(lead_owner__profile__user_manager_email=request.user.email)
                                            )

    feedbacks_in_progress = feedbacks_in_progress.filter(status='IN PROGRESS').count()
    feedbacks_resolved = Feedback.objects.filter(Q(user__email=request.user.email) | Q(user__profile__user_manager_email=request.user.email)
                                            | Q(lead_owner__email=request.user.email)
                                            | Q(lead_owner__profile__user_manager_email=request.user.email)
                                            )
    feedbacks_resolved = feedbacks_resolved.filter(status='RESOLVED').count()
    feedback_list['feedbacks_new'] = feedbacks_new
    feedback_list['feedbacks_in_progress'] = feedbacks_in_progress
    feedback_list['feedbacks_resolved'] = feedbacks_resolved

    return render(request, 'main/index.html', {'customer_testimonials': customer_testimonials, 'lead_status_dict': lead_status_dict,
                                               'user_profile': user_profile, 'question_list': question_list, 'locations': locations,
                                               'feedback_list': feedback_list, 'feedbacks': feedbacks})


@login_required
def add_manager_info(request):
    """ Add manager information for new user """
    if request.method == 'POST':
        try:
            user_details = UserDetails.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            user_details = UserDetails()
            user_details.user = request.user

        user_details.user_manager_name = request.POST.get('user_manager_name', None)
        user_details.user_manager_email = request.POST.get('user_manager_email', None)
        user_details.save()
        return redirect('main.views.home')
    return render(request, 'main/add_manager_info.html')


@login_required
@manager_info_required
def team(request):
    return render(request, 'main/team.html')


@login_required
@manager_info_required
def view_feedback(request, id):
    """ Detail view of a feedback """
    comments = list()
    try:
        feedback = Feedback.objects.get(id=id)
        comments = FeedbackComment.objects.filter(feedback__id=id)
    except ObjectDoesNotExist:
        feedback = None

    can_resolve = True
    if request.user.email == feedback.lead_owner.email:
        can_resolve = False
    return render(request, 'main/view_feedback.html', {'feedback': feedback,
                                                       'comments': comments,
                                                       'can_resolve': can_resolve,
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
    return render(request, 'main/list_feedback.html', {'feedbacks': feedbacks,
                                                       'media_url': settings.MEDIA_URL + 'feedback/'})


@login_required
@manager_info_required
def create_feedback(request, lead_id=None):
    """ Create feed back """
    locations = Location.objects.all()
    programs = Team.objects.all()
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

        feedback_details.language = request.POST['language']
        feedback_location = Location.objects.get(location_name=request.POST['location'])
        feedback_details.location = feedback_location

        feedback_details.feedback_type = request.POST['type']
        feedback_details.description = request.POST['description']
        feedback_details.program_id = request.POST['program']

        try:
            # if lead owner not exist, assign lead to default user
            lead_owner = User.objects.get(email=request.POST['lead_owner'])
            feedback_details.lead_owner = lead_owner
        except ObjectDoesNotExist:
            pass
        if request.FILES:
            feedback_details.attachment = request.FILES['attachment_name']

        feedback_details.save()
        # feedback_details = notify_feedback_activity(request, feedback_details)

        return redirect('main.views.list_feedback')
    return render(request, 'main/feedback_mail/feedback_form.html', {'locations': locations, 'programs': programs, 'lead': lead})


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
