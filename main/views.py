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
from lib.helpers import (get_week_start_end_days, first_day_of_month, last_day_of_month, previous_quarter)
from django.http import Http404

from forum.models import *
from forum.views.readers import question_list
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


def home(request):
    """ Application landing view """
    # check if user logged in
    if not request.user.is_authenticated():
        return redirect('auth.views.user_login')

    return redirect('main.views.main_home')


@manager_info_required
def main_home(request):
    """ Google Portal Home/Index Page """
    feed_url = mark_safe(request.path + "?type=rss&q=" + "mostvoted")

    questions_list = question_list(request, Question.objects.all(), None, None, None, None, feed_url=feed_url)
    for q in questions_list:
        print q

    return render(request, 'main/index.html', {'questions': questions_list})


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