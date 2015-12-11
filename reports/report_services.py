import csv
import os
import mimetypes
from datetime import datetime, date, timedelta
from leads.models import Leads, RegalixTeams, Team, Location, TreatmentType, WPPLeads, PicassoLeads
from reports.models import QuarterTargetLeads, Region, CSATReport
from lib.helpers import (get_week_start_end_days, first_day_of_month, get_quarter_date_slots,
                         last_day_of_month, date_range_by_quarter, dsum, prev_quarter_date_range, get_months_from_date,
                         get_previous_month_start_end_days, get_weeks_in_quarter_to_date, is_manager)
from django.conf import settings
from django.http import HttpResponse
import time
import collections
from collections import OrderedDict
from django.db.models import Count, Avg


class ReportService(object):

    def __init__(self):
        pass

    @staticmethod
    def get_all_code_type():
        ''' Get all code types '''
        return list(Leads.objects.exclude(type_1__in=['', 'WPP']).values_list(
            'type_1', flat=True).distinct().order_by('type_1'))

    @staticmethod
    def get_all_lead_status():
        ''' Get all lead status '''
        return list(Leads.objects.exclude(lead_status='').values_list(
            'lead_status', flat=True).distinct().order_by('lead_status'))

    @staticmethod
    def get_all_locations():
        ''' Get all Location name '''
        return list(Leads.objects.exclude(country='').values_list('country', flat=True).distinct().order_by('country'))

    @staticmethod
    def get_all_regalix_teams():
        ''' Get all regalix Team'''
        return list(RegalixTeams.objects.values_list('team_name', flat=True).distinct().order_by('team_name'))

    @staticmethod
    def get_all_teams():
        ''' Get all team name '''
        teams = list(Leads.objects.values_list('team', flat=True).distinct().order_by('team'))
        # if space in teams then move to last position
        if '' in teams:
            teams.remove('')
            teams.append('')
        return teams

    @staticmethod
    def get_current_quarter(dt):
        if (1 <= dt.month <= 3):
            quarterly = "Q1"
        elif (4 <= dt.month <= 6):
            quarterly = "Q2"
        elif (7 <= dt.month <= 9):
            quarterly = "Q3"
        else:
            quarterly = "Q4"

        return quarterly

    @staticmethod
    def get_date_range_by_timeline(timeline):
        ''' Get start and end date by timeline options: thisweek, lastweek, thismonth and lastmonth '''
        if len(timeline) > 1:
            # get date range by given date_range
            start_date = datetime.strptime(str(timeline[0]), "%b %d, %Y")
            end_date = datetime.strptime(str(timeline[1]), "%b %d, %Y")
            return start_date, end_date
        else:
            if timeline[0] == 'today':
                today = datetime.utcnow()
                return datetime(today.year, today.month, today.day), datetime(today.year, today.month, today.day, 23, 59, 59)
            elif timeline[0] == 'this_week':
                current_week = date.today().isocalendar()[1]
                current_year = datetime.utcnow().year
                return get_week_start_end_days(current_year, current_week)
            elif timeline[0] == 'last_week':
                current_week = date.today().isocalendar()[1]
                last_week = current_week - 1
                current_year = datetime.utcnow().year
                return get_week_start_end_days(current_year, last_week)
            elif timeline[0] == 'this_month':
                return first_day_of_month(datetime.utcnow()), last_day_of_month(datetime.utcnow())
            elif timeline[0] == 'last_month':
                return get_previous_month_start_end_days(datetime.utcnow())
            elif timeline[0] == 'this_quarter':
                return date_range_by_quarter(ReportService.get_current_quarter(datetime.utcnow()))

    @staticmethod
    def get_leads_by_location(location, lead_status, code_types, start_date, end_date):
        ''' Get leads by country/locations '''

        leads = Leads.objects.filter(country=location, created_date__gte=start_date,
                                     created_date__lte=end_date, lead_status__in=lead_status,
                                     type_1__in=code_types).order_by('country')
        return leads

    @staticmethod
    def get_leads_by_team(team, lead_status, code_types, start_date, end_date):
        ''' Get leads by team '''
        leads = Leads.objects.filter(team=team, created_date__gte=start_date,
                                     created_date__lte=end_date, lead_status__in=lead_status,
                                     type_1__in=code_types).order_by('team')
        return leads

    @staticmethod
    def get_leads_by_locations(locations, lead_status, code_types, start_date, end_date):
        ''' Get leads by country/locations '''

        leads = Leads.objects.filter(country__in=locations, created_date__gte=start_date,
                                     created_date__lte=end_date, lead_status__in=lead_status,
                                     type_1__in=code_types).order_by('country')
        return leads

    @staticmethod
    def get_leads_by_teams(teams, lead_status, code_types, start_date, end_date):
        ''' Get leads by team '''
        leads = Leads.objects.filter(team__in=teams, created_date__gte=start_date,
                                     created_date__lte=end_date, lead_status__in=lead_status,
                                     type_1__in=code_types).order_by('team')
        return leads

    @staticmethod
    def get_leads_by_team_and_location(team, location, lead_status, code_types, start_date, end_date):
        ''' Get leads by team and location'''

        leads = Leads.objects.filter(country=location, team=team, lead_status__in=lead_status,
                                     type_1__in=code_types, created_date__gte=start_date,
                                     created_date__lte=end_date).order_by('created_date')
        return leads

    @staticmethod
    def get_leads_by_status_and_code_types(lead_status, code_types, start_date, end_date):
        ''' Get Implemented Reports with CR ratio '''

        leads = Leads.objects.filter(created_date__gte=start_date,
                                     created_date__lte=end_date,
                                     lead_status__in=lead_status,
                                     type_1__in=code_types).order_by('lead_status')
        return leads

    @staticmethod
    def get_leads_by_teams_and_locations(teams, locations, lead_status, code_types, start_date, end_date):
        ''' Get leads '''

        leads = Leads.objects.filter(team__in=teams,
                                     country__in=locations,
                                     created_date__gte=start_date,
                                     created_date__lte=end_date,
                                     lead_status__in=lead_status,
                                     type_1__in=code_types).order_by('lead_status')
        return leads

    @staticmethod
    def get_leads_for_individual(email, start_date, end_date):
        ''' Get the individual Leads '''
        leads = Leads.objects.filter(google_rep_email=email,
                                     lead_status__in=settings.LEAD_STATUS,
                                     created_date__gte=start_date,
                                     created_date__lte=end_date)
        return leads

    # ========================================================optimization ======================

    @staticmethod
    def get_report_details_for_filters(report_timeline, code_types, teams, countries, start_date, end_date, emails):
        report_detail = dict()
        query = {'created_date__gte': start_date, 'created_date__lte': end_date, 'type_1__in': code_types}
        if emails and teams and countries:
            query['google_rep_email__in'] = emails
            query['country__in'] = countries
            query['team__in'] = teams
            leads = Leads.objects.values_list('id', flat=True).exclude(type_1='WPP').filter(**query)

        elif not emails and teams and countries:
            query['country__in'] = countries
            query['team__in'] = teams
            leads = Leads.objects.values_list('id', flat=True).exclude(type_1='WPP').filter(**query)

        elif emails and not teams and not countries:
            query['google_rep_email__in'] = emails
            leads = Leads.objects.values_list('id', flat=True).exclude(type_1='WPP').filter(**query)

        elif not emails and not teams and countries:
            query['country__in'] = countries
            leads = Leads.objects.values_list('id', flat=True).exclude(type_1='WPP').filter(**query)

        elif emails and not teams and countries:
            query['country__in'] = countries
            query['google_rep_email__in'] = emails
            leads = Leads.objects.values_list('id', flat=True).exclude(type_1='WPP').filter(**query)

        lead_ids = leads

        lead_status_summary = ReportService.get_leads_status_summary(lead_ids)

        lead_status_analysis_table_grp = list()

        for code_type in code_types:

            lead_status_analysis_grp = {code_type: ''}  

            leads_per_code_type_grp = Leads.objects.filter(type_1=code_type, id__in=lead_ids).values('lead_status').annotate(dcount=Count('lead_status'))

            lead_status_analysis_grp[code_type] = ReportService.get_lead_status_analysis(leads_per_code_type_grp)

            lead_status_analysis_table_grp.append(lead_status_analysis_grp)
        pie_chart_dict = dict()
        
        for cod_typ in lead_status_analysis_table_grp:
            key = cod_typ.keys()[0]
            value = cod_typ[key]['Total']
            pie_chart_dict[key] = value

        # week_on_week_trends = ReportService.get_week_on_week_trends_details(lead_ids, countries, teams, code_types)
        timeline_chart_details = ReportService.get_timeline_chart_details(report_timeline, lead_ids, countries, teams, code_types, emails)
        report_detail.update({'lead_status_summary': lead_status_summary,
                              'piechart': pie_chart_dict,
                              'table_header': settings.LEAD_STATUS_DICT,
                              'lead_code_type_analysis': sorted(lead_status_analysis_table_grp),
                              # 'week_on_week_details_in_qtd': week_on_week_trends,
                              'timeline_chart_details': timeline_chart_details,
                              'sort_keys': sorted(timeline_chart_details)})
        return report_detail

    @staticmethod
    def get_leads_status_summary(lead_ids):
        lead_status_analysis = Leads.objects.exclude(lead_status='Rework Required').filter(id__in=lead_ids).values('lead_status').annotate(count=Count('pk'))
        leads_status_summary = {key: 0 for key in settings.LEAD_STATUS_DICT.keys()}
        total_leads = 0
        for key in settings.LEAD_STATUS_DICT.keys():
            for lead_status_count in lead_status_analysis:
                if lead_status_count['lead_status'] in settings.LEAD_STATUS_DICT[key]:
                    leads_status_summary[key] = leads_status_summary[key] + lead_status_count['count']
                    total_leads += leads_status_summary[key]

        # Rework required lead status changes
        rr_inactive_leads = Leads.objects.filter(id__in=lead_ids, lead_status='Rework Required', lead_sub_status='RR - Inactive').count()

        rework_required_implemented_leads = Leads.objects.exclude(lead_sub_status='RR - Inactive').filter(id__in=lead_ids, lead_status='Rework Required').count()

        leads_status_summary['In Active'] += rr_inactive_leads

        leads_status_summary['Implemented'] += rework_required_implemented_leads

        # Rework required lead status ends here

        leads_status_summary['total_leads'] = len(lead_ids)

        leads_status_summary['TAT'] = Leads.objects.filter(id__in=lead_ids).aggregate(Avg('tat'))['tat__avg']
        return leads_status_summary

    @staticmethod
    def get_timeline_chart_details(report_timeline, lead_ids, countries, teams, code_types, emails):
        if len(report_timeline) <= 1:
            timeline = str(report_timeline[0])
            if timeline in ['this_week', 'last_week', 'today']:
                week_on_week_trends = dict()
                cur_week = date.today().isocalendar()[1]
                year = datetime.utcnow().year
                for week_num in range(cur_week - 3, cur_week + 1):
                    start_date, end_date = get_week_start_end_days(year, week_num)
                    week_on_week_trends['Week ' + str(week_num)] = {'leads_won': 0, 'total_leads_submitted': 0}
                    if emails:
                        query_total = {'google_rep_email__in': emails, 'country__in': countries, 'team__in': teams, 'type_1__in': code_types}
                    else:
                        query_total = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types}
                    start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
                    query_total['created_date__gte'] = start_date
                    query_total['created_date__lte'] = end_date
                    week_on_week_trends['Week ' + str(week_num)]['total_leads_submitted'] = Leads.objects.filter(**query_total).count()
                    query_total['lead_status'] = 'Rework Required'
                    rr_implemented_leads = Leads.objects.exclude(lead_sub_status='RR - Inactive').filter(**query_total).count()
                    del query_total['lead_status']
                    query_total['lead_status__in'] = settings.LEAD_STATUS_DICT['Implemented']
                    week_on_week_trends['Week ' + str(week_num)]['leads_won'] = Leads.objects.filter(**query_total).count() + rr_implemented_leads
                return week_on_week_trends
            elif timeline in ['this_month', 'last_month']:
                week_on_week_trends = dict()
                year = datetime.utcnow().year
                if timeline == 'this_month':
                    first_day = first_day_of_month(datetime.utcnow())
                    last_day = last_day_of_month(datetime.utcnow())
                else:
                    first_day, last_day = get_previous_month_start_end_days(datetime.utcnow())

                index = 0
                for i in range(first_day.isocalendar()[1], last_day.isocalendar()[1] + 1):
                    index = index + 1
                    start_date, end_date = get_week_start_end_days(year, i)
                    if i == first_day.isocalendar()[1]:
                        start_date = first_day
                        end_date = end_date
                    elif i == last_day.isocalendar()[1]:
                        start_date = start_date
                        end_date = last_day
                    start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
                    week_on_week_trends['Week ' + str(index)] = {'leads_won': 0, 'total_leads_submitted': 0}
                    if emails:
                        query_total = {'google_rep_email__in': emails, 'country__in': countries, 'team__in': teams, 'type_1__in': code_types}
                    else:
                        query_total = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types}
                    query_total['created_date__gte'] = start_date
                    query_total['created_date__lte'] = end_date
                    week_on_week_trends['Week ' + str(index)]['total_leads_submitted'] = Leads.objects.filter(**query_total).count()
                    query_total['lead_status__in'] = ['Rework Required']
                    rr_implemented_leads = Leads.objects.exclude(lead_sub_status='RR - Inactive').filter(**query_total).count()
                    del query_total['lead_status__in']
                    query_total['lead_status__in'] = settings.LEAD_STATUS_DICT['Implemented']
                    week_on_week_trends['Week ' + str(index)]['leads_won'] = Leads.objects.filter(**query_total).count() + rr_implemented_leads

                return week_on_week_trends

            elif timeline in ['this_quarter']:
                month_on_month_trends = dict()
                months = get_months_from_date(datetime.utcnow())
                for idx, month in enumerate(months):
                    month_on_month_trends['Month ' + str(idx + 1)] = {'leads_won': 0, 'total_leads_submitted': 0}
                    start_date = datetime(datetime.utcnow().year, month, 1, 0, 0, 0)
                    last_day = last_day_of_month(start_date)
                    end_date = datetime(last_day.year, last_day.month, last_day.day, 23, 59, 59)
                    query_total = dict()
                    if emails:
                        query_total = {'google_rep_email__in': emails, 'country__in': countries, 'team__in': teams, 'type_1__in': code_types}
                    else:
                        query_total = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types}
                    query_total['created_date__gte'] = start_date
                    query_total['created_date__lte'] = end_date
                    month_on_month_trends['Month ' + str(idx + 1)]['total_leads_submitted'] = Leads.objects.filter(**query_total).count()

                    query_total['lead_status__in'] = ['Rework Required']
                    rr_implemented_leads = Leads.objects.exclude(lead_sub_status='RR - Inactive').filter(**query_total).count()
                    del query_total['lead_status__in']

                    query_total['lead_status__in'] = settings.LEAD_STATUS_DICT['Implemented']
                    month_on_month_trends['Month ' + str(idx + 1)]['leads_won'] = Leads.objects.filter(**query_total).count() + rr_implemented_leads
                    del query_total['lead_status__in']

                return month_on_month_trends
        else:
            week_on_week_trends = ReportService.get_week_on_week_trends_details(lead_ids, countries, teams, code_types)
            return week_on_week_trends

    @staticmethod
    def get_week_on_week_trends_details(lead_ids, countries, teams, code_types):
        ''' Week on week analysis of leads won over leads submitted '''

        week_on_week_trends = dict()
        weeks_in_qtd = get_weeks_in_quarter_to_date()
        for index in range(1, len(weeks_in_qtd) + 1):

            week_on_week_trends[index] = {'leads_won': 0}

            if index == 1:
                start_date, end_date = weeks_in_qtd[index - 1]
                start_date = datetime(end_date.year, end_date.month, 1, 0, 0, 0)
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

            elif index == len(weeks_in_qtd):
                start_date, end_date = weeks_in_qtd[index - 1]
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                end_date = datetime(start_date.year, start_date.month, last_day_of_month(start_date).day, 23, 59, 59)

            else:
                start_date, end_date = weeks_in_qtd[index - 1]
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

            # query = {'id__in': lead_ids, 'country__in': countries, 'team__in': teams, 'type_1__in': code_types, 'created_date__gte': start_date, 'created_date__lte': end_date}
            query = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types, 'created_date__gte': start_date, 'created_date__lte': end_date}

            if teams and countries:
                week_on_week_trends[index]['total_leads_submitted'] = Leads.objects.filter(**query).count()

                query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']

                week_on_week_trends[index]['leads_won'] = Leads.objects.exclude(lead_sub_status='RR - Inactive').filter(**query).count()
                week_on_week_trends[index]['date_range'] = '%s to %s' % (start_date, end_date)

        return week_on_week_trends

    @staticmethod
    def get_program_report_by_locations(teams, countries, code_types):
        """ Get reports for each Programs by all locations """

        # teams.append('')

        week = int(time.strftime("%W")) + 1
        year = int(time.strftime("%Y"))
        week_start_date, week_end_date = get_week_start_end_days(year, week)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(datetime.utcnow())

        quarter_end_date = datetime.utcnow()

        prev_qtr_start_dt, prev_qtr_end_dt = prev_quarter_date_range(datetime.utcnow())

        prev_qtr_year = prev_qtr_start_dt.year

        quarter = ReportService.get_current_quarter(prev_qtr_start_dt)

        team_dict = {team.id: team.team_name for team in Team.objects.all()}

        location_dict = {}

        for location in Location.objects.all():
            location_dict[location.id] = location.location_name

        target_leads = QuarterTargetLeads.objects.filter(quarter=quarter, year=prev_qtr_year).values('location', 'program', 'target_leads').annotate(count=Count('pk'))

        week_query = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types, 'created_date__gte': week_start_date, 'created_date__lte': week_end_date}

        week_leads_total = Leads.objects.filter(**week_query).values('country', 'team').annotate(count=Count('pk'))

        week_query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
        total_week_leads = Leads.objects.values_list('id', flat=True).exclude(lead_sub_status='RR - Inactive').filter(**week_query)
        week_leads_wins = Leads.objects.filter(id__in=total_week_leads).values('country', 'team').annotate(count=Count('pk'))

        quarter_query = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types, 'created_date__gte': quarter_start_date, 'created_date__lte': quarter_end_date}

        quarter_leads_total = Leads.objects.filter(**quarter_query).values('country', 'team').annotate(count=Count('pk'))

        quarter_query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']

        qtr_win_leads = Leads.objects.values_list('id', flat=True).exclude(lead_sub_status='RR - Inactive').filter(**quarter_query)

        quarter_leads_wins = Leads.objects.filter(id__in=qtr_win_leads).values('country', 'team').annotate(count=Count('pk'))

        prev_qtr_query = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types, 'created_date__gte': prev_qtr_start_dt, 'created_date__lte': prev_qtr_end_dt}

        prev_qtr_leads_total = Leads.objects.exclude().filter(**prev_qtr_query).values('country', 'team').annotate(count=Count('pk'))
        detail = dict()

        for team in teams:
            detail[team] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'locations': {}, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0.0}
            for country in countries:
                detail[team]['locations'][country] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0.0}

        detail = ReportService.get_updated_detail_dict(week_leads_total, detail, 'week_total')
        detail = ReportService.get_updated_detail_dict(week_leads_wins, detail, 'week_win')
        detail = ReportService.get_updated_detail_dict(quarter_leads_total, detail, 'qtd_total')
        detail = ReportService.get_updated_detail_dict(quarter_leads_wins, detail, 'qtd_win')
        detail = ReportService.get_updated_detail_dict(prev_qtr_leads_total, detail, 'end_qtr_total')

        for trgt_leads in target_leads:
            team = team_dict[trgt_leads['program']]
            location = location_dict[trgt_leads['location']]
            if trgt_leads['program'] in team_dict and trgt_leads['location'] in location_dict:
                if detail[team]['locations'][location]:
                    detail[team]['locations'][location]['end_qtr_target'] = trgt_leads['target_leads']
                    loc_out_vs_trgt = float(detail[team]['locations'][location]['end_qtr_total']) / detail[team]['locations'][location]['end_qtr_target'] if detail[team]['locations'][location]['end_qtr_target'] != 0 else 0
                    detail[team]['locations'][location]['out_vs_trgt'] = round(loc_out_vs_trgt, 2) * 100

        for program in detail.keys():
            program_target = list()
            for loc in detail[program]['locations'].keys():
                program_target.append(detail[program]['locations'][loc]['end_qtr_target'])
            detail[program]['end_qtr_target'] = sum(program_target)
            out_vs_trgt = float(detail[program]['end_qtr_total']) / detail[program]['end_qtr_target'] if detail[program]['end_qtr_target'] != 0 else 0
            detail[program]['out_vs_trgt'] = round(out_vs_trgt, 2) * 100

        return detail

    @staticmethod
    def get_updated_detail_dict(result, detail, param):

        for res in result:
            if res['team'] in detail:
                if res['country'] in detail[res['team']]['locations']:
                    detail[res['team']]['locations'][res['country']][param] = res['count']
                    detail[res['team']][param] += res['count']

        return detail

    @staticmethod
    def get_region_report_by_program(countries, teams, code_types):
        """ Get reports for each Programs by all locations """
        week = int(time.strftime("%W")) + 1
        year = int(time.strftime("%Y"))
        week_start_date, week_end_date = get_week_start_end_days(year, week)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(datetime.utcnow())

        quarter_end_date = datetime.utcnow()

        prev_qtr_start_dt, prev_qtr_end_dt = prev_quarter_date_range(datetime.utcnow())

        prev_qtr_year = prev_qtr_start_dt.year

        quarter = ReportService.get_current_quarter(prev_qtr_start_dt)

        team_dict = {team.id: team.team_name for team in Team.objects.all()}

        location_dict = {}

        for location in Location.objects.all():
            location_dict[location.id] = location.location_name

        week_query = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types, 'created_date__gte': week_start_date, 'created_date__lte': week_end_date}

        week_leads_total = Leads.objects.filter(**week_query).values('country', 'team').annotate(count=Count('pk'))

        week_query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
        total_week_leads = Leads.objects.values_list('id', flat=True).exclude(lead_sub_status='RR - Inactive').filter(**week_query)
        week_leads_wins = Leads.objects.filter(id__in=total_week_leads).values('country', 'team').annotate(count=Count('pk'))

        quarter_query = {'country__in': countries, 'team__in': teams, 'type_1__in': code_types, 'created_date__gte': quarter_start_date, 'created_date__lte': quarter_end_date}

        quarter_leads_total = Leads.objects.filter(**quarter_query).values('country', 'team').annotate(count=Count('pk'))

        quarter_query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']

        qtr_win_leads = Leads.objects.values_list('id', flat=True).exclude(lead_sub_status='RR - Inactive').filter(**quarter_query)

        quarter_leads_wins = Leads.objects.filter(id__in=qtr_win_leads).values('country', 'team').annotate(count=Count('pk'))

        prev_qtr_leads_total = Leads.objects.filter(country__in=countries, team__in=teams, type_1__in=code_types,
                                                    created_date__gte=prev_qtr_start_dt, created_date__lte=prev_qtr_end_dt).values('country', 'team').annotate(count=Count('pk'))

        target_leads = QuarterTargetLeads.objects.filter(quarter=quarter, year=prev_qtr_year).values('location', 'program', 'target_leads').annotate(count=Count('pk'))

        detail = dict()

        for location in countries:
            detail[location] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'programs': {}, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0}
            for team in teams:
                detail[location]['programs'][team] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0}

        detail = ReportService.get_region_view_detail_dict(week_leads_total, detail, 'week_total')
        detail = ReportService.get_region_view_detail_dict(week_leads_wins, detail, 'week_win')
        detail = ReportService.get_region_view_detail_dict(quarter_leads_total, detail, 'qtd_total')
        detail = ReportService.get_region_view_detail_dict(quarter_leads_wins, detail, 'qtd_win')
        detail = ReportService.get_region_view_detail_dict(prev_qtr_leads_total, detail, 'end_qtr_total')

        for trgt_leads in target_leads:
            team = team_dict[trgt_leads['program']]
            location = location_dict[trgt_leads['location']]
            if trgt_leads['program'] in team_dict and trgt_leads['location'] in location_dict:
                if detail[location]['programs'][team]:
                    detail[location]['programs'][team]['end_qtr_target'] = trgt_leads['target_leads']
                    pgm_out_vs_trgt = float(detail[location]['programs'][team]['end_qtr_total']) / detail[location]['programs'][team]['end_qtr_target'] if detail[location]['programs'][team]['end_qtr_target'] != 0 else 0
                    detail[location]['programs'][team]['out_vs_trgt'] = round(pgm_out_vs_trgt, 2) * 100

        for location in detail.keys():
            location_target = list()
            for pgm in detail[location]['programs'].keys():
                location_target.append(detail[location]['programs'][pgm]['end_qtr_target'])
            detail[location]['end_qtr_target'] = sum(location_target)
            out_vs_trgt = float(detail[location]['end_qtr_total']) / detail[location]['end_qtr_target'] if detail[location]['end_qtr_target'] != 0 else 0
            detail[location]['out_vs_trgt'] = round(out_vs_trgt, 2) * 100

        return detail

    @staticmethod
    def get_region_view_detail_dict(result, detail, param):
        for res in result:
            if res['country'] in detail:
                if res['team'] in detail[res['country']]['programs']:
                    detail[res['country']]['programs'][res['team']]['end_qtr_total'] = res['count']
                    detail[res['country']][param] += res['count']

        return detail

    @staticmethod
    def get_wpp_report_details_for_filters(start_date, end_date, emails):
        treatment_types = [treatment_type.name for treatment_type in TreatmentType.objects.all()]
        wpp_report_detail = dict()
        if emails:
            query = {'created_date__gte': start_date, 'created_date__lte': end_date,
                     'google_rep_email__in': emails, 'lead_status__in': settings.WPP_LEAD_STATUS, 'treatment_type__in': treatment_types}
        else:
            query = {'created_date__gte': start_date, 'created_date__lte': end_date, 'lead_status__in': settings.WPP_LEAD_STATUS, 'treatment_type__in': treatment_types}

        wpp_lead_status_counts = WPPLeads.objects.filter(**query).values('lead_status').annotate(count=Count('pk'))
        wpp_lead_status_count_dict = {str(rec['lead_status']): rec['count'] for rec in wpp_lead_status_counts}
        wpp_lead_status_count_dict['TOTAL'] = WPPLeads.objects.filter(**query).count()
        wpp_lead_status_count_dict['TAT'] = WPPLeads.objects.filter(**query).aggregate(Avg('tat'))['tat__avg']

        key_order = [sts for sts in settings.WPP_LEAD_STATUS]
        key_order.append('TAT')
        key_order.append('TOTAL')

        for lead_status in settings.WPP_LEAD_STATUS:
                if lead_status not in wpp_lead_status_count_dict:
                    wpp_lead_status_count_dict[lead_status] = 0

        if wpp_lead_status_count_dict['TAT'] is None or '':
            wpp_lead_status_count_dict['TAT'] = 0

        wpp_keyorder = {k: v for v, k in enumerate(key_order)}
        wpp_report_detail['wpp_lead_status_analysis'] = OrderedDict(sorted(wpp_lead_status_count_dict.items(), key=lambda i: wpp_keyorder.get(i[0])))
        wpp_report_detail['wpp_treatment_type_analysis'], wpp_report_detail['pie_chart_dict'] = ReportService.get_wpp_treatment_type_lead_status_analysis(query)
        return wpp_report_detail

    @staticmethod
    def get_wpp_treatment_type_lead_status_analysis(query):

        wpp_treatment_type_lead_status_analysis = dict()
        lead_status_per_treatment_type = WPPLeads.objects.filter(**query).values('treatment_type').annotate(count=Count('pk'))
        pie_chart_dict = {str(rec['treatment_type']): rec['count'] for rec in lead_status_per_treatment_type}

        key_order = [sts for sts in settings.WPP_LEAD_STATUS]
        key_order.append('TAT')
        key_order.append('TOTAL')
        wpp_keyorder = {k: v for v, k in enumerate(key_order)}

        for treatement_type in TreatmentType.objects.all():
            query['treatment_type'] = treatement_type
            lead_status_per_treatment_type = WPPLeads.objects.filter(**query).values('lead_status').annotate(count=Count('pk'))
            lead_status_per_treatment_type_dict = {str(rec['lead_status']): rec['count'] for rec in lead_status_per_treatment_type}
            for lead_status in settings.WPP_LEAD_STATUS:
                if lead_status not in lead_status_per_treatment_type_dict:
                    lead_status_per_treatment_type_dict[lead_status] = 0
            lead_status_per_treatment_type_dict['TOTAL'] = WPPLeads.objects.filter(**query).count()
            treatement_type_tat = WPPLeads.objects.filter(**query).aggregate(Avg('tat'))['tat__avg']
            if treatement_type_tat:
                lead_status_per_treatment_type_dict['TAT'] = treatement_type_tat
            else:
                lead_status_per_treatment_type_dict['TAT'] = 0
            wpp_treatment_type_lead_status_analysis[str(treatement_type.name)] = OrderedDict(sorted(lead_status_per_treatment_type_dict.items(), key=lambda i: wpp_keyorder.get(i[0])))

        return wpp_treatment_type_lead_status_analysis, pie_chart_dict

    # ======================================================end of optimization==============

    @staticmethod
    def get_unmapped_survey(selected_filters, report_type, start_date, end_date):
        csat_query = dict()
        csat_query['survey_date__gte'] = start_date
        csat_query['survey_date__lte'] = end_date

        if 'survey_channel_phone' in selected_filters:
            csat_query['channel__in'] = ['PHONE']
        if 'survey_channel_email' in selected_filters:
            csat_query['channel__in'] = ['EMAIL']
        if 'survey_channel_combined' in selected_filters:
            csat_query['channel__in'] = ['EMAIL', 'PHONE']

        unmapped_count = CSATReport.objects.exclude(category='MAPPED').filter(**csat_query).count()
        return unmapped_count

    @staticmethod
    def get_csat_report(selected_filters, report_type, start_date, end_date):
        report_data = list()
        key_response = {1: 'Extremely satisfied', 2: 'Moderately satisfied', 3: 'Slightly satisfied', 4: 'Neither satisfied nor dissatisfied', 5: 'Slightly dissatisfied', 6: 'Moderately dissatisfied', 7: 'Extremely dissatisfied'}

        csat_query = dict()
        if 'sel_all' in selected_filters:
            csat_query['category__in'] = ['MAPPED', 'UNMAPPED']
            csat_query['channel__in'] = ['EMAIL', 'PHONE']
            csat_query['process__in'] = ['TAG', 'SHOPPING']
        else:
            if 'survey_category_combined' in selected_filters:
                csat_query['category__in'] = ['MAPPED', 'UNMAPPED']
            if 'survey_category_mapped' in selected_filters:
                csat_query['category__in'] = ['MAPPED']
            if 'survey_category_unmapped' in selected_filters:
                csat_query['category__in'] = ['UNMAPPED']

            if 'survey_channel_phone' in selected_filters:
                csat_query['channel__in'] = ['PHONE']
            if 'survey_channel_email' in selected_filters:
                csat_query['channel__in'] = ['EMAIL']
            if 'survey_channel_combined' in selected_filters:
                csat_query['channel__in'] = ['EMAIL', 'PHONE']

            if 'process_tag' in selected_filters:
                csat_query['process__in'] = ['TAG']
            if 'process_shopping' in selected_filters:
                csat_query['process__in'] = ['SHOPPING']
            if 'process_combined' in selected_filters:
                csat_query['process__in'] = ['TAG', 'SHOPPING']

            # if 'language_english' in selected_filters:
            #     csat_query['langauge__in'] = ['ENGLISH']
            # if 'language_combined' in selected_filters:
            #     csat_query = csat_query

        csat_query['survey_date__gte'] = start_date
        csat_query['survey_date__lte'] = end_date

        if report_type == 'Region':
            region_query = dict()
            region_query['created_date__gte'] = start_date
            region_query['created_date__lte'] = end_date
            region_query['country__in'] = ReportService.get_all_locations()

            total_leads, implemented_leads = ReportService.get_region_report_counts(region_query, selected_filters)
            

            regions = Region.objects.all()


            for region in regions:
                query = dict()
                region_data = dict()
                region_data['Region'] = region.name
                region_locations = Location.objects.filter(region=region).values_list('location_name', flat=True)
                query['country__in'] = region_locations
                query['created_date__gte'] = start_date
                query['created_date__lte'] = end_date
                region_data['Leads'] , region_data['Wins'] = ReportService.get_region_report_counts(query, selected_filters)
                
                region_data['Leads in pcg'] = ReportService.get_percentage_value(region_data['Leads'], total_leads)

                region_data['Wins in pcg'] = ReportService.get_percentage_value(region_data['Wins'], region_data['Leads'])


                csat_query_tagteam_location, lead_owner_name = ReportService.get_csat_query_for_tagteam_location(selected_filters)
                if 'tag_location_palo_alto' in selected_filters:
                    csat_query['lead_owner_name__in'] = csat_query_tagteam_location

                csat_query['region__in'] = region_locations
                if 'language_english' in selected_filters:
                    csat_query['language'] = 'ENGLISH'
                    region_csat = CSATReport.objects.exclude(lead_owner_name__in=lead_owner_name)
                    region_csat = region_csat.filter(**csat_query).values('q1').annotate(dcount=Count('q1'))
                elif 'language_non_english' in selected_filters:
                    region_csat = CSATReport.objects.exclude(lead_owner_name__in=lead_owner_name)
                    region_csat = region_csat.exclude(language='ENGLISH').filter(**csat_query).values('q1').annotate(dcount=Count('q1'))
                else:
                    region_csat = CSATReport.objects.exclude(lead_owner_name__in=lead_owner_name)
                    region_csat = region_csat.filter(**csat_query).values('q1').annotate(dcount=Count('q1'))

                region_data = ReportService.get_response_dict(region_csat, region_data, key_response)

                report_data.append(region_data)
        elif report_type == 'Program':
            query = dict()
            programs = list(Leads.objects.filter(**query).values_list('team', flat=True).distinct().order_by('team'))
            query['created_date__gte'] = start_date
            query['created_date__lte'] = end_date
            query['team__in'] = programs
            report_type = 'team'


            total_leads_dict, total_leads_count, implemented_leads_dict, implemented_leads_count = ReportService.get_leads_details_based_on_selected_filters(query, csat_query, selected_filters, report_type) 

            csat_query_tagteam_location, lead_owner_name = ReportService.get_csat_query_for_tagteam_location(selected_filters)
            if 'tag_location_palo_alto' in selected_filters:
                csat_query['lead_owner_name__in'] = csat_query_tagteam_location

            csat_query['program__in'] = programs
            region_csat_type = 'program'
            region_csat = ReportService.get_region_csat_for_language(selected_filters, region_csat_type, lead_owner_name, csat_query)
           
            details = {'report_type': 'Program', 'total_leads_count': total_leads_count, 'implemented_leads_count': implemented_leads_count, 'lead_attribute': 'team', 'csat_attribute': 'program'}
            report_data = ReportService.get_report_record_from_values_dict(total_leads_dict, implemented_leads_dict, region_csat, programs, details)

        elif report_type == 'Location':
            query = dict()
            locations = list(Leads.objects.filter(**query).values_list('country', flat=True).distinct().order_by('country'))
            query['created_date__gte'] = start_date
            query['created_date__lte'] = end_date
            locations.append('')
            query['country__in'] = locations
            report_type = 'country'
            total_leads_dict, total_leads_count, implemented_leads_dict, implemented_leads_count = ReportService.get_leads_details_based_on_selected_filters(query, csat_query, selected_filters, report_type) 

            csat_query_tagteam_location, lead_owner_name = ReportService.get_csat_query_for_tagteam_location(selected_filters)
            if 'tag_location_palo_alto' in selected_filters:
                csat_query['lead_owner_name__in'] = csat_query_tagteam_location

            csat_query['region__in'] = locations
            region_csat_type = 'region'
            region_csat = ReportService.get_region_csat_for_language(selected_filters, region_csat_type, lead_owner_name, csat_query)

            details = {'report_type': 'Location', 'total_leads_count': total_leads_count, 'implemented_leads_count': implemented_leads_count, 'lead_attribute': 'country', 'csat_attribute': 'region'}
            report_data = ReportService.get_report_record_from_values_dict(total_leads_dict, implemented_leads_dict, region_csat, locations, details)

        elif report_type == 'Task Type':
            query = dict()
            code_types = list(Leads.objects.filter(**query).values_list('type_1', flat=True).distinct().order_by('type_1'))
            query['created_date__gte'] = start_date
            query['created_date__lte'] = end_date
            code_types.append('')
            query['type_1__in'] = code_types
            report_type = 'type_1'
            total_leads_dict, total_leads_count, implemented_leads_dict, implemented_leads_count = ReportService.get_leads_details_based_on_selected_filters(query, csat_query, selected_filters, report_type)
            
            csat_query_tagteam_location, lead_owner_name = ReportService.get_csat_query_for_tagteam_location(selected_filters)
            if 'tag_location_palo_alto' in selected_filters:
                csat_query['lead_owner_name__in'] = csat_query_tagteam_location

            csat_query['code_type__in'] = code_types

            region_csat_type = 'code_type'
            region_csat = ReportService.get_region_csat_for_language(selected_filters, region_csat_type, lead_owner_name, csat_query)
            details = {'report_type': 'Task Type', 'total_leads_count': total_leads_count, 'implemented_leads_count': implemented_leads_count, 'lead_attribute': 'type_1', 'csat_attribute': 'code_type'}
            report_data = ReportService.get_report_record_from_values_dict(total_leads_dict, implemented_leads_dict, region_csat, code_types, details)

        elif report_type == 'Lead Owner':
            query = dict()
            query['created_date__gte'] = start_date
            query['created_date__lte'] = end_date
            lead_owners = Leads.objects.filter(**query).values_list('lead_owner_name', 'lead_owner_email').distinct().order_by('lead_owner_name')
            lead_onwer_dict = {lead_owner[1]: lead_owner[0] for lead_owner in lead_owners}
            lead_owner_emails = [key for key, value in lead_onwer_dict.iteritems()]
            lead_owner_emails.append('')
            query['lead_owner_email__in'] = lead_owner_emails
            report_type = 'lead_owner_email'
            total_leads_dict, total_leads_count, implemented_leads_dict, implemented_leads_count = ReportService.get_leads_details_based_on_selected_filters(query, csat_query, selected_filters, report_type)
            
            csat_query_tagteam_location, lead_owner_name = ReportService.get_csat_query_for_tagteam_location(selected_filters)
            if 'tag_location_palo_alto' in selected_filters:
                csat_query['lead_owner_name__in'] = csat_query_tagteam_location

            csat_query['lead_owner__in'] = lead_owner_emails

            region_csat_type = 'lead_owner'
            region_csat = ReportService.get_region_csat_for_language(selected_filters, region_csat_type, lead_owner_name, csat_query)

            details = {'report_type': 'Lead Owner', 'total_leads_count': total_leads_count, 'implemented_leads_count': implemented_leads_count, 'lead_attribute': 'lead_owner_email', 'csat_attribute': 'lead_owner'}
            report_data = ReportService.get_report_record_from_values_dict(total_leads_dict, implemented_leads_dict, region_csat, lead_owner_emails, details)
            for report in report_data:
                for key, value in lead_onwer_dict.iteritems():
                    if report['Lead Owner'] == key:
                        report['Lead Owner'] = value
                    elif report['Lead Owner'] == '':
                        report['Lead Owner'] = 'Others'
        return report_data

    @staticmethod
    def get_leads_details_based_on_selected_filters(query, csat_query, selected_filters, report_type):
        if 'process_tag' in selected_filters:
            shopping_code_types = ['Google Shopping Setup', 'Google Shopping Migration']
        elif 'process_shopping' in selected_filters:
            shopping_code_types = []
            query['type_1__in'] = ['Google Shopping Setup', 'Google Shopping Migration']
        else:
            shopping_code_types = []

        query_tagteam_location, lead_owner_name = ReportService.get_csat_query_for_tagteam_location(selected_filters)
        if 'tag_location_palo_alto' in selected_filters:
            query['lead_owner_name__in'] = query_tagteam_location

        lead_owner_list = ['tom@regalix-inc.com', 'tadashis@google.com', 'yukieh@google.com', 'abaldessin@regalix-inc.com', 'jmartens@regalix-inc.com', 'cburak@google.com', 'arnulfom@google.com']    
        if report_type == 'lead_owner_email':
            if 'tag_location_palo_alto' in selected_filters:
                query['lead_owner_email__in'] = ['tom@regalix-inc.com', 'tadashis@google.com', 'yukieh@google.com', 'abaldessin@regalix-inc.com', 'jmartens@regalix-inc.com', 'cburak@google.com', 'arnulfom@google.com']
            elif 'tag_location_bangalore' in selected_filters:
                query['lead_owner_email__in'] = [lead for lead in query['lead_owner_email__in'] if lead not in lead_owner_list]

        if 'language_english' in selected_filters:
            query['language'] = 'ENGLISH'
            total_leads_dict = Leads.objects.exclude(type_1__in=shopping_code_types).filter(**query).values(report_type).annotate(cnt=Count(report_type))
            total_leads_dict = total_leads_dict.exclude(lead_owner_name__in=lead_owner_name)
            total_leads_count = Leads.objects.exclude(lead_owner_name__in=lead_owner_name)
            total_leads_count = total_leads_count.exclude(type_1__in=shopping_code_types).filter(**query).values(report_type).count()
            query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
            implemented_leads_dict = Leads.objects.filter(**query).exclude(type_1__in=shopping_code_types).values(report_type).annotate(cnt=Count(report_type))
            implemented_leads_dict = implemented_leads_dict.exclude(lead_sub_status='RR - Inactive')
            implemented_leads_dict = implemented_leads_dict.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads_count = Leads.objects.filter(**query).exclude(type_1__in=shopping_code_types)
            implemented_leads_count = implemented_leads_count.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads_count = implemented_leads_count.exclude(lead_sub_status='RR - Inactive').values(report_type).count()
        elif 'language_non_english' in selected_filters:
            total_leads_dict = Leads.objects.filter(**query).exclude(language='ENGLISH').values(report_type).annotate(cnt=Count(report_type))
            total_leads_dict = total_leads_dict.exclude(lead_owner_name__in=lead_owner_name)
            total_leads_dict = total_leads_dict.exclude(type_1__in=shopping_code_types)
            total_leads_count = Leads.objects.filter(**query).exclude(language='ENGLISH')
            total_leads_count = total_leads_count.exclude(lead_owner_name__in=lead_owner_name)
            total_leads_count = total_leads_count.exclude(type_1__in=shopping_code_types).values(report_type).count()
            query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
            implemented_leads_dict = Leads.objects.filter(**query).exclude(type_1__in=shopping_code_types).values(report_type).annotate(cnt=Count(report_type))
            implemented_leads_dict = implemented_leads_dict.exclude(language='ENGLISH')
            implemented_leads_dict = implemented_leads_dict.exclude(lead_sub_status='RR - Inactive')
            implemented_leads_dict = implemented_leads_dict.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads_count = Leads.objects.filter(**query).exclude(type_1__in=shopping_code_types)
            implemented_leads_count = implemented_leads_count.exclude(language='ENGLISH')
            implemented_leads_count = implemented_leads_count.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads_count = implemented_leads_count.exclude(lead_sub_status='RR - Inactive').values(report_type).count()
        else:
            total_leads_dict = Leads.objects.exclude(type_1__in=shopping_code_types).filter(**query).values(report_type).annotate(cnt=Count(report_type))
            total_leads_dict = total_leads_dict.exclude(lead_owner_name__in=lead_owner_name)
            total_leads_count = Leads.objects.filter(**query).exclude(lead_owner_name__in=lead_owner_name)
            total_leads_count = Leads.objects.exclude(type_1__in=shopping_code_types).values(report_type).count()
            query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
            implemented_leads_dict = Leads.objects.filter(**query).exclude(type_1__in=shopping_code_types).values(report_type).annotate(cnt=Count(report_type))
            implemented_leads_dict = implemented_leads_dict.exclude(lead_sub_status='RR - Inactive')
            implemented_leads_dict = implemented_leads_dict.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads_count = Leads.objects.filter(**query).exclude(type_1__in=shopping_code_types)
            implemented_leads_count = implemented_leads_count.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads_count = implemented_leads_count.exclude(lead_sub_status='RR - Inactive').values(report_type).count()
        return total_leads_dict, total_leads_count, implemented_leads_dict, implemented_leads_count


    @staticmethod
    def get_region_report_counts(region_query, selected_filters):
        if 'tag_location_palo_alto' in selected_filters:
            region_query['lead_owner_name__in'] = ['Tom Du', 'Tadashi Soga', 'Yukie Hirano', 'Aurora Baldessin', 'Janno Martens', 'Carolina Burak', 'Arnulfo Maldonado']
            lead_owner_name = []
        elif 'tag_location_bangalore' in selected_filters:
            lead_owner_name = ['Tom Du', 'Tadashi Soga', 'Yukie Hirano', 'Aurora Baldessin', 'Janno Martens', 'Carolina Burak', 'Arnulfo Maldonado']
        else:
            lead_owner_name = []


        if 'process_tag' in selected_filters:
            shopping_code_types = ['Google Shopping Setup', 'Google Shopping Migration']

            total_leads = Leads.objects.exclude(lead_owner_name__in=lead_owner_name)
            total_leads = total_leads.exclude(type_1__in=shopping_code_types).filter(**region_query).count()
            region_query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
            implemented_leads = Leads.objects.exclude(type_1__in=shopping_code_types).filter(**region_query)
            implemented_leads = implemented_leads.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads = implemented_leads.exclude(lead_sub_status='RR - Inactive').count()

        elif 'process_shopping' in selected_filters:
            region_query['type_1__in'] = ['Google Shopping Setup', 'Google Shopping Migration']
            total_leads = Leads.objects.exclude(lead_owner_name__in=lead_owner_name).filter(**region_query).count()
            region_query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
            implemented_leads = Leads.objects.filter(**region_query)
            implemented_leads = implemented_leads.exclude(lead_owner_name__in=lead_owner_name)
            implemented_leads = implemented_leads.exclude(lead_sub_status='RR - Inactive').count()
        else:
            shopping_code_types = []
            total_leads = Leads.objects.filter(**region_query).count()
            region_query['lead_status__in'] = ['Implemented', 'Pending QC - WIN', 'Rework Required']
            implemented_leads = Leads.objects.exclude(lead_sub_status='RR - Inactive').filter(**region_query).count()

        return total_leads, implemented_leads

    @staticmethod
    def get_response_dict(response_dict, region_data, key_response):
        total_response = 0
        total_transferred = 0
        for value in key_response.values():
            region_data[value] = 0

        for resp in response_dict:
            if resp['q1'] in key_response:
                if resp['q1'] != 0:
                    total_response += resp['dcount']
                total_transferred += resp['dcount']
                region_data[key_response[resp['q1']]] = resp['dcount']

        for response in key_response.values():
            if response in region_data:
                region_data['%s in pcg' % (response)] = ReportService.get_percentage_value(region_data[response], total_response)
        region_data['Grand Total'] = total_response
        region_data['Transfer Rate'] = total_transferred
        region_data['Response Rate in pcg'] = ReportService.get_percentage_value(total_transferred, region_data.get('Wins'))
        region_data['Transfer Rate in pcg'] = ReportService.get_percentage_value(total_response, region_data.get('Wins'))
        return region_data

    @staticmethod
    def get_percentage_value(numerator, denaminator):
        try:
            result = round((float(numerator) / denaminator) * 100, 2)
        except Exception as e:
            result = 0.0
        return result

    @staticmethod
    def get_report_record_from_values_dict(total_leads_dict, implemented_leads_dict, csat_report_dict_lists, keys, details):
        key_response = {0: '', 1: 'Extremely satisfied', 2: 'Moderately satisfied', 3: 'Slightly satisfied', 4: 'Neither satisfied nor dissatisfied', 5: 'Slightly dissatisfied', 6: 'Moderately dissatisfied', 7: 'Extremely dissatisfied'}
        global report_type
        report_type = details['report_type']
        report_records = {key: {report_type: key, 'Leads': 0, 'Wins': 0, 'Leads in pcg': 0, '': 0, 'Extremely satisfied in pcg': 0, 'Extremely satisfied': 0, 'Moderately satisfied in pcg': 0, 'Moderately satisfied': 0, 'Slightly satisfied in pcg': 0, 'Slightly satisfied': 0, 'Neither satisfied nor dissatisfied in pcg': 0, 'Neither satisfied nor dissatisfied': 0, 'Slightly dissatisfied in pcg': 0, 'Slightly dissatisfied': 0, 'Wins in pcg': 0, 'Moderately dissatisfied in pcg': 0, 'Moderately dissatisfied': 0, 'Extremely dissatisfied in pcg': 0, 'Extremely dissatisfied': 0, 'Grand Total': 0, 'Transfer Rate': 0, 'Transfer Rate in pcg': 0, 'Response Rate in pcg': 0} for key in keys}
        for key, value in report_records.iteritems():
            for total_dict in total_leads_dict:
                if key == total_dict[details['lead_attribute']]:
                    value['Leads'] = total_dict.get('cnt', 0)
                    value['Leads in pcg'] = ReportService.get_percentage_value(total_dict['cnt'], details['total_leads_count'])
            for implemented_dict in implemented_leads_dict:
                if key == implemented_dict[details['lead_attribute']]:
                    value['Wins'] = implemented_dict.get('cnt', 0)
                    for total_dict in total_leads_dict:
                        if total_dict[details['lead_attribute']] == implemented_dict[details['lead_attribute']]:
                            value['Wins in pcg'] = ReportService.get_percentage_value(implemented_dict['cnt'], total_dict['cnt'])
            for csat_dict in csat_report_dict_lists:
                if key == csat_dict[details['csat_attribute']]:
                    value[key_response[csat_dict['q1']]] = csat_dict.get('dcount')
                    if csat_dict['q1'] != 0:
                        value['Grand Total'] += csat_dict.get('dcount')
                    value['Transfer Rate'] += csat_dict.get('dcount')
                    value['Response Rate in pcg'] = ReportService.get_percentage_value(value['Transfer Rate'], value['Wins'])
                    value['Transfer Rate in pcg'] = ReportService.get_percentage_value(value['Grand Total'], value['Wins'])
            for csat_dict in csat_report_dict_lists:
                if key == csat_dict[details['csat_attribute']]:
                    value['%s in pcg' % (key_response[csat_dict['q1']])] = ReportService.get_percentage_value(csat_dict['dcount'], value['Grand Total'])
            if details['csat_attribute'] == 'program':
                if value['Program'] == '':
                    value['Program'] = 'Others'
            if details['csat_attribute'] == 'code_type':
                if value['Task Type'] == '':
                    value['Task Type'] = 'Others'
        report_records = collections.OrderedDict(sorted(report_records.items()))
        return report_records.values()

    @staticmethod
    def get_csat_query_for_tagteam_location(selected_filters):
        if 'tag_location_palo_alto' in selected_filters:
            csat_query = ['Tom Du', 'Tadashi Soga', 'Yukie Hirano', 'Aurora Baldessin', 'Janno Martens', 'Carolina Burak', 'Arnulfo Maldonado']
            lead_owner_name = []
        elif 'tag_location_bangalore' in selected_filters:
            lead_owner_name = ['Tom Du', 'Tadashi Soga', 'Yukie Hirano', 'Aurora Baldessin', 'Janno Martens', 'Carolina Burak', 'Arnulfo Maldonado']
            csat_query = []
        else:
            lead_owner_name = []
            csat_query = []
        return csat_query, lead_owner_name

    @staticmethod
    def get_region_csat_for_language(selected_filters, region_csat_type, lead_owner_name, csat_query):
        if 'language_english' in selected_filters:
            csat_query['language'] = 'ENGLISH'
            region_csat = CSATReport.objects.exclude(lead_owner_name__in=lead_owner_name)
            region_csat = region_csat.filter(**csat_query).values('q1', region_csat_type).annotate(dcount=Count(region_csat_type))
        elif 'language_non_english' in selected_filters:
            region_csat = CSATReport.objects.exclude(lead_owner_name__in=lead_owner_name)
            region_csat = region_csat.exclude(language='ENGLISH').filter(**csat_query).values('q1', region_csat_type).annotate(dcount=Count(region_csat_type))
        else:
            region_csat = CSATReport.objects.exclude(lead_owner_name__in=lead_owner_name)
            region_csat = region_csat.filter(**csat_query).values('q1', region_csat_type).annotate(dcount=Count(region_csat_type))
        return region_csat

    @staticmethod
    def get_csat_compare_result(current_report_data, previous_report_data, report_type, comparison):
        key_response = {'Grand Total': 0, 'Leads':0, 'Wins': 0, 'Extremely satisfied': 0, 'Moderately satisfied': 0, 'Slightly satisfied': 0, 'Neither satisfied nor dissatisfied': 0, 'Slightly dissatisfied': 0, 'Moderately dissatisfied': 0, 'Extremely dissatisfied': 0}
        total_response_count = {'TotalGrand Total': 0, 'report_type': 'Total', 'TotalLeads': 0, 'TotalWins': 0, 'Total': 0, 'TotalExtremely satisfied': 0, 'TotalModerately satisfied': 0, 'TotalSlightly satisfied': 0, 'TotalNeither satisfied nor dissatisfied': 0, 'TotalSlightly dissatisfied': 0, 'TotalModerately dissatisfied': 0, 'TotalExtremely dissatisfied': 0}
        current_list = []
        previous_list = []
        
        if comparison == 'yes':
            for current_report in current_report_data:
                for previous_report in previous_report_data:
                    if current_report[report_type] == previous_report[report_type]:
                        if current_report['Leads'] != 0 and previous_report['Leads'] != 0:
                            current_list.append(current_report)
                            previous_list.append(previous_report)
            return current_list, previous_list
        else:
            for current_report in current_report_data:
                if current_report['Leads'] != 0:
                    for key, value in current_report.iteritems():
                        for key1, value1 in key_response.iteritems():
                            if key == key1:
                                total_response_count['Total'+key1] += value
                    current_list.append(current_report)
            current_list.append(total_response_count)
            return current_list, previous_list

    @staticmethod
    def get_average_tat_for_leads(leads):
        implemented_leads = list()
        first_contacted_leads = list()
        for lead in leads:
            if lead.lead_status == 'Implemented':
                implemented_leads.append(lead)
            if lead.first_contacted_on:
                first_contacted_leads.append(lead)

        implemented_leads_tat = ReportService.get_average_of_implemented(implemented_leads)
        return implemented_leads_tat

    @staticmethod
    def get_lead_code_type_analysis(leads, code_types):
        ''' Code type analysis for Leads'''
        code_type_analysis = {c_type: 0 for c_type in code_types}
        for lead in leads:
            if lead.type_1 in code_types:
                code_type_analysis[lead.type_1] += 1
        return code_type_analysis

    @staticmethod
    def get_implemented_leads_and_leads_count(query):
        ''' Returns Implemented Leads and implemented leads count '''
        query['lead_status__in'] == ['Implemented', 'Pending QC - WIN', 'Rework Required']
        implemented_leads = Leads.exclude(lead_sub_status='RR - Inactive').filter(**query)
        implemented_leads_count = Leads.exclude(lead_sub_status='RR - Inactive').filter(**query).count()
        return implemented_leads, implemented_leads_count

    @staticmethod
    def get_lead_status_analysis(leads):
        lead_dict = settings.LEAD_STATUS_DICT
        status_dict = {'In Queue': 0, 'In Progress': 0, 'Attempting Contact': 0, 'In Active': 0, 'Implemented': 0, 'Total': 0}
        for lead in leads:
            for key, value in lead.iteritems():
                for status, status_list in lead_dict.iteritems():
                    if lead[key] in  status_list:
                        status_dict[status] = lead['dcount'] 
        for key, value in status_dict.iteritems():
            if key != 'Total':
                status_dict['Total'] += value                

        keyorder = {k: v for v, k in enumerate(['In Queue', 'In Progress', 'Attempting Contact', 'In Active', 'Implemented', 'Total'])}
        lead_status_analysis = OrderedDict(sorted(status_dict.items(), key=lambda i: keyorder.get(i[0])))
        return lead_status_analysis

    @staticmethod
    def get_leads_reports(leads, lead_status, code_types):
        ''' Get LEADS report '''
        l_status, tat_report = ReportService.get_lead_status_by_code_type(leads, lead_status, code_types)
        reports, total = ReportService.get_total_by_code_types(l_status, code_types)
        reports.extend(tat_report)
        return reports, total

    @staticmethod
    def get_lead_status_by_code_type(leads, lead_status, code_types):
        code_details = {c_type: 0 for c_type in code_types}
        status_details = {str(l_status): code_details for l_status in lead_status}
        implemented_leads = list()
        first_contacted_leads = list()
        tat_implemented_rec = dict()
        tat_fco_rec = dict()
        lead_rec = dict()
        advertiser_leads = list()
        regalix_leads = list()
        advertiser_missed_appointment = dict()
        regalix_missed_appointment = dict()
        dial_leads = list()
        dials_rec = dict()
        missed_advertiser_appnt = 0
        missed_regalix_appnt = 0
        number_of_dials = 0
        for lead in leads:
            # LEAD REPORTS
            if lead.lead_status not in lead_rec:
                lead_rec[lead.lead_status] = {c_type: 0 for c_type in code_types}
                lead_rec[lead.lead_status][lead.type_1] = 1
            else:
                cnt = lead_rec.get(lead.lead_status).get(lead.type_1)
                lead_rec[lead.lead_status][lead.type_1] = cnt + 1

            # TAT Reports
            if lead.lead_status == 'Implemented':
                implemented_leads.append(lead)
            if lead.first_contacted_on:
                first_contacted_leads.append(lead)

            # Missed appointments
            if lead.lead_sub_status in ['RX- Met Appointment', 'AD - Missed Appointment']:
                missed_advertiser_appnt += 1
                advertiser_leads.append(lead)

            if lead.lead_sub_status == 'RX - Missed Appointment':
                missed_regalix_appnt += 1
                regalix_leads.append(lead)

            # Number of calls or Dials reports
            if lead.dials:
                number_of_dials += lead.dials
                dial_leads.append(lead)
        l_status = list()
        for s in ['Pending QC - DEAD LEAD', 'Pending QC - WIN', 'Rework Required', 'Appointment Set (GS)']:
            if s in lead_status:
                lead_status.remove(s)

        for status in lead_status:
            temp = {'lead_status_name': status}
            if str(status) in lead_rec.keys():
                # Consider Appointment Set (GS) lead status as In Queue
                if str(status) == 'In Queue':
                    if 'Appointment Set (GS)' in lead_rec.keys():
                        in_queue = dsum(lead_rec[str(status)], lead_rec['Appointment Set (GS)'])
                    else:
                        in_queue = lead_rec[str(status)]
                    temp.update(in_queue)
                # Consider Pending QC - DEAD LEAD, WIN and Rework Required lead status as In Progress
                elif str(status) == 'In Progress':
                    in_progress = lead_rec[str(status)]
                    if 'Pending QC - DEAD LEAD' in lead_rec.keys():
                        in_progress = dsum(in_progress, lead_rec['Pending QC - DEAD LEAD'])
                    if 'Pending QC - WIN' in lead_rec.keys():
                        in_progress = dsum(in_progress, lead_rec['Pending QC - WIN'])
                    if 'Rework Required' in lead_rec.keys():
                        in_progress = dsum(in_progress, lead_rec['Rework Required'])
                    temp.update(in_progress)
                else:
                    temp.update(lead_rec[str(status)])
            else:
                temp.update(status_details[str(status)])
            l_status.append(temp)

        # Turn Around Time reports
        avg_implemented = ReportService.get_average_of_implemented(implemented_leads)
        avg_contacted = ReportService.get_average_of_first_contacted(first_contacted_leads)

        tat_implemented_rec.update(ReportService.get_tat_implemented_report_by_code_type(implemented_leads, code_types))
        tat_fco_rec.update(ReportService.get_tat_fco_report_by_code_type(first_contacted_leads, code_types))
        tat_implemented_rec.update({'total': avg_implemented, 'lead_status_name': 'TAT (First Contact Made)'})
        tat_fco_rec.update({'total': avg_contacted, 'lead_status_name': 'TAT (Implemented)'})

        # Missed Appointments Reports
        advertiser_missed_appointment.update(ReportService.get_advertiser_missed_appointment_by_code_type(advertiser_leads, code_types))
        regalix_missed_appointment.update(ReportService.get_regalix_missed_appointment_by_code_type(regalix_leads, code_types))
        advertiser_missed_appointment.update(({'total': missed_advertiser_appnt, 'lead_status_name': 'Advertiser Missed appointments'}))
        regalix_missed_appointment.update(({'total': missed_regalix_appnt, 'lead_status_name': 'Regalix Missed appointments'}))

        # Number of Calls/Dials Report
        dials_rec.update(ReportService.get_dial_by_code_type(dial_leads, code_types))
        dials_rec.update({'total': number_of_dials, 'lead_status_name': 'Number of Calls'})

        return l_status, [tat_implemented_rec, tat_fco_rec, advertiser_missed_appointment, regalix_missed_appointment, dials_rec]

    @staticmethod
    def get_total_by_code_types(reports, code_types):
        ''' Get total count by code types '''
        code_details = {c_type: 0 for c_type in code_types}
        total = dict()
        implemented = dict()
        for row in reports:
            row_total = 0
            for key, value in row.iteritems():
                if key in code_details:
                    code_details[key] += value
                    row_total += value
            row.update({'total': row_total})
            if row['lead_status_name'] == 'Implemented':
                # Get implemented row for calculate Conversion Ratio
                implemented = row

        total.update(code_details)
        total.update({'lead_status_name': 'Total', 'total': sum(code_details.values())})
        if implemented:
            cr_row = ReportService.get_cr_row(implemented, code_details)
            reports.append(cr_row)
        reports.append(total)
        return reports, total

    # ######################################### TAT Reports Starts Here ####################################

    @staticmethod
    def get_tat_implemented_report_by_code_type(implemented_leads, code_types):
        ''' Split TAT leads by code types '''

        c_types = dict()
        for lead in implemented_leads:
            if lead.type_1 not in c_types:
                c_types[lead.type_1] = {'count': 1, 'days': 0}
                c_types[lead.type_1]['days'] += ReportService.get_tat_by_implemented(
                    lead.date_of_installation, lead.appointment_date, lead.created_date)
            else:
                cnt = c_types[lead.type_1]['count']
                c_types[lead.type_1]['count'] = cnt + 1
                c_types[lead.type_1]['days'] += ReportService.get_tat_by_implemented(
                    lead.date_of_installation, lead.appointment_date, lead.created_date)

        tat_rec = dict()
        for code in code_types:
            if code in c_types:
                tat_rec[code] = c_types[code]['days'] / c_types[code]['count']
            else:
                tat_rec[code] = 'No Leads'

        return tat_rec

    @staticmethod
    def get_tat_fco_report_by_code_type(first_contacted_leads, code_types):
        ''' Split TAT leads by code types '''

        c_types = dict()
        for lead in first_contacted_leads:
            if lead.type_1 not in c_types:
                c_types[lead.type_1] = {'count': 1, 'days': 0}
                c_types[lead.type_1]['days'] += ReportService.get_tat_by_first_contacted_on(
                    lead.first_contacted_on, lead.appointment_date, lead.created_date)
            else:
                cnt = c_types[lead.type_1]['count']
                c_types[lead.type_1]['count'] = cnt + 1
                c_types[lead.type_1]['days'] += ReportService.get_tat_by_first_contacted_on(
                    lead.first_contacted_on, lead.appointment_date, lead.created_date)

        tat_rec = dict()
        for code in code_types:
            if code in c_types:
                tat_rec[code] = c_types[code]['days'] / c_types[code]['count']
            else:
                tat_rec[code] = 'No Leads'

        return tat_rec

    @staticmethod
    def get_average_of_implemented(leads):
        days = 0
        for lead in leads:
            if lead.team in settings.SERVICES:
                days += ReportService.get_tat_by_implemented_for_service(lead.date_of_installation, lead.created_date) if lead.date_of_installation else 0
            else:
                days += ReportService.get_tat_by_implemented(lead.date_of_installation, lead.appointment_date, lead.created_date) if lead.date_of_installation else 0

        if days:
            return round(float(days) / len(leads), 2)
        return days

    @staticmethod
    def get_average_of_first_contacted(leads):
        days = 0
        for lead in leads:
            days += ReportService.get_tat_by_first_contacted_on(lead.first_contacted_on, lead.appointment_date, lead.created_date)

        if days:
            return round(float(days) / len(leads), 2)
        return days

    @staticmethod
    def get_tat_by_implemented(implemented_date, appointment_date, created_date):
        ''' Get Turn Around Time by two dates
            1. TAT is difference between Appointment date and Implemented date.
            2. In case Appointment date is blank, use Created date instead.
        '''
        if implemented_date:
            if appointment_date:
                diff = max([implemented_date, appointment_date]) - min([implemented_date, appointment_date])
            else:
                diff = max([implemented_date, created_date]) - min([implemented_date, created_date])
            days = diff.days
        else:
            days = 0
        return days

    @staticmethod
    def get_tat_by_first_contacted_on(fco, appointment_date, created_date):
        ''' Get Turn Around Time by two dates
            TAT is difference between Appointment date and First Contact date.
            In case Appointment date is blank, use Created date instead.
        '''
        days = 0
        if fco:
            if appointment_date:
                diff = max([fco, appointment_date]) - min([fco, appointment_date])
            else:
                diff = max([fco, created_date]) - min([fco, created_date])
            days = diff.days
        return days

    @staticmethod
    def get_tat_by_implemented_for_service(implemented_date, created_date):
        ''' Get Turn Around Time by two dates
            1. TAT is difference between Appointment date and Implemented date.
            2. In case Appointment date is blank, use Created date instead.
            Only For Team Belongs to SERVICES and ...
        '''
        if implemented_date:
            diff = max([implemented_date, created_date]) - min([implemented_date, created_date])
            days = diff.days
        else:
            days = 0
        return days

    @staticmethod
    def get_implemented_tat_by_code(code_type, start_date, end_date, teams=None, locations=None):
        if teams and locations:
            implemented_leads = Leads.objects.filter(type_1=code_type, lead_status='Implemented',
                                                     team__in=teams, country__in=locations,
                                                     created_date__gte=start_date, created_date__lte=end_date)
        elif teams and not locations:
            implemented_leads = Leads.objects.filter(type_1=code_type, lead_status='Implemented',
                                                     team__in=teams,
                                                     created_date__gte=start_date, created_date__lte=end_date)
        elif locations and not teams:
            implemented_leads = Leads.objects.filter(type_1=code_type, lead_status='Implemented',
                                                     country__in=locations,
                                                     created_date__gte=start_date, created_date__lte=end_date)
        else:
            implemented_leads = Leads.objects.filter(
                type_1=code_type, lead_status='Implemented', created_date__gte=start_date, created_date__lte=end_date)
        return ReportService.get_average_of_implemented(implemented_leads)

    @staticmethod
    def get_first_contacted_tat_by_code(code_type, start_date, end_date, teams=None, locations=None):
        if teams and locations:
            first_contacted_leads = Leads.objects.exclude(
                first_contacted_on__isnull=True).filter(type_1=code_type,
                                                        team__in=teams,
                                                        country__in=locations,
                                                        created_date__gte=start_date,
                                                        created_date__lte=end_date)
        elif teams and not locations:
            first_contacted_leads = Leads.objects.exclude(
                first_contacted_on__isnull=True).filter(type_1=code_type,
                                                        team__in=teams,
                                                        created_date__gte=start_date,
                                                        created_date__lte=end_date)
        elif locations and not teams:
            first_contacted_leads = Leads.objects.exclude(
                first_contacted_on__isnull=True).filter(type_1=code_type,
                                                        country__in=locations,
                                                        created_date__gte=start_date,
                                                        created_date__lte=end_date)
        else:
            first_contacted_leads = Leads.objects.exclude(first_contacted_on__isnull=True).filter(
                type_1=code_type, created_date__gte=start_date, created_date__lte=end_date)

        return ReportService.get_average_of_first_contacted(first_contacted_leads)

    # ######################################### TAT Reports Ends Here ####################################

    @staticmethod
    def get_summary_by_code_types_and_status(summary_type, code_types, lead_status, start_date, end_date, teams, locations):
        # get summary
        report_detail = dict()
        total_summary = {'Implemented': 0, 'In Queue': 0, 'wins': 0, 'total_leads': 0}
        total_tag_summary = {'Implemented': 0, 'In Queue': 0, 'wins': 0, 'total_leads': 0}
        if summary_type == 'tag':
            all_code_types = ['Google Shopping Migration', 'Google Shopping Setup']
        else:
            all_code_types = code_types

        for c_type in all_code_types:
            report_detail[c_type] = dict()
            for status in lead_status:
                if teams and locations:
                    report_detail[c_type][status] = len(Leads.objects.filter(
                        type_1=c_type, lead_status=status, team__in=teams, country__in=locations,
                        created_date__gte=start_date, created_date__lte=end_date))
                elif teams:
                    report_detail[c_type][status] = len(Leads.objects.filter(
                        type_1=c_type, lead_status=status, team__in=teams,
                        created_date__gte=start_date, created_date__lte=end_date))
                elif locations:
                    report_detail[c_type][status] = len(Leads.objects.filter(
                        type_1=c_type, lead_status=status, country__in=locations,
                        created_date__gte=start_date, created_date__lte=end_date))
                else:
                    report_detail[c_type][status] = len(Leads.objects.filter(
                        type_1=c_type, lead_status=status, created_date__gte=start_date, created_date__lte=end_date))
            if teams and locations:
                report_detail[c_type]['total_leads'] = len(Leads.objects.filter(
                    type_1=c_type, lead_status__in=lead_status, team__in=teams, country__in=locations,
                    created_date__gte=start_date, created_date__lte=end_date))

            elif teams:
                report_detail[c_type]['total_leads'] = len(Leads.objects.filter(
                    type_1=c_type, team__in=teams, lead_status__in=lead_status, created_date__gte=start_date, created_date__lte=end_date))

            elif locations:
                report_detail[c_type]['total_leads'] = len(Leads.objects.filter(
                    type_1=c_type, country__in=locations, lead_status__in=lead_status, created_date__gte=start_date, created_date__lte=end_date))

            else:
                report_detail[c_type]['total_leads'] = len(Leads.objects.filter(
                    type_1=c_type, lead_status__in=lead_status, created_date__gte=start_date, created_date__lte=end_date))

            # Get TAT for Implemented and First Contacted On
            report_detail[c_type]['tat_implemented'] = ReportService.get_implemented_tat_by_code(
                c_type, start_date, end_date, teams, locations)
            report_detail[c_type]['tat_first_contacted'] = ReportService.get_first_contacted_tat_by_code(
                c_type, start_date, end_date, teams, locations)
            # Calculate wins percentage of implemented leads
            wins = ReportService.get_conversion_ratio(report_detail[c_type]['Implemented'], report_detail[c_type]['total_leads'])
            report_detail[c_type]['wins'] = wins
        if teams and locations:
            # Get total summary report
            total_summary['total_leads'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=lead_status, team__in=teams, country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['Implemented'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented', team__in=teams, country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['In Queue'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=['In Queue', 'Appointment Set (GS)'], team__in=teams, country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['wins'] = ReportService.get_conversion_ratio(total_summary['Implemented'], total_summary['total_leads'])
            implemented_leads = Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented', team__in=teams, country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date)
            contacted_leads = Leads.objects.exclude(first_contacted_on__isnull=True).filter(
                type_1__in=code_types, lead_status__in=lead_status, team__in=teams, country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date)
            total_summary['tat_implemented'] = ReportService.get_average_of_implemented(implemented_leads)
            total_summary['tat_first_contacted'] = ReportService.get_average_of_first_contacted(contacted_leads)

        elif teams:
            # Get total summary report
            total_summary['total_leads'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=lead_status, team__in=teams,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['Implemented'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented', team__in=teams,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['In Queue'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=['In Queue', 'Appointment Set (GS)'], team__in=teams,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['wins'] = ReportService.get_conversion_ratio(total_summary['Implemented'], total_summary['total_leads'])
            implemented_leads = Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented', team__in=teams,
                created_date__gte=start_date, created_date__lte=end_date)
            contacted_leads = Leads.objects.exclude(first_contacted_on__isnull=True).filter(
                type_1__in=code_types, lead_status__in=lead_status, team__in=teams,
                created_date__gte=start_date, created_date__lte=end_date)
            total_summary['tat_implemented'] = ReportService.get_average_of_implemented(implemented_leads)
            total_summary['tat_first_contacted'] = ReportService.get_average_of_first_contacted(contacted_leads)
        elif locations:
            # Get total summary report
            total_summary['total_leads'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=lead_status, country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['Implemented'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented', country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['In Queue'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=['In Queue', 'Appointment Set (GS)'], country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['wins'] = ReportService.get_conversion_ratio(total_summary['Implemented'], total_summary['total_leads'])
            implemented_leads = Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented', country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date)
            contacted_leads = Leads.objects.exclude(first_contacted_on__isnull=True).filter(
                type_1__in=code_types, lead_status__in=lead_status, country__in=locations,
                created_date__gte=start_date, created_date__lte=end_date)
            total_summary['tat_implemented'] = ReportService.get_average_of_implemented(implemented_leads)
            total_summary['tat_first_contacted'] = ReportService.get_average_of_first_contacted(contacted_leads)
        else:
            # Get total summary report
            total_summary['total_leads'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=lead_status,
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['Implemented'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented',
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['In Queue'] = len(Leads.objects.filter(
                type_1__in=code_types, lead_status__in=['In Queue', 'Appointment Set (GS)'],
                created_date__gte=start_date, created_date__lte=end_date))
            total_summary['wins'] = ReportService.get_conversion_ratio(total_summary['Implemented'], total_summary['total_leads'])
            implemented_leads = Leads.objects.filter(
                type_1__in=code_types, lead_status='Implemented', created_date__gte=start_date, created_date__lte=end_date)
            contacted_leads = Leads.objects.exclude(first_contacted_on__isnull=True).filter(
                type_1__in=code_types, lead_status__in=lead_status, created_date__gte=start_date, created_date__lte=end_date)
            total_summary['tat_implemented'] = ReportService.get_average_of_implemented(implemented_leads)
            total_summary['tat_first_contacted'] = ReportService.get_average_of_first_contacted(contacted_leads)

        # Get Total Tag leads summary report
        # List all tag leads
        c_types = [code for code in code_types if code not in ['Google Shopping Migration', 'Google Shopping Setup']]
        if not teams:
            teams = ReportService.get_all_teams()
        if not locations:
            locations = ReportService.get_all_locations()

        total_tag_summary['total_leads'] = len(Leads.objects.filter(
            lead_status__in=lead_status, type_1__in=c_types, team__in=teams, country__in=locations,
            created_date__gte=start_date, created_date__lte=end_date))
        total_tag_summary['Implemented'] = len(Leads.objects.filter(
            lead_status='Implemented', type_1__in=c_types, team__in=teams, country__in=locations,
            created_date__gte=start_date, created_date__lte=end_date))
        total_tag_summary['In Queue'] = len(Leads.objects.filter(
            lead_status__in=['In Queue', 'Appointment Set (GS)'], type_1__in=c_types, team__in=teams, country__in=locations,
            created_date__gte=start_date, created_date__lte=end_date))
        total_tag_summary['wins'] = ReportService.get_conversion_ratio(total_tag_summary['Implemented'], total_tag_summary['total_leads'])
        tag_implemented_leads = Leads.objects.filter(
            lead_status='Implemented', type_1__in=c_types, team__in=teams, country__in=locations,
            created_date__gte=start_date, created_date__lte=end_date)
        tag_contacted_leads = Leads.objects.exclude(first_contacted_on__isnull=True).filter(
            lead_status__in=lead_status, type_1__in=c_types, team__in=teams, country__in=locations,
            created_date__gte=start_date, created_date__lte=end_date)
        total_tag_summary['tat_implemented'] = ReportService.get_average_of_implemented(tag_implemented_leads)
        total_tag_summary['tat_first_contacted'] = ReportService.get_average_of_first_contacted(tag_contacted_leads)
        report_detail['total'] = total_summary
        report_detail['total_tag'] = total_tag_summary

        # Return report summary if leads
        if total_summary['total_leads']:
            return report_detail
        else:
            # return {} if no leads
            return {}

    @staticmethod
    def get_cr_row(implemented, code_details):
        ''' Get Conversion Ratio row by each Table '''
        row = dict()
        for codes in code_details.keys():
            cr = ReportService.get_conversion_ratio(implemented[codes], code_details[codes])
            row[codes] = cr
        total_cr = ReportService.get_conversion_ratio(implemented['total'], sum(code_details.values()))
        row.update({'lead_status_name': 'Conversion Ratio', 'total': total_cr})
        return row

    @staticmethod
    def get_conversion_ratio(actual, total):
        ''' Calculate Conversion Ratio '''
        cRatio = 0
        if total:
            cRatio = round(float(actual) / int(total) * 100, 2)
        return cRatio

    @staticmethod
    def is_all_status_exist(lead_status):
        ''' Check if all standerd status exist in lead_status'''
        flag = False
        for status in settings.LEAD_STATUS:
            if status in lead_status:
                flag = True
            else:
                flag = False
                break

        return flag

    # ##################### Missed Appointments starts ###########################
    @staticmethod
    def get_advertiser_missed_appointment_by_code_type(advertiser_leads, code_types):
        ''' get Advertiser Missed leads by code types '''
        missed_rec = dict()
        for lead in advertiser_leads:
            if lead.lead_sub_status in ['RX- Met Appointment', 'AD - Missed Appointment']:
                if lead.type_1 not in missed_rec:
                    missed_rec[lead.type_1] = 1
                else:
                    cnt = missed_rec[lead.type_1]
                    missed_rec[lead.type_1] = cnt + 1

        for code in code_types:
            if code not in missed_rec:
                missed_rec[code] = 0

        return missed_rec

    @staticmethod
    def get_regalix_missed_appointment_by_code_type(regalix_leads, code_types):
        ''' get Regalix Missed leads by code types '''

        missed_rec = dict()
        for lead in regalix_leads:
            if lead.lead_sub_status in ['RX - Missed Appointment']:
                if lead.type_1 not in missed_rec:
                    missed_rec[lead.type_1] = 1
                else:
                    cnt = missed_rec[lead.type_1]
                    missed_rec[lead.type_1] = cnt + 1

        for code in code_types:
            if code not in missed_rec:
                missed_rec[code] = 0

        return missed_rec
    # ##################### Missed Appointments ends #############################

    # ##################### Number of Dials report starts ########################
    @staticmethod
    def get_dial_by_code_type(dial_leads, code_types):
        ''' get Number of Dial leads by code types '''
        dials_rec = dict()
        for lead in dial_leads:
            if lead.dials:
                if lead.type_1 not in dials_rec:
                    dials_rec[lead.type_1] = lead.dials
                else:
                    dials = dials_rec[lead.type_1]
                    dials_rec[lead.type_1] = dials + lead.dials

        for code in code_types:
            if code not in dials_rec:
                dials_rec[code] = 0

        return dials_rec

    @staticmethod
    def get_picasso_report_details_for_filters(start_date, end_date, emails):
        picasso_report_detail = dict()
        if emails:
            query = {'created_date__gte': start_date, 'created_date__lte': end_date,
                     'google_rep_email__in': emails, 'lead_status__in': settings.PICASSO_LEAD_STATUS}
        else:
            query = {'created_date__gte': start_date, 'created_date__lte': end_date, 'lead_status__in': settings.PICASSO_LEAD_STATUS}

        picasso_lead_status_counts = PicassoLeads.objects.filter(**query).values('lead_status').annotate(count=Count('pk'))
        picasso_lead_status_count_dict = {str(rec['lead_status']): rec['count'] for rec in picasso_lead_status_counts}
        picasso_lead_status_count_dict['TOTAL'] = PicassoLeads.objects.filter(**query).count()

        key_order = [sts for sts in settings.PICASSO_LEAD_STATUS]
        key_order.append('TOTAL')

        for lead_status in settings.PICASSO_LEAD_STATUS:
            if lead_status not in picasso_lead_status_count_dict:
                picasso_lead_status_count_dict[lead_status] = 0

        picasso_keyorder = {k: v for v, k in enumerate(key_order)}
        picasso_report_detail['picasso_lead_status_analysis'] = OrderedDict(sorted(picasso_lead_status_count_dict.items(), key=lambda i: picasso_keyorder.get(i[0])))
        picasso_report_detail['picasso_program_type_analysis'], picasso_report_detail['pie_chart_dict'] = ReportService.get_picasso_objective_type_lead_status_analysis(query)
        return picasso_report_detail

    @staticmethod
    def get_picasso_objective_type_lead_status_analysis(query):
        picasso_program_type_lead_status_analysis = dict()
        lead_status_per_objective_type = PicassoLeads.objects.filter(**query).values('team').annotate(count=Count('pk'))
        pie_chart_dict = {str(rec['team']): rec['count'] for rec in lead_status_per_objective_type}
        pie_chart_dict = collections.OrderedDict(sorted(pie_chart_dict.items()))

        key_order = [sts for sts in settings.PICASSO_LEAD_STATUS]
        key_order.append('TOTAL')
        picasso_keyorder = {k: v for v, k in enumerate(key_order)}

        for team in lead_status_per_objective_type:
            query['team'] = team.get('team')
            lead_status_per_objective_type = PicassoLeads.objects.filter(**query).values('lead_status').annotate(count=Count('pk'))
            lead_status_per_objective_type_dict = {str(rec['lead_status']): rec['count'] for rec in lead_status_per_objective_type}
            for lead_status in settings.PICASSO_LEAD_STATUS:
                if lead_status not in lead_status_per_objective_type_dict:
                    lead_status_per_objective_type_dict[lead_status] = 0
            lead_status_per_objective_type_dict['TOTAL'] = PicassoLeads.objects.filter(**query).count()
            picasso_program_type_lead_status_analysis[team.get('team')] = OrderedDict(sorted(lead_status_per_objective_type_dict.items(), key=lambda i: picasso_keyorder.get(i[0])))
        for key, value in picasso_program_type_lead_status_analysis.iteritems():
            if key == '':
                picasso_program_type_lead_status_analysis['Others'] = picasso_program_type_lead_status_analysis[key]
                del picasso_program_type_lead_status_analysis[key]
        picasso_program_type_lead_status_analysis = collections.OrderedDict(sorted(picasso_program_type_lead_status_analysis.items()))
        return picasso_program_type_lead_status_analysis, pie_chart_dict
    # ##################### Number of Dials report ends ###########################


class DownloadLeads(object):

    def __init__(self):
        pass

    @staticmethod
    def get_leads_by_report_type(code_types, teams, countries, start_date, end_date, emails):
        if emails and teams and countries:
            leads = Leads.objects.exclude(type_1='WPP').filter(country__in=countries, team__in=teams, type_1__in=code_types,
                                                               created_date__gte=start_date, created_date__lte=end_date,
                                                               google_rep_email__in=emails)

        elif not emails and teams and countries:
            leads = Leads.objects.exclude(type_1='WPP').filter(country__in=countries, team__in=teams, type_1__in=code_types,
                                                               created_date__gte=start_date, created_date__lte=end_date)

        elif emails and not teams and not countries:
            leads = Leads.objects.exclude(type_1='WPP').filter(type_1__in=code_types, google_rep_email__in=emails,
                                                               created_date__gte=start_date, created_date__lte=end_date)

        elif not emails and not teams and countries:
            leads = Leads.objects.exclude(type_1='WPP').filter(country__in=countries, type_1__in=code_types,
                                                               created_date__gte=start_date, created_date__lte=end_date)

        elif emails and not teams and countries:
            leads = Leads.objects.exclude(type_1='WPP').filter(country__in=countries, type_1__in=code_types,
                                                               google_rep_email__in=emails, created_date__gte=start_date,
                                                               created_date__lte=end_date)

        return leads

    @staticmethod
    def download_lead_report(leads, from_date, to_date, selected_fields):
        filename = "leads-%s-to-%s" % (datetime.strftime(from_date, "%d-%b-%Y"), datetime.strftime(to_date, "%d-%b-%Y"))
        selected_fields.append('Lead Sub-Status')
        leads = DownloadLeads.get_leads_for_report(leads, from_date, to_date, selected_fields)
        path = "/tmp/%s.csv" % (filename)
        DownloadLeads.conver_to_csv(path, leads, selected_fields)
        return path

    @staticmethod
    def get_leads_for_report(leads, from_date, to_date, selected_fields):
        results = list()
        for lead in leads:
            row = dict()
            lead_dict = dict()

            row['Email'] = str(lead.google_rep_email.encode('utf-8'))
            row['E-commerce'] = lead.ecommerce
            row['Lead Owner'] = str(lead.lead_owner_name.encode('utf-8'))
            row['Regalix E-mails'] = str(lead.lead_owner_email.encode('utf-8'))
            row['Company / Account'] = str(lead.company.encode('utf-8'))

            row['Customer ID'] = lead.customer_id
            row['First Name'] = str(lead.first_name.encode('utf-8'))
            row['Last Name'] = str(lead.last_name.encode('utf-8'))
            row['Phone'] = str(lead.phone.encode('utf-8'))

            row['First Name - optional'] = str(lead.first_name_optional.encode('utf-8'))
            row['Last Name - optional'] = str(lead.last_name_optional.encode('utf-8'))
            row['Phone - optional'] = str(lead.phone_optional.encode('utf-8'))
            row['Email - optional'] = str(lead.email_optional.encode('utf-8'))

            row['Time Zone'] = lead.time_zone
            row['Regalix Comment'] = str(lead.regalix_comment.encode('utf-8'))
            row['Google Comment'] = str(lead.google_comment.encode('utf-8'))

            row['Code'] = str(lead.code_1.encode('utf-8'))
            row['URL'] = str(lead.url_1.encode('utf-8'))
            row['Comment 1'] = str(lead.comment_1.encode('utf-8'))

            row['Google Account Manager'] = str(lead.google_rep_name.encode('utf-8'))
            row['Lead Status'] = lead.lead_status
            row['Location'] = lead.country
            row['Task Type'] = str(lead.type_1.encode('utf-8'))
            row['Team'] = lead.team
            row['Dials'] = lead.dials
            row['Rescheduled Appointments'] = lead.rescheduled_appointment
            row['Lead Sub-Status'] = lead.lead_sub_status

            # Format ex: 18/07/2014
            if lead.date_of_installation:
                row['Date of Installation'] = str(datetime.strftime(lead.date_of_installation, "%d/%m/%Y"))
            else:
                row['Date of Installation'] = None

            row['Create Date'] = str(datetime.strftime(lead.created_date, "%d/%m/%Y"))

            # Date formate in csv ex: 01/07/2014 03:42:00
            if lead.appointment_date:
                row['Appointment Date'] = datetime.strftime(lead.appointment_date, "%d/%m/%Y %I:%M:%S")
            else:
                row['Appointment Date'] = None

            if lead.first_contacted_on:
                row['1st Contacted on'] = datetime.strftime(lead.first_contacted_on, "%d/%m/%Y %I:%M:%S")
            else:
                row['1st Contacted on'] = None

            row['Lead ID'] = lead.sf_lead_id
            row['TAT'] = lead.tat

            for field in selected_fields:
                if field in row.keys():
                    lead_dict[field] = row[field]

            results.append(lead_dict)

        return results

    @staticmethod
    def get_leads_for_picasso_report(leads, from_date, to_date, selected_fields):
        results = list()
        for lead in leads:
            row = dict()
            lead_dict = dict()

            row['Email'] = str(lead.google_rep_email.encode('utf-8'))
            row['Lead Owner'] = str(lead.lead_owner_name.encode('utf-8'))
            row['Regalix E-mails'] = str(lead.lead_owner_email.encode('utf-8'))
            row['Company / Account'] = str(lead.company.encode('utf-8'))

            row['Customer ID'] = lead.customer_id
            row['First Name'] = str(lead.first_name.encode('utf-8'))
            row['Last Name'] = str(lead.last_name.encode('utf-8'))
            row['Phone'] = str(lead.phone.encode('utf-8'))

            row['Goal'] = str(lead.code_1.encode('utf-8'))
            row['URL'] = str(lead.url_1.encode('utf-8'))
            row['Recommondation'] = str(lead.comment_1.encode('utf-8'))
            row['Internal CID'] = str(lead.internal_cid)
            row['POD Name'] = str(lead.pod_name.encode('utf-8'))
            row['Objectives'] = str(lead.picasso_objective.encode('utf-8')).replace(';', ',')

            row['Google Account Manager'] = str(lead.google_rep_name.encode('utf-8'))
            row['Lead Status'] = lead.lead_status
            row['Task Type'] = str(lead.type_1.encode('utf-8'))
            row['Team'] = lead.team

            row['Lead ID'] = lead.sf_lead_id

            for field in selected_fields:
                if field in row.keys():
                    lead_dict[field] = row[field]

            results.append(lead_dict)

        return results

    @staticmethod
    def download_lead_data(from_date, to_date, fields_type):
        from_date = datetime.strptime(from_date, "%b %d, %Y")
        to_date = datetime.strptime(to_date, "%b %d, %Y")
        to_date = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59)
        filename = "leads-%s-to-%s" % (datetime.strftime(from_date, "%d-%b-%Y"), datetime.strftime(to_date, "%d-%b-%Y"))
        leads = DownloadLeads.get_leads(from_date, to_date, fields_type)
        path = "/tmp/%s.csv" % (filename)
        if fields_type == 'REPORT':
            fields = ['Create Date', 'Google Account Manager', 'Lead Status', 'Location', 'Date of installation',
                      'Task Type', 'Team', 'Lead ID', '1st Contacted on', 'Appointment Date', 'Rescheduled Appointments',
                      'Lead Sub-Status', 'Dials']
        else:
            fields = ['Create Date', 'Google Account Manager', 'E-commerce', 'Lead Owner', 'Company / Account', 'Lead Status',
                      'Location', 'Customer ID', 'First Name', 'Last Name', 'Phone', 'Email', 'First Name - optional',
                      'Last Name - optional', 'Phone - optional', 'Email - optional', 'Date of installation', 'Time Zone',
                      'Regalix Comment', 'Google Comment', 'Code', 'URL', 'Task Type', 'Comment 1', 'Team', 'Lead ID',
                      '1st Contacted on', 'Appointment Date', 'Rescheduled Appointments', 'Dead Lead (Date)',
                      'Regalix E-mails', 'Lead Sub-Status', 'Dials']

        DownloadLeads.conver_to_csv(path, leads, fields)
        return path

    @staticmethod
    def get_leads(from_date, to_date, fields_type):
        leads = Leads.objects.filter(created_date__gte=from_date, created_date__lte=to_date)
        results = list()
        for lead in leads:
            row = dict()
            if fields_type == 'ALL':
                row['Email'] = str(lead.google_rep_email.encode('utf-8'))
                row['E-commerce'] = lead.ecommerce
                row['Lead Owner'] = str(lead.lead_owner_name.encode('utf-8'))
                row['Regalix E-mails'] = str(lead.lead_owner_email.encode('utf-8'))
                row['Company / Account'] = str(lead.company.encode('utf-8'))

                row['Customer ID'] = lead.customer_id
                row['First Name'] = str(lead.first_name.encode('utf-8'))
                row['Last Name'] = str(lead.last_name.encode('utf-8'))
                row['Phone'] = str(lead.phone.encode('utf-8'))

                row['First Name - optional'] = str(lead.first_name_optional.encode('utf-8'))
                row['Last Name - optional'] = str(lead.last_name_optional.encode('utf-8'))
                row['Phone - optional'] = str(lead.phone_optional.encode('utf-8'))
                row['Email - optional'] = str(lead.email_optional.encode('utf-8'))

                row['Time Zone'] = lead.time_zone
                row['Regalix Comment'] = str(lead.regalix_comment.encode('utf-8'))
                row['Google Comment'] = str(lead.google_comment.encode('utf-8'))

                row['Code'] = str(lead.code_1.encode('utf-8'))
                row['URL'] = str(lead.url_1.encode('utf-8'))
                row['Comment 1'] = str(lead.comment_1.encode('utf-8'))

            row['Google Account Manager'] = str(lead.google_rep_name.encode('utf-8'))
            row['Lead Status'] = lead.lead_status
            row['Location'] = lead.country
            row['Task Type'] = str(lead.type_1.encode('utf-8'))
            row['Team'] = lead.team
            row['Dials'] = lead.dials
            row['Rescheduled Appointments'] = lead.rescheduled_appointment
            row['Lead Sub-Status'] = lead.lead_sub_status

            # Format ex: 18/07/2014
            if lead.date_of_installation:
                row['Date of installation'] = str(datetime.strftime(lead.date_of_installation, "%d/%m/%Y"))
            else:
                row['Date of installation'] = None
            row['Create Date'] = str(datetime.strftime(lead.created_date, "%d/%m/%Y"))

            # Date formate in csv ex: 01/07/2014 03:42:00
            if lead.appointment_date:
                row['Appointment Date'] = datetime.strftime(lead.appointment_date, "%d/%m/%Y %I:%M:%S")
            else:
                row['Appointment Date'] = None

            if lead.first_contacted_on:
                row['1st Contacted on'] = datetime.strftime(lead.first_contacted_on, "%d/%m/%Y %I:%M:%S")
            else:
                row['1st Contacted on'] = None

            row['Lead ID'] = lead.sf_lead_id
            results.append(row)

        return results

    @staticmethod
    def conver_to_csv(path, rows, fields):
        writer = csv.DictWriter(open(path, 'w'), fields, delimiter=',')
        writer.writeheader()
        for row in rows:
            try:
                writer.writerow(row)
            except Exception as e:
                # print row
                print e

    @staticmethod
    def get_downloaded_file_response(path):
        filename = os.path.basename(path)
        mimetype, encoding = mimetypes.guess_type(filename)
        response = HttpResponse(mimetype=mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        response.write(file(path, "rb").read())
        return response


class TrendsReportServices(object):

    def __init__(self):
        pass

    @staticmethod
    def get_trends_report_program_wise(teams, code_types, timeline):
        reports = list()
        first_row = [timeline]
        first_row.extend(teams)
        first_row.extend(['TOTAL LEADS'])
        if '' in first_row:
            first_row[first_row.index('')] = 'Other'
        reports.append(first_row)
        if (timeline == 'Weeks'):
            currentWeek = datetime.utcnow().isocalendar()[1]
            for w in range(1, currentWeek + 1):
                week_name = 'W%s' % (str(w))
                start_date, end_date = get_week_start_end_days(datetime.utcnow().year, w)
                reports.append(TrendsReportServices.get_trend_reports_by_teams(week_name, teams, code_types, start_date, end_date))
        elif(timeline == 'Quarters'):
            currentMonth = int(datetime.utcnow().month)
            currentQuarter = int(currentMonth / 3)
            for q in range(1, currentQuarter + 1):
                quarter_name = 'Q%s' % (str(q))
                start_date, end_date = date_range_by_quarter('Q%s' % (str(q)))
                reports.append(TrendsReportServices.get_trend_reports_by_teams(quarter_name, teams, code_types, start_date, end_date))
        elif(timeline == 'Months'):
            currentMonth = datetime.utcnow().month
            for m in range(1, currentMonth + 1):
                month_name = 'M%s' % (str(m))
                c_month = datetime(datetime.utcnow().year, m, 1)
                start_date = first_day_of_month(c_month)
                end_date = last_day_of_month(c_month)
                reports.append(TrendsReportServices.get_trend_reports_by_teams(month_name, teams, code_types, start_date, end_date))
        return reports

    @staticmethod
    def get_for_win_total_and_conversionratio(team, code_types, timeline):
        reports = list()
        first_row = [timeline, 'Total Leads', 'Wins', 'Conversion Ratio %']
        reports.append(first_row)
        if (timeline == 'Weeks'):
            currentWeek = datetime.utcnow().isocalendar()[1]
            for w in range(1, currentWeek + 1):
                weekname = 'W%s' % (str(w))
                start_date, end_date = get_week_start_end_days(datetime.utcnow().year, w)
                reports.append(TrendsReportServices.get_total_win_conversio_ratio_by_teams(weekname, team, code_types, start_date, end_date))
        elif(timeline == 'Quarters'):
            currentMonth = int(datetime.utcnow().month)
            currentQuarter = int(currentMonth / 3)
            for q in range(1, currentQuarter + 1):
                quartername = 'Q%s' % (str(q))
                start_date, end_date = date_range_by_quarter('Q%s' % (str(q)))
                reports.append(TrendsReportServices.get_total_win_conversio_ratio_by_teams(quartername, team, code_types, start_date, end_date))
        elif (timeline == 'Months'):
            currentMonth = datetime.utcnow().month
            for m in range(1, currentMonth + 1):
                lead_team = list()
                lead_team.append('M%s' % (str(m)))
                monthname = 'M%s' % (str(m))
                c_month = datetime(datetime.utcnow().year, m, 1)
                start_date = first_day_of_month(c_month)
                end_date = last_day_of_month(c_month)
                reports.append(TrendsReportServices.get_total_win_conversio_ratio_by_teams(monthname, team, code_types, start_date, end_date))
        return reports

    @staticmethod
    def get_trend_reports_by_teams(name, teams, code_types, start_date, end_date):
        lead_team = list()
        lead_team.append(name)
        totalLeads = 0
        for team in teams:
            leads = len(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date, team=team, type_1__in=code_types))
            lead_team.append(leads)
            totalLeads = totalLeads + leads
        lead_team.append(totalLeads)
        return lead_team

    @staticmethod
    def get_total_win_conversio_ratio_by_teams(timelinename, teams, code_types, start_date, end_date):
        lead_team = list()
        lead_team.append(timelinename)
        totalLeads = len(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date, team__in=teams, type_1__in=code_types))
        lead_team.append(totalLeads)
        win = len(Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date, lead_status='Implemented', team__in=teams, type_1__in=code_types))
        lead_team.append(win)
        if (totalLeads != 0):
            cr = round(float(win) / totalLeads * 100, 2)
        else:
            cr = 0.0
        lead_team.append(cr)
        return lead_team
