"""
common helper function for project goes here
"""

import re
import pytz
import uuid
import calendar
from functools import wraps
from datetime import datetime, timedelta, date
from collections import defaultdict
import operator

from xlrd import XL_CELL_DATE, xldate_as_tuple

from django.db.models import Q, Count
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User

from main.models import UserDetails
from leads.models import Leads, WPPLeads, PicassoLeads, Timezone
from reports.models import MeetingMinutes
from lib.salesforce import SalesforceApi
from representatives.models import AvailabilityForTAT, AvailabilityForBoltTAT

def send_mail(subject, body, mail_from, to, bcc, attachments, template_added=False):
    bcc.append(settings.BCC_EMAIL)
    if settings.SFDC == 'STAGE':
        subject = 'STAGE - ' + subject
        to = set()
    email = EmailMultiAlternatives(subject, body, mail_from, to, bcc)
    if template_added:
        email.attach_alternative(body, "text/html")

    for attachment in attachments:
        email.attach(
            attachment.name,
            attachment.read()
        )
    try:
        email.send()
    except Exception, e:
        print e


# import smtplib
# from os.path import basename
# from email.mime.application import MIMEApplication
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.utils import COMMASPACE, formatdate


# def send_welcome_mail(send_from, send_to, subject, body, files=list()):
#     # msg = MIMEMultipart(
#     #     From=send_from,
#     #     To=COMMASPACE.join(send_to),
#     #     # Date=formatdate(localtime=True),
#     #     Subject=subject
#     # )

#     msg = MIMEMultipart()
#     msg['Subject'] = subject
#     msg['From'] = send_from
#     msg['To'] = COMMASPACE.join(send_to)

#     msg.attach(MIMEText(body.encode('ascii', 'ignore'), 'html'))

#     for f in files:
#         msg.attach(MIMEApplication(
#             f.read(),
#             f.name
#         ))

#     try:
#         smtp = smtplib.SMTP('localhost')
#         smtp.sendmail(send_from, send_to, msg.as_string())
#         smtp.close()
#     except Exception:
#         print Exception


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


def wpp_user_required(func):
    def _decorator(request, *args, **kwargs):
        # provide wpp access to only google wpp users
        user_groups = [str(grp['name']) for grp in request.user.groups.values('name')]
        if 'WPP' in user_groups or 'TAG-AND-WPP' in user_groups or 'wpp' in request.META['HTTP_HOST']:
            response = func(request, *args, **kwargs)
            # maybe do something after the view_func call
            return response
        else:
            redirect_url = 'main.views.home'
            return redirect(redirect_url)
    return wraps(func)(_decorator)


def tag_user_required(func):
    def _decorator(request, *args, **kwargs):
        # provide wpp access to only google wpp users
        user_groups = [str(grp['name']) for grp in request.user.groups.values('name')]
        if 'TAG-AND-WPP' not in user_groups and 'WPP' in user_groups:
            redirect_url = 'main.views.home'
            return redirect(redirect_url)
        else:
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
            if not user_details.user_manager_email:
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
    day_week = date(year, 1, 1)
    day_week = day_week - timedelta(day_week.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    current_day = day_week + dlt
    current_week = day_week + dlt + timedelta(days=6)
    return current_day, current_week


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
    if qtr_week_cur > 8:
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


def wpp_lead_status_count_analysis(email, treatment_type_list, start_date=None, end_date=None):
    wpp_lead_status = ['01. UI/UX','02. Design','03. Development','04. Testing','05. Staging','06. Implementation','07. Self Development']
    wpp_lead_sub_status = ['In Queue','Rework Required','Design In Progress', 'Awaiting Review','Advertiser Delay','In Queue - Website Archive','In Queue - Awaiting Developer','Development In Progress','Inactive - Customer Decision','Testing In Progress','Rework In Progress','Inactive - Unable to Reach Customer','Attempting Contact','Win - Implemented by Regalix','Self Development - Complete','Self Development - To be Verified','Self Development  - Did Not Occur']
    if is_manager(email):
        email_list = get_user_list_by_manager(email)
        email_list.append(email)
    else:
        email_list = [email]
    if start_date and end_date:
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        query = {'created_date__gte': start_date, 'created_date__lte': end_date, 'treatment_type__in': treatment_type_list, 'lead_status__in': wpp_lead_status}
        wpp_lead_status_analysis = WPPLeads.objects.exclude(type_1='WPP - Nomination').filter(**query).values('lead_status').annotate(count=Count('pk'))
        total_count = WPPLeads.objects.filter(**query).count()
        nominated_leads = WPPLeads.objects.exclude(type_1='WPP').filter(created_date__gte=start_date, created_date__lte=end_date, type_1='WPP - Nomination').count()
    else:
        mylist = [Q(google_rep_email__in=email_list), Q(lead_owner_email__in=email_list)]
        query = {'treatment_type__in': treatment_type_list, 'lead_status__in': settings.WPP_LEAD_STATUS}
        wpp_lead_status_analysis = WPPLeads.objects.exclude(type_1='WPP - Nomination').filter(reduce(operator.or_, mylist), **query).values('lead_status').annotate(count=Count('pk'))
        total_count = WPPLeads.objects.filter(reduce(operator.or_, mylist), **query).count()
        query['type_1'] = 'WPP - Nomination'
        nominated_leads = WPPLeads.objects.exclude(type_1='WPP').filter(type_1='WPP - Nomination').count()
    
    wpp_lead_sub_status = {}

    wpp_lead_status_dict = {'total_leads': 0,
                            'in_ui_ux_review': 0,
                            'in_stage': 0,
                            'in_design': 0,
                            'in_testing': 0,
                            'in_development': 0,
                            'in_self_development': 0,
                            'implemented': 0,
                            'nominated_leads': 0,
                            }


    for k in wpp_lead_status:
        wpp_lead_sub_status_dict = {
        'In_Queue':0,
        'Attempting_Contact':0,
        'Rework_Required':0,
        'Rework_In_Progress':0,
        'Inactive_Customer_Decision':0,
        'Inactive_Unable_to_Reach_Customer':0,
        'Design_In_Progress':0,
        'Awaiting_Review':0,
        'Advertiser_Delay':0,
        'In_Queue_Website_Archive':0,
        'In_Queue_Awaiting_Developer':0,
        'Development_In_Progress':0,
        'Testing_In_Progress':0,
        'Win_Implemented_by_Regalix':0,
        'Self_Development_Complete':0,
        'Self_Development_To_be_Verified':0,
        'Self_Development_Did_Not_Occur':0
        }
        wpp_lead_sub_status[k] = 0
        lead = WPPLeads.objects.exclude(type_1='WPP - Nomination').filter(created_date__gte=start_date, created_date__lte=end_date,treatment_type__in=treatment_type_list,lead_status=k)
        for j in lead:
            if k == j.lead_status:
                if 'In Queue' in str(j.lead_sub_status) and 'In Queue Website Archive' not in str(j.lead_sub_status) and 'In Queue Awaiting Developer' not in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['In_Queue'] += 1
                elif 'Attempting Contact' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Attempting_Contact'] += 1
                elif 'Rework Required' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Rework_Required'] += 1
                elif 'Rework In Progress' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Rework_In_Progress'] += 1                
                elif 'Inactive - Customer Decision' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Inactive_Customer_Decision'] += 1               
                elif 'Inactive - Unable to Reach Customer' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Inactive_Unable_to_Reach_Customer'] += 1               
                elif 'Design In Progress' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Design_In_Progress'] += 1                
                elif 'Awaiting Review' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Awaiting_Review'] += 1
                elif 'Advertiser Delay' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Advertiser_Delay'] += 1
                elif 'In Queue - Website Archive' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['In_Queue_Website_Archive'] += 1
                elif 'In Queue-Awaiting Developer' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['In_Queue_Awaiting_Developer'] += 1
                elif 'Development In Progress' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Development_In_Progress'] += 1
                elif 'Testing In Progress' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Testing_In_Progress'] += 1
                elif 'Win Implemented by Regalix' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Win_Implemented_by_Regalix'] += 1
                elif 'Self Development - Complete' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Self_Development_Complete'] += 1
                elif 'Self Development - To be Verified' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Self_Development_To_be_Verified'] += 1
                elif 'Self Development - Did Not Occur' in str(j.lead_sub_status):
                    wpp_lead_sub_status_dict['Self_Development_Did_Not_Occur'] += 1
        wpp_lead_sub_status[k] = wpp_lead_sub_status_dict      
    
    for status_dict in wpp_lead_status_analysis:
        if status_dict['lead_status'] == '01. UI/UX':
            wpp_lead_status_dict['in_ui_ux_review'] += status_dict['count']
        elif status_dict['lead_status'] == '02. Design':
            wpp_lead_status_dict['in_design'] += status_dict['count']
        elif status_dict['lead_status'] == '03. Development':
            wpp_lead_status_dict['in_development'] += status_dict['count']
        elif status_dict['lead_status'] == '04. Testing':
            wpp_lead_status_dict['in_testing'] += status_dict['count']
        elif status_dict['lead_status'] == '05. Staging':
            wpp_lead_status_dict['in_stage'] += status_dict['count']
        elif status_dict['lead_status'] == '06. Implementation':
            wpp_lead_status_dict['implemented'] += status_dict['count']
        elif status_dict['lead_status'] == '07. Self Development':
            wpp_lead_status_dict['in_self_development'] += status_dict['count']

    wpp_lead_status_dict['lead_sub_status'] = wpp_lead_sub_status
    wpp_lead_status_dict['total_leads'] = total_count
    wpp_lead_status_dict['nominated_leads'] = nominated_leads

    return wpp_lead_status_dict


def get_count_of_each_lead_status_by_rep(email, lead_form, start_date=None, end_date=None):
    """ get Count of Each Lead Status by rep/manager/email """
    if is_manager(email):
        email_list = get_user_list_by_manager(email)
        email_list.append(email)
    else:
        email_list = [email]

    if lead_form == 'normal':

        lead_status = settings.LEAD_STATUS
        lead_status_dict = {'total_leads': 0,
                            'implemented': 0,
                            'in_progress': 0,
                            'attempting_contact': 0,
                            'in_queue': 0,
                            'in_active': 0,
                            'in_progress': 0,
                            }

        if start_date and end_date:
            mylist = [Q(lead_status__in=lead_status)]
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            query = {'created_date__gte': start_date, 'created_date__lte': end_date}
        else:
            mylist = [Q(google_rep_email__in=email_list), Q(lead_owner_email__in=email_list)]
            query = {'lead_status__in': lead_status}

        lead_status_dict['total_leads'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['Rework Required']
        rr_total_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count()
        del query['lead_status__in']

        query['lead_status__in'] = settings.LEAD_STATUS_DICT['In Progress']
        lead_status_dict['in_progress'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count()
        query['lead_status__in'] = settings.LEAD_STATUS_DICT['Attempting Contact']
        lead_status_dict['attempting_contact'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count()
        query['lead_status__in'] = settings.LEAD_STATUS_DICT['In Queue']
        lead_status_dict['in_queue'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['Rework Required']
        query['lead_sub_status'] = 'RR - Inactive'
        rr_inactive_leads = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count()
        del query['lead_status__in']
        del query['lead_sub_status']

        rr_implemented_leads = rr_total_leads - rr_inactive_leads

        query['lead_status__in'] = settings.LEAD_STATUS_DICT['Implemented']
        lead_status_dict['implemented'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count() + rr_implemented_leads

        query['lead_status__in'] = settings.LEAD_STATUS_DICT['In Active']
        lead_status_dict['in_active'] = Leads.objects.exclude(type_1__in=['WPP', '']).filter(reduce(operator.or_, mylist), **query).count() + rr_inactive_leads

    elif lead_form == 'wpp':
        lead_status = settings.WPP_LEAD_STATUS
        if start_date and end_date:
            mylist = [Q(type_1='WPP')]
            query = {'lead_status__in': lead_status, 'created_date__gte': start_date, 'created_date__lte': end_date}
        else:
            mylist = [Q(google_rep_email__in=email_list), Q(lead_owner_email__in=email_list)]
            query = {'lead_status__in': lead_status, 'type_1': 'WPP'}

        lead_status_dict = {'total_leads': 0,
                            'open': 0,
                            'in_ui_ux_review': 0,
                            'in_file_transfer': 0,
                            'on_hold': 0,
                            'in_mockup': 0,
                            'mockup_review': 0,
                            'deferred': 0,
                            'in_development': 0,
                            'in_stage': 0,
                            'in_stage_adv_impl': 0,
                            'implemented': 0,
                            'ab_testing': 0,
                            }

        lead_status_dict['total_leads'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['Open']
        lead_status_dict['open'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['In UI/UX Review']
        lead_status_dict['in_ui_ux_review'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['In Stage - Adv Implementation']
        lead_status_dict['in_stage_adv_impl'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['On Hold']
        lead_status_dict['on_hold'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['In Mockup']
        lead_status_dict['in_mockup'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['Mockup Review']
        lead_status_dict['mockup_review'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['Deferred']
        lead_status_dict['deferred'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['In Development']
        lead_status_dict['in_development'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['In Stage']
        lead_status_dict['in_stage'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['Implemented']
        lead_status_dict['implemented'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

        query['lead_status__in'] = ['In A/B Test']
        lead_status_dict['ab_testing'] = Leads.objects.filter(reduce(operator.or_, mylist), **query).count()

    elif lead_form == 'picasso':
        lead_status = settings.PICASSO_LEAD_STATUS
        if start_date and end_date:
            mylist = [Q(type_1='PICASSO')]
            query = {'lead_status__in': lead_status, 'created_date__gte': start_date, 'created_date__lte': end_date}
        else:
            mylist = [Q(google_rep_email__in=email_list), Q(lead_owner_email__in=email_list)]
            query = {'lead_status__in': lead_status, 'type_1': 'PICASSO'}
        lead_status = {'In Queue': 0, 'Audited': 0, 'Delivered': 0}
        total_lead_status_dict = PicassoLeads.objects.filter(reduce(operator.or_, mylist), **query).values('lead_status').annotate(cnt=Count('lead_status'))
        for lead_status_cnt in total_lead_status_dict:
            lead_status[lead_status_cnt.get('lead_status')] = lead_status_cnt.get('cnt')
        lead_status_dict = {key.replace(' ', '_'): value for key, value in lead_status.iteritems()}
    return lead_status_dict


def get_user_profile(user):
    try:
        user_profile = UserDetails.objects.get(user_id=user.id)
        return user_profile
    except ObjectDoesNotExist:
        return None


def is_manager(email):
    # email = 'tkhan@regalix-inc.com'
    managers_list = UserDetails.objects.filter(user_manager_email=email)
    if managers_list:
        return True
    return False


def get_user_list_by_manager(email):
    """ """
    # email = 'tkhan@regalix-inc.com'
    users = UserDetails.objects.filter(user_manager_email=email).values_list("user").distinct()
    user_emails = User.objects.filter(id__in=users)
    user_list = list()
    for user in user_emails:
        user_list.append(user.email)
    return user_list


def get_manager_by_user(email):
    user = User.objects.get(email=email)
    user_profile = UserDetails.objects.get(user_id=user.id)
    return user_profile


def get_user_under_manager(email):
    """ """
    users = UserDetails.objects.filter(user_manager_email=email).values_list("user").distinct()
    return User.objects.filter(id__in=users)


def prev_quarter_date_range(ref):
    if ref.month < 4:
        return get_quarter_date_slots(date(ref.year - 1, 12, 31))
    elif ref.month < 7:
        return get_quarter_date_slots(date(ref.year, 3, 31))
    elif ref.month < 10:
        return get_quarter_date_slots(date(ref.year, 6, 30))
    return get_quarter_date_slots(date(ref.year, 9, 30))


def get_months_from_date(dt):
    month = dt.month
    if month in [1, 2, 3]:
        months = [1, 2, 3]
    elif month in [4, 5, 6]:
        months = [4, 5, 6]
    elif month in [7, 8, 9]:
        months = [7, 8, 9]
    else:
        months = [10, 11, 12]
    return months


def get_rep_details_from_leads(reps, start_date, end_date):

    user_monthly_lead_status_dict = month_on_month_leads_details(reps, start_date, end_date)

    # for ele in user_monthly_lead_status_dict.keys():
    #     if ele not in reps:
    #         print ele

    total_leads_dict = Leads.objects.exclude(type_1='WPP').values('google_rep_email').filter(created_date__gt=start_date, created_date__lt=end_date).annotate(count=Count('lead_status'))
    implemented_leads_dict = Leads.objects.exclude(type_1='WPP', lead_sub_status='RR - Inactive').values('google_rep_email').filter(created_date__gt=start_date, created_date__lt=end_date, lead_status__in=['Implemented', 'Rework Required', 'Pending QC - WIN']).annotate(count=Count('lead_status'))
    users_total_leads = {str(rec['google_rep_email']): rec['count'] for rec in total_leads_dict}
    users_implemented_leads = {str(rec['google_rep_email']): rec['count'] for rec in implemented_leads_dict}

    user_dict = UserDetails.objects.filter(user__email__in=reps).values('location__location_name', 'user__email', 'user__first_name', 'user__last_name', 'profile_photo_url', 'team__team_name')
    for user in user_dict:
        query = {'created_date__gte': start_date, 'created_date__lte': end_date, 'google_rep_email': user['user__email']}
        user['code_types'] = get_rep_code_type_details(query)

    for record in user_dict:
        if record['user__email'] in user_monthly_lead_status_dict.keys():
            record['monthly_lead_status'] = user_monthly_lead_status_dict[record['user__email']]
        if record['user__email'] in users_total_leads.keys():
            record['total_leads'] = users_total_leads[record['user__email']]
        if record['user__email'] in users_implemented_leads.keys():
            record['implemented_leads'] = users_implemented_leads[record['user__email']]

    return user_dict


def get_rep_code_type_details(query):
    code_types = dict()
    code_types_count = Leads.objects.filter(**query).values('type_1').annotate(count=Count('pk'))
    for each_type in code_types_count:
            if each_type:
                code_types[str(each_type['type_1'])] = each_type['count']
    return code_types


def get_lead_status_details(lead_sub_status_count):
    top_3_sub_status = dict()
    for each_sub_status in lead_sub_status_count:
        if each_sub_status:
            top_3_sub_status[str(each_sub_status['lead_sub_status'])] = each_sub_status['count']
    return top_3_sub_status


def month_on_month_leads_details(reps, start_date, end_date):
    # total leads with each rep
    total_leads = Leads.objects.exclude(type_1='WPP').extra({'created_month': 'month(created_date)'}).values('google_rep_email', 'created_month').order_by().annotate(total_leads=Count('lead_status')).filter(google_rep_email__in=reps, created_date__gt=start_date, created_date__lt=end_date)
    month_details = dict()
    for record in total_leads:
        if str(record['google_rep_email']) not in month_details.keys():
            month_details[str(record['google_rep_email'])] = {record['created_month']: {'total_leads': record['total_leads']}}
        else:
            month_details[str(record['google_rep_email'])].update({record['created_month']: {'total_leads': record['total_leads']}})

    # Implemted leads count with each rep
    impl_leads = Leads.objects.exclude(type_1='WPP', lead_sub_status='RR - Inactive').extra({'created_month': 'month(created_date)'}).values('google_rep_email', 'created_month').order_by().annotate(imple_leads=Count('lead_status')).filter(created_date__gt=start_date, created_date__lt=end_date, lead_status__in=['Implemented', 'Pending QC - WIN', 'Rework Required'])
    for record in impl_leads:
        if str(record['google_rep_email']) not in month_details.keys():
            month_details[str(record['google_rep_email'])] = {record['created_month']: {'imple_leads': record['imple_leads']}}
        else:
            if record['created_month'] in month_details[str(record['google_rep_email'])].keys():
                if month_details[str(record['google_rep_email'])][record['created_month']]:
                    month_details[str(record['google_rep_email'])][record['created_month']].update({'imple_leads': record['imple_leads']})
            else:
                print record['google_rep_email'], '=='

    return month_details


def create_new_user(email):
    """ Create New User """
    username = email.split('@')[0]
    user = User.objects.create_user(username, email)
    user.first_name = username
    user.save()
    return user


def convert_excel_data_into_list(workbook):
    # excel sheet data
    sheet = workbook.sheet_by_index(0)
    excel_data = list()
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
    return excel_data


def logs_to_events(call_logs):
    events = []
    for log in call_logs:
        event = dict()
        seller_name = str(log.seller_name.encode('utf-8')) if log.seller_name else ''
        seller_id = str(log.seller_id) if log.seller_id else ''
        phone_number = str(log.phone_number) if log.phone_number else ''
        alternate_number = str(log.alternate_number) if log.alternate_number else ''
        event['title'] = seller_name + ' ' + seller_id + ' ' + phone_number + ' ' + alternate_number

        chicago_timezone = pytz.timezone('America/Chicago')
        meeting_time = datetime.strptime(str(log.meeting_time), "%Y-%m-%d %H:%M:%S")
        utc_date = pytz.utc.normalize(chicago_timezone.localize(meeting_time))

        tz_ist = Timezone.objects.get(zone_name='IST')
        meeting_time_ist = SalesforceApi.convert_utc_to_timezone(utc_date, tz_ist.time_value)
        event['start'] = datetime.strftime(meeting_time_ist, "%Y-%m-%dT%H:%M:%S")
        event['end'] = datetime.strftime(meeting_time_ist + timedelta(minutes=30), "%Y-%m-%dT%H:%M:%S")
        events.append(event)
    return events


def get_picasso_count_of_each_lead_status_by_rep(email, objective_type, start_date=None, end_date=None):
    if is_manager(email):
        email_list = get_user_list_by_manager(email)
        email_list.append(email)
    else:
        email_list = [email]

    lead_status = {'In Queue': 0, 'Audited': 0, 'Delivered': 0, 'Total': 0}

    if start_date and end_date:
        mylist = [Q(lead_status__in=lead_status)]
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        query = {'created_date__gte': start_date, 'created_date__lte': end_date}
    else:
        mylist = [Q(google_rep_email__in=email_list), Q(lead_owner_email__in=email_list)]
        query = {'lead_status__in': lead_status}

    if objective_type != 'all':
        query['picasso_objective'] = objective_type

    total_lead_status_dict = PicassoLeads.objects.filter(reduce(operator.or_, mylist), **query).values('lead_status').annotate(cnt=Count('lead_status'))
    lead_status['Total'] = sum([total_leads.get('cnt') for total_leads in total_lead_status_dict])
    for lead_status_cnt in total_lead_status_dict:
        lead_status[lead_status_cnt.get('lead_status')] = lead_status_cnt.get('cnt')
    picasso_lead_status = {key.replace(' ', '_'): value for key, value in lead_status.iteritems()}
    return picasso_lead_status


def check_lead_submitter_for_empty(topper_dict):
    no_leads = False
    for dt_range, user_list in topper_dict.iteritems():
        if not user_list:
            no_leads = True
            return no_leads
    return no_leads


def get_unique_uuid(lead_type):
    unique_rf_id = str(uuid.uuid4())[:13].replace('-', '')
    try:
        if lead_type == 'Picasso':
            PicassoLeads.objects.get(ref_uuid=unique_rf_id)
            get_unique_uuid('Picasso')
        elif lead_type == 'Wpp':
            WPPLeads.objects.get(ref_uuid=unique_rf_id)
            get_unique_uuid('Wpp')
        else:
            MeetingMinutes.objects.get(ref_uuid=unique_rf_id)
            get_unique_uuid('meeting_minutes')

    except:
        return unique_rf_id

# getting tat for normal picasso Audit
def get_tat_for_picasso(source):
    if source == 'SFDC':
        end_date = datetime.now(pytz.UTC)   # end date in utc today
        start_date = datetime(2016, 01, 01, 0, 0, 0, tzinfo=pytz.utc)
        start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
        end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
        sf = SalesforceApi.connect_salesforce()
        code_type = 'Picasso'
        where_clause_picasso = "WHERE (CreatedDate >= %s AND CreatedDate <= %s) AND Code_Type__c = '%s'" % (start_date,
                                                                                                    end_date, code_type)
        sql_query_picasso = "select count() from Lead %s" % (where_clause_picasso)
        result = sf.query_all(sql_query_picasso)
        no_of_inqueue_leads = result['totalSize'] + 1
    else:
        start_date = datetime.today()
        start_date = datetime(start_date.year, 1, 1, 0, 0)
        no_of_inqueue_leads = PicassoLeads.objects.exclude(lead_status__in=['Issue Case', 'Delivered', 'Unsupported Language'])\
            .filter(created_date__gte=start_date, type_1='Picasso').count() #+ 1

    tz_ist = Timezone.objects.get(zone_name='IST')
    ist_today = SalesforceApi.convert_utc_to_timezone(datetime.utcnow(), tz_ist.time_value)
    today_in_ist = datetime(ist_today.year, ist_today.month, ist_today.day)
    availabilities = AvailabilityForTAT.objects.filter(date_in_ist__gte=today_in_ist).order_by('date_in_ist')
    lookup_sum = 0
    '''
        Not sure why they were adding the todays transaction leads to queue lead count, this was causing the count mis-match,
        hence, commenting that code.
    '''
    total_no_of_inqueue_leads = no_of_inqueue_leads #+ get_todays_transition_leads()
    target_details = {'estimated_date': today_in_ist, 'lookup_sum': '', 'no_of_inqueue_leads': 1}
    for availability in availabilities:
        if availability.availability_count and availability.audits_per_date:
            lookup_sum += availability.availability_count * availability.audits_per_date
            if lookup_sum > total_no_of_inqueue_leads:
                estimated_date = availability.date_in_ist + timedelta(days=2)  # two days buffer
                if estimated_date.weekday() == 5:
                    target_details['estimated_date'] = estimated_date + timedelta(days=2)
                elif estimated_date.weekday() == 6:
                    target_details['estimated_date'] = estimated_date + timedelta(days=1)
                else:
                    target_details['estimated_date'] = estimated_date
                target_details['lookup_sum'] = lookup_sum
                target_details['no_of_inqueue_leads'] = no_of_inqueue_leads
                return target_details

    # lookup_sum = 0
    audits_remaining = total_no_of_inqueue_leads - lookup_sum + 2  # two days buffer
    default_emp = 7
    default_audits_per_emp = 4
    default_audits_per_day = default_emp * default_audits_per_emp
    no_of_days_for_remaining_audits = audits_remaining / default_audits_per_day
    estimated_date = target_details['estimated_date'] + timedelta(days=no_of_days_for_remaining_audits)
    if estimated_date.weekday() == 5:
        target_details['estimated_date'] = estimated_date + timedelta(days=2)
    elif estimated_date.weekday() == 6:
        target_details['estimated_date'] = estimated_date + timedelta(days=1)
    else:
        target_details['estimated_date'] = estimated_date
    target_details['no_of_inqueue_leads'] = no_of_inqueue_leads
    return target_details

# tat for bolt
def get_tat_for_bolt(source):
    if source == 'SFDC':
        end_date = datetime.now(pytz.UTC)   # end date in utc today
        start_date = datetime(2016, 01, 01, 0, 0, 0, tzinfo=pytz.utc)
        start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
        end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
        sf = SalesforceApi.connect_salesforce()
        code_type = 'BOLT'
        where_clause_picasso = "WHERE (CreatedDate >= %s AND CreatedDate <= %s) AND Code_Type__c = '%s'" % (start_date, end_date, code_type)
        sql_query_picasso = "select count() from Lead %s" % (where_clause_picasso)
        result = sf.query_all(sql_query_picasso)
        no_of_inqueue_leads = result['totalSize'] + 1
    else:
        start_date = datetime.today()
        start_date = datetime(start_date.year, 1, 1, 0, 0)
        no_of_inqueue_leads = PicassoLeads.objects.exclude(lead_status__in=['Issue Case', 'Delivered', 'Unsupported Language'])\
            .filter(created_date__gte=start_date, type_1='BOLT').count() #+ 1

    tz_ist = Timezone.objects.get(zone_name='IST')
    ist_today = SalesforceApi.convert_utc_to_timezone(datetime.utcnow(), tz_ist.time_value)
    today_in_ist = datetime(ist_today.year, ist_today.month, ist_today.day)
    availabilities = AvailabilityForBoltTAT.objects.filter(date_in_ist__gte=today_in_ist).order_by('date_in_ist')
    lookup_sum = 0
    '''
        Not sure why they were adding the todays transaction leads to queue lead count, this was causing the count mis-match,
        hence, commenting that code.
    '''
    total_no_of_inqueue_leads = no_of_inqueue_leads #+ get_todays_transition_leads()
    target_details = {'estimated_date': today_in_ist, 'lookup_sum': '', 'no_of_inqueue_leads': 1}
    for availability in availabilities:
        if availability.availability_count and availability.audits_per_date:
            lookup_sum += availability.availability_count * availability.audits_per_date
            if lookup_sum > total_no_of_inqueue_leads:
                estimated_date = availability.date_in_ist + timedelta(days=2)  # two days buffer
                if estimated_date.weekday() == 5:
                    target_details['estimated_date'] = estimated_date + timedelta(days=2)
                elif estimated_date.weekday() == 6:
                    target_details['estimated_date'] = estimated_date + timedelta(days=1)
                else:
                    target_details['estimated_date'] = estimated_date
                target_details['lookup_sum'] = lookup_sum
                target_details['no_of_inqueue_leads'] = no_of_inqueue_leads
                return target_details

    # lookup_sum = 0
    audits_remaining = total_no_of_inqueue_leads - lookup_sum + 2  # two days buffer
    default_emp = 7
    default_audits_per_emp = 4
    default_audits_per_day = default_emp * default_audits_per_emp
    no_of_days_for_remaining_audits = audits_remaining / default_audits_per_day
    estimated_date = target_details['estimated_date'] + timedelta(days=no_of_days_for_remaining_audits)
    if estimated_date.weekday() == 5:
        target_details['estimated_date'] = estimated_date + timedelta(days=2)
    elif estimated_date.weekday() == 6:
        target_details['estimated_date'] = estimated_date + timedelta(days=1)
    else:
        target_details['estimated_date'] = estimated_date
    target_details['no_of_inqueue_leads'] = no_of_inqueue_leads
    return target_details


def get_todays_transition_leads():
    start_date = datetime.utcnow()
    start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    end_date = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59)
    ist_timezone = 'IST'
    selected_tzone = Timezone.objects.get(zone_name=ist_timezone)
    ist_today = SalesforceApi.convert_utc_to_timezone(start_date, selected_tzone.time_value)
    today_changed_leads = PicassoLeads.objects.filter(lead_status__in=['Delivered'],
                                                      updated_date__gte=start_date,
                                                      updated_date__lte=end_date, date_of_installation=ist_today.date()).count()
    return today_changed_leads


def save_file(file_data, file_path):
    with open(file_path, 'wb+') as destination:
        for chunk in file_data.chunks():
            destination.write(chunk)
        destination.close()
    return file_path

def is_cid(cid):
    reg = '\d{3}-\d{3}-\d{4}$'
    return re.match(reg, cid)
