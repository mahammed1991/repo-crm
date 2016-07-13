
import re
import json
from datetime import datetime
from collections import OrderedDict
import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden

from leads.models import PicassoLeads, Leads, Team, Location, Timezone, CodeType
from report_services import ReportService, DownloadLeads, TrendsReportServices
from lib.helpers import get_quarter_date_slots, is_manager, get_user_under_manager, wpp_user_required, tag_user_required, logs_to_events, prev_quarter_date_range, get_unique_uuid
from reports.models import LeadSummaryReports, KickOffProgram, KickoffTagteam, ChromebookInventory
from main.models import UserDetails, WPPMasterList
from reports.models import Region, CallLogAccountManager, MeetingMinutes, MeetingActionItems
from lib.helpers import (send_mail)
from models import RLSABulkUpload


@login_required
@tag_user_required
def reports(request):
    """ New Report """
    report_type = 'default_report'
    report_timeline = ['today']
    start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    manager = is_manager(request.user.email)
    team_members = list()
    if manager:
        members = get_user_under_manager(request.user.email)
        team_members.append(request.user)
        for member in members:
            team_members.append(member)

    locations = ReportService.get_all_locations()
    teams = ReportService.get_all_teams()
    rgx_teams = Region.objects.all()
    if '' in teams:
        teams.remove('')
        teams.append('Other')
    code_types = ReportService.get_all_code_type()
    code_types = [str(codes.encode('utf-8')) for codes in code_types]
    report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, locations, start_date, end_date, list())
    if len(report_timeline) > 1:
        tag = "Week On Week Trends"
    else:
        if str(report_timeline[0]) in ['today', 'this_week', 'last_week', 'this_month', 'last_month']:
            tag = "Week On Week Trends"
        elif str(report_timeline[0]) == 'this_quarter':
            tag = "Month On Month Trends"
    report_details = {'reports': report_detail, 'code_types': code_types,
                      'report_type': report_type, 'report_timeline': report_timeline, 'team': teams, 'tag': tag}
    return render(request, 'reports/reports.html', {'locations': locations, 'manager': manager, 'team_members': team_members,
                                                    'teams': teams, 'rgx_teams': rgx_teams, 'code_types': code_types, 'report_details': json.dumps(report_details)})


@login_required
@tag_user_required
def reports_new(request):
    """New Report"""
    report_type = 'default_report'
    report_timeline = ['this_quarter']
    start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    manager = is_manager(request.user.email)
    team_members = list()
    if manager:
        members = get_user_under_manager(request.user.email)
        team_members.append(request.user)
        for member in members:
            team_members.append(member)
    locations = ReportService.get_all_locations()
    teams = ReportService.get_all_teams()
    rgx_teams = Region.objects.all()
    if '' in teams:
        teams.remove('')
        teams.append('Other')
    code_types = ReportService.get_all_code_type()
    code_types = [str(codes.encode('utf-8')) for codes in code_types]
    report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, locations, start_date, end_date, list())
    if len(report_timeline) > 1:
        tag = "Week On Week Trends"
    else:
        if str(report_timeline[0]) in ['today', 'this_week', 'last_week', 'this_month', 'last_month']:
            tag = "Week On Week Trends"
        elif str(report_timeline[0]) == 'this_quarter':
            tag = "Month On Month Trends"
    report_details = {'reports': report_detail, 'code_types': code_types,
                      'report_type': report_type, 'report_timeline': report_timeline, 'team': teams, 'tag': tag}
    return render(request, 'reports/reports_new.html', {'locations': locations, 'manager': manager, 'team_members': team_members,
                                                        'teams': teams, 'rgx_teams': rgx_teams, 'code_types': code_types, 'report_details': json.dumps(report_details)})


@login_required
def get_selected_new_reports(request):
    """ New Report Details
    """
    report_detail = dict()
    if request.is_ajax():
        report_type = request.GET.get('report_type', None)
        report_timeline = request.GET.getlist('report_timeline[]')
        region = request.GET.get('region')
        countries = request.GET.getlist('countries[]')
        teams = request.GET.getlist('team[]')
        team_members = request.GET.getlist('team_members[]')
        ldap_id = request.GET.get('ldap_id', None)
        program_split = request.GET.get('program_split', None)
        location_split = request.GET.get('location_split', None)

        report_details = dict()
        emails = list()
        if report_type == 'leadreport_individualRep':
            if ldap_id:
                email = User.objects.select_related('email').get(pk=ldap_id)
                emails = [email]
            else:
                email = request.user.email
                emails = [email]

        if 'all' in team_members:
            if len(team_members) > 1:
                team_members.remove('all')
            else:
                team_members = team_members

        if report_type == 'leadreport_teamLead':
            emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))

        teams, team_members, countries, start_date, end_date, code_types, emails, leads = ReportService.get_related_data_for_reports(teams, team_members, region, report_timeline, emails, countries)

        lead_ids = leads
        # if '' in teams:
        #     teams.remove('')
        report_split_detail = dict()
        # if report_type == 'default_report':
        #     report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, list())
        if report_type == 'leadreport_individualRep':
            report_detail = ReportService.get_leads_status_summary(lead_ids)
        elif report_type == 'leadreport_teamLead':
            team_emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
            report_detail = ReportService.get_leads_status_summary(lead_ids)
        elif report_type == 'leadreport_programview':
            report_detail = ReportService.get_leads_status_summary(lead_ids)
            if program_split:
                report_split_detail['program_report'] = ReportService.get_program_report_by_locations(teams, countries, code_types)
        elif report_type == 'leadreport_regionview':
            report_detail = ReportService.get_leads_status_summary(lead_ids)
            if location_split:
                report_split_detail['region_report'] = ReportService.get_region_report_by_program(countries, teams, code_types)
        else:
            pass

        report_details = {'reports': report_detail, 'report_type': report_type, 'report_timeline': report_timeline,
                          'region': region, 'report_split_detail': report_split_detail}

        return HttpResponse(json.dumps(report_details))


def get_selected_report_view(request):
    report_detail = dict()
    if request.is_ajax:
        report_view_type = request.GET.get('report_view_type')
        report_type = request.GET.get('report_type', None)
        report_timeline = request.GET.getlist('report_timeline[]')
        region = request.GET.get('region')
        countries = request.GET.getlist('countries[]')
        teams = request.GET.getlist('team[]')
        team_members = request.GET.getlist('team_members[]')
        ldap_id = request.GET.get('ldap_id', None)
        program_split = request.GET.get('program_split', None)
        location_split = request.GET.get('location_split', None)

        report_details = dict()
        emails = list()
        if report_type == 'leadreport_individualRep':
            if ldap_id:
                email = User.objects.select_related('email').get(pk=ldap_id)
                emails = [email]
            else:
                email = request.user.email
                emails = [email]

        if 'all' in team_members:
            if len(team_members) > 1:
                team_members.remove('all')
            else:
                team_members = team_members

        if report_type == 'leadreport_teamLead':
            emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
            emails.append(emails)

        teams, team_members, countries, start_date, end_date, code_types, emails, leads = ReportService.get_related_data_for_reports(teams, team_members, region, report_timeline, emails, countries)

        lead_ids = leads
        report_split_detail = dict()
        lead_status_summary = list()
        lead_status_analysis_table_grp = list()
        pie_chart_dict = dict()
        timeline_chart_details = list()

        if location_split:
            report_split_detail['region_report'] = ReportService.get_region_report_by_program(countries, teams, code_types)

        if program_split:
            report_split_detail['program_report'] = ReportService.get_program_report_by_locations(teams, countries, code_types)

        if report_view_type == 'lead_summary_status':
            lead_status_summary = ReportService.get_leads_status_summary(lead_ids)
        elif report_view_type == 'task_type_analysis':
            for code_type in code_types:
                lead_status_analysis_grp = {code_type: ''}
                leads_per_code_type_grp = Leads.objects.filter(type_1=code_type, id__in=lead_ids).values('lead_status').annotate(dcount=Count('lead_status'))
                lead_status_analysis_grp[code_type] = ReportService.get_lead_status_analysis(leads_per_code_type_grp)
                lead_status_analysis_table_grp.append(lead_status_analysis_grp)

            for cod_typ in lead_status_analysis_table_grp:
                key = cod_typ.keys()[0]
                value = cod_typ[key]['Total']
                pie_chart_dict[key] = value
        elif report_view_type == 'week_on_week_trends':
            timeline_chart_details = ReportService.get_timeline_chart_details(report_timeline, lead_ids, countries, teams, code_types, emails)
        else:
            pass

        if len(report_timeline) > 1:
            tag = "Week On Week Trends"
        else:
            if str(report_timeline[0]) in ['today', 'this_week', 'last_week', 'this_month', 'last_month']:
                tag = "Week On Week Trends"
            elif str(report_timeline[0]) == 'this_quarter':
                tag = "Month On Month Trends"

        report_details = {'report_split_detail': report_split_detail, 'report_timeline': report_timeline, 'report_type': report_type, 'report_view_type': report_view_type, 
                          'lead_status_summary': lead_status_summary, 'lead_status_analysis_table_grp': sorted(lead_status_analysis_table_grp),
                          'pie_chart_dict': pie_chart_dict, 'timeline_chart_details': timeline_chart_details, 'tag': tag, 'code_types': code_types,
                          'table_header': settings.LEAD_STATUS_DICT, 'sort_keys': sorted(timeline_chart_details)}

        return HttpResponse(json.dumps(report_details))


@login_required
def get_current_quarter_report(request):
    ''' Get Reports of Current Quarter '''
    # by default should be current Quarter
    start_date, end_date = get_quarter_date_slots(datetime.utcnow())
    code_types = ReportService.get_all_code_type()
    code_types = [str(codes.encode('utf-8')) for codes in code_types if 'www.' not in codes and 'http:' not in codes and 'https:' not in codes]
    lead_status = [l for l in settings.LEAD_STATUS]

    if 'In Queue' in lead_status:
            lead_status.append('Appointment Set (GS)')
    if 'In Progress' in lead_status:
        lead_status.extend(['Pending QC - DEAD LEAD', 'Pending QC - WIN', 'Rework Required'])

    # ##################### cron job reports for Current Quarter start here ######################
    # Get summary report by code types and lead_status
    c_types = ['total', 'total_tag', 'Google Shopping Migration', 'Google Shopping Setup', 'Existing Datafeed Optimization']
    report_details = LeadSummaryReports.objects.filter(code_type__in=c_types)
    report_detail = dict()
    for rep in report_details:
        report_detail[rep.code_type] = dict()
        report_detail[rep.code_type]['total_leads'] = int(rep.total_leads)
        report_detail[rep.code_type]['wins'] = float(rep.win)
        report_detail[rep.code_type]['Implemented'] = int(rep.implemented)
        report_detail[rep.code_type]['In Queue'] = rep.in_queue
        report_detail[rep.code_type]['tat_implemented'] = int(rep.tat_implemented)
        report_detail[rep.code_type]['tat_first_contacted'] = int(rep.tat_first_contacted)
    # ##################### cron job reports for Current Quarter ends here ######################

    # Get summary report by code types and lead_status
    # report_detail = ReportService.get_summary_by_code_types_and_status(
    #    'tag', code_types, lead_status, start_date, end_date, teams=list(), locations=list())

    quarter = ReportService.get_current_quarter(datetime.utcnow())
    start_month = datetime.strftime(start_date, '%b')
    end_month = datetime.strftime(end_date, '%b')
    report_title = "LEADS %s SUMMARY - %s to %s %s" % (quarter, start_month.upper(), end_month.upper(), datetime.utcnow().year)

    return HttpResponse(json.dumps({'reports': report_detail, 'code_types': code_types, 'report_title': report_title}))


@login_required
def get_new_reports(request):
    """ New Report Details
    """
    report_detail = dict()
    if request.is_ajax():
        report_type = request.GET.get('report_type', None)
        report_timeline = request.GET.getlist('report_timeline[]')
        region = request.GET.get('region')
        countries = request.GET.getlist('countries[]')
        teams = request.GET.getlist('team[]')
        team_members = request.GET.getlist('team_members[]')
        ldap_id = request.GET.get('ldap_id', None)
        program_split = request.GET.get('program_split', None)
        location_split = request.GET.get('location_split', None)

        # Get teams
        if 'all' in teams:
            if len(teams) > 1:
                teams.remove('all')
            else:
                teams = ReportService.get_all_teams()
        else:
            if not teams:
                teams = ReportService.get_all_teams()
            else:
                teams = teams

        # Get teams
        if 'all' in team_members:
            if len(team_members) > 1:
                team_members.remove('all')
            else:
                team_members = team_members

        final_countries = list()

        if region:
            if region == 'all':
                final_countries = ReportService.get_all_locations()
            else:
                if 'all' in countries:
                    if len(countries) > 1:
                        countries.remove('all')
                        final_countries = list(Location.objects.values_list('location_name', flat=True).filter(id__in=countries).distinct().order_by('location_name'))
                    else:
                        final_countries = ReportService.get_all_locations()
                else:
                    final_countries = list(Location.objects.values_list('location_name', flat=True).filter(id__in=countries).distinct().order_by('location_name'))
        else:
            final_countries = ReportService.get_all_locations()

        countries = final_countries

        if report_timeline:
            start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)


        code_types = list(Leads.objects.exclude(type_1__in=['', 'WPP']).filter(created_date__gte=start_date, created_date__lte=end_date).values_list(
            'type_1', flat=True).distinct().order_by('type_1'))
        code_types = [str(codes.encode('utf-8')) for codes in code_types]

        report_details = dict()
        if ldap_id:
            email = User.objects.select_related('email').get(pk=ldap_id)
        else:
            email = request.user.email

        # if '' in teams:
        #     teams.remove('')

        # if report_type == 'default_report':
        #     report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, list())
        if report_type == 'leadreport_individualRep':
            report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, [email])
        elif report_type == 'leadreport_teamLead':
            team_emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
            report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, team_emails)
        elif report_type == 'leadreport_programview':
            report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, list())
            if program_split:
                report_detail['program_report'] = ReportService.get_program_report_by_locations(teams, countries, code_types)
        elif report_type == 'leadreport_regionview':
            report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, list())
            if location_split:
                report_detail['region_report'] = ReportService.get_region_report_by_program(countries, teams, code_types)
        else:
            pass

        if len(report_timeline) > 1:
            tag = "Week On Week Trends"
        else:
            if str(report_timeline[0]) in ['today', 'this_week', 'last_week', 'this_month', 'last_month']:
                tag = "Week On Week Trends"
            elif str(report_timeline[0]) == 'this_quarter':
                tag = "Month On Month Trends"

        report_details = {'reports': report_detail, 'code_types': code_types,
                          'report_type': report_type, 'report_timeline': report_timeline,
                          'region': region, 'team': teams, 'tag': tag}

        return HttpResponse(json.dumps(report_details))


@csrf_exempt
@login_required
def get_download_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('download_report_type')
        report_timeline = request.POST.get('download_report_timeline')
        region = request.POST.get('download_region')
        countries = request.POST.get('download_countries')
        teams = request.POST.get('download_team')
        team_members = request.POST.get('download_team_members')
        selected_fields = request.POST.get('download_selectedFields')
        ldap_id = request.POST.get('form_ldap_id')
        report_timeline = report_timeline.split(',') if report_timeline else []
        countries = countries.split(',') if countries else []
        teams = teams.split(',') if teams else []
        team_members = team_members.split(',') if team_members else []
        selected_fields = selected_fields.split(',') if selected_fields else []
        # Get teams
        if 'all' in teams:
            if len(teams) > 1:
                teams.remove('all')
            else:
                teams = ReportService.get_all_teams()
        else:
            teams = teams

        # Get teams
        if 'all' in team_members:
            if len(team_members) > 1:
                team_members.remove('all')
            else:
                team_members = team_members

        if region == 'all':
            countries = ReportService.get_all_locations()
        else:
            if 'all' in countries:
                if len(countries) > 1:
                    countries.remove('all')
                    countries = list(Location.objects.values_list('location_name', flat=True).filter(id__in=countries).distinct().order_by('location_name'))
                else:
                    countries = ReportService.get_all_locations()
            else:
                countries = list(Location.objects.values_list('location_name', flat=True).filter(id__in=countries).distinct().order_by('location_name'))

        code_types = ReportService.get_all_code_type()
        code_types = [str(codes.encode('utf-8')) for codes in code_types]

        if report_type != 'historical_report':
            if report_timeline:
                if report_timeline > 1:
                    report_timeline = [dt.replace('-', ',') for dt in report_timeline]
                    start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
                    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
                else:
                    start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
                    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        else:
            start_date = re.search(r'\d{4}-\d{2}-\d{2}', report_timeline[0]).group()
            end_date = re.search(r'\d{4}-\d{2}-\d{2}', report_timeline[1]).group()

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            # start_date = start_date + datetime.timedelta(days=1)

            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # end_date = end_date + datetime.timedelta(days=1)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

        if ldap_id:
            email = User.objects.select_related('email').get(pk=ldap_id)
        else:
            email = request.user.email

        if report_type == 'default_report':
            leads = DownloadLeads.get_leads_by_report_type(code_types, teams, countries, start_date, end_date, list())
        elif report_type == 'leadreport_individualRep':
            leads = DownloadLeads.get_leads_by_report_type(code_types, teams, countries, start_date, end_date, [email])
        elif report_type == 'leadreport_teamLead':
            team_emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
            leads = DownloadLeads.get_leads_by_report_type(code_types, teams, countries, start_date, end_date, team_emails)
        elif report_type == 'leadreport_programview':
            leads = DownloadLeads.get_leads_by_report_type(code_types, teams, countries, start_date, end_date, list())
        elif report_type == 'leadreport_regionview':
            leads = DownloadLeads.get_leads_by_report_type(code_types, teams, countries, start_date, end_date, list())
        elif report_type == 'historical_report':
            leads = DownloadLeads.get_leads_by_report_type(code_types, teams, countries, start_date, end_date, list())
        else:
            pass

        path = DownloadLeads.download_lead_report(leads, start_date, end_date, selected_fields)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response


@login_required
@wpp_user_required
def wpp_master_list(request):
    wpp_master_list = WPPMasterList.objects.all()
    return render(request, 'reports/wpp_master_list.html', {'wpp_master_list': wpp_master_list})


@login_required
@wpp_user_required
def wpp_reports(request):
    """ WPP Reports """

    manager = is_manager(request.user.email)
    team_members = list()
    if manager:
        members = get_user_under_manager(request.user.email)
        team_members.append(request.user)
        for member in members:
            team_members.append(member)
    return render(request, 'reports/wpp_reports.html', {'manager': manager, 'team_members': team_members})


def get_wpp_reports(request):
    """ New Report Details
    """
    wpp_report_detail = dict()
    if request.is_ajax():
        report_type = request.GET.get('report_type', None)
        report_timeline = request.GET.getlist('report_timeline[]')
        team_members = request.GET.getlist('team_members[]')

        if report_timeline:
            start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

        wpp_report_details = dict()

        # Get teams
        if 'all' in team_members:
            if len(team_members) > 1:
                team_members.remove('all')
            else:
                team_members = team_members
        if report_type == 'default_report':
            wpp_report_detail = ReportService.get_wpp_report_details_for_filters(start_date, end_date, list())
        elif report_type == 'leadreport_individualRep':
            wpp_report_detail = ReportService.get_wpp_report_details_for_filters(start_date, end_date, [request.user.email])
        elif report_type == 'leadreport_teamLead':
            team_emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
            wpp_report_detail = ReportService.get_wpp_report_details_for_filters(start_date, end_date, team_emails)
        elif report_type == 'leadreport_superUser':
            wpp_report_detail = ReportService.get_wpp_report_details_for_filters(start_date, end_date, list())
        else:
            pass

        wpp_report_detail['treatment_type_header'] = [sts for sts in settings.WPP_LEAD_STATUS]
        wpp_report_detail['treatment_type_header'].append('TAT')
        wpp_report_detail['treatment_type_header'].append('TOTAL')

        status_list = [status for status in settings.WPP_LEAD_STATUS]
        status_list.append('TOTAL')
        bar_chart_data = [['Lead Status']]
        for status in status_list:
            status_row = [status]
            for treatment_type in wpp_report_detail['wpp_treatment_type_analysis']:
                status_row.append(wpp_report_detail['wpp_treatment_type_analysis'][treatment_type][status])
            bar_chart_data.append(status_row)
        bar_chart_data[0].extend(wpp_report_detail['wpp_treatment_type_analysis'].keys())

        wpp_report_detail['bar_chart_data'] = bar_chart_data
        wpp_report_details = {'reports': wpp_report_detail,
                              'report_type': report_type, 'report_timeline': report_timeline}
        
        del wpp_report_details['reports']['wpp_lead_status_analysis']['nominated_leads']
        return HttpResponse(json.dumps(wpp_report_details))


@login_required
def get_user_name(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        if ' ' in query:
            query = query.split(' ')[0]
        qs = User.objects.all()
        users = qs.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.first_name + " " + user.last_name
            user_json['value'] = user.first_name + " " + user.last_name
            user_json['username'] = user.username
            try:
                user_details = UserDetails.objects.get(user_id=user.id)
                user_json['manager'] = user_details.user_manager_name if user_details.user_manager_name else None
                user_json['team'] = user_details.team.team_name if user_details.team else None
                user_json['region'] = user_details.location.location_name if user_details.location else None
            except UserDetails.DoesNotExist:
                user_json['manager'] = None
                user_json['team'] = None
                user_json['region'] = None
            results.append(user_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def get_countries(request):
    if request.is_ajax():
        region_id = request.GET.get('team_id')
        regn = Region.objects.get(pk=region_id)
        locations = regn.location.all()
        countries = list()
        for location in locations:
            countries.append({"id": location.id, "name": location.location_name})
        return HttpResponse(json.dumps(countries))


@login_required
def get_reports(request):
    ''' Get report by Filter '''
    if request.is_ajax():
        # Get type of report
        # report_type = request.GET.get('report_type', None)
        report_type = "lead_report"

        # Get process filters
        # Get Lead Status
        lead_status = request.GET.getlist('lead_status[]')
        if 'all' in lead_status:
            if len(lead_status) > 1:
                lead_status.remove('all')
            else:
                # get all lead status
                lead_status = [l for l in settings.LEAD_STATUS]

        if 'In Queue' in lead_status:
            lead_status.append('Appointment Set (GS)')
        if 'In Progress' in lead_status:
            lead_status.extend(['Pending QC - DEAD LEAD', 'Pending QC - WIN', 'Rework Required'])

        # Get Code Types
        code_types = request.GET.getlist('code_types[]')
        if 'all' in code_types:
            if len(code_types) > 1:
                code_types.remove('all')
            else:
                # get all code types
                code_types = ReportService.get_all_code_type()
        code_types = [str(codes.encode('utf-8')) for codes in code_types if 'www.' not in codes and 'http:' not in codes and 'https:' not in codes]

        # Get timeline filters
        quarterly = request.GET.get('quarterly', None)
        monthly = request.GET.get('monthly', None)
        weekly = request.GET.get('weekly', None)
        date_range = request.GET.getlist('date_range[]')
        # Get other filters
        location = request.GET.getlist('location[]')
        team = request.GET.getlist('team[]')

        # Get locations
        if 'all' in location:
            if len(location) > 1:
                location.remove('all')
            else:
                location = ReportService.get_all_locations()
        locations = [str(loc) for loc in location]

        # Get teams
        if 'all' in team:
            if len(team) > 1:
                team.remove('all')
            else:
                team = ReportService.get_all_teams()
        teams = [str(t) for t in team]

        # split by location or team
        program_split = request.GET.get('team_split', None)
        location_split = request.GET.get('location_split', None)
        status_split = request.GET.get('status_split', None)
        code_split = request.GET.get('code_split', None)

        # Getting TAT report
        report_stage = request.GET.get('stage', None)

        # Get date range by timeline filter
        timeline = dict()
        if quarterly or monthly or weekly or date_range:
            timeline['quarterly'] = request.GET.get('quarterly', None)
            timeline['monthly'] = request.GET.get('monthly', None)
            timeline['weekly'] = request.GET.get('weekly', None)
            timeline['date_range'] = request.GET.getlist('date_range[]')
            start_date, end_date = ReportService.get_date_range_by_timeline(timeline)
        else:
            # by default should be current Quarter
            start_date, end_date = get_quarter_date_slots(datetime.utcnow())
            timeline['quarterly'] = ReportService.get_current_quarter(datetime.utcnow())

        report_summary = dict()
        # Get summary report by code types and lead_status only if Implemented in lead status
        if 'Implemented' in lead_status and ReportService.is_all_status_exist(lead_status):
            report_summary = ReportService.get_summary_by_code_types_and_status(
                'all', code_types, lead_status, start_date, end_date, teams, locations)

        # Report Details
        final_report = list()
        total = dict()
        year = datetime.utcnow().year
        month = ''
        report = list()
        total = dict()
        leads = list()
        if not program_split and not location_split and teams and locations:
            leads = ReportService.get_leads_by_teams_and_locations(teams, locations, lead_status, code_types, start_date, end_date)
            if leads:
                # Get reports based on report type, (LEAD or TAT REPORTS)
                if report_type == 'lead_report':
                    report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
            else:
                report = list()
                total = dict()
            final_report.append({'report': report, 'total': total, 'team': teams, 'location': locations})
            report_filter = "both"
        elif teams and locations:
            if len(teams) == 1 and len(locations) == 1:
                team = teams[0]
                location = locations[0]
                leads = ReportService.get_leads_by_team_and_location(
                    team, location, lead_status, code_types, start_date, end_date)
                if leads:
                    # Get reports based on report type, (LEAD or TAT REPORTS)
                    if report_type == 'lead_report':
                        report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                else:
                    report = list()
                    total = dict()
                final_report.append({'team': team if team else 'Other', 'location': location, 'report': report, 'total': total})
                report_filter = "both"
            elif len(teams) == 1 and len(locations) > 1:
                # Check if location wise split or not
                if location_split:
                    for location in locations:
                        leads = ReportService.get_leads_by_team_and_location(
                            teams[0], location, lead_status, code_types, start_date, end_date)
                        if leads:
                            # Get reports based on report type, (LEAD or TAT REPORTS)
                            if report_type == 'lead_report':
                                report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                        else:
                            report = list()
                            total = dict()
                        final_report.append({'team': team if team else 'Other', 'location': location, 'report': report, 'total': total})
                    report_filter = "location"
                else:
                    leads = ReportService.get_leads_by_teams_and_locations(teams, locations, lead_status, code_types, start_date, end_date)
                    if leads:
                        # Get reports based on report type, (LEAD or TAT REPORTS)
                        if report_type == 'lead_report':
                            report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                    else:
                        report = list()
                        total = dict()
                    final_report.append({'report': report, 'total': total, 'team': team, 'location': locations})
                    report_filter = "both"
            elif len(locations) == 1 and len(teams) > 1:
                if program_split:
                    for team in teams:
                        leads = ReportService.get_leads_by_team_and_location(
                            team, locations[0], lead_status, code_types, start_date, end_date)
                        if leads:
                            # Get reports based on report type, (LEAD or TAT REPORTS)
                            if report_type == 'lead_report':
                                report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                        else:
                            report = list()
                            total = dict()
                        final_report.append({'team': team if team else 'Other', 'location': location, 'report': report, 'total': total})
                    report_filter = "team"
                else:
                    leads = ReportService.get_leads_by_teams_and_locations(teams, locations, lead_status, code_types, start_date, end_date)
                    if leads:
                        # Get reports based on report type, (LEAD or TAT REPORTS)
                        if report_type == 'lead_report':
                            report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                    else:
                        report = list()
                        total = dict()
                    final_report.append({'report': report, 'total': total, 'team': teams, 'location': locations})
                    report_filter = "both"
            elif program_split and location_split:
                for team in teams:
                    for location in locations:
                        leads = ReportService.get_leads_by_team_and_location(
                            team, location, lead_status, code_types, start_date, end_date)
                        if leads:
                            # Get reports based on report type, (LEAD or TAT REPORTS)
                            if report_type == 'lead_report':
                                report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                        else:
                            report = list()
                            total = dict()
                        final_report.append({'team': team, 'location': location, 'report': report, 'total': total})
                report_filter = 'both_split'
            elif program_split:
                for team in teams:
                    leads = ReportService.get_leads_by_teams_and_locations(
                        [team], locations, lead_status, code_types, start_date, end_date)
                    if leads:
                        # Get reports based on report type, (LEAD or TAT REPORTS)
                        if report_type == 'lead_report':
                            report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                    else:
                        report = list()
                        total = dict()
                    final_report.append({'team': team, 'location': locations, 'report': report, 'total': total})
                report_filter = "team_split"
            else:
                # report type is location
                for location in locations:
                    leads = ReportService.get_leads_by_teams_and_locations(
                        teams, [location], lead_status, code_types, start_date, end_date)
                    if leads:
                        # Get reports based on report type, (LEAD or TAT REPORTS)
                        if report_type == 'lead_report':
                            report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                    else:
                        report = list()
                        total = dict()
                    final_report.append({'location': location, 'team': teams, 'report': report, 'total': total})
                report_filter = "location_split"
        elif locations and not teams:
            if not location_split:
                leads = ReportService.get_leads_by_locations(
                    locations, lead_status, code_types, start_date, end_date)
                if leads:
                    # Get reports based on report type, (LEAD or TAT REPORTS)
                    if report_type == 'lead_report':
                        report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                else:
                    report = list()
                    total = dict()
                final_report.append({'location': location, 'report': report, 'total': total})
                report_filter = 'normal'
            else:
                for location in locations:
                    leads = ReportService.get_leads_by_location(
                        location, lead_status, code_types, start_date, end_date)
                    if leads:
                        # Get reports based on report type, (LEAD or TAT REPORTS)
                        if report_type == 'lead_report':
                            report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                    else:
                        report = list()
                        total = dict()
                    final_report.append({'location': location, 'report': report, 'total': total})
                report_filter = 'location'
        elif teams and not locations:
            if not program_split:
                leads = ReportService.get_leads_by_teams(
                    teams, lead_status, code_types, start_date, end_date)

                if leads:
                    # Get reports based on report type, (LEAD or TAT REPORTS)
                    if report_type == 'lead_report':
                        report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                else:
                    report = list()
                    total = dict()
                final_report.append({'team': team if team else 'Other', 'report': report, 'total': total})
                report_filter = 'normal'
            else:
                for team in teams:
                    leads = ReportService.get_leads_by_team(
                        team, lead_status, code_types, start_date, end_date)
                    if leads:
                        # Get reports based on report type, (LEAD or TAT REPORTS)
                        if report_type == 'lead_report':
                            report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
                    else:
                        report = list()
                        total = dict()
                    final_report.append({'team': team if team else 'Other', 'report': report, 'total': total})
                report_filter = 'team'
        else:
            leads = ReportService.get_leads_by_status_and_code_types(lead_status, code_types, start_date, end_date)
            if leads:
                # Get reports based on report type, (LEAD or TAT REPORTS)
                if report_type == 'lead_report':
                    report, total = ReportService.get_leads_reports(leads, lead_status, code_types)
            else:
                report = list()
                total = dict()
            final_report.append({'report': report, 'total': total})
            report_filter = "normal"

        # get year and month if reports by perticular month
        if 'monthly' in timeline:
            year = start_date.year
            month = datetime.strftime(start_date, '%B')

        start_date = datetime.strftime(start_date, '%b/%d/%Y') if start_date else ''
        end_date = datetime.strftime(end_date, '%b/%d/%Y') if end_date else ''
        if not report_summary:
            report_summary = ''

        mimetype = 'application/json'
        return HttpResponse(json.dumps({'reports': final_report, 'lead_status': lead_status, 'year': year, 'month': month,
                                        'code_types': code_types, 'report_filter': report_filter, 'locations': locations, 'teams': teams,
                                        'start_date': start_date, 'end_date': end_date, 'stage': report_stage, 'leads': settings.LEAD_STATUS,
                                        'timeline': timeline, 'report_type': report_type, 'status_split': status_split, 'code_split': code_split,
                                        'report_summary': report_summary}), mimetype)


# Download leads to csv
@login_required
def download_leads(request):
    """ Download leads from Database """
    if request.method == 'POST':
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')
        fields_type = request.POST.get('fields_type')
        path = DownloadLeads.download_lead_data(from_date, to_date, fields_type)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response

    return render(request, 'reports/download_leads.html')


# Trends Reports
@login_required
def get_trends_reports(request):
    if request.is_ajax():
        team = request.GET.getlist('teams[]')
        code_types = request.GET.getlist('code_types[]')
        timeline = str(request.GET.get('timeLine'))
        report_type = str(request.GET.get('report_type'))
        reports = list()
        if 'all' in code_types:
            if len(code_types) > 1:
                code_types.remove('all')
            else:
                # get all code types
                code_types = ReportService.get_all_code_type()
        code_types = [str(codes.encode('utf-8')) for codes in code_types if 'www.' not in codes and 'http:' not in codes and 'https:' not in codes]
        # Get teams
        if 'all' in team:
            if len(team) > 1:
                team.remove('all')
            else:
                team = ReportService.get_all_teams()
        teams = [str(t) for t in team]
        if (report_type == 'trend_report_program_wise'):
            reports = TrendsReportServices.get_trends_report_program_wise(teams, code_types, timeline)
        elif(report_type == 'trends_report_for_win_and_total'):
            reports = TrendsReportServices.get_for_win_total_and_conversionratio(teams, code_types, timeline)
    # creating this tableReports for draw table

    table_reports = list()
    for i in range(len(reports[0])):
        table_reports.append([row[i] for row in reports])
    mimetype = 'application/json'
    return HttpResponse(json.dumps({'reports': reports, 'tableReports': table_reports,
                                    'timeline': timeline, 'teams': teams, 'code_types': code_types, 'report_type': report_type}), mimetype)


@login_required
def download_timezones_by_location(request):
    """ List all Timezones by Locations """
    location_list = list()
    locations = Location.objects.all().order_by('location_name')
    path = "/tmp/location_list.csv"
    fields = ['Location Name', 'Zone Name', 'Time Value']

    for location in locations:
        for timezone in location.time_zone.all():
            location_list.append({'Location Name': location.location_name,
                                  'Zone Name': timezone.zone_name, 'Time Value': timezone.time_value})
    DownloadLeads.conver_to_csv(path, location_list, fields)
    response = DownloadLeads.get_downloaded_file_response(path)
    return response


@login_required
@wpp_user_required
def call_audit_sheet(request):
    """ CALL AUDIT SHEET """

    return render(request, 'reports/call_audit_sheet.html')


@login_required
def google_doc(request):

    users = CallLogAccountManager.objects.values_list('username', flat=True).distinct().order_by('username')
    users = [str(user) for user in users]
    call_logs = CallLogAccountManager.objects.all()
    events = logs_to_events(call_logs)
    return render(request, 'reports/calendar_view.html', {'events': events, 'users': users})


def user_events(request):
    users = CallLogAccountManager.objects.values_list('username', flat=True).distinct().order_by('username')
    users = [str(user) for user in users]
    if request.is_ajax():
        user = str(request.GET.get('user'))
        if user != 'all':
            user_logs = CallLogAccountManager.objects.filter(username=user)
        else:
            user_logs = CallLogAccountManager.objects.all()
        events = logs_to_events(user_logs)
    return HttpResponse(json.dumps({'events': events, 'users': users}))


@login_required
def csat_reports(request):
    if request.is_ajax():
        report_type = str(request.GET.get('report_type'))
        timeline = request.GET.getlist('timeline[]')
        comparison = request.GET.get('comparison', None)
        selected_filters = request.GET.getlist('filter[]')
        survey_for_unmapped = None
        if 'survey_channel_phone' in selected_filters:
            channel = 'PHONE'
        elif 'survey_channel_email' in selected_filters:
            channel = 'EMAIL'
        else:
            channel = 'Combined'

        if 'process_tag' in selected_filters:
            process = 'Tag'
        elif 'process_shopping' in selected_filters:
            process = 'Shopping'
        else:
            process = 'Combined'

        if 'survey_category_unmapped' in selected_filters:
            if timeline:
                current_timeline_start, current_timeline_end = ReportService.get_date_range_by_timeline(timeline)
                current_timeline_end = datetime(current_timeline_end.year, current_timeline_end.month, current_timeline_end.day, 23, 59, 59)
            survey_for_unmapped = ReportService.get_unmapped_survey(selected_filters, report_type, current_timeline_start, current_timeline_end)

        if comparison == 'yes':
            if timeline:
                if timeline[0] == 'this_week':
                    current_timeline_start, current_timeline_end = ReportService.get_date_range_by_timeline(timeline)
                    previous_timeline_start, previous_timeline_end = ReportService.get_date_range_by_timeline(['last_week'])
                elif timeline[0] == 'this_month':
                    current_timeline_start, current_timeline_end = ReportService.get_date_range_by_timeline(timeline)
                    previous_timeline_start, previous_timeline_end = ReportService.get_date_range_by_timeline(['last_month'])
                elif timeline[0] == 'this_quarter':
                    current_timeline_start, current_timeline_end = ReportService.get_date_range_by_timeline(timeline)
                    previous_timeline_start, previous_timeline_end = prev_quarter_date_range(datetime.now())

            current_timeline_end = datetime(current_timeline_end.year, current_timeline_end.month, current_timeline_end.day, 23, 59, 59)
            previous_timeline_end = datetime(previous_timeline_end.year, previous_timeline_end.month, previous_timeline_end.day, 23, 59, 59)

            current_report_data = ReportService.get_csat_report(selected_filters, report_type, current_timeline_start, current_timeline_end)
            previous_report_data = ReportService.get_csat_report(selected_filters, report_type, previous_timeline_start, previous_timeline_end)
            current_report_data, previous_report_data = ReportService.get_csat_compare_result(current_report_data, previous_report_data, report_type, comparison)
        else:
            if timeline:
                current_timeline_start, current_timeline_end = ReportService.get_date_range_by_timeline(timeline)
                current_timeline_end = datetime(current_timeline_end.year, current_timeline_end.month, current_timeline_end.day, 23, 59, 59)

            current_report_data = ReportService.get_csat_report(selected_filters, report_type, current_timeline_start, current_timeline_end)
            previous_report_data = ''
            current_report_data, previous_report_data = ReportService.get_csat_compare_result(current_report_data, previous_report_data, report_type, comparison)

        return HttpResponse(json.dumps({'report_data': current_report_data, 'previous_report_data': previous_report_data, 'report_type': report_type, 'process': process, 'channel': channel, 'comparison': comparison, 'survey_for_unmapped': survey_for_unmapped}))
    return render(request, 'reports/csat_reports.html')


@login_required
def picasso_reports(request):
    if request.is_ajax():
        report_type = request.GET.get('report_type', None)
        report_timeline = request.GET.getlist('report_timeline[]')
        team_members = request.GET.getlist('team_members[]')

        if report_timeline:
            start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

        picasso_report_details = dict()

        # Get teams
        if 'all' in team_members:
            if len(team_members) > 1:
                team_members.remove('all')
            else:
                team_members = team_members
        if report_type == 'default_report':
            picasso_report_detail = ReportService.get_picasso_report_details_for_filters(start_date, end_date, list())
        elif report_type == 'leadreport_individualRep':
            picasso_report_detail = ReportService.get_picasso_report_details_for_filters(start_date, end_date, [request.user.email])
        elif report_type == 'leadreport_teamLead':
            team_emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
            picasso_report_detail = ReportService.get_picasso_report_details_for_filters(start_date, end_date, team_emails)
        elif report_type == 'leadreport_superUser':
            picasso_report_detail = ReportService.get_picasso_report_details_for_filters(start_date, end_date, list())
        else:
            pass

        picasso_report_detail['program_type_header'] = [sts for sts in settings.PICASSO_LEAD_STATUS]
        picasso_report_detail['program_type_header'].append('TOTAL')

        status_list = [status for status in settings.PICASSO_LEAD_STATUS]
        status_list.append('TOTAL')

        bar_chart_data = [['Lead Status']]
        for status in status_list:
            status_row = [status]
            for treatment_type in picasso_report_detail['picasso_program_type_analysis']:
                status_row.append(picasso_report_detail['picasso_program_type_analysis'][treatment_type][status])
            bar_chart_data.append(status_row)
        bar_chart_data[0].extend(picasso_report_detail['picasso_program_type_analysis'].keys())

        picasso_report_detail['bar_chart_data'] = bar_chart_data
        picasso_report_details = {'reports': picasso_report_detail,
                                  'report_type': report_type, 'report_timeline': report_timeline}

        return HttpResponse(json.dumps(picasso_report_details))
    manager = is_manager(request.user.email)
    team_members = list()
    if manager:
        team_members = get_user_under_manager(request.user.email)
    return render(request, 'reports/picasso_reports.html', {'picasso': True, 'manager': manager, 'team_members': team_members})


def download_picasso_report(request):
    report_type = request.POST.get('download_report_type', None)
    report_timeline = request.POST.getlist('download_report_timeline')
    team_members = request.POST.getlist('download_team_members[]')

    if report_timeline:
        start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

    # Get teams
    if 'all' in team_members:
        if len(team_members) > 1:
            team_members.remove('all')
        else:
            team_members = team_members
    if report_type == 'default_report':
        leads = PicassoLeads.objects.filter(created_date__gte=start_date, created_date__lte=end_date)
    elif report_type == 'leadreport_individualRep':
        leads = PicassoLeads.objects.filter(created_date__gte=start_date, created_date__lte=end_date, google_rep_email__in=[request.user.email])
    elif report_type == 'leadreport_teamLead':
        team_emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
        team_emails.append(request.user.email)
        leads = PicassoLeads.objects.filter(created_date__gte=start_date, created_date__lte=end_date, google_rep_email__in=team_emails)
    elif report_type == 'leadreport_superUser':
        leads = PicassoLeads.objects.filter(created_date__gte=start_date, created_date__lte=end_date)

    selected_fields = ['Google Account Manager', 'Email', 'Team', 'Customer ID', 'Internal CID', 'POD Name', 'Company / Account', 'Objectives', 'Recommondation', 'URL', 'Lead Status', 'Lead ID', 'Goal', 'Lead Owner','First Name', 'Last Name', 'Additional Notes']
    filename = "leads-%s-to-%s" % (datetime.strftime(start_date, "%d-%b-%Y"), datetime.strftime(end_date, "%d-%b-%Y"))
    leads = DownloadLeads.get_leads_for_picasso_report(leads, start_date, end_date, selected_fields)
    path = "/tmp/%s.csv" % (filename)
    DownloadLeads.conver_to_csv(path, leads, selected_fields)
    response = DownloadLeads.get_downloaded_file_response(path)
    return response


# Meeting page template rendering view
@login_required
def meeting_minutes(request):
    regalix_email = list()
    google_email = list()
    key_points_dict = dict()
    action_plan_dict = dict()
    tenantive_agenda_dict = dict()
    link_file_name_dict = dict()
    attach_file_name_dict = dict()

    if request.method == 'POST':
        key_points = OrderedDict()
        action_plans = OrderedDict()
        meeting_minutes = MeetingMinutes()
        meeting_minutes.organized_by = request.user.email
        meeting_minutes.subject_timeline = request.POST.get('subject')
        meeting_minutes.other_subject = request.POST.get('other_subject')
        # meeting_minutes.subject_type = request.POST.get('subject')
        # meeting_minutes.other_subject = request.POST.get('other_subject')
        meeting_date = request.POST.get('meeting_date')
        meeting_time = request.POST.get('meeting_time')
        meeting_datetime = meeting_date + ' ' + meeting_time
        meeting_minutes.meeting_time_in_ist = datetime.strptime(meeting_datetime, '%d.%m.%Y %I:%M %p')
        meeting_minutes.google_poc = request.POST.get('google_poc')
        meeting_minutes.regalix_poc = request.POST.get('regalix_poc')
        meeting_minutes.google_team = request.POST.get('google_team')

        meeting_minutes.meeting_audience = request.POST.get('meeting_audience')
        
        if request.POST.get('meeting_audience') == 'internal_meeting':
            meeting_minutes.region = request.POST.get('internal_region')
            meeting_minutes.location = request.POST.get('internal_location')
        else:
            meeting_minutes.region = request.POST.get('region')
            meeting_minutes.location = request.POST.get('location')

        meeting_minutes.program = request.POST.get('program')
        meeting_minutes.program_type = request.POST.get('program_type')
        next_meeting_date = request.POST.get('next_meeting_date', None)
        next_meeting_time = request.POST.get('next_meeting_time', None)
        if next_meeting_date and next_meeting_time:
            next_meeting_datetime = next_meeting_date + ' ' + next_meeting_time
            meeting_minutes.next_meeting_datetime = datetime.strptime(next_meeting_datetime, '%d.%m.%Y %I:%M %p')

        total_keypoints_count = request.POST.get('no_of_keypoints')
        total_actionplan_count = request.POST.get('no_of_actionplans')
        total_tenantive_agenda = request.POST.get('no_of_tenantive_agenda')
        total_link_file_name = request.POST.get('no_of_file_name_link')
        total_attach_file_name = request.POST.get('no_of_file_name_attach')

        for i in range(1, int(total_keypoints_count) + 1):
            key_points['topic_' + str(i)] = request.POST['topic_' + str(i)]
            key_points['highlight_' + str(i)] = request.POST['highlight_' + str(i)]

        action_plans_items_list = list()
        for i in range(1, int(total_actionplan_count) + 1):
            action_plans_items = dict()
            action_plans_items['action_item_name'] = request.POST['action_item_' + str(i)]
            action_plans_items['action_item_owner'] = request.POST['owner_' + str(i)]
            action_plans_items['action_item_date'] = request.POST['action_date_' + str(i)]
            action_plans_items_list.append(action_plans_items)
            action_plans['action_item_' + str(i)] = request.POST['action_item_' + str(i)]
            action_plans['owner_' + str(i)] = request.POST['owner_' + str(i)]
            action_plans['action_date_' + str(i)] = request.POST['action_date_' + str(i)]

        tenantive_agenda_list = list()
        for i in range(1, int(total_tenantive_agenda) + 1):
            tenantive_agenda_list.append(request.POST['agenda_text_' + str(i)])
            tenantive_agenda_dict['agenda_text_' + str(i)] = request.POST['agenda_text_' + str(i)]

        link_file_name_list = list()
        for i in range(1, int(total_link_file_name) + 1):
            link_file_name_list.append(request.POST['file_name_link_'+str(i)])
            link_file_name_dict['file_name_link_'+str(i)] = request.POST['file_name_link_'+str(i)]

        attach_file_name_list = list()
        for i in range(1, int(total_attach_file_name) + 1):
            attach_file_name_list.append(request.POST['file_name_attach_'+str(i)])
            attach_file_name_dict['file_name_attach_'+str(i)] = request.POST['file_name_attach_'+str(i)]

        meeting_minutes.key_points = json.dumps(key_points)
        meeting_minutes.tenantive_agenda = json.dumps(tenantive_agenda_dict)
        meeting_minutes.action_plan = json.dumps(action_plans)
        meeting_minutes.link_file_name = json.dumps(link_file_name_dict)
        meeting_minutes.attach_file_name = json.dumps(attach_file_name_dict)

        meeting_minutes.attachment_1 = request.FILES.get('file_info_1')
        meeting_minutes.attachment_2 = request.FILES.get('file_info_2')
        meeting_minutes.attachment_3 = request.FILES.get('file_info_3')
        meeting_minutes.attachment_4 = request.FILES.get('file_info_4')
        meeting_minutes.attachment_5 = request.FILES.get('file_info_5')

        meeting_minutes.attached_link_1 = request.POST.get('file_info_text_1')
        meeting_minutes.attached_link_2 = request.POST.get('file_info_text_2')
        meeting_minutes.attached_link_3 = request.POST.get('file_info_text_3')
        meeting_minutes.attached_link_4 = request.POST.get('file_info_text_4')
        meeting_minutes.attached_link_5 = request.POST.get('file_info_text_5')

        meeting_minutes.save()

        attendees_list = list()
        attendees = request.POST.get('attendees').replace(', ', ',')
        attendees_list = attendees.split(',')
        if attendees_list[-1] == '':
            attendees_list.pop(-1)
        get_attendees_list = User.objects.filter(email__in=attendees_list).values_list('id', flat=True)
        meeting_minutes.attendees.add(*get_attendees_list)

        bcc_list = list()
        bcc = request.POST.get('bcc').replace(', ', ',')
        bcc_list = bcc.split(',')
        if bcc_list[-1] == '':
            bcc_list.pop(-1)
        get_bcc_list = User.objects.filter(email__in=bcc_list).values_list('id', flat=True)
        meeting_minutes.bcc.add(*get_bcc_list)


        unique_id = get_unique_uuid('meeting_minutes')
        meeting_minutes.ref_uuid = unique_id
        meeting_minutes.save()

        for i in range(1, int(total_actionplan_count) + 1):
            meeting_action_items = MeetingActionItems()
            meeting_action_items.meeting_minutes = meeting_minutes
            meeting_action_items.action_items = request.POST['action_item_' + str(i)]
            meeting_action_items.owners = request.POST['owner_' + str(i)]
            target_date = request.POST['action_date_' + str(i)]
            meeting_action_items.target_date = datetime.strptime(target_date, '%d.%m.%Y')
            meeting_action_items.save()

        mail_list = list()
        attendees_list_for_email_template = list()
        for attendee in attendees_list:
            mail_list.append(str(attendee))
            attendees_list_for_email_template.append(str(attendee))
        if request.POST.get('google_poc') != 'NA':
            mail_list.append(str(request.POST.get('google_poc')))
        mail_list.append(str(request.POST.get('regalix_poc')))

        bcc_email_list = list()
        for each_bcc in bcc_list:
            bcc_email_list.append(str(each_bcc))

        # get object by unique id stored in unique id generated @1225
        link_to_last_data_for_email = MeetingMinutes.objects.all().last()

        attendees_list_last = list()
        if link_to_last_data_for_email:
            link_for_last_meeting_email = link_to_last_data_for_email.ref_uuid
            last_link_attendees = link_to_last_data_for_email.attendees.values('email')


        if last_link_attendees:
            for attendee in last_link_attendees:
                attendees_list_last.append(str(attendee['email']))
                attendees_email_list = ' ,  '.join(attendees_list)
        else:
            attendees_email_list = ' ,  '.join(attendees_list_for_email_template)

        if meeting_minutes.meeting_audience == 'internal_meeting':
            mail_subject = "Meeting Minutes: %s  %s  %s  %s  %s" % (meeting_minutes.program, meeting_minutes.program_type, meeting_minutes.subject_timeline, meeting_minutes.other_subject, meeting_minutes.meeting_time_in_ist.date())
        else:
            mail_subject = "Meeting Minutes: %s  %s  %s  %s  %s  %s" % (meeting_minutes.program, meeting_minutes.program_type, meeting_minutes.google_team, meeting_minutes.subject_timeline, meeting_minutes.other_subject, meeting_minutes.meeting_time_in_ist.date())
        mail_body = get_template('reports/email_templates/minute_meeting_objectives.html').render(
            Context({
                'last_meeting_link_id': request.META['wsgi.url_scheme'] + '://' + request.META['HTTP_HOST'] + "/reports/link-last-meeting/" + str(link_for_last_meeting_email),
                'subject_timeline': meeting_minutes.subject_timeline,
                'meeting_date': meeting_minutes.meeting_time_in_ist.date(),
                'meeting_time': meeting_minutes.meeting_time_in_ist.time(),
                'google_poc': meeting_minutes.google_poc,
                'regalix_poc': meeting_minutes.regalix_poc,
                'google_team': meeting_minutes.google_team,
                'attendees': attendees_email_list,
                'region': meeting_minutes.region,
                'location': meeting_minutes.location,
                'internal_meeting': meeting_minutes.meeting_audience,
                'program': meeting_minutes.program,
                'program_type': meeting_minutes.program_type,
                'other_subject': meeting_minutes.other_subject,

                'action_plans_items': action_plans_items_list,

                # 'next_meeting_time': meeting_minutes.next_meeting_datetime.time(),
                # 'next_meeting_date': meeting_minutes.next_meeting_datetime.date(),
                'tenantive_agenda': tenantive_agenda_list,
            })
        )
        if meeting_minutes.program == 'TAG Team':
            mail_from = 'Google Implementation Team'
        elif meeting_minutes.program == 'WPP':
            mail_from = 'PICASSO Build Team'
        else:
            mail_from = 'PICASSO Team'
        mail_to = mail_list
        bcc = set(bcc_email_list)
        attachments = list()
        send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)
        return redirect('reports.views.meeting_minutes_thankyou')

    managers = User.objects.values_list('email', flat=True)
    for manager in managers:
        if 'google.com' in manager:
            google_email.append(str(manager))
        else:
            regalix_email.append(str(manager))

    programs = Team.objects.exclude(is_active=False).values_list('team_name', flat=True)
    locations = Location.objects.filter(is_active=True)
    programs = [str(p) for p in programs]
    managers = [str(m) for m in managers]
    regions = Region.objects.all()
    all_regions = list()
    region_locations = dict()
    all_locations = list()
    for loc in locations:
        l = {'id': int(loc.id), 'name': str(loc.location_name)}
        all_locations.append(l)
    for rgn in regions:
        for loc in rgn.location.all():
            region_locations[int(rgn.id)] = [int(loc.id) for loc in rgn.location.filter()]
        region_dict = dict()
        region_dict['id'] = int(rgn.id)
        region_dict['name'] = str(rgn.name)
        all_regions.append(region_dict)
    last_meeting = {}
    new_subject_timeline = 0
    link_region = 0
    link_location = 0
    link_program = ''
    link_program_type = ''
    last_meeting_link = {}
    other_subject = {}

    # send mail
    return render(request, 'reports/meeting_minutes.html', {'other_subject': other_subject, 'last_meeting_link': last_meeting_link,
                                                            'tenantive_agenda_dict': tenantive_agenda_dict,
                                                            'link_program_type': link_program_type, 'link_program': link_program, 'link_location': link_location,
                                                            'link_region': link_region, 'new_subject_timeline': new_subject_timeline, 'action_plan_dict': action_plan_dict,
                                                            'key_points_dict': key_points_dict, 'all_locations': all_locations, 'region_locations': region_locations,
                                                            'regions': regions, 'last_meeting': last_meeting, 'locations': locations, 'managers': managers,
                                                            'regalix_email': regalix_email, 'google_email': google_email, 'programs': programs})


@login_required
def link_last_meeting(request, last_id):
    region_locations = dict()
    all_locations = dict()
    programs = dict()
    google_email = dict()
    regalix_email = dict()
    attendees_list = list()
    bcc_list = list()
    next_meeting_date = ''
    next_meeting_time = ''
    try:
        last_meeting = MeetingMinutes.objects.get(ref_uuid=last_id)
    except MeetingMinutes.DoesNotExist:
        return redirect('main.views.main_home')

    new_subject_timeline = 1
    meeting_date = last_meeting.meeting_time_in_ist.date()
    last_meeting_link = datetime.strftime(meeting_date, '%d.%m.%Y')
    meeting_time = last_meeting.meeting_time_in_ist.time()
    if last_meeting.next_meeting_datetime:
        next_meeting_date = last_meeting.next_meeting_datetime.date()
        next_meeting_time = last_meeting.next_meeting_datetime.time()
    subject_timeline = last_meeting.subject_timeline
    attendees = last_meeting.attendees.values('email')
    bcc = last_meeting.bcc.values('email')
    other_subject = last_meeting.other_subject
    link_region = last_meeting.region
    link_location = last_meeting.location
    link_program = last_meeting.program
    link_program_type = last_meeting.program_type
    link_google_team = last_meeting.google_team

    meeting_audience = last_meeting.meeting_audience

    attach_link_1 = last_meeting.attached_link_1
    attach_link_2 = last_meeting.attached_link_2
    attach_link_3 = last_meeting.attached_link_3
    attach_link_4 = last_meeting.attached_link_4
    attach_link_5 = last_meeting.attached_link_5

    attach_file_1 = ''
    attach_file_2 = ''
    attach_file_3 = ''
    attach_file_4 = ''
    attach_file_5 = ''
    if last_meeting.attachment_1:
        attach_file_1 = last_meeting.attachment_1.name
    if last_meeting.attachment_2:
        attach_file_2 = last_meeting.attachment_2.name
    if last_meeting.attachment_3:
        attach_file_3 = last_meeting.attachment_3.name
    if last_meeting.attachment_4:
        attach_file_4 = last_meeting.attachment_4.name
    if last_meeting.attachment_5:
        attach_file_5 = last_meeting.attachment_5.name


    attach_file_name_1 = ''
    attach_file_name_2 = ''
    attach_file_name_3 = ''
    attach_file_name_4 = ''
    attach_file_name_5 = ''
    key_order_attach_file_name = {k:v for v, k in enumerate(['file_name_attach_1', 'file_name_attach_2', 'file_name_attach_3', 'file_name_attach_4', 'file_name_attach_5'])}
    attach_file_name_dict = OrderedDict(sorted(last_meeting.attach_file_name.items(), key=lambda i: key_order_attach_file_name.get(i[0])))
    if 'file_name_attach_1' in last_meeting.attach_file_name:
        attach_file_name_1 = attach_file_name_dict['file_name_attach_1']
    if 'file_name_attach_2' in last_meeting.attach_file_name:
        attach_file_name_2 = attach_file_name_dict['file_name_attach_2']
    if 'file_name_attach_3' in last_meeting.attach_file_name:
        attach_file_name_3 = attach_file_name_dict['file_name_attach_3']
    if 'file_name_attach_4' in last_meeting.attach_file_name:
        attach_file_name_4 = attach_file_name_dict['file_name_attach_4']
    if 'file_name_attach_5' in last_meeting.attach_file_name:
        attach_file_name_5 = attach_file_name_dict['file_name_attach_5']

    link_file_name_1 = ''
    link_file_name_2 = ''
    link_file_name_3 = ''
    link_file_name_4 = ''
    link_file_name_5 = ''
    key_order_link_file_name = {k:v for v, k in enumerate(['file_name_link_1', 'file_name_link_2', 'file_name_link_3', 'file_name_link_4', 'file_name_link_5'])}
    link_file_name_dict = OrderedDict(sorted(last_meeting.link_file_name.items(), key=lambda i: key_order_link_file_name.get(i[0])))
    if 'file_name_link_1' in last_meeting.link_file_name:
        link_file_name_1 = link_file_name_dict['file_name_link_1']
    if 'file_name_link_2' in last_meeting.link_file_name:
        link_file_name_2 = link_file_name_dict['file_name_link_2']
    if 'file_name_link_3' in last_meeting.link_file_name:
        link_file_name_3 = link_file_name_dict['file_name_link_3']
    if 'file_name_link_4' in last_meeting.link_file_name:
        link_file_name_4 = link_file_name_dict['file_name_link_4']
    if 'file_name_link_5' in last_meeting.link_file_name:
        link_file_name_5 = link_file_name_dict['file_name_link_5']
    media_url = settings.MEDIA_URL

    submit_disabled = False

    if attendees:
        for attendee in attendees:
            attendees_list.append(str(attendee['email']))
        attendees_email_list = ' ,  '.join(attendees_list)
    else:
        attendees_email_list = 'Attendee Email id not available'

    if bcc:
        for each_bcc in bcc:
            bcc_list.append(str(each_bcc['email']))
        bcc_email_list = ' ,  '.join(bcc_list)
    else:
        bcc_email_list = 'Email id not available'

    key_order_agenda = {k:v for v, k in enumerate(['agenda_text_1', 'agenda_text_2', 'agenda_text_3', 'agenda_text_4', 'agenda_text_5', 'agenda_text_6', 'agenda_text_7', 'agenda_text_8', 'agenda_text_9', 'agenda_text_10', 'agenda_text_11', 'agenda_text_12', 'agenda_text_14', 'agenda_text_15'])}
    tenantive_agenda_dict = OrderedDict(sorted(last_meeting.tenantive_agenda.items(), key=lambda i: key_order_agenda.get(i[0])))

    key_order_action = {k:v for v, k in enumerate(['action_item_1', 'owner_1', 'action_date_1', 'action_item_2', 'owner_2', 'action_date_2', 'action_item_3', 'owner_3', 'action_date_3', 'action_item_4', 'owner_4', 'action_date_4' ,'action_item_5', 'owner_5', 'action_date_5', 'action_item_6', 'owner_6', 'action_date_6', 'action_item_7', 'owner_7', 'action_date_7', 'action_item_8', 'owner_8', 'action_date_8', 'action_item_9', 'owner_9', 'action_date_9', 'action_item_10', 'owner_10', 'action_date_10', 'action_item_11', 'owner_11', 'action_date_11', 'action_item_12', 'owner_12', 'action_date_12', 'action_item_13', 'owner_13', 'action_date_13', 'action_item_14', 'owner_14', 'action_date_14', 'action_item_15', 'owner_15', 'action_date_15',])}
    action_plan_dict = OrderedDict(sorted(last_meeting.action_plan.items(), key=lambda i: key_order_action.get(i[0])))

    key_order = {k:v for v, k in enumerate(['topic_1', 'highlight_1', 'topic_2', 'highlight_2', 'topic_3', 'highlight_3', 'topic_4', 'highlight_4','topic_5', 'highlight_5', 'topic_6', 'highlight_6', 'topic_7', 'highlight_7', 'topic_8', 'highlight_8', 'topic_9', 'highlight_9', 'topic_10', 'highlight_10', 'topic_11', 'highlight_11', 'topic_12', 'highlight_12', 'topic_13', 'highlight_13', 'topic_14', 'highlight_14', 'topic_15', 'highlight_15',])}    
    key_points_dict = OrderedDict(sorted(last_meeting.key_points.items(), key=lambda i: key_order.get(i[0])))

    return render(request, 'reports/meeting_minutes.html', {'submit_disabled': submit_disabled,
                                                            'last_meeting_link': json.dumps(last_meeting_link),
                                                            'tenantive_agenda_dict': json.dumps(tenantive_agenda_dict),
                                                            'link_program_type': link_program_type, 'link_google_team': link_google_team,
                                                            'link_program': link_program, 'link_location': link_location,
                                                            'link_region': json.dumps(link_region), 'other_subject': other_subject,
                                                            'regalix_email': regalix_email, 'programs': programs, 'google_email': google_email,
                                                            'new_subject_timeline': new_subject_timeline, 'all_locations': all_locations,
                                                            'region_locations': region_locations, 'action_plan_dict': json.dumps(action_plan_dict),
                                                            'key_points_dict': json.dumps(key_points_dict), 'attendees_email_list': attendees_email_list,
                                                            'subject_timeline': json.dumps(subject_timeline), 'last_meeting': last_meeting,
                                                            'meeting_date': meeting_date, 'meeting_time': meeting_time, 'next_meeting_date': next_meeting_date,
                                                            'next_meeting_time': next_meeting_time, 'attach_link_1': attach_link_1, 'attach_link_2': attach_link_2, 
                                                            'attach_link_3': attach_link_3, 'attach_link_4': attach_link_4, 'attach_link_5': attach_link_5, 
                                                            'attach_file_1': attach_file_1, 'attach_file_2': attach_file_2, 'attach_file_3': attach_file_3, 
                                                            'attach_file_4': attach_file_4, 'attach_file_5': attach_file_5, 'bcc_email_list': bcc_email_list, 'media_url': media_url, 'meeting_audience': meeting_audience, 
                                                            'attach_file_name_1': attach_file_name_1, 'attach_file_name_2': attach_file_name_2, 'attach_file_name_3': attach_file_name_3, 'attach_file_name_4': attach_file_name_4, 
                                                            'attach_file_name_5': attach_file_name_5, 'link_file_name_1': link_file_name_1, 'link_file_name_2': link_file_name_2,
                                                            'link_file_name_3': link_file_name_3, 'link_file_name_4': link_file_name_4, 'link_file_name_5': link_file_name_5})


@login_required
def meeting_minutes_thankyou(request):
    return_url = reverse('reports.views.meeting_minutes')
    return render(request, 'reports/meeting_minutes_thankyou.html', {'return_url': return_url})


@login_required
def export_meeting_minutes(request):
    if request.method == 'POST':
        excel_header = ['Meeting Date', 'Subject Line', 'Link']
        meeting_date_from = request.POST.get('date_from')
        meeting_date_to = request.POST.get('date_to')
        program = request.POST.get('program')
        meeting_date_from = datetime.strptime(meeting_date_from, '%m/%d/%Y')
        meeting_date_to = datetime.strptime(meeting_date_to, '%m/%d/%Y')
        if program != 'all':
            meeting_minutes = MeetingMinutes.objects.filter(meeting_time_in_ist__range=(meeting_date_from, meeting_date_to),
                                                        program=program)
        else:
            meeting_minutes = MeetingMinutes.objects.filter(meeting_time_in_ist__range=(meeting_date_from, meeting_date_to))
        final_meeting_list = list()
        for meeting_minute in meeting_minutes:
            meeting_minute_dict = dict()
            meeting_date = meeting_minute.meeting_time_in_ist.date()
            meeting_minute_dict['Meeting Date'] = datetime.strftime(meeting_date, '%m/%d/%Y')
            if meeting_minute.meeting_audience == 'internal_meeting':
                meeting_minute_dict['Subject Line'] = meeting_minute.program + ' ' + meeting_minute.program_type + ' ' + meeting_minute.subject_timeline + ' ' + meeting_minute.other_subject
            else:
                meeting_minute_dict['Subject Line'] = meeting_minute.program + ' ' + meeting_minute.program_type + ' ' + meeting_minute.google_team + ' ' + meeting_minute.subject_timeline + ' ' + meeting_minute.other_subject
            if meeting_minute.ref_uuid:
                meeting_minute_dict['Link'] = request.META['wsgi.url_scheme'] + '://' + request.META['HTTP_HOST'] + "/reports/link-last-meeting/" + str(meeting_minute.ref_uuid)
            else:
                meeting_minute_dict['Link'] = ''
            final_meeting_list.append(meeting_minute_dict)

        filename = "meeting-minutes"
        path = write_appointments_to_csv(final_meeting_list, excel_header, filename)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response
    return render(request, 'reports/export_meeting_minutes.html', {})

def write_appointments_to_csv(result, collumn_attr, filename):
    path = "/tmp/%s.csv" % (filename)
    DownloadLeads.conver_to_csv(path, result, collumn_attr)
    return path


@login_required
def export_action_items(request):

    if request.method == 'POST':
        meetings_date_from = request.POST.get('date_from')
        meetings_date_to = request.POST.get('date_to')
        program = request.POST.get('program')
        meeting_date_from = datetime.strptime(meetings_date_from, '%m/%d/%Y')
        meeting_date_to = datetime.strptime(meetings_date_to, '%m/%d/%Y')
        if request.POST.get('reference_id'):
            attendees_list = list()
            attendees_email_list= list()
            bcc_list = list()
            update_status = MeetingActionItems.objects.get(id=request.POST.get('reference_id'))
            update_status.status = request.POST.get('status')
            if request.POST.get('status') == 'Closed':
                update_status.closed_by = request.user.get_full_name()
            elif request.POST.get('status') == 'Reopened':
                update_status.reopened_by = request.user.get_full_name()
            else:
                update_status.resolved_by = request.user.get_full_name()
            update_status.save()
            attendees = update_status.meeting_minutes.attendees.values('email')
            bcc = update_status.meeting_minutes.bcc.values('email')
            for attendee in attendees:
                attendees_list.append(str(attendee['email']))
            attendees_email_list = ' ,  '.join(attendees_list)

            attendees_list.append(str(update_status.meeting_minutes.google_poc))
            attendees_list.append(str(update_status.meeting_minutes.regalix_poc))
            if request.POST.get('status') == 'Closed':
                status_changed_by = update_status.closed_by
            elif request.POST.get('status') == 'Reopened':
                status_changed_by = update_status.reopened_by
            else:
                status_changed_by = update_status.resolved_by


            for each_bcc in bcc:
                bcc_list.append(str(each_bcc['email']))
            bcc_email_list = ' ,  '.join(bcc_list)
            mail_subject = "Meeting Minutes: %s  %s  %s  %s  %s" % (update_status.meeting_minutes.program, update_status.meeting_minutes.program_type, update_status.meeting_minutes.subject_timeline, update_status.meeting_minutes.other_subject, update_status.meeting_minutes.meeting_time_in_ist.date())
            mail_body = get_template('reports/email_templates/minute_meeting_status.html').render(
            Context({
                'last_meeting_link_id': request.META['wsgi.url_scheme'] + '://' + request.META['HTTP_HOST'] + "/reports/link-last-meeting/" + str(update_status.meeting_minutes.ref_uuid),
                'subject_timeline': update_status.meeting_minutes.subject_timeline,
                'meeting_date': update_status.meeting_minutes.meeting_time_in_ist.date(),
                'meeting_time': update_status.meeting_minutes.meeting_time_in_ist.time(),
                'google_poc': update_status.meeting_minutes.google_poc,
                'regalix_poc': update_status.meeting_minutes.regalix_poc,
                'google_team': update_status.meeting_minutes.google_team,
                'attendees': attendees_email_list,
                'region': update_status.meeting_minutes.region,
                'status': update_status.status,
                'action_item': update_status.action_items,
                'owner': update_status.owners,
                'target_date': update_status.target_date,
                'status_changed_by': status_changed_by,
                'location': update_status.meeting_minutes.location,
                'internal_meeting': update_status.meeting_minutes.meeting_audience,
                'program': update_status.meeting_minutes.program,
                'program_type': update_status.meeting_minutes.program_type,
                'other_subject': update_status.meeting_minutes.other_subject,
                })
            )
            if update_status.meeting_minutes.program == 'TAG Team':
                mail_from = 'Google Implementation Team'
            elif update_status.meeting_minutes.program == 'WPP':
                mail_from = 'PICASSO Build Team'
            else:
                mail_from = 'PICASSO Team'
            mail_to = attendees_list
            bcc = set(bcc_email_list)
            attachments = list()
            send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

        
        if program != 'all':
            meeting_minutes = MeetingMinutes.objects.filter(meeting_time_in_ist__range=(meeting_date_from, meeting_date_to),
                                                            program=program).values_list('id', flat=True)
        else:
            meeting_minutes = MeetingMinutes.objects.filter(meeting_time_in_ist__range=(meeting_date_from, meeting_date_to)).values_list('id', flat=True)

        filter_by_status = request.POST.get('report_status')
        if filter_by_status:
            try:
                if  filter_by_status == 'open':
                    meeting_action_items = MeetingActionItems.objects.filter(meeting_minutes_id__in=meeting_minutes,
                                                                status=filter_by_status).order_by('-created_date')
                if filter_by_status == 'closed':
                    meeting_action_items = MeetingActionItems.objects.filter(meeting_minutes_id__in=meeting_minutes,
                                                                status=filter_by_status).order_by('-created_date')
                if filter_by_status == 'reopened':
                    meeting_action_items = MeetingActionItems.objects.filter(meeting_minutes_id__in=meeting_minutes,
                                                                status=filter_by_status).order_by('-created_date')
                if filter_by_status == 'resolved':
                    meeting_action_items = MeetingActionItems.objects.filter(meeting_minutes_id__in=meeting_minutes,
                                                                status=filter_by_status).order_by('-created_date')
            except:
                pass
        else:
            filter_by_status = "View All Status"
            meeting_action_items = MeetingActionItems.objects.filter(meeting_minutes_id__in=meeting_minutes).order_by('-created_date')

        all_records_list = list()
        for action_items in meeting_action_items:
            each_record_dict = dict()
            meeting_date = action_items.meeting_minutes.meeting_time_in_ist.date()
            each_record_dict['Action Item Id'] = action_items.id
            each_record_dict['Meeting Date'] = datetime.strftime(meeting_date, '%m/%d/%Y')
            each_record_dict['Subject Timeline'] = action_items.meeting_minutes.program + ' ' + action_items.meeting_minutes.program_type + ' ' + action_items.meeting_minutes.subject_timeline + ' ' + action_items.meeting_minutes.other_subject
            each_record_dict['Action Items'] = action_items.action_items
            each_record_dict['Owners'] = action_items.owners
            target_date = action_items.target_date
            each_record_dict['Target Date'] = datetime.strftime(target_date, '%m/%d/%Y')
            each_record_dict['Status'] = action_items.status

            if action_items.closed_by:
                each_record_dict['Closed By'] = action_items.closed_by
            else:
                each_record_dict['Closed By'] = '-'

            if action_items.reopened_by:
                each_record_dict['Reopened By'] = action_items.reopened_by
            else:
                each_record_dict['Reopened By'] = '-'

            if action_items.resolved_by:
                each_record_dict['Resolved By'] = action_items.resolved_by
            else:
                each_record_dict['Resolved By'] = '-'
            all_records_list.append(each_record_dict)
        status = {}
        status['status'] = filter_by_status
        return render(request, 'reports/export_action_items.html', {'status':json.dumps(status), 'all_records_list': json.dumps(all_records_list), 'meetings_date_from': meetings_date_from, 'meetings_date_to': meetings_date_to, 'program': program})
    meetings_date_from = ''
    meetings_date_to = ''
    program = ''
    all_records_list = ''
    status = {}
    status['status'] = 'undefined'
    return render(request, 'reports/export_action_items.html', {'status':json.dumps(status),'all_records_list': all_records_list, 'meetings_date_from': meetings_date_from, 'meetings_date_to': meetings_date_to, 'program': program})


def get_meeting_minutes(request):
    if request.is_ajax():
        meeting_date_from = request.GET.get('meeting_date_from')
        meeting_date_to = request.GET.get('meeting_date_to')
        program = request.GET.get('program')
        meeting_date_from = datetime.strptime(meeting_date_from, '%m/%d/%Y')
        meeting_date_to = datetime.strptime(meeting_date_to, '%m/%d/%Y')
        if program != 'all':
            meeting_minutes = MeetingMinutes.objects.filter(meeting_time_in_ist__range=(meeting_date_from, meeting_date_to),
                                                            program=program)
        else:
            meeting_minutes = MeetingMinutes.objects.filter(meeting_time_in_ist__range=(meeting_date_from, meeting_date_to))
        final_meeting_list = list()
        for meeting_minute in meeting_minutes:
            meeting_minute_dict = dict()
            meeting_date = meeting_minute.meeting_time_in_ist.date()
            meeting_minute_dict['link_meeting_date'] = datetime.strftime(meeting_date, '%m/%d/%Y')
            meeting_minute_dict['program'] = meeting_minute.program
            meeting_minute_dict['program_type'] = meeting_minute.program_type
            if meeting_minute.meeting_audience == 'internal_meeting':
                meeting_minute_dict['google_team'] = ''
            else:
                meeting_minute_dict['google_team'] = meeting_minute.google_team
            meeting_minute_dict['subject_timeline'] = meeting_minute.subject_timeline
            meeting_minute_dict['other_subject'] = meeting_minute.other_subject
            meeting_minute_dict['ref_uuid'] = meeting_minute.ref_uuid
            final_meeting_list.append(meeting_minute_dict)
    return HttpResponse(json.dumps(final_meeting_list))


def generate_link(request):
    if request.is_ajax():
        subject_timeline = request.GET.get('subject')
        program = request.GET.get('program')
        program_type = request.GET.get('program_type')
        if program_type:
            meeting_minutes = MeetingMinutes.objects.filter(subject_timeline=subject_timeline, program=program, program_type=program_type).last()
        else:
            meeting_minutes = MeetingMinutes.objects.filter(subject_timeline=subject_timeline, program=program).last()

        if meeting_minutes:
            link_last_meeting = request.META['wsgi.url_scheme'] + '://' + request.META['HTTP_HOST'] + "/reports/link-last-meeting/" + str(meeting_minutes.ref_uuid)
        else:
            link_last_meeting = 'No Data'
    return HttpResponse(json.dumps(link_last_meeting))


@login_required
def program_kick_off(request):
    if request.method == 'POST':
        kickoffprogram = KickOffProgram()

        kickoffprogram.program_name = request.POST.get('program_name')
        kickoffprogram.google_poc_locations = request.POST.get('google_poc_location')
        kickoffprogram.advertiser_type = request.POST.getlist('advertiser_type')

        codetype_list = list()
        code_type_data = request.POST.getlist('codeTypeList')
        for data in code_type_data:
            codetype_list.append(str(data))
        kickoffprogram.codetypeslist = codetype_list

        program_start_date = request.POST.get('program_start_date')
        kickoffprogram.programe_start_date = datetime.strptime(program_start_date, '%d.%m.%Y')

        programe_end_date = request.POST.get('program_end_date')
        kickoffprogram.programe_end_date = datetime.strptime(programe_end_date, '%d.%m.%Y')

        estimated_lead_no = request.POST.get('estimated_lead_no')
        estimated_lead_finish_period = request.POST.get('subject_estimated_day')
        kickoffprogram.estimated_lead_volume = estimated_lead_no + ' ' + estimated_lead_finish_period

        kickoffprogram.program_overview_objective = request.POST.get('program_overview')
        kickoffprogram.subject_estimated_day = request.POST.get('subject-estimated-day')
        kickoffprogram.expectations = request.POST.get('expectations')
        kickoffprogram.explain_workflow = request.POST.get('explain_workflow')
        kickoffprogram.win_criteria = request.POST.get('win_criteria')

        tag_team_connect_method = request.POST.get('connect') + ','
        tag_team_connect_day = request.POST.get('tagteam-connect-day') + ','
        tag_team_connect_time = request.POST.get('tag_meeting_time') + ','
        tag_team_connect_timezone = request.POST.get('tagteam-connect-timezone')
        kickoffprogram.tag_team_connect_detail = tag_team_connect_method + tag_team_connect_day + str(tag_team_connect_time) + str(tag_team_connect_timezone)

        kickoffprogram.project_related_url = request.POST.get('file_info_text_1')
        kickoffprogram.code_type_list = request.POST.getlist('codeTypeList')

        kickoffprogram.lead_sub_mode = request.POST.get('lead_submission')
        if request.POST.get('lead_submission') == "others":
            kickoffprogram.lead_subbmission_other_val = request.POST.get('lead_sub_other')

        kickoffprogram.real_time_support_chat = request.POST.get('real_time_chat')
        kickoffprogram.real_time_support_live_trans = request.POST.get('real_time_live_trans')

        kickoffprogram.comments = request.POST.get('comments')

        count_of_succes_matrix = request.POST.get('count_of_success_matrix')
        succes_matrics_dict = dict()
        for i in range(1, int(count_of_succes_matrix) + 1):
            succes_matrics_dict['succes_metrices_one_' + str(i)] = request.POST.get('succes_metrices_one_' + str(i))
            succes_matrics_dict['succes_metrices_two_' + str(i)] = request.POST.get('succes_metrices_two_' + str(i))
            succes_matrics_dict['succes_metrices_three_' + str(i)] = request.POST.get('succes_metrices_three_' + str(i))
        kickoffprogram.succes_matrix = json.dumps(succes_matrics_dict)

        link_file_name_dict = dict()
        count_of_file_url_name = request.POST.get('count_url_file_name')
        for i in range(1, int(count_of_file_url_name) + 1):
            link_file_name_dict['file_name_link_' + str(i)] = request.POST.get('file_name_link_' + str(i))
        kickoffprogram.file_url_name = json.dumps(link_file_name_dict)

        kickoffprogram.attached_url_link_1 = request.POST.get('file_info_text_1')
        kickoffprogram.attached_url_link_2 = request.POST.get('file_info_text_2')
        kickoffprogram.attached_url_link_3 = request.POST.get('file_info_text_3')
        kickoffprogram.attached_url_link_4 = request.POST.get('file_info_text_4')
        kickoffprogram.attached_url_link_5 = request.POST.get('file_info_text_5')

        attach_file_name = dict()
        for i in range(1, int(count_of_file_url_name) + 1):
            attach_file_name['file_name_attach_'+str(i)] = request.POST.get('file_name_attach_' + str(i))
        kickoffprogram.file_upload_name = json.dumps(attach_file_name)

        kickoffprogram.upload_file_attachment_1 = request.FILES.get('file_info_1')
        kickoffprogram.upload_file_attachment_2 = request.FILES.get('file_info_2')
        kickoffprogram.upload_file_attachment_3 = request.FILES.get('file_info_3')
        kickoffprogram.upload_file_attachment_4 = request.FILES.get('file_info_4')
        kickoffprogram.upload_file_attachment_5 = request.FILES.get('file_info_5')

        kickoffprogram.program_created_by = request.user.email

        kickoffprogram.save()

        location_multiselect = request.POST.getlist('locationTypeList')
        get_location = Location.objects.filter(location_name__in=location_multiselect).values_list('id', flat=True)
        kickoffprogram.target_locations.add(*get_location)

        regions_multiselect = request.POST.getlist('regionTypeList')
        get_regions = Region.objects.filter(name__in=regions_multiselect).values_list('id', flat=True)
        kickoffprogram.region.add(*get_regions)

        google_poc_list = list()
        google_poc = request.POST.get('google_poc').replace(', ', ',')
        google_poc_list = google_poc.split(',')
        google_poc_list.pop(-1)
        get_google_poc_list = User.objects.filter(email__in=google_poc_list).values_list('id', flat=True)
        kickoffprogram.google_poc.add(*get_google_poc_list)

        # this bellow field as been killed as suggested, fieled in in database
        # google_poc_email_list = list()
        # google_poc_email = request.POST.get('google_poc_email').replace(', ', ',')
        # google_poc_email_list = google_poc_email.split(',')
        # google_poc_email_list.pop(-1)
        # get_google_poc_email_list = User.objects.filter(email__in=google_poc_email_list).values_list('id', flat=True)
        # kickoffprogram.google_poc_email.add(*get_google_poc_email_list)

        # this bellow code is  used for futer use field is already in database
        # bcc_list = list()
        # bcc = request.POST.get('kick_off_bcc').replace(', ', ',')
        # bcc_list = bcc.split(',')
        # if bcc_list[-1] == '':
        #     bcc_list.pop(-1)
        # get_bcc_list = User.objects.filter(email__in=bcc_list).values_list('id', flat=True)
        # kickoffprogram.bcc_kick_off.add(*get_bcc_list)

        bcc_google_poc_list = list()
        for each_email in google_poc_list:
            bcc_google_poc_list.append(str(each_email))

        mail_to = list()
        latest_program = KickOffProgram.objects.filter(program_created_by=request.user.email).last()
        acces_link = request.META['wsgi.url_scheme']+'://'+request.META['HTTP_HOST']+"/reports/kickoff-export-detail/"+str(latest_program.id)
        mail_from = "Google TagTeam"
        user = request.user.email
        name_of_submiter = request.user.first_name + ' ' + request.user.last_name
        mail_to = ['srinivasans@regalix-inc.com', 'kushalappa.theetharamada@regalix-inc.com', str(user)]
        mail_subject = "TagTeam Support Request [New Program - %s ]" % (kickoffprogram.program_name)
        mail_body = get_template('reports/email_templates/kick_off_form_submission.html').render(Context({'program_name': kickoffprogram.program_name, 'acces_link':acces_link, 'google_poc':google_poc, 'name_of_submiter':name_of_submiter}))
        bcc = set(bcc_google_poc_list)
        attachments = list()
        send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

        return redirect('reports.views.kickoff_thankyou')

    location_based_zones = dict()
    locations = Location.objects.filter(is_active=True)
    for loc in locations:
            location_name = str(loc.location_name)
            location_based_zones[location_name] = [{'zone_name':str(tz['zone_name']), 'time_value':str(tz['time_value'])} for tz in loc.time_zone.values()]
    
    google_email = list()
    all_mail = list()
    managers = User.objects.values_list('email', flat=True)
    bcc_field = managers 
    for manager in managers:
        if 'google.com' in manager:
            google_email.append(str(manager))
        all_mail.append(str(manager))
    regions = Region.objects.all()
    #locations = Location.objects.filter(is_active=True)
    region_locations = dict()
    all_locations = list()
    for loc in locations:
            l = {'id': int(loc.id), 'name': str(loc.location_name)}
            all_locations.append(l)
    for rgn in regions:
            for loc in rgn.location.all():
                region_locations[int(rgn.id)] = [int(loc.id) for loc in rgn.location.filter()]
    # code type  fetching ReportService
    code_types_name = ReportService.get_all_code_type()

    region_based_locations = dict()
    for regn in regions:
        location_list_values = list()
        for item in regn.location.values('location_name').filter(is_active=True):
            location_list_values.append(item['location_name'])
        region_based_locations[regn.name] = location_list_values

    # timezone fetching
    #timezone = Timezone.objects.values_list('zone_name', 'time_value')
    
    CodeTypevalues = CodeType.objects.all()
    final_codetypes = []
    for item in CodeTypevalues:
        if item.name != "RLSA Bulk Implementation":
            final_codetypes.append(str(item.name))

    return render(request, 'reports/kick_off.html', {'regions': regions,
                                                     'google_email': google_email,
                                                     'managers': all_mail,
                                                     'code_types_name': final_codetypes,
                                                     'locations': locations,
                                                     'region_locations': region_locations,
                                                     'all_locations': all_locations,
                                                     'bcc_field':bcc_field,
                                                     #'timezone':timezone,
                                                     'region_based_locations': json.dumps(region_based_locations),
                                                     'location_based_zones': json.dumps(location_based_zones)})


@login_required
def kickoff_thankyou(request):
    return_url = reverse('reports.views.program_kick_off')
    return render(request, 'reports/kickoff_thankyou.html', {'return_url': return_url})

@login_required
def tagteam_kickoff_thankyou(request):
    latest_program = KickoffTagteam.objects.filter(tagteam_added_by=request.user.email).last()
    program_id = latest_program.kickoff_program_id
    return render(request, 'reports/tagteam_kickoff_thankyou.html', {"program_id":program_id})



@login_required
def kickoff_export(request):
    if request.method == 'POST':
        kickoff_date_from = request.POST.get('date_from')
        kickoff_date_to = request.POST.get('date_to')
        kickoff_date_from = datetime.strptime(kickoff_date_from, '%m/%d/%Y')
        kickoff_date_to = datetime.strptime(kickoff_date_to, '%m/%d/%Y')
        kick_off_selected = KickOffProgram.objects.filter(created_date__range=[kickoff_date_from, kickoff_date_to])
        selected_kickoff_list = list()
        for each_kick_off in kick_off_selected:
            kickoff_dict = dict()
            created_date = each_kick_off.created_date
            start_date_converted = datetime.strftime(created_date, '%d.%m.%Y')
            kickoff_dict['Created Date'] = start_date_converted
            kickoff_dict['Program Name'] = each_kick_off.program_name
            kickoff_dict['Access Link'] = request.META['wsgi.url_scheme']+'://'+request.META['HTTP_HOST']+"/reports/kickoff-export-detail/"+str(each_kick_off.id)
            selected_kickoff_list.append(kickoff_dict)
        excel_header = ['Program Name', 'Access Link', 'Created Date']
        filename = "kick-off-programs"
        path = write_kickoffprogram_to_csv(selected_kickoff_list, excel_header, filename)
        response = DownloadLeads.get_downloaded_file_response(path)
        return response
    all_records_kickoff_list = list()
    getall_kickoff_records = KickOffProgram.objects.all().order_by('-created_date')
    count = 0
    for each_record in getall_kickoff_records:
        each_record_dict = dict()
        each_record_dict['program_name'] = each_record.program_name
        each_record_dict['program_id'] = each_record.id
        count = count + 1
        each_record_dict['counter'] = count
        all_records_kickoff_list.append(each_record_dict)
    return render(request, 'reports/kick_off_export.html', {'getall_kickoff_records': all_records_kickoff_list})


def write_kickoffprogram_to_csv(result, collumn_attr, filename):
    path = "/tmp/%s.csv" % (filename)
    DownloadLeads.conver_to_csv(path, result, collumn_attr)
    return path


def get_kickoff_program(request):
    if request.is_ajax():
        kickoff_date_from = request.GET.get('kickoff_date_from')
        kickoff_date_to = request.GET.get('kickoff_date_to')
        kickoff_date_from = datetime.strptime(kickoff_date_from, '%m/%d/%Y')
        kickoff_date_to = datetime.strptime(kickoff_date_to, '%m/%d/%Y')
        kick_off_selected = KickOffProgram.objects.filter(created_date__range=[kickoff_date_from, kickoff_date_to])
        selected_kickoff_list = list()
        for each_kick_off in kick_off_selected:
            kickoff_dict = dict()
            created_date = each_kick_off.created_date
            start_date_converted = datetime.strftime(created_date, '%d.%m.%Y')

            kickoff_dict['created_date'] = start_date_converted
            kickoff_dict['program'] = each_kick_off.program_name
            kickoff_dict['access_id'] = request.META['wsgi.url_scheme'] +'://'+request.META['HTTP_HOST']+"/reports/kickoff-export-detail/"+str(each_kick_off.id)
            selected_kickoff_list.append(kickoff_dict)
        return HttpResponse(json.dumps(selected_kickoff_list))


@login_required
def kickoff_export_detail(request, program_id):
    try:
        get_kickoff_record = KickOffProgram.objects.get(id=program_id)
    except KickOffProgram.DoesNotExist:
        return redirect('reports.views.kickoff_export')
        # adding tagteam in page
    training_start = None
    training_end = None
    live_date = None
    reps_email_list = None
    meeting_time = None
    meeting_date = None
    email_bcc_list = None
    try:
        get_kickoff_tagteam = KickoffTagteam.objects.get(kickoff_program_id=program_id)
        if get_kickoff_tagteam:

            reps_display = get_kickoff_tagteam.all_reps
            data_reps_list = str(reps_display)
            clean = data_reps_list.replace("u'","")
            clean_data = clean.replace(",","")
            reps_email_list = clean_data.translate(None,"[]'")

            meeting_time = get_kickoff_tagteam.kickoff_meeting_date_time.time()
            meeting_date = get_kickoff_tagteam.kickoff_meeting_date_time.date()
            training_start = get_kickoff_tagteam.training_start_date.date()
            training_end = get_kickoff_tagteam.training_start_date.date()
            live_date = get_kickoff_tagteam.golive_date.date()

            bcc_tagteam = get_kickoff_tagteam.bcc_tagteam.values('email')
            email_bcc_list = list()
            for mailids in bcc_tagteam:
                email_bcc_list.append(str(mailids['email']))
            email_bcc_list = ','.join(email_bcc_list)


        else:
            reps_email_list = None
            meeting_time = None
            meeting_date = None
            training_start = None
            training_end = None
            live_date = None
            email_bcc_list = None

    except KickoffTagteam.DoesNotExist:
            get_kickoff_tagteam = None

    # displaying the disabled kickof program to add tagteam
    if get_kickoff_record:
        # getting manyToMany feild goole poc email fetching
        google_pocs = get_kickoff_record.google_poc.values('email')
        google_poc_list = list()
        for mailids in google_pocs:
            google_poc_list.append(str(mailids['email']))
        googlepoc_email_list = ', \n'.join(google_poc_list)

        # getting ManyToMany feild goole poc email second email ids fetching
        google_email_pocs = get_kickoff_record.google_poc_email.values('email')
        google_poc_email_list = list()
        for google_email_mail_ids in google_email_pocs:
            google_poc_email_list.append(str(google_email_mail_ids['email']))
        google_poc_email_list = ', '.join(google_poc_email_list)

        # getting ManyToMany feild BCC email email ids fetching
        # bcc_kick_off_prg = get_kickoff_record.bcc_kick_off.values('email')
        # bcc_kick_off_prg_list = list()
        # for mail_ids in bcc_kick_off_prg:
        #     bcc_kick_off_prg_list.append(str(google_email_mail_ids['email']))
        # bcc_kick_off_prg_list = ','.join(bcc_kick_off_prg_list)

        # getting all regions from the manyToMany feild
        region_list = list()
        get_region_list = get_kickoff_record.region.values('name')
        for region in get_region_list:
            for key, val in region.iteritems():
                region_list.append(val)
        region_list = ',  '.join(region_list)

        target_location_list = list()
        get_target_location = get_kickoff_record.target_locations.values('location_name')
        for location in get_target_location:
            for key, val in location.iteritems():
                target_location_list.append(val)
        target_location_list = ', '.join(target_location_list)

        get_kickoff_record.advertiser_type

        advertizer_list = get_kickoff_record.advertiser_type
        data = str(advertizer_list)
        clean_data = data.replace("u'","")
        clean_data_advertize_data = clean_data.translate(None,"[]'")

        get_codetype_list = get_kickoff_record.codetypeslist
        final_type_codelist_with_quotes = str(get_codetype_list[1:-1])
        final_type_codelist_clean_underscore = final_type_codelist_with_quotes.replace("_"," ")
        final_type_codelist_clean = final_type_codelist_clean_underscore.replace(",",",\n")
        removing_quot = final_type_codelist_clean.replace("'","")
        final_type_codelist = removing_quot

    start_date = get_kickoff_record.programe_start_date
    start_date_converted = datetime.strftime(start_date, '%d.%m.%Y')
    end_date = get_kickoff_record.programe_end_date
    end_date_converted = datetime.strftime(end_date, '%d.%m.%Y')

    extract_estimated_volume = get_kickoff_record.estimated_lead_volume
    estimated_number = int(re.search(r'\d+', extract_estimated_volume).group())
    estimated_volume = ''.join([i for i in extract_estimated_volume if not i.isdigit()])

    lead_mode = get_kickoff_record.lead_sub_mode
    if lead_mode == "portal":
        lead_type = True
    else:
        lead_type = False

    chat = get_kickoff_record.real_time_support_chat
    if chat == "on":
        type_chat = True
    else:
        type_chat = False
    live_trans = get_kickoff_record.real_time_support_live_trans
    if live_trans == "on":
        type_live = True
    else:
        type_live = False
    chat = get_kickoff_record.real_time_support_chat
    live_trans = get_kickoff_record.real_time_support_live_trans
    chat_and_live = ''
    if chat == "on":
        if chat == live_trans:
            chat_and_live = True
            type_live = False
            type_chat = False
        else:
            chat_and_live = False

    tag_team_connect_splitting = get_kickoff_record.tag_team_connect_detail
    tag_team_connect_each_data = re.split(',|, \n', tag_team_connect_splitting)
    type_of_connect = tag_team_connect_each_data[0]
    type_of_connect_day = tag_team_connect_each_data[1]
    type_of_connect_time = tag_team_connect_each_data[2]
    type_of_connect_timezone = tag_team_connect_each_data[3]

    key_order_matrix = {k: v for v, k in enumerate(['succes_metrices_one_1', 'succes_metrices_two_1', 'succes_metrices_three_1', 'succes_metrices_one_2', 'succes_metrices_two_2', 'succes_metrices_three_2', 'succes_metrices_one_3', 'succes_metrices_two_3', 'succes_metrices_three_3', 'succes_metrices_one_4', 'succes_metrices_two_4', 'succes_metrices_three_4', 'succes_metrices_one_5', 'succes_metrices_two_5','succes_metrices_three_5'])}
    success_matrix_dict = OrderedDict(sorted(get_kickoff_record.succes_matrix.items(), key=lambda i: key_order_matrix.get(i[0])))

    attach_link_1 = get_kickoff_record.attached_url_link_1
    attach_link_2 = get_kickoff_record.attached_url_link_2
    attach_link_3 = get_kickoff_record.attached_url_link_3
    attach_link_4 = get_kickoff_record.attached_url_link_4
    attach_link_5 = get_kickoff_record.attached_url_link_5

    attach_file_1 = ''
    attach_file_2 = ''
    attach_file_3 = ''
    attach_file_4 = ''
    attach_file_5 = ''
    if get_kickoff_record.upload_file_attachment_1:
        attach_file_1 = get_kickoff_record.upload_file_attachment_1.name
    if get_kickoff_record.upload_file_attachment_2:
        attach_file_2 = get_kickoff_record.upload_file_attachment_2.name
    if get_kickoff_record.upload_file_attachment_3:
        attach_file_3 = get_kickoff_record.upload_file_attachment_3.name
    if get_kickoff_record.upload_file_attachment_4:
        attach_file_4 = get_kickoff_record.upload_file_attachment_4.name
    if get_kickoff_record.upload_file_attachment_5:
        attach_file_5 = get_kickoff_record.upload_file_attachment_5.name

    attach_file_name_1 = ''
    attach_file_name_2 = ''
    attach_file_name_3 = ''
    attach_file_name_4 = ''
    attach_file_name_5 = ''
    key_order_attach_file_name = {k:v for v, k in enumerate(['file_name_attach_1', 'file_name_attach_2', 'file_name_attach_3', 'file_name_attach_4', 'file_name_attach_5'])}
    attach_file_name_dict = OrderedDict(sorted(get_kickoff_record.file_upload_name.items(), key=lambda i: key_order_attach_file_name.get(i[0])))
    if 'file_name_attach_1' in get_kickoff_record.file_upload_name:
        attach_file_name_1 = attach_file_name_dict['file_name_attach_1']
    if 'file_name_attach_2' in get_kickoff_record.file_upload_name:
        attach_file_name_2 = attach_file_name_dict['file_name_attach_2']
    if 'file_name_attach_3' in get_kickoff_record.file_upload_name:
        attach_file_name_3 = attach_file_name_dict['file_name_attach_3']
    if 'file_name_attach_4' in get_kickoff_record.file_upload_name:
        attach_file_name_4 = attach_file_name_dict['file_name_attach_4']
    if 'file_name_attach_5' in get_kickoff_record.file_upload_name:
        attach_file_name_5 = attach_file_name_dict['file_name_attach_5']

    link_file_name_1 = ''
    link_file_name_2 = ''
    link_file_name_3 = ''
    link_file_name_4 = ''
    link_file_name_5 = ''
    key_order_link_file_name = {k:v for v, k in enumerate(['file_name_link_1', 'file_name_link_2', 'file_name_link_3', 'file_name_link_4', 'file_name_link_5'])}
    link_file_name_dict = OrderedDict(sorted(get_kickoff_record.file_url_name.items(), key=lambda i: key_order_link_file_name.get(i[0])))
    if 'file_name_link_1' in get_kickoff_record.file_url_name:
        link_file_name_1 = link_file_name_dict['file_name_link_1']
    if 'file_name_link_2' in get_kickoff_record.file_url_name:
        link_file_name_2 = link_file_name_dict['file_name_link_2']
    if 'file_name_link_3' in get_kickoff_record.file_url_name:
        link_file_name_3 = link_file_name_dict['file_name_link_3']
    if 'file_name_link_4' in get_kickoff_record.file_url_name:
        link_file_name_4 = link_file_name_dict['file_name_link_4']
    if 'file_name_link_5' in get_kickoff_record.file_url_name:
        link_file_name_5 = link_file_name_dict['file_name_link_5']
    media_url = settings.MEDIA_URL

    #*************************************
    # auto populate email in tagteam detail
    managers = User.objects.values_list('email', flat=True)
    google_email = list()
    for manager in managers:
        google_email.append(str(manager))


    # adding tag team Storing tagteam detaile & triggering mail
    if request.method == 'POST':
        tagteamkickoff = KickoffTagteam()
        tagteamkickoff.kickoff_program = get_kickoff_record

        tagteamkickoff.tagteam_added_by = request.user.email

        tagteamkickoff.primery_poc = request.POST.get('primery_poc')
        tagteamkickoff.secondary_poc = request.POST.get('secondary_poc')
        tagteamkickoff.qa = request.POST.get('qa')
        tagteamkickoff.qc = request.POST.get('qc')
        tagteamkickoff.trainer = request.POST.get('trainer')
        tagteamkickoff.all_reps = request.POST.getlist('tagaddreps')

        tagteam_kickoff_meeting_date = request.POST.get('k_o_meeting_date')
        tagteam_kickoff_meeting_time = request.POST.get('kickoff_meeting_time')
        kickoff_meeting_date_time_add = tagteam_kickoff_meeting_date + ' ' + tagteam_kickoff_meeting_time
        tagteamkickoff.kickoff_meeting_date_time = datetime.strptime(kickoff_meeting_date_time_add, '%d.%m.%Y %I:%M %p')

        training_start_date = request.POST.get('training_start_date')
        tagteamkickoff.training_start_date = datetime.strptime(training_start_date, '%d.%m.%Y')
        training_end_date = request.POST.get('training_end_date')
        tagteamkickoff.training_end_date = datetime.strptime(training_end_date, '%d.%m.%Y')

        golive_date = request.POST.get('go_live_date')
        tagteamkickoff.golive_date = datetime.strptime(golive_date, '%d.%m.%Y')

        tagteamkickoff.save()

        bcc_list = list()
        bcc = request.POST.get('kick_off_tagteam_bcc').replace(', ', ',')
        bcc_list = bcc.split(',')
        if bcc_list[-1] == '':
            bcc_list.pop(-1)
        get_bcc_list = User.objects.filter(email__in=bcc_list).values_list('id', flat=True)
        tagteamkickoff.bcc_tagteam.add(*get_bcc_list)
        

        tagteamkickoff.save()

        # mailing functionalities
        set_off_bcc_mails = list()
        for each_mail in bcc_list:
            set_off_bcc_mails.append(str(each_mail))
       
        latest_program = KickoffTagteam.objects.filter(tagteam_added_by=request.user.email).last()
        acces_link = request.META['wsgi.url_scheme']+'://'+request.META['HTTP_HOST']+"/reports/kickoff-export-detail/"+str(get_kickoff_record.id)

        program = tagteamkickoff.kickoff_program.program_name
        google_pocs = googlepoc_email_list
        kick_off_created = tagteamkickoff.kickoff_program.created_date

        mail_to = list()
        program_created_by = tagteamkickoff.kickoff_program.program_created_by
        mail_from = request.user.first_name + ' ' + request.user.last_name
        user = request.user.email
        tagteam_added_by = request.user.first_name + ' ' + request.user.last_name
        going_live = golive_date
        mail_subject = "TagTeam Added [New Program - %s ]" % (program)
        mail_to = ['srinivasans@regalix-inc.com', 'kushalappa.theetharamada@regalix-inc.com', str(user)]
        mail_body = get_template('reports/email_templates/tagteam_added_kickoff.html').render(Context({'program_name': program, 'acces_link':acces_link,'google_pocs':google_pocs,'kick_off_created':kick_off_created, 'going_live':going_live,'program_created_by':program_created_by,'tagteam_added_by':tagteam_added_by}))
        bcc = set(set_off_bcc_mails)
        attachments = list()
        send_mail(mail_subject, mail_body, mail_from, mail_to, list(bcc), attachments, template_added=True)

        return redirect('reports.views.tagteam_kickoff_thankyou')



    return render(request,'reports/kick_off_export_detail.html', {'get_kickoff_record': get_kickoff_record,
                                                                  'googlepoc_list': googlepoc_email_list,
                                                                  'google_poc_email_list': google_poc_email_list,
                                                                  #'bcc_kick_off_prg_list':bcc_kick_off_prg_list,
                                                                  'region_list': region_list,
                                                                  'start_date_converted': start_date_converted,
                                                                  'end_date_converted': end_date_converted,
                                                                  'target_location_list': target_location_list,
                                                                  'estimated_number': estimated_number,
                                                                  'estimated_volume': estimated_volume,
                                                                  'lead_type': lead_type,
                                                                  'type_chat': type_chat,
                                                                  'type_live': type_live,
                                                                  'chat_and_live': chat_and_live,
                                                                  'type_of_connect': type_of_connect,
                                                                  'type_of_connect_day': type_of_connect_day,
                                                                  'type_of_connect_time': type_of_connect_time,
                                                                  'type_of_connect_timezone':type_of_connect_timezone,
                                                                  'matrix': json.dumps(success_matrix_dict),
                                                                  'attach_link_1': attach_link_1, 'attach_link_2': attach_link_2, 
                                                                  'attach_link_3': attach_link_3, 'attach_link_4': attach_link_4, 'attach_link_5': attach_link_5, 
                                                                  'attach_file_1': attach_file_1, 'attach_file_2': attach_file_2, 'attach_file_3': attach_file_3, 
                                                                  'attach_file_4': attach_file_4, 'attach_file_5': attach_file_5, 'media_url': media_url,
                                                                  'attach_file_name_1': attach_file_name_1, 'attach_file_name_2': attach_file_name_2, 'attach_file_name_3': attach_file_name_3, 'attach_file_name_4': attach_file_name_4, 
                                                                  'attach_file_name_5': attach_file_name_5, 'link_file_name_1': link_file_name_1, 'link_file_name_2': link_file_name_2,
                                                                  'link_file_name_3': link_file_name_3, 'link_file_name_4': link_file_name_4, 'link_file_name_5': link_file_name_5,
                                                                  'all_mail': google_email,
                                                                  'final_type_codelist': final_type_codelist,
                                                                  'clean_data_advertize_data':clean_data_advertize_data,
                                                                  # tagteam detayls passing
                                                                  'get_kickoff_tagteam':get_kickoff_tagteam,
                                                                  'reps_email_list':reps_email_list,
                                                                  'training_start_date_display':training_start,
                                                                  'training_end_date_display':training_end,
                                                                  'go_live_date_display':live_date,
                                                                  'meeting_time':meeting_time,
                                                                  'meeting_date_display':meeting_date,
                                                                  'email_bcc_list':email_bcc_list,
                                                                  })
@login_required
def rlsa_bulk_upload_report(request):
    """

    Args:
        request: Request

    Returns: Render response RLSA Bulk upload report HTML

    """
    if request.is_ajax():
        resp = {}
        uploads = []
        if request.user.groups.filter(name='SUPERUSER'):
            records = RLSABulkUpload.objects.all()
        else:
            records = RLSABulkUpload.objects.all(id=request.user.id)
        for rec in records:
            upload = {
                      'uploaded_by': rec.uploaded_by.first_name + " " + rec.uploaded_by.last_name,
                      'upload_id': rec.upload_id,
                      'uploaded_on': time.mktime(rec.created_date.timetuple()),
                      'file_guid': rec.file_path.split('/')[-1].split('.')[0],
                      'file_name': rec.original_name,
                      'created_leads': rec.uploaded_leads,
                      'failed_leads': rec.total_leads - rec.uploaded_leads
                      }
            uploads.append(upload)
        resp['data'] = uploads
        resp['success'] = True
        return HttpResponse(json.dumps(resp), 'application/json')

    return render(request, 'reports/rlsa_bulk_report.html')

@login_required
def download_rlsa_bulk_file(request):
    file_guid = request.GET.get('guid', None)
    if file_guid:
        file_path = settings.MEDIA_ROOT + '/rlsa_bulk_csv/'+ str(file_guid) + ".csv"
        row = RLSABulkUpload.objects.get(file_path=file_path)
        data = open(file_path, 'r').read()
        resp = HttpResponse(data, mimetype='application/x-download')
        resp['Content-Disposition'] = 'attachment;filename='+row.original_name
        return resp
    else:
        return HttpResponse(json.dumps({'success':False, 'msg': 'Invalid Request'}), 'application/json')

# -------------------------------------------------------
#                   Inventory Management
# -------------------------------------------------------
@login_required
@csrf_exempt
def inventory_handler(request):
    """
    Args:
        request: Request Object
    Returns: Based on request Method, i.e. if "GET", it will return all the inventory data, if "POST", creates a new
    inventory record, if "PUT", updates an existing inventory record.

    """
    if request.method == "GET":
        if request.user.groups.filter(name='INVENTORYUSER'):
            inventory_details = request.GET.get('inventory', False)
            if inventory_details:
                data = []
                records = ChromebookInventory.objects.all().order_by('employee_name')
                for rec in records:
                    da = {
                        'employee_id': rec.employee_id,
                        'employee_alias': rec.employee_alias,
                        'employee_name': rec.employee_name,
                        'employee_ldap': rec.employee_ldap,
                        'employee_project': rec.employee_project,
                        'device_type': rec.device_type,
                        'mac_id': rec.mac_id,
                        'employee_status': rec.employee_status,
                        'device_status': rec.device_status,
                        'returned_on': rec.returned_on,
                        'issued_on': time.mktime(rec.issued_on.timetuple()),
                        'id': rec.id
                    }
                    data.append(da)
                resp = {'success': True, 'data': data}
                return HttpResponse(json.dumps(resp), content_type='application/json')
            return render(request, 'reports/inventory_manager.html')
        else:
            from django.core import exceptions
            raise exceptions.PermissionDenied
    elif request.method == "POST":
        data = json.loads(request.body)
        # Mandatory Fields
        name = data['name']
        ldap = data['ldap']
        project = data['project']
        emp_id = data['emp_id']

        cbi = ChromebookInventory()

        cbi.created_by = request.user
        cbi.modified_by = request.user
        cbi.employee_alias = data.get('alias')
        cbi.employee_id = emp_id
        cbi.employee_name = name
        cbi.employee_ldap = ldap
        cbi.employee_project = project
        cbi.device_type = data.get('deviceType')
        cbi.mac_id = data.get('macId')
        emp_stat = data.get('employeeStatus')
        if emp_stat == 'active':
            emp_stat = True
        else:
            emp_stat = False
        dev_stat = data.get('deviceStatus')
        if dev_stat == 'assigned':
            dev_stat = True
        else:
            dev_stat = False
        cbi.employee_status = emp_stat
        cbi.device_status = dev_stat
        cbi.issued_on = datetime.strptime(data.get('issuedOn'), "%d-%m-%Y")
        try:
            cbi.save()
            resp = {'success': True, 'type':'new', 'msg': 'User data saved succesfully',
                    'data': {'id': cbi.id}}
        except IntegrityError:
            resp = {'success': False, 'type':'duplicate', 'msg': 'User data already exists.'}
        return HttpResponse(json.dumps(resp), content_type='application/json')
    elif request.method == "PUT":
        data = json.loads(request.body)
        # Mandatory Fields
        id = data['row_id']
        name = data['name']
        ldap = data['ldap']
        emp_id = data['emp_id']
        project = data['project']

        cbi = ChromebookInventory.objects.get(id=id)

        cbi.modified_by = request.user
        cbi.employee_alias = data.get('alias')
        cbi.employee_name = name
        cbi.employee_id = emp_id
        cbi.employee_ldap = ldap
        cbi.employee_project = project
        cbi.device_type = data.get('deviceType')
        cbi.mac_id = data.get('macId')
        emp_stat = data.get('employeeStatus')
        if emp_stat == 'active':
            emp_stat = True
        else:
            emp_stat = False
        dev_stat = data.get('deviceStatus')
        if dev_stat == 'assigned':
            dev_stat = True
        else:
            dev_stat = False
        cbi.employee_status = emp_stat
        cbi.device_status = dev_stat
        try:
            issued_on = datetime.strptime(data.get('issuedOn'), "%d-%m-%Y")
        except:
            issued_on = datetime.strptime(data.get('issuedOn'), "%d-%m-%y")
        cbi.issued_on = issued_on
        cbi.save()
        resp = {'success': True, 'msg': 'User data saved succesfully'}
        return HttpResponse(json.dumps(resp), content_type='application/json')
