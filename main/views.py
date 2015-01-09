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
from leads.models import Location, Leads
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

    return render(request, 'main/index.html', {'customer_testimonials': customer_testimonials, 'lead_status_dict': lead_status_dict,
                                               'user_profile': user_profile, 'question_list': question_list, 'locations': locations})


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
