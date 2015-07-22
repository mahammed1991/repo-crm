from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from datetime import datetime
from leads.models import Location
from report_services import ReportService, DownloadLeads, TrendsReportServices
from lib.helpers import get_quarter_date_slots, is_manager, get_user_under_manager
from django.conf import settings
from reports.models import LeadSummaryReports
from main.models import UserDetails
from django.db.models import Q
from reports.models import Region
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import re


@login_required
def reports(request):
    """ New Report """

    manager = is_manager(request.user.email)
    team_members = list()
    if manager:
        team_members = get_user_under_manager(request.user.email)

    locations = ReportService.get_all_locations()
    teams = ReportService.get_all_teams()
    rgx_teams = Region.objects.all()
    if '' in teams:
        teams.remove('')
        teams.append('Other')
    code_types = ReportService.get_all_code_type()
    code_types = [str(codes.encode('utf-8')) for codes in code_types]
    return render(request, 'reports/reports.html', {'locations': locations, 'manager': manager, 'team_members': team_members,
                                                    'teams': teams, 'rgx_teams': rgx_teams,
                                                    'code_types': code_types})


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
    c_types = ['total', 'total_tag', 'Google Shopping Migration', 'Google Shopping Setup']
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
        code_types = ReportService.get_all_code_type()
        code_types = [str(codes.encode('utf-8')) for codes in code_types]

        if report_timeline:
            start_date, end_date = ReportService.get_date_range_by_timeline(report_timeline)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

        report_details = dict()
        if ldap_id:
            email = User.objects.select_related('email').get(pk=ldap_id)
        else:
            email = request.user.email

        # if '' in teams:
        #     teams.remove('')

        if report_type == 'default_report':
            report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, list())
        elif report_type == 'leadreport_individualRep':
            report_detail = ReportService.get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, [email])
        elif report_type == 'leadreport_teamLead':
            team_emails = list(User.objects.values_list('email', flat=True).filter(id__in=team_members).distinct().order_by('first_name'))
            team_emails.append(email)
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
            team_emails.append(email)
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
