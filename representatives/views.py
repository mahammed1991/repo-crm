from datetime import datetime, timedelta
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from main.models import UserDetails
from leads.models import Timezone, RegalixTeams, Location, TimezoneMapping, Leads, WPPLeads
from representatives.models import (
    Availability,
    ScheduleLog,
    AvailabilityForTAT
)
from reports.report_services import DownloadLeads
from lib.salesforce import SalesforceApi
from django.db.models import Q
from lib.helpers import send_mail
from django.template.loader import get_template
from django.template import Context
from django.db.models import Count
from collections import OrderedDict


# Create your views here.
@login_required
def users(request):
    """ List all Google representatives"""
    users = User.objects.all()

    roles = {
        1: 'Admin',
        2: 'Google Manager',
        3: 'Google Representative',
        4: 'Implementation Consultant'
    }

    return render(request, 'representatives/users.html', {'users': users, 'roles': roles})


@login_required
def add_edit_user(request, id=None):
    """ Manage Users information """
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        user = None

    if request.method == 'POST':
        if not user:
            user = User()

        user.email = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        try:
            user.profile.role = request.POST['ref_role_id']
            user.profile.user_supporting_region = request.POST['user_supporting_region']
            user.profile.user_manager_name = request.POST['user_manager_name']
            user.profile.user_manager_email = request.POST['user_manager_email']
            user.profile.save()
        except ObjectDoesNotExist:
            user_details = UserDetails()
            user_details.user = user
            user_details.role = request.POST['ref_role_id']
            user_details.user_supporting_region = request.POST['user_supporting_region']
            user_details.user_manager_name = request.POST['user_manager_name']
            user_details.user_manager_email = request.POST['user_manager_email']
            user_details.save()

        return redirect('representatives.views.users')

    return render(request, 'representatives/add_edit_user.html', {'rep_user': user})


@login_required
def plan_schedule(request, plan_month=0, plan_day=0, plan_year=0, process_type='TAG', team_id=0):
    """ Manage scheduling appointments"""

    time_zone = 'IST'
    if request.method == 'POST':
        changed_reords_in_slot = list()
        selected_tzone = Timezone.objects.get(zone_name=time_zone)
        slected_week_start_date = request.POST.get('schedule_week_start_date')
        slected_week_start_date = datetime.strptime(slected_week_start_date, '%m-%d-%Y')

        selected_team_id = request.POST.get('team')
        selected_team = RegalixTeams.objects.get(id=selected_team_id)

        for key, value in request.POST.items():
            if key.startswith('input'):
                # check each slot and add slots count if exists
                data_in_a_day = int(request.POST.get(key) or 0)
                keys = key.split('_')  # input_16_6_2014_0_0 / input_16_6_2014_0_30
                slot_day = int(keys[1])
                slot_month = int(keys[2])
                slot_year = int(keys[3])
                slot_hour = int(keys[4])
                slot_minutes = int(keys[5])

                slot_date = datetime(slot_year, slot_month, slot_day, slot_hour, slot_minutes)

                utc_date = SalesforceApi.get_utc_date(slot_date, selected_tzone.time_value)

                # if record already exist update availability count
                try:
                    availability = Availability.objects.get(date_in_utc=utc_date, team=selected_team)
                    if availability.availability_count != data_in_a_day:
                        updated_slot = get_created_or_updated_slot_details(selected_team, utc_date, selected_tzone, availability.availability_count, data_in_a_day)
                        changed_reords_in_slot.append(updated_slot)
                        desc = availability.availability_count
                        availability.availability_count = data_in_a_day
                        availability.save()

                        log = ScheduleLog()
                        log.user = request.user
                        log.availability = availability
                        log.availability_count = availability.availability_count
                        log.booked_count = availability.booked_count
                        log.description = str(desc) + " is Updated to " + str(availability.availability_count)
                        log.save()
                except ObjectDoesNotExist:
                    # create record if it doesn't exist and only if user added some slot information
                    if data_in_a_day:
                        availability = Availability()
                        availability.availability_count = data_in_a_day
                        availability.date_in_utc = utc_date
                        availability.team = selected_team
                        new_slot = get_created_or_updated_slot_details(selected_team, utc_date, selected_tzone, 0, data_in_a_day)
                        changed_reords_in_slot.append(new_slot)
                        availability.save()

                        log = ScheduleLog()
                        log.user = request.user
                        log.availability = availability
                        log.availability_count = availability.availability_count
                        log.booked_count = availability.booked_count
                        log.description = str(0) + " is Updated to " + str(data_in_a_day)
                        log.save()

        # trigger a mail with changes in slot
        if changed_reords_in_slot:
            changed_reords_in_slot = sorted(changed_reords_in_slot, key=lambda k: k['date_time'], reverse=True)
            mail_slot_changes(request, selected_team, changed_reords_in_slot)

        plan_month = slected_week_start_date.month
        plan_day = slected_week_start_date.day
        plan_year = slected_week_start_date.year

    exclude_types = ['MIGRATION']
    if request.user.groups.filter(name='OPERATIONS'):
        if not request.user.groups.filter(Q(name='WPP') | Q(name='TAG-AND-WPP')):
            exclude_types.append('WPP')
        teams = RegalixTeams.objects.filter(process_type=process_type, is_active=True).exclude(team_name='default team')
        process_types = RegalixTeams.objects.exclude(process_type__in=exclude_types).values_list('process_type', flat=True).distinct().order_by()
    else:
        process_types = RegalixTeams.objects.exclude(
            process_type='MIGRATION').filter(Q(team_lead__in=[request.user.id]) | Q(team_manager__in=[request.user.id]), is_active=True).values_list('process_type', flat=True).distinct().order_by()

        if process_type == 'TAG' and process_type not in process_types:
            if 'SHOPPING' in process_types:
                process_type = 'SHOPPING'
            else:
                process_type = 'WPP'
        teams = RegalixTeams.objects.filter(Q(team_lead__in=[request.user.id]) | Q(team_manager__in=[request.user.id]), process_type=process_type, is_active=True).exclude(team_name='default team').distinct().order_by()
    if not teams:
        # if team is not specified, select first team by default
        return render(
            request,
            'representatives/plan_schedule.html',
            {'error': True,
             'message': "No Teams"
             }
        )
    elif not int(team_id):
        # get first team for the selected process
        try:
            RegalixTeams.objects.get(process_type=process_type, id=team_id)
        except ObjectDoesNotExist:
            return redirect(
                'representatives.views.plan_schedule',
                plan_month=plan_month,
                plan_day=plan_day,
                plan_year=plan_year,
                process_type=process_type,
                team_id=teams[0].id
            )

    if not int(plan_month):
        # if month is not specified, select current month
        today = datetime.today()
        plan_month = today.month
        return redirect(
            'representatives.views.plan_schedule',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
            process_type=process_type,
            team_id=team_id
        )

    if not int(plan_day):
        # if day is not specified, select today's day
        today = datetime.today()
        plan_day = today.day
        return redirect(
            'representatives.views.plan_schedule',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
            process_type=process_type,
            team_id=team_id
        )

    if not int(plan_year):
        # if year is not specified, select current year
        today = datetime.today()
        plan_year = today.year
        return redirect(
            'representatives.views.plan_schedule',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
            process_type=process_type,
            team_id=team_id
        )

    # create date from week start day
    plan_date = datetime(int(plan_year), int(plan_month), int(plan_day))

    # if week start day is not monday, select appropriate start week day of given date
    if plan_date.weekday():
        plan_date -= timedelta(days=plan_date.weekday())
        return redirect(
            'representatives.views.plan_schedule',
            plan_month=plan_date.month,
            plan_day=plan_date.day,
            plan_year=plan_date.year,
            process_type=process_type,
            team_id=team_id
        )

    # prepare slot dates to display
    plan_dates = {
        'day1': plan_date,
        'day2': plan_date + timedelta(days=1),
        'day3': plan_date + timedelta(days=2),
        'day4': plan_date + timedelta(days=3),
        'day5': plan_date + timedelta(days=4),
        'day6': plan_date + timedelta(days=5)
    }

    # compute next week and previous week start dates
    prev_week = plan_date + timedelta(days=-7)
    next_week = plan_date + timedelta(days=7)

    tzone = Timezone.objects.get(zone_name=time_zone)
    utc_date = SalesforceApi.get_utc_date(plan_date, tzone.time_value)
    utc_start_date = utc_date
    utc_end_date = utc_start_date + timedelta(days=6)
    selected_team = RegalixTeams.objects.get(id=team_id)
    appointments_list = Availability.objects.filter(
        date_in_utc__range=(utc_start_date, utc_end_date),
        team=selected_team)

    #  for daylight savings notifications
    daylight_marquee_msg = ''
    today = datetime.today()
    locations = selected_team.location.all()
    for location in locations:
        if location.daylight_start and location.daylight_end:
            if today >= location.daylight_start and today <= location.daylight_end:
                date_difference = location.daylight_end.date() - today.date()
                if date_difference.days <= 15:
                    daylight_marquee_msg += 'Daylight Saving ends on %s for %s::' %(location.daylight_end.strftime("%B %d, %Y"), location.location_name)
            if today < location.daylight_start:
                date_difference = location.daylight_start.date() - today.date()
                if date_difference.days <= 15:
                    daylight_marquee_msg += 'Daylight Saving starts on %s for %s::' % (location.daylight_start.strftime("%B %d, %Y"), location.location_name)

    diff = divmod((utc_date - plan_date).total_seconds(), 60)
    diff_in_minutes = diff[0]
    total_booked = dict()
    total_available = dict()
    # prepare appointments slot keys
    appointments = dict()
    for key, _date in plan_dates.items():
        total_booked[datetime.strftime(_date, '%Y_%m_%d')] = []
        total_available[datetime.strftime(_date, '%Y_%m_%d')] = []
        for hour in range(24):
            # even hour slot
            minutes = 0
            even_key = 'input_'  # input_16_6_2014_0_00
            even_key += '0' + str(_date.day) if len(str(_date.day)) == 1 else str(_date.day)
            even_key += '_'
            even_key += '0' + str(_date.month) if len(str(_date.month)) == 1 else str(_date.month)
            even_key += '_' + str(_date.year) + '_' + str(hour) + '_' + str(minutes)

            appointments[even_key] = dict()
            appointments[even_key]['value'] = 0
            appointments[even_key]['disabled'] = True if datetime(
                _date.year, _date.month, _date.day, hour, minutes) < datetime.utcnow() else False

            # odd hour slot
            minutes = 30
            odd_key = 'input_'  # input_16_6_2014_0_00
            odd_key += '0' + str(_date.day) if len(str(_date.day)) == 1 else str(_date.day)
            odd_key += '_'
            odd_key += '0' + str(_date.month) if len(str(_date.month)) == 1 else str(_date.month)
            odd_key += '_' + str(_date.year) + '_' + str(hour) + '_' + str(minutes)

            appointments[odd_key] = dict()
            appointments[odd_key]['value'] = 0
            appointments[odd_key]['disabled'] = True if datetime(
                _date.year, _date.month, _date.day, hour, minutes) < datetime.utcnow() else False

    # calculate slots available vs booked for week
    for apptmnt in appointments_list:
        apptmnt.date_in_utc -= timedelta(minutes=diff_in_minutes)

        key = 'input_' + datetime.strftime(apptmnt.date_in_utc, '%d_%m_%Y') + \
            '_' + str(apptmnt.date_in_utc.hour) + '_' + str(apptmnt.date_in_utc.minute)
        appointments[key]['value'] = int(apptmnt.availability_count)
        appointments[key]['booked'] = int(apptmnt.booked_count)
        total_available[datetime.strftime(apptmnt.date_in_utc, '%Y_%m_%d')].append(int(apptmnt.availability_count))
        total_booked[datetime.strftime(apptmnt.date_in_utc, '%Y_%m_%d')].append(int(apptmnt.booked_count))
    total_slots = list()
    for key, value in sorted(total_available.iteritems()):
        total_slots.append({'available': sum(value), 'booked': sum(total_booked[key])})

    return render(
        request,
        'representatives/plan_schedule.html',
        {'schedule_date': plan_date,
         'time_zone': time_zone,
         'dates': plan_dates,
         'appointments': appointments,
         'prev_week': prev_week,
         'next_week': next_week,
         'teams': teams,
         'plan_month': plan_month,
         'plan_day': plan_day,
         'plan_year': plan_year,
         'process_type': process_type,
         'process_types': process_types,
         'selected_team': selected_team,
         'total_slots': total_slots,
         'daylight_marquee_msg': daylight_marquee_msg,
         }
    )


@login_required
def availability_list(request, avail_month=0, avail_day=0, avail_year=0, process_type='TAG', location_id=0, time_zone='IST'):
    # if month is not specified, select current month
    if not int(avail_month):
        today = datetime.today()
        avail_month = today.month
        return redirect(
            'representatives.views.availability_list',
            avail_month=avail_month,
            avail_day=avail_day,
            avail_year=avail_year,
            process_type=process_type,
            location_id=location_id,
            time_zone=time_zone
        )

    # if day is not specified, select today's day
    if not int(avail_day):
        today = datetime.today()
        avail_day = today.day
        return redirect(
            'representatives.views.availability_list',
            avail_month=avail_month,
            avail_day=avail_day,
            avail_year=avail_year,
            process_type=process_type,
            location_id=location_id,
            time_zone=time_zone
        )

    # if year is not specified, select current year
    if not int(avail_year):
        today = datetime.today()
        avail_year = today.year
        return redirect(
            'representatives.views.availability_list',
            avail_month=avail_month,
            avail_day=avail_day,
            avail_year=avail_year,
            process_type=process_type,
            location_id=location_id,
            time_zone=time_zone
        )

    # create date from week start day
    avail_date = datetime(int(avail_year), int(avail_month), int(avail_day), 0, 0, 0)

    # if week start day is not monday, select appropriate start week day of given date
    if avail_date.weekday():
        avail_date -= timedelta(days=avail_date.weekday())
        return redirect(
            'representatives.views.availability_list',
            avail_month=avail_date.month,
            avail_day=avail_date.day,
            avail_year=avail_date.year,
            process_type=process_type,
            location_id=location_id,
            time_zone=time_zone
        )

    # compute next week and previous week start dates
    prev_week = avail_date + timedelta(days=-7)
    next_week = avail_date + timedelta(days=7)

    # prepare slot dates to display
    avail_dates = {
        'day1': avail_date,
        'day2': avail_date + timedelta(days=1),
        'day3': avail_date + timedelta(days=2),
        'day4': avail_date + timedelta(days=3),
        'day5': avail_date + timedelta(days=4)
    }

    # get UTC date for selected based on selected timezone
    tz = Timezone.objects.get(zone_name=time_zone)
    utc_date = SalesforceApi.get_utc_date(avail_date, tz.time_value)

    # filter and block past appointment slots
    today_date = datetime.utcnow()

    utc_start_date = utc_date if utc_date > today_date else today_date
    utc_end_date = utc_date + timedelta(days=5)

    # For Location Germay we have only one regalix team for both TAG ang Shopping form.
    # If Location Gernamy and process_type is SHOPPING refer avalability slots from team TAG - EMEA - German
    # if int(location_id) == 47 and process_type == 'SHOPPING':
    #     process_type = 'TAG'

    # get all appointments for future dates in the given week
    slots_data = Availability.objects.filter(
        date_in_utc__range=(utc_start_date, utc_end_date),
        team__location__id=location_id,
        team__process_type=process_type
    )

    diff = divmod((utc_date - avail_date).total_seconds(), 60)
    diff_in_minutes = diff[0]

    # set default value
    std_diff_in_minutes = diff_in_minutes
    ds_diff_in_minutes = diff_in_minutes
    is_daylight_now = False
    daylight_start = None
    daylight_end = None
    std_time_zone = None
    ds_time_zone = None
    # New Feature for future appointments in daylight saving mode
    try:
        location = Location.objects.get(id=location_id)
        if location.daylight_start and location.daylight_end:
            daylight_start = datetime(location.daylight_start.year, location.daylight_start.month, location.daylight_start.day, 0, 0, 0)
            daylight_end = datetime(location.daylight_end.year, location.daylight_end.month, location.daylight_end.day, 0, 0, 0)
            daylight_start = SalesforceApi.get_utc_date(daylight_start, tz.time_value)
            daylight_end = SalesforceApi.get_utc_date(daylight_end, tz.time_value)
            std_time_zones_list = TimezoneMapping.objects.values_list('standard_timezone', flat=True).distinct()
            ds_time_zones_list = TimezoneMapping.objects.values_list('daylight_timezone', flat=True).distinct()
            if tz.id in ds_time_zones_list:
                timezone_mapping = TimezoneMapping.objects.get(daylight_timezone_id=tz.id)
            elif tz.id in std_time_zones_list:
                timezone_mapping = TimezoneMapping.objects.get(standard_timezone_id=tz.id)

            std_timezone = timezone_mapping.standard_timezone
            utc_ds_date = SalesforceApi.get_utc_date(avail_date, std_timezone.time_value)
            diff = divmod((utc_ds_date - avail_date).total_seconds(), 60)
            std_diff_in_minutes = diff[0]

            ds_time_zone = timezone_mapping.daylight_timezone
            utc_ds_date = SalesforceApi.get_utc_date(avail_date, ds_time_zone.time_value)
            diff = divmod((utc_ds_date - avail_date).total_seconds(), 60)
            ds_diff_in_minutes = diff[0]

            # # Check if appointment slot is between the daylight time
            # if utc_start_date >= daylight_start and utc_start_date <= daylight_end:
            #     is_daylight_now = True
            #     try:
            #         # Get standard timezone ussing TimezoneMapping table
            #         if tz.id in ds_time_zones_list:
            #             timezone_mapping = TimezoneMapping.objects.get(daylight_timezone_id=tz.id)
            #             new_time_zone = timezone_mapping.daylight_timezone
            #             utc_ds_date = SalesforceApi.get_utc_date(avail_date, new_time_zone.time_value)
            #             diff = divmod((utc_ds_date - avail_date).total_seconds(), 60)
            #             new_diff_in_minutes = diff[0]
            #             new_time_zone1 = timezone_mapping.standard_timezone
            #             utc_ds_date1 = SalesforceApi.get_utc_date(avail_date, new_time_zone1.time_value)
            #             diff1 = divmod((utc_ds_date1 - avail_date).total_seconds(), 60)
            #             new_diff_in_minutes1 = diff1[0]
            #         elif tz.id in std_time_zones_list:
            #             timezone_mapping = TimezoneMapping.objects.get(standard_timezone_id=tz.id)
            #             new_time_zone = timezone_mapping.daylight_timezone
            #             utc_std_date = SalesforceApi.get_utc_date(avail_date, new_time_zone.time_value)
            #             diff = divmod((utc_std_date - avail_date).total_seconds(), 60)
            #             new_diff_in_minutes = diff[0]
            #             new_time_zone1 = timezone_mapping.standard_timezone
            #             utc_ds_date1 = SalesforceApi.get_utc_date(avail_date, new_time_zone1.time_value)
            #             diff1 = divmod((utc_ds_date1 - avail_date).total_seconds(), 60)
            #             new_diff_in_minutes1 = diff1[0]
            #     except ObjectDoesNotExist:
            #         std_diff_in_minutes = diff_in_minutes
            # else:
            #     is_daylight_now = False
            #     try:
            #         ds_time_zone = TimezoneMapping.objects.get(standard_timezone_id=tz.id)
            #         ds_time_zone = ds_time_zone.daylight_timezone
            #         utc_ds_date = SalesforceApi.get_utc_date(avail_date, ds_time_zone.time_value)
            #         ds_diff = divmod((utc_ds_date - avail_date).total_seconds(), 60)
            #         ds_diff_in_minutes = ds_diff[0]
            #         timezone_mapping = TimezoneMapping.objects.get(standard_timezone_id=tz.id)
            #         new_time_zone1 = timezone_mapping.standard_timezone
            #         utc_ds_date1 = SalesforceApi.get_utc_date(avail_date, new_time_zone1.time_value)
            #         diff1 = divmod((utc_ds_date1 - avail_date).total_seconds(), 60)
            #         new_diff_in_minutes1 = diff1[0]
            #     except ObjectDoesNotExist:
            #         ds_diff_in_minutes = diff_in_minutes
            #     print ds_diff_in_minutes
    except ObjectDoesNotExist:
        location = None

    appointments = dict()
    timezone_for_appointments = dict()
    for key, _date in avail_dates.items():
        for hour in range(24):
            # Even Hour slot
            even_key = 'input_' + datetime.strftime(_date, '%d_%m_%Y') + '_' + str(hour)
            appointments[even_key] = 0

            # Odd Hour slot
            odd_key = 'input_' + datetime.strftime(_date, '%d_%m_%Y') + '_' + str(hour)
            appointments[odd_key] = 0

    slot_diff = 0
    for apptmnt in slots_data:
        # related_timezone = time_zone
        # print time_zone, apptmnt.date_in_utc
        # # If Daylight saving changes in between the slots/appointments
        # if location and daylight_start and daylight_end:
        #     if is_daylight_now:
        #         # If week starts with day light savings and ends with in the week then
        #         # Calculate appointments on standard timezones
        #         if apptmnt.date_in_utc >= daylight_start and apptmnt.date_in_utc <= daylight_end:
        #             apptmnt.date_in_utc -= timedelta(minutes=new_diff_in_minutes)
        #             related_timezone = new_time_zone.zone_name if new_time_zone else time_zone
        #         else:
        #             apptmnt.date_in_utc -= timedelta(minutes=new_diff_in_minutes1)
        #     else:
        #         print 'not day light each slot'
        #         # If week starts with standard timezones and ends with in the week then
        #         # Calculate appointments on daylight timezones
        #         print 'ds_diff_in_minutes', ds_diff_in_minutes, 'new_diff_in_minutes1', new_diff_in_minutes1
        #         if apptmnt.date_in_utc >= daylight_start and apptmnt.date_in_utc <= daylight_end:
        #             apptmnt.date_in_utc -= timedelta(minutes=ds_diff_in_minutes)
        #             related_timezone = ds_time_zone.zone_name if ds_time_zone else time_zone
        #         else:
        #             apptmnt.date_in_utc -= timedelta(minutes=new_diff_in_minutes1)
        # else:
        #     apptmnt.date_in_utc -= timedelta(minutes=diff_in_minutes)

        if location and daylight_start and daylight_end:
            if apptmnt.date_in_utc >= daylight_start and apptmnt.date_in_utc <= daylight_end:
                apptmnt.date_in_utc -= timedelta(minutes=ds_diff_in_minutes)
                related_timezone = ds_time_zone
            else:
                apptmnt.date_in_utc -= timedelta(minutes=std_diff_in_minutes)
                related_timezone = std_timezone
        else:
            apptmnt.date_in_utc = SalesforceApi.convert_utc_to_timezone(apptmnt.date_in_utc, tz.time_value)
            related_timezone = tz

        slot_diff = apptmnt.date_in_utc.minute
        key = 'input_' + datetime.strftime(apptmnt.date_in_utc, '%d_%m_%Y') + \
            '_' + str(apptmnt.date_in_utc.hour) + '_' + str(apptmnt.date_in_utc.minute)
        if apptmnt.availability_count > apptmnt.booked_count:
            appointments[key] = int(apptmnt.availability_count - apptmnt.booked_count)
        else:
            appointments[key] = 0
        timezone_for_appointments[key] = str(related_timezone)

    return render(
        request,
        'leads/availability_list.html',
        {'time_zone': time_zone,
         'location_id': location_id,
         'time_zone_desc': time_zone + ' (UTC' + tz.time_value + ')',
         'dates': avail_dates,
         'appointments': appointments,
         'timezone_for_appointments': timezone_for_appointments,
         'slot_diff': slot_diff,
         'process_type': process_type,
         'prev_week': prev_week,
         'next_week': next_week,
         }
    )


@login_required
@csrf_exempt
def check_and_add_appointment(request):
    response = dict()
    if request.method == 'POST':
        request_tzone = request.POST.get('time_zone')
        location_id = request.POST.get('location_id')
        requested_slots = json.loads(request.POST.get('slots'))

        # in case multiple slots needs to fill at once(TAG/SHOPPING)
        slots_filled = list()
        for selected_slot in requested_slots:
            requested_date = selected_slot['time']
            requested_date = datetime.strptime(requested_date, '%m/%d/%Y %I:%M %p')

            process_type = selected_slot['type']

            # For Location Germay we have only one regalix team for both TAG ang Shopping form.
            # If Location Gernamy and process_type is SHOPPING refer avalability slots from team TAG - EMEA - German
            # if int(location_id) == 47 and process_type == 'SHOPPING':
            #     process_type = 'TAG'

            response['status'] = 'FAILED'
            response['type'] = process_type

            # time zone conversion
            tz = Timezone.objects.get(zone_name=request_tzone)
            utc_date = SalesforceApi.get_utc_date(requested_date, tz.time_value)

            alotted_slots = Availability.objects.filter(
                date_in_utc=utc_date,
                team__location__id=location_id,
                team__process_type=process_type
            )

            for slot in alotted_slots:
                if datetime.utcnow() >= utc_date:
                    response['status'] = 'FAILED'
                elif slot.booked_count < slot.availability_count:
                    slot.booked_count += 1
                    slot.save()
                    response['status'] = 'SUCCESS'
                    slots_filled.append(slot.id)
                    break

            if response['status'] == 'FAILED':
                if slots_filled:
                    Availability.objects.filter(id__in=slots_filled).update(booked_count=F('booked_count') - 1)
                break

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def copy_appointment_to_next_week(request, plan_month=0, plan_day=0, plan_year=0, team_id=0):
    response = dict()
    appointment_list = list()

    week_end_date = datetime(int(plan_year), int(plan_month), int(plan_day))
    if week_end_date.weekday():
        week_end_date -= timedelta(days=week_end_date.weekday())

    # substract 330 minutes(5:30 hours) since the configuration is doing for indian team
    week_start_date = week_end_date - timedelta(days=7) - timedelta(seconds=(330 * 60))
    week_end_date = week_end_date - timedelta(seconds=(330 * 60)) - timedelta(seconds=1)

    availability_data = Availability.objects.filter(
        date_in_utc__range=(week_start_date, week_end_date),
        team_id=team_id
    )

    # get UTC date for selected based on selected timezone
    for avail_data in availability_data:
        appointment_dict = dict()
        # Get data for current week(to avoid template processing the logic)
        ist_date = avail_data.date_in_utc + timedelta(seconds=(330 * 60)) + timedelta(days=7)

        appointment_dict.update({
            'availability_count': avail_data.availability_count,
            'date_in_utc': datetime.strftime(ist_date, '%d_%m_%Y_%H_%M'),
        })
        appointment_list.append(appointment_dict)

    response['appointment'] = appointment_list
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def export_appointments(request):
    """ Export Appointments by Availability/Booked """

    default_process_type = ['TAG', 'SHOPPING', 'WPP']
    process_types = RegalixTeams.objects.exclude(process_type='MIGRATION').values_list('process_type', flat=True).distinct().order_by()
    teams = RegalixTeams.objects.filter(process_type__in=process_types).exclude(team_name='default team')
    default_teams = RegalixTeams.objects.filter(process_type__in=default_process_type, is_active=True).exclude(team_name='default team')

    tag_by_team = dict()
    for team in teams:
        rec = {
            'name': str(team.team_name),
            'id': str(team.id)
        }
        if team.process_type not in tag_by_team:
            tag_by_team[str(team.process_type)] = [rec]
        else:
            tag_by_team[str(team.process_type)].append(rec)

    post_result_dict = {}
    if request.method == 'POST':
        from_date = request.POST.get('date_from')
        to_date = request.POST.get('date_to')
        process_type = request.POST.getlist('selectedProcessType')
        regalix_team = request.POST.getlist('selectedTeams')
        from_date = datetime.strptime(from_date, "%d/%m/%Y %H:%M")
        to_date = datetime.strptime(to_date, "%d/%m/%Y %H:%M")
        to_date = datetime(to_date.year, to_date.month, to_date.day, to_date.hour, to_date.minute, 59)

        time_zone = 'IST'
        selected_tzone = Timezone.objects.get(zone_name=time_zone)
        from_utc_date = SalesforceApi.get_utc_date(from_date, selected_tzone.time_value)
        to_utc_date = SalesforceApi.get_utc_date(to_date, selected_tzone.time_value)
        diff = divmod((from_utc_date - from_date).total_seconds(), 60)
        diff_in_minutes = diff[0]

        regalix_teams = RegalixTeams.objects.filter(id__in=regalix_team)
        post_result_dict = {process: [] for process in process_type}
        for team in regalix_teams:
            if team.process_type in post_result_dict:
                post_result_dict[team.process_type].append(int(team.id))

        collumn_attr = ['Hours', 'Team']
        s_date = from_date
        while True:
            if s_date <= to_date:
                collumn_attr.append(datetime.strftime(s_date, "%d/%m/%Y"))
                s_date = s_date + timedelta(days=1)
            else:
                break

        total_result = list()
        for rglx_team in regalix_teams:
            team_name = rglx_team.team_name
            if team_name[0] == 'S':
                process_type = 'SHOPPING'
            elif team_name[0] == 'T':
                process_type = 'TAG'
            else:
                process_type = 'WPP'
            # get all appointments for selected dates in given range

            slots_data = Availability.objects.filter(
                date_in_utc__range=(from_date, to_date),
                team__id=rglx_team.id,
                team__process_type=process_type
            ).order_by('team')

            result = list()
            team_name = rglx_team.team_name
            for i in range(0, 24):
                for j in range(00, 60):
                    mydict = {}
                    if len(str(i)) == 1:
                        indx = '0%s' % (i)
                    else:
                        indx = str(i)
                    if len(str(j)) == 1:
                        j = '0%s' % (j)
                    else:
                        j = str(j)
                    hour = "%s:%s" % (indx, j)
                    for ele in collumn_attr:
                        if ele == 'Team':
                            mydict[ele] = team_name
                        elif ele == 'Hours':
                            mydict[ele] = hour
                        else:
                            mydict[ele] = '-'

                    result.append(mydict)

            total_appointments = dict()
            for slot in slots_data:
                # time zone conversion
                requested_date = slot.date_in_utc
                requested_date -= timedelta(minutes=diff_in_minutes)
                _date = datetime.strftime(requested_date, "%d/%m/%Y")
                _time = datetime.strftime(requested_date, "%H:%M")
                availability_count = slot.availability_count
                booked_count = slot.booked_count
                if _date in total_appointments:
                    total_appointments[_date]['booked_count'] += booked_count
                    total_appointments[_date]['availability_count'] += availability_count
                else:
                    total_appointments[_date] = {'booked_count': booked_count, 'availability_count': availability_count}
                val = "%s|%s" % (booked_count, availability_count)

                for rec in result:
                    if str(_time) in rec.values():
                        rec[_date] = val

            total_dict = dict()
            for ele in collumn_attr:
                if ele == 'Team':
                    total_dict[ele] = ''
                elif ele == 'Hours':
                    total_dict[ele] = 'Total'
                else:
                    total_dict[ele] = '-'

            for _date_ele in total_appointments:
                if _date_ele in total_dict:
                    total_dict[_date_ele] = "%s|%s" % (str(total_appointments[_date_ele]['booked_count']), str(total_appointments[_date_ele]['availability_count']))

            total_result.extend(result)
            total_result.append(total_dict)

        filename = "appointments-%s-to-%s" % (datetime.strftime(from_date, "%d-%m-%Y"), datetime.strftime(to_date, "%d-%m-%Y"))
        path = write_appointments_to_csv(total_result, collumn_attr, filename)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response

    return render(request, 'representatives/export_appointments.html', {'teams': teams,
                                                                        'default_teams': default_teams,
                                                                        'process_types': process_types,
                                                                        'default_process_type': default_process_type,
                                                                        'post_result_dict': json.dumps(post_result_dict),
                                                                        'tag_by_team': tag_by_team})


@login_required
def export_appointments_with_schedule_appointments(request):
    """ Export Appointments by Availability/Booked """

    default_process_type = ['TAG', 'SHOPPING', 'WPP']
    process_types = RegalixTeams.objects.exclude(process_type='MIGRATION').values_list('process_type', flat=True).distinct().order_by()
    teams = RegalixTeams.objects.filter(process_type__in=process_types).exclude(team_name='default team')
    default_teams = RegalixTeams.objects.filter(process_type__in=default_process_type, is_active=True).exclude(team_name='default team')

    tag_by_team = dict()
    for team in teams:
        rec = {
            'name': str(team.team_name),
            'id': str(team.id)
        }
        if team.process_type not in tag_by_team:
            tag_by_team[str(team.process_type)] = [rec]
        else:
            tag_by_team[str(team.process_type)].append(rec)

    post_result_dict = {}
    if request.method == 'POST':
        from_date = request.POST.get('date_from')
        to_date = request.POST.get('date_to')
        process_type = request.POST.getlist('selectedProcessType')
        regalix_team = request.POST.getlist('selectedTeams')
        from_date = datetime.strptime(from_date, "%Y/%m/%d %H:%M")
        to_date = datetime.strptime(to_date, "%Y/%m/%d %H:%M")
        to_date = datetime(to_date.year, to_date.month, to_date.day, to_date.hour, to_date.minute, 59)

        time_zone = 'IST'

        selected_tzone = Timezone.objects.get(zone_name=time_zone)
        from_utc_date = SalesforceApi.get_utc_date(from_date, selected_tzone.time_value)
        to_utc_date = SalesforceApi.get_utc_date(to_date, selected_tzone.time_value)
        diff = divmod((from_utc_date - from_date).total_seconds(), 60)
        diff_in_minutes = diff[0]

        regalix_teams = RegalixTeams.objects.filter(id__in=regalix_team)
        post_result_dict = {process: [] for process in process_type}
        for team in regalix_teams:
            if team.process_type in post_result_dict:
                post_result_dict[team.process_type].append(int(team.id))

        collumn_attr = ['Hours', 'Team']
        s_date = from_date
        while True:
            if s_date <= to_date:
                collumn_attr.append((datetime.strftime(s_date, "%d/%m/%Y")) + ' AV|F')
                collumn_attr.append((datetime.strftime(s_date, "%d/%m/%Y")) + ' RS')
                s_date = s_date + timedelta(days=1)
            else:
                break
        total_result = list()
        for rglx_team in regalix_teams:
            team_name = rglx_team.team_name
            if team_name[0] == 'S':
                process_type = 'SHOPPING'
            elif team_name[0] == 'T':
                process_type = 'TAG'
            else:
                process_type = 'WPP'
            # get all appointments for selected dates in given range
            if process_type == 'SHOPPING':
                schedule_data = Leads.objects.exclude(rescheduled_appointment_in_ist=None).filter(
                    rescheduled_appointment_in_ist__range=(from_date, to_date),
                    country__in=rglx_team.location.values_list('location_name'),
                    type_1__in=['Google Shopping Setup', 'Google Shopping Migration']).values('rescheduled_appointment_in_ist').annotate(dcount=Count('rescheduled_appointment_in_ist'))
            elif process_type == 'TAG':
                schedule_data = Leads.objects.exclude(rescheduled_appointment_in_ist=None)
                schedule_data = schedule_data.exclude(type_1__in=['Google Shopping Setup', 'Google Shopping Migration']).filter(
                    rescheduled_appointment_in_ist__range=(from_date, to_date),
                    country__in=rglx_team.location.values_list('location_name')).values('rescheduled_appointment_in_ist').annotate(dcount=Count('rescheduled_appointment_in_ist'))
            else:
                schedule_data = WPPLeads.objects.exclude(rescheduled_appointment_in_ist=None).filter(
                    rescheduled_appointment_in_ist__range=(from_date, to_date),
                    country__in=rglx_team.location.values_list('location_name')).values('rescheduled_appointment_in_ist').annotate(dcount=Count('rescheduled_appointment_in_ist'))

            slots_data = Availability.objects.filter(
                date_in_utc__range=(from_utc_date, to_utc_date),
                team__id=rglx_team.id,
                team__process_type=process_type
            ).order_by('team')

            result = list()
            team_name = rglx_team.team_name
            for i in range(0, 24):
                for j in range(0, 60):
                    mydict = {}
                    if len(str(i)) == 1:
                        indx = '0%s' % (i)
                    else:
                        indx = str(i)
                    if len(str(j)) == 1:
                        j = '0%s' % (j)
                    else:
                        j = str(j)
                    hour = "%s:%s" % (indx, j)
                    for ele in collumn_attr:
                        if ele == 'Team':
                            mydict[ele] = team_name
                        elif ele == 'Hours':
                            mydict[ele] = hour
                        else:
                            mydict[ele] = '-'

                    result.append(mydict)

            total_appointments = dict()
            for data in schedule_data:
                requested_date = data.get('rescheduled_appointment_in_ist')
                _date = (datetime.strftime(requested_date, "%d/%m/%Y")+ ' RS')
                _time = datetime.strftime(requested_date, "%H:%M")
                booked_count = data.get('dcount')
                if _date in total_appointments:
                    total_appointments[_date]['booked_count'] += booked_count
                else:
                    total_appointments[_date] = {'booked_count': booked_count}
                val = "%s" % (booked_count)

                for rec in result:
                    if str(_time) in rec.values():
                        rec[_date] = val

            total_schedule = dict()
            for slot in slots_data:
                # time zone conversion
                requested_date = slot.date_in_utc
                requested_date -= timedelta(minutes=diff_in_minutes)
                _date = (datetime.strftime(requested_date, "%d/%m/%Y")+ ' AV|F')
                _time = datetime.strftime(requested_date, "%H:%M")
                availability_count = slot.availability_count
                booked_count = slot.booked_count
                if _date in total_schedule:
                    total_schedule[_date]['booked_count'] += booked_count
                    total_schedule[_date]['availability_count'] += availability_count
                else:
                    total_schedule[_date] = {'booked_count': booked_count, 'availability_count': availability_count}
                val = "%s|%s" % (booked_count, availability_count)

                for rec in result:
                    if str(_time) in rec.values():
                        rec[_date] = val

            total_dict = dict()
            for ele in collumn_attr:
                if ele == 'Team':
                    total_dict[ele] = ''
                elif ele == 'Hours':
                    total_dict[ele] = 'Total'
                else:
                    total_dict[ele] = '-'

            for _date_ele in total_schedule:
                if _date_ele in total_dict:
                    total_dict[_date_ele] = "%s|%s" % (str(total_schedule[_date_ele]['booked_count']), str(total_schedule[_date_ele]['availability_count']))

            for _date_ele in total_appointments:
                if _date_ele in total_dict:
                    total_dict[_date_ele] = "%s" % (str(total_appointments[_date_ele]['booked_count']))

            total_result.extend(result)
            total_result.append(total_dict)

        # remove empty records from total_result
        filter_result = list()
        for each_result in total_result:
            count = 0
            for key, value in each_result.iteritems():
                if each_result[key] == '-':
                    count += 1
                if count == (len(collumn_attr) - 2):
                    filter_result.append(each_result)

        for each_result in filter_result:
            if each_result in total_result:
                total_result.remove(each_result)

        filename = "appointments-%s-to-%s" % (datetime.strftime(from_date, "%d-%m-%Y"), datetime.strftime(to_date, "%d-%m-%Y"))
        path = write_appointments_to_csv(total_result, collumn_attr, filename)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response

    return render(request, 'representatives/export_appointments_with_schedule_appointments.html', {'teams': teams,
                                                                                                   'default_teams': default_teams,
                                                                                                   'process_types': process_types,
                                                                                                   'default_process_type': default_process_type,
                                                                                                   'post_result_dict': json.dumps(post_result_dict),
                                                                                                   'tag_by_team': tag_by_team})


def write_appointments_to_csv(result, collumn_attr, filename):
    path = "/tmp/%s.csv" % (filename)
    DownloadLeads.conver_to_csv(path, result, collumn_attr)
    return path


def get_created_or_updated_slot_details(team, _date, selected_tzone, prev_available_cnt, updated_cnt):
    slot = {}
    ist_date = SalesforceApi.convert_utc_to_timezone(_date, selected_tzone.time_value)
    date_time = datetime.strftime(ist_date, '%b %d, %Y-%I:%M %p').split('-')
    _date, _time = date_time[0], date_time[1]
    slot['team'] = team
    slot['date'] = _date
    slot['time'] = _time
    slot['date_time'] = datetime.strftime(ist_date, '%Y-%m-%d %I:%M %p')
    slot['prev_available_cnt'] = int(prev_available_cnt)
    slot['updated_cnt'] = updated_cnt
    return slot


def mail_slot_changes(request, selected_team, changed_records):
    if request.POST.get('process_type') != 'WPP':
        signature = 'Tag Team'
    else:
        signature = 'WPP Team'
    mail_body = get_template('representatives/slot_changes_mail.html').render(
        Context({
            'records': changed_records,
            'team': selected_team,
            'signature': signature
        })
    )
    mail_subject = "Hey!!! %s, %s Booked %s Appointment Slot" % (
        request.user.first_name, request.user.last_name, selected_team.team_name)

    team_lead = [str(leader.email) for leader in selected_team.team_lead.all()]
    team_manager = [str(manager.email) for manager in selected_team.team_manager.all()]
    email_list = team_lead + team_manager
    mail_to = set(
        email_list
    )

    bcc = set([])

    mail_from = 'google@regalix-inc.com'

    attachments = list()

    send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)


@login_required
def total_appointments(request, plan_month=0, plan_day=0, plan_year=0):
    """ Manage scheduling appointments"""
    default_process_type = ['TAG', 'SHOPPING', 'WPP']
    process_type = ['TAG', 'SHOPPING', 'WPP']
    exclude_types = ['MIGRATION']
    if request.user.groups.filter(name='OPERATIONS'):
        if not request.user.groups.filter(Q(name='WPP') | Q(name='TAG-AND-WPP')):
            exclude_types.append('WPP')
        teams = RegalixTeams.objects.filter(process_type__in=process_type, is_active=True).exclude(team_name='default team')
        process_types = RegalixTeams.objects.exclude(process_type__in=exclude_types).values_list('process_type', flat=True).distinct().order_by()
    else:
        process_types = RegalixTeams.objects.exclude(
            process_type='MIGRATION').filter(Q(team_lead__in=[request.user.id]) | Q(team_manager__in=[request.user.id]), is_active=True).values_list('process_type', flat=True).distinct().order_by()

        teams = RegalixTeams.objects.filter(Q(team_lead__in=[request.user.id]) | Q(team_manager__in=[request.user.id]), process_type__in=process_types, is_active=True).exclude(team_name='default team').distinct().order_by()
    if not teams:
        # if team is not specified, select first team by default
        return render(
            request,
            'representatives/total_appointments.html',
            {'error': True,
             'message': "No Teams"
             }
        )

    team_ids = RegalixTeams.objects.filter(process_type__in=process_type, is_active=True).exclude(team_name='default team').values('id')
    time_zone = 'IST'
    post_result_dict = {}
    if request.method == 'POST':
        if 'prev_week_start_date' in request.POST:
            team_ids = request.POST.get('prevselectedTeams')
            process_type = request.POST.get('prevselectedProcessType')
            team_ids = team_ids.split(',')
            process_type = process_type.split(',')
            week_start_date = datetime.strptime(str(request.POST.get('prev_week_start_date')), '%m-%d-%Y')
            plan_year, plan_month, plan_day = week_start_date.year, week_start_date.month, week_start_date.day
        elif 'next_week_start_date' in request.POST:
            team_ids = request.POST.get('nextselectedTeams')
            process_type = request.POST.get('nextselectedProcessType')
            team_ids = team_ids.split(',')
            process_type = process_type.split(',')
            week_start_date = datetime.strptime(str(request.POST.get('next_week_start_date')), '%m-%d-%Y')
            plan_year, plan_month, plan_day = week_start_date.year, week_start_date.month, week_start_date.day
        else:
            team_ids = request.POST.getlist('selectedTeams')
            process_type = request.POST.getlist('selectedProcessType')
            week_start_date = datetime.strptime(str(request.POST.get('schedule_week_start_date')), '%m-%d-%Y')
            plan_year, plan_month, plan_day = week_start_date.year, week_start_date.month, week_start_date.day

        selected_teams = RegalixTeams.objects.filter(id__in=team_ids)
        post_result_dict = {process: [] for process in process_type}
        for team in selected_teams:
            if team.process_type in post_result_dict:
                post_result_dict[team.process_type].append(int(team.id))

    teams = RegalixTeams.objects.filter(process_type__in=process_type, is_active=True).exclude(team_name='default team')
    default_teams = RegalixTeams.objects.filter(process_type__in=default_process_type, is_active=True).exclude(team_name='default team')
    process_types = RegalixTeams.objects.exclude(process_type__in=exclude_types).values_list('process_type', flat=True).distinct().order_by()

    if not int(plan_month):
        # if month is not specified, select current month
        today = datetime.today()
        plan_month = today.month
        return redirect(
            'representatives.views.total_appointments',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
            # process_type=process_type,
            # team_id=team_id
        )

    if not int(plan_day):
        # if day is not specified, select today's day
        today = datetime.today()
        plan_day = today.day
        return redirect(
            'representatives.views.total_appointments',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
            # process_type=process_type,
            # team_id=team_id
        )

    if not int(plan_year):
        # if year is not specified, select current year
        today = datetime.today()
        plan_year = today.year
        return redirect(
            'representatives.views.total_appointments',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
            # process_type=process_type,
            # team_id=team_id
        )

    # create date from week start day
    plan_date = datetime(int(plan_year), int(plan_month), int(plan_day))
    # if week start day is not monday, select appropriate start week day of given date
    if plan_date.weekday():
        plan_date -= timedelta(days=plan_date.weekday())
        return redirect(
            'representatives.views.total_appointments',
            plan_month=plan_date.month,
            plan_day=plan_date.day,
            plan_year=plan_date.year,
            # process_type=process_type,
            # team_id=team_id
        )

    # prepare slot dates to display
    plan_dates = {
        'day1': plan_date,
        'day2': plan_date + timedelta(days=1),
        'day3': plan_date + timedelta(days=2),
        'day4': plan_date + timedelta(days=3),
        'day5': plan_date + timedelta(days=4),
        'day6': plan_date + timedelta(days=5)
    }

    # compute next week and previous week start dates
    prev_week = plan_date + timedelta(days=-7)
    next_week = plan_date + timedelta(days=7)

    tzone = Timezone.objects.get(zone_name=time_zone)
    utc_date = SalesforceApi.get_utc_date(plan_date, tzone.time_value)
    utc_start_date = utc_date
    utc_end_date = utc_start_date + timedelta(days=6)

    process = json.dumps(process_type)
    selected_teams = RegalixTeams.objects.filter(id__in=team_ids)

    result_dict = {process: [] for process in process_type}
    for team in selected_teams:
        if team.process_type in result_dict:
            result_dict[team.process_type].append(int(team.id))

    appointments_list = Availability.objects.filter(
        date_in_utc__range=(utc_start_date, utc_end_date),
        team__in=selected_teams)

    diff = divmod((utc_date - plan_date).total_seconds(), 60)
    diff_in_minutes = diff[0]
    total_booked = dict()
    total_available = dict()
    # prepare appointments slot keys
    appointments = dict()
    for key, _date in plan_dates.items():
        total_booked[datetime.strftime(_date, '%Y_%m_%d')] = []
        total_available[datetime.strftime(_date, '%Y_%m_%d')] = []
        for hour in range(24):
            # even hour slot
            minutes = 0
            even_key = 'input_'  # input_16_6_2014_0_00
            even_key += '0' + str(_date.day) if len(str(_date.day)) == 1 else str(_date.day)
            even_key += '_'
            even_key += '0' + str(_date.month) if len(str(_date.month)) == 1 else str(_date.month)
            even_key += '_' + str(_date.year) + '_' + str(hour) + '_' + str(minutes)

            appointments[even_key] = dict()
            appointments[even_key]['value'] = 0
            appointments[even_key]['booked'] = 0
            appointments[even_key]['disabled'] = True if datetime(
                _date.year, _date.month, _date.day, hour, minutes) < datetime.utcnow() else False

            # odd hour slot
            minutes = 30
            odd_key = 'input_'  # input_16_6_2014_0_00
            odd_key += '0' + str(_date.day) if len(str(_date.day)) == 1 else str(_date.day)
            odd_key += '_'
            odd_key += '0' + str(_date.month) if len(str(_date.month)) == 1 else str(_date.month)
            odd_key += '_' + str(_date.year) + '_' + str(hour) + '_' + str(minutes)

            appointments[odd_key] = dict()
            appointments[odd_key]['value'] = 0
            appointments[odd_key]['booked'] = 0
            appointments[odd_key]['disabled'] = True if datetime(
                _date.year, _date.month, _date.day, hour, minutes) < datetime.utcnow() else False

    # calculate slots available vs booked for week
    for apptmnt in appointments_list:
        apptmnt.date_in_utc -= timedelta(minutes=diff_in_minutes)

        key = 'input_' + datetime.strftime(apptmnt.date_in_utc, '%d_%m_%Y') + \
            '_' + str(apptmnt.date_in_utc.hour) + '_' + str(apptmnt.date_in_utc.minute)
        appointments[key]['value'] += int(apptmnt.availability_count)
        appointments[key]['booked'] += int(apptmnt.booked_count)

        total_available[datetime.strftime(apptmnt.date_in_utc, '%Y_%m_%d')].append(int(apptmnt.availability_count))
        total_booked[datetime.strftime(apptmnt.date_in_utc, '%Y_%m_%d')].append(int(apptmnt.booked_count))
    total_slots = list()
    for key, value in sorted(total_available.iteritems()):
        total_slots.append({'available': sum(value), 'booked': sum(total_booked[key])})

    return render(
        request,
        'representatives/total_appointments.html',
        {'schedule_date': plan_date,
         'time_zone': time_zone,
         'dates': plan_dates,
         'appointments': appointments,
         'prev_week': prev_week,
         'next_week': next_week,
         'default_teams': default_teams,
         'teams': teams,
         'plan_month': plan_month,
         'plan_day': plan_day,
         'plan_year': plan_year,
         'process_type': process_type,
         'process_types': process_types,
         'total_slots': total_slots,
         'result_dict': json.dumps(result_dict),
         'process': process,
         'default_process_type': default_process_type,
         'post_result_dict': json.dumps(post_result_dict),
         }
    )


def appointments_calendar(request):
    from leads.models import Leads
    from django.db.models import Count
    total_events = list()
    leads_dict = Leads.objects.exclude(rescheduled_appointment_in_ist=None).values('rescheduled_appointment_in_ist', 'customer_id').annotate(count=Count('pk'))
    for res_time in leads_dict:
        if res_time['rescheduled_appointment_in_ist']:
            res_dict = dict()
            res_dict['title'] = ' CID - %s, Total Resch - %s' % (str(res_time['customer_id']), res_time['count'])
            res_dict['start'] = datetime.strftime(res_time['rescheduled_appointment_in_ist'], "%Y-%m-%dT%H:%M:%S")
            res_dict['end'] = datetime.strftime(res_time['rescheduled_appointment_in_ist'] + timedelta(minutes=20), "%Y-%m-%dT%H:%M:%S")
            total_events.append(res_dict)
    return render(request, 'representatives/appointments_calendar.html', {'events': total_events})


@login_required
def tat_details(request, plan_month=0, plan_day=0, plan_year=0):
    """ Manage scheduling appointments"""

    if not int(plan_month):
        # if month is not specified, select current month
        today = datetime.today()
        plan_month = today.month
        return redirect(
            'representatives.views.tat_details',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
        )

    if not int(plan_day):
        # if day is not specified, select today's day
        today = datetime.today()
        plan_day = today.day
        return redirect(
            'representatives.views.tat_details',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
        )

    if not int(plan_year):
        # if year is not specified, select current year
        today = datetime.today()
        plan_year = today.year
        return redirect(
            'representatives.views.tat_details',
            plan_month=plan_month,
            plan_day=plan_day,
            plan_year=plan_year,
        )

    # create date from week start day
    plan_date = datetime(int(plan_year), int(plan_month), int(plan_day))
    # if week start day is not monday, select appropriate start week day of given date
    if plan_date.weekday():
        plan_date -= timedelta(days=plan_date.weekday())
        return redirect(
            'representatives.views.tat_details',
            plan_month=plan_date.month,
            plan_day=plan_date.day,
            plan_year=plan_date.year,
        )

    if request.method == 'POST':
        # time_zone = 'IST'
        # selected_tzone = Timezone.objects.get(zone_name=time_zone)
        for key, value in request.POST.items():
            if key.startswith('input'):
                data_in_a_day = int(request.POST.get(key) or 0)
                keys = key.split('_')  # input_16_6_2014_0_0 / input_16_6_2014_0_30
                slot_day = int(keys[1])
                slot_month = int(keys[2])
                slot_year = int(keys[3])
                slot_type = keys[4]
                slot_date = datetime(slot_year, slot_month, slot_day)
                # utc_date = SalesforceApi.get_utc_date(slot_date, selected_tzone.time_value)
                if slot_type == 'count':
                    emp_count = int(data_in_a_day)
                    try:
                        tat_record = AvailabilityForTAT.objects.get(date_in_ist=slot_date)
                        tat_record.availability_count = emp_count
                        tat_record.save()
                    except ObjectDoesNotExist:
                        tat_record = AvailabilityForTAT(date_in_ist=slot_date, availability_count=emp_count)
                        tat_record.save()
                else:
                    audits_per_day = int(data_in_a_day)
                    try:
                        tat_record = AvailabilityForTAT.objects.get(date_in_ist=slot_date)
                        tat_record.audits_per_date = audits_per_day
                        tat_record.save()
                    except ObjectDoesNotExist:
                        tat_record = AvailabilityForTAT(date_in_ist=slot_date, audits_per_date=audits_per_day)
                        tat_record.save()

    plan_dates = OrderedDict()
    for i in range(1, 6):
        plan_dates['day' + str(i)] = plan_date + timedelta(i - 1)

    counts_list = list()
    for key, _date in plan_dates.items():
        mydict = dict()
        count_key = 'input_'
        count_key += '0' + str(_date.day) if len(str(_date.day)) == 1 else str(_date.day)
        count_key += '_'
        count_key += '0' + str(_date.month) if len(str(_date.month)) == 1 else str(_date.month)
        count_key += '_' + str(_date.year)
        mydict['input'] = count_key
        mydict['count'] = 1
        mydict['audit'] = 3
        counts_list.append(mydict)

    week_start = plan_date
    week_end = plan_date + timedelta(4)
    details = AvailabilityForTAT.objects.filter(date_in_ist__gte=week_start, date_in_ist__lte=week_end).order_by('date_in_ist')
    for detail in details:
        _date = detail.date_in_ist
        count_key = 'input_'
        count_key += '0' + str(_date.day) if len(str(_date.day)) == 1 else str(_date.day)
        count_key += '_'
        count_key += '0' + str(_date.month) if len(str(_date.month)) == 1 else str(_date.month)
        count_key += '_' + str(_date.year)
        for each_dict in counts_list:
            if each_dict['input'] == count_key:
                each_dict['count'] = detail.availability_count
                each_dict['audit'] = detail.audits_per_date

    # compute next week and previous week start dates
    prev_week = plan_date + timedelta(days=-6)
    next_week = plan_date + timedelta(days=8)

    return render(
        request,
        'representatives/tat_details.html',
        {'schedule_date': plan_date,
         'dates': plan_dates,
         'prev_week': prev_week,
         'next_week': next_week,
         'plan_month': plan_month,
         'plan_day': plan_day,
         'plan_year': plan_year,
         'counts_dict': counts_list,
         'picasso': True,
         }
    )
