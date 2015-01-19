"""
common helper function for project goes here
"""
from datetime import datetime, timedelta, date
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from functools import wraps
import calendar
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from collections import defaultdict


from main.models import UserDetails
from leads.models import Leads


def send_mail(subject, body, mail_from, to, bcc, attachments, template_added=False):
    email = EmailMultiAlternatives(subject, body, mail_from, to, bcc)
    if template_added:
        email.attach_alternative(body, "text/html")

    for attachment in attachments:
        email.attach(
            attachment.name,
            attachment.read()
        )

    email.send()


def get_quarter_date_slots(input_date):
    # calculate quarter start date form given date
    q_st_day = 1
    q_st_month = input_date.month
    q_st_year = input_date.year

    if q_st_month < 4:
        q_st_month = 1
    elif q_st_month < 7:
        q_st_month = 4
    elif q_st_month < 10:
        q_st_month = 7
    else:
        q_st_month = 10

    # calculate quarter end date till last second of the day
    next_q_year = q_st_year
    next_q_month = q_st_month + 3
    if next_q_month > 12:
        next_q_month = 1
        next_q_year += 1

    quarter_start_date = datetime(q_st_year, q_st_month, q_st_day)
    quarter_end_date = datetime(next_q_year, next_q_month, q_st_day) - timedelta(seconds=1)

    return quarter_start_date, quarter_end_date


def google_user(func):
    def _decorator(request, *args, **kwargs):
        # maybe do something before the view_func call
        # provide feedback create access to only google users
        if request.user.email.endswith(settings.ADMIN_DOMAIN):
            redirect_url = request.META.get('HTTP_REFERRER')
            if not redirect_url:
                redirect_url = 'main.views.home'
            return redirect(redirect_url)
        response = func(request, *args, **kwargs)
        # maybe do something after the view_func call
        return response
    return wraps(func)(_decorator)


def manager_info_required(func):
    def _decorator(request, *args, **kwargs):
        try:
            # check if user has manager information filled in
            # otherwise redirect to add/edit manager info section
            user_details = UserDetails.objects.get(user_id=request.user.id)
            if not user_details.user_manager_name or not user_details.user_manager_email:
                return redirect('main.views.edit_profile_info')
        except ObjectDoesNotExist:
            return redirect('main.views.edit_profile_info')

        response = func(request, *args, **kwargs)
        # maybe do something after the view_func call
        return response
    return wraps(func)(_decorator)


def first_day_of_month(d):
    ''' returns first day of the month '''
    return date(d.year, d.month, 1)


def last_day_of_month(d):
    ''' returns last day of the month '''

    year = int(datetime.strftime(d, "%Y"))
    month = int(datetime.strftime(d, "%m"))
    end_day = date(year, month, list(calendar.monthrange(year, month))[1])
    return end_day


def get_week_start_end_days(year, week):
    d = date(year, 1, 1)
    d = d - timedelta(d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)


def date_range_by_quarter(quarter):
    date_now = datetime.utcnow()
    q_st_year = date_now.year
    if quarter == 'Q1':
        q1 = datetime(q_st_year, 1, 1)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(q1)
    elif quarter == 'Q2':
        q2 = datetime(q_st_year, 4, 1)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(q2)
    elif quarter == 'Q3':
        q3 = datetime(q_st_year, 7, 1)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(q3)
    else:
        q4 = datetime(q_st_year, 10, 1)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(q4)

    return quarter_start_date, quarter_end_date


def date_by_month_name(month, year=None):
    if not year:
        date_now = datetime.utcnow()
        year = date_now.year
    formate = "%s %s" % (month, year)
    return datetime.strptime(formate, "%m %Y")


def get_weeks_by_year(year):
    weeks = list()
    for week in range(1, 53):
        start_date, end_date = get_week_start_end_days(year, week)
        s_month = start_date.strftime("%b")
        e_month = end_date.strftime("%b")
        if s_month == e_month:
            week = "W%s (%s %s-%s)" % (week, s_month, start_date.day, end_date.day)
        else:
            week = "W%s (%s %s- %s %s)" % (week, s_month, start_date.day, e_month, end_date.day)
        weeks.append(week)
    return weeks


def get_weeks_in_quarter_to_date():
    ''' Gives the weeks in quarter to date'''
    qtr_start, qtr_end = get_quarter_date_slots(datetime.utcnow())
    qtr_week_star = qtr_start.isocalendar()[1]
    qtr_week_end = qtr_end.isocalendar()[1]
    qtr_week_cur = datetime.utcnow().isocalendar()[1]
    week_dates = []
    if qtr_week_cur < 8:
        week_range = range(qtr_week_star, qtr_week_cur + 1)
    else:
        week_range = range(qtr_week_star + (qtr_week_end - 6), qtr_week_end + 1)
    for week in week_range:
        start_date, end_date = get_week_start_end_days(datetime.utcnow().year, week)
        week_dates.append((start_date, end_date))
    return week_dates


def dsum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


def previous_quarter(ref):
    if ref.month < 4:
        return date(ref.year - 1, 12, 31)
    elif ref.month < 7:
        return date(ref.year, 3, 31)
    elif ref.month < 10:
        return date(ref.year, 6, 30)
    return date(ref.year, 9, 30)


def get_previous_month_start_end_days(d):
    """ Start Date and End date of Previous Month """
    if d.month == 1:
        start_date = date(d.year - 1, 12, 1)
    else:
        start_date = date(d.year, d.month - 1, 1)
    year = int(start_date.year)
    month = int(start_date.month)
    end_day = date(year, month, list(calendar.monthrange(year, month))[1])
    return start_date, end_day


def get_count_of_each_lead_status_by_rep(email, start_date=None, end_date=None):
    """ get Count of Each Lead Status by rep/manager/email """

    lead_status_dict = {'total_leads': 0,
                        'implemented': 0,
                        'in_progress': 0,
                        'attempting_contact': 0,
                        'in_queue': 0,
                        'in_active': 0,
                        'in_progress': 0,
                        }

    if 'regalix' in email:
        lead_status_dict['total_leads'] = Leads.objects.filter(lead_owner_email=email).count()
        lead_status_dict['implemented'] = Leads.objects.filter(lead_status='Implemented', lead_owner_email=email).count()
        lead_status_dict['in_progress'] = Leads.objects.filter(lead_status='In Progress', lead_owner_email=email).count()
        lead_status_dict['attempting_contact'] = Leads.objects.filter(lead_status='Attempting Contact', lead_owner_email=email).count()
        lead_status_dict['in_queue'] = Leads.objects.filter(lead_status='In Queue', lead_owner_email=email).count()
        lead_status_dict['in_active'] = Leads.objects.filter(lead_status='In Active', lead_owner_email=email).count()
    elif 'google' in email:
        lead_status_dict['total_leads'] = Leads.objects.filter(google_rep_email=email).count()
        lead_status_dict['implemented'] = Leads.objects.filter(lead_status='Implemented', google_rep_email=email).count()
        lead_status_dict['in_progress'] = Leads.objects.filter(lead_status='In Progress', google_rep_email=email).count()
        lead_status_dict['attempting_contact'] = Leads.objects.filter(lead_status='Attempting Contact', google_rep_email=email).count()
        lead_status_dict['in_queue'] = Leads.objects.filter(lead_status='In Queue', google_rep_email=email).count()
        lead_status_dict['in_active'] = Leads.objects.filter(lead_status='In Active', google_rep_email=email).count()

    return lead_status_dict


def get_user_profile(user):
    try:
        user_profile = UserDetails.objects.get(user_id=user.id)
        return user_profile
    except ObjectDoesNotExist:
        return None
