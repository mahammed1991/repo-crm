import csv
import os
import mimetypes
from datetime import datetime, date
from leads.models import Leads, RegalixTeams, Team, Location
from reports.models import QuarterTargetLeads
from lib.helpers import (get_week_start_end_days, first_day_of_month, get_quarter_date_slots,
                         last_day_of_month, date_range_by_quarter, dsum, prev_quarter_date_range,
                         get_previous_month_start_end_days, get_weeks_in_quarter_to_date, is_manager)
from django.conf import settings
from django.http import HttpResponse
import time


class ReportService(object):

    def __init__(self):
        pass

    @staticmethod
    def get_all_code_type():
        ''' Get all code types '''
        return list(Leads.objects.exclude(type_1='').values_list(
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

    # @staticmethod
    # def get_date_range_by_timeline(timeline):
    #     ''' Get start and end date by timeline options: Weekly, Monthly, Quarterly and date range '''
    #     if timeline['quarterly']:
    #         # get date range by quarterly
    #         start_date, end_date = date_range_by_quarter(timeline['quarterly'])
    #     elif timeline['monthly']:
    #         # get date range by monthly
    #         month = date_by_month_name(int(timeline['monthly']))
    #         start_date = first_day_of_month(month)
    #         end_date = last_day_of_month(month)

    #     elif timeline['weekly']:
    #         # get date range by weekly
    #         date_now = datetime.utcnow()
    #         start_date, end_date = get_week_start_end_days(date_now.year, int(timeline['weekly']))
    #     else:
    #         # get date range by given date_range
    #         start_date = datetime.strptime(str(timeline['date_range'][0]), "%b %d, %Y")
    #         end_date = datetime.strptime(str(timeline['date_range'][1]), "%b %d, %Y")

    #     return start_date, end_date

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

    @staticmethod
    def get_leads_status_summary(lead_ids):
        ''' Get Leads staus summary for Leads '''
        leads = Leads.objects.filter(id__in=lead_ids)
        leads_status_summary = dict()
        leads_status_summary['TAT'] = ReportService.get_average_tat_for_leads(leads)
        lead_status_dict = settings.LEAD_STATUS_DICT
        total_leads = 0
        for key in lead_status_dict.keys():
            leads_status_summary[key] = len(Leads.objects.filter(lead_status__in=lead_status_dict[key], id__in=lead_ids))
            total_leads += len(Leads.objects.filter(lead_status__in=lead_status_dict[key], id__in=lead_ids))

        leads_status_summary['total_leads'] = total_leads
        return leads_status_summary

    @staticmethod
    def get_week_on_week_trends_details(lead_ids):
        ''' Week on week analysis of leads won over leads submitted '''
        week_on_week_trends = dict()
        weeks_in_qtd = get_weeks_in_quarter_to_date()

        for index in range(1, len(weeks_in_qtd) + 1):

            week_on_week_trends[index] = {'leads_won': 0}
            start_date, end_date = weeks_in_qtd[index - 1]
            print 'start_date, end_date', start_date, end_date
            #leads = Leads.objects.filter(id__in=lead_ids, created_date__gte=start_date, created_date__lte=end_date)
            leads = Leads.objects.filter(created_date__gte=start_date, created_date__lte=end_date)
            for lead in leads:
                if lead.lead_status == 'Implemented':
                    week_on_week_trends[index]['leads_won'] += 1
            week_on_week_trends[index]['total_leads_submitted'] = len(leads)

        return week_on_week_trends

    @staticmethod
    def get_report_details_for_filters(code_types, teams, countries, start_date, end_date, emails):
        #import ipdb;ipdb.set_trace()
        report_detail = dict()
        if emails and teams and countries:
            leads = Leads.objects.filter(country__in=countries, team__in=teams, type_1__in=code_types,
                                         created_date__gte=start_date, created_date__lte=end_date,
                                         google_rep_email__in=emails)

        elif not emails and teams and countries:
            leads = Leads.objects.filter(country__in=countries, team__in=teams, type_1__in=code_types,
                                         created_date__gte=start_date, created_date__lte=end_date)

        elif emails and not teams and not countries:
            leads = Leads.objects.filter(type_1__in=code_types, google_rep_email__in=emails,
                                         created_date__gte=start_date, created_date__lte=end_date)

        elif not emails and not teams and countries:
            leads = Leads.objects.filter(country__in=countries, type_1__in=code_types,
                                         created_date__gte=start_date, created_date__lte=end_date)

        elif emails and not teams and countries:
            leads = Leads.objects.filter(country__in=countries, type_1__in=code_types, google_rep_email__in=emails,
                                         created_date__gte=start_date, created_date__lte=end_date)

        lead_ids = [lead.id for lead in leads]

        leads_status_summary = ReportService.get_leads_status_summary(lead_ids)

        lead_status_analysis_table = list()

        for code_type in code_types:

            lead_status_analysis = {code_type: ''}

            leads_per_code_type = Leads.objects.filter(type_1=code_type, id__in=lead_ids)

            lead_status_analysis[code_type] = ReportService.get_lead_status_analysis(leads_per_code_type)

            lead_status_analysis_table.append(lead_status_analysis)

        pie_chart_dict = dict()

        for cod_typ in lead_status_analysis_table:
            key = cod_typ.keys()[0]
            value = cod_typ[key]['Total']
            pie_chart_dict[key] = value

        week_on_week_trends = ReportService.get_week_on_week_trends_details(lead_ids)

        report_detail.update({'lead_status_summary': leads_status_summary,
                              'piechart': pie_chart_dict,
                              'table_header': settings.LEAD_STATUS_DICT,
                              'lead_code_type_analysis': lead_status_analysis_table,
                              'week_on_week_details_in_qtd': week_on_week_trends})
        return report_detail

    @staticmethod
    def get_program_report_by_locations(teams, countries):
        """ Get reports for each Programs by all locations """
        
        week = int(time.strftime("%W")) + 1
        year = int(time.strftime("%Y"))
        week_start_date, week_end_date = get_week_start_end_days(year, week)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(datetime.utcnow())
        quarter_end_date = datetime.utcnow()

        week_wise_leads = Leads.objects.filter(country__in=countries, team__in=teams,
                                               created_date__gte=week_start_date, created_date__lte=week_end_date)

        quarter_wise_leads = Leads.objects.filter(country__in=countries, team__in=teams,
                                                  created_date__gte=quarter_start_date, created_date__lte=quarter_end_date)

        prev_qtr_start_dt, prev_qtr_end_dt = prev_quarter_date_range(datetime.utcnow())

        prev_qtr_leads = Leads.objects.filter(country__in=countries, team__in=teams,
                                              created_date__gte=prev_qtr_start_dt, created_date__lte=prev_qtr_end_dt)

        prev_qtr_year = prev_qtr_start_dt.year

        quarter = ReportService.get_current_quarter(prev_qtr_start_dt)

        team_dict = {team.team_name: team.id for team in Team.objects.all()}

        location_dict = {location.location_name: location.id for location in Location.objects.all()}

        target_leads = QuarterTargetLeads.objects.filter(quarter=quarter, year=prev_qtr_year)

        target_leads = {"%s_%s_%s_%s" %(target_lead.program_id, target_lead.location_id, target_lead.quarter, target_lead.year): target_lead.target_leads for target_lead in target_leads}

        detail = dict()

        if '' in teams:
            teams.remove('')

        for team in teams:
            detail[team] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'locations': {}, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0.0}
            for country in countries:
                detail[team]['locations'][country] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0.0}

        for lead in week_wise_leads:
            if lead.team in detail.keys():
                detail[lead.team]['week_total'] = detail[lead.team]['week_total'] + 1
                if lead.lead_status == 'Implemented':
                    detail[lead.team]['week_win'] = detail[lead.team]['week_win'] + 1

                if lead.country in detail[lead.team]['locations'].keys():
                    detail[lead.team]['locations'][lead.country]['week_total'] = detail[lead.team]['locations'][lead.country]['week_total'] + 1
                    if lead.lead_status == 'Implemented':
                        detail[lead.team]['locations'][lead.country]['week_win'] = detail[lead.team]['locations'][lead.country]['week_win'] + 1

        for lead in quarter_wise_leads:
            if lead.team in detail.keys():
                detail[lead.team]['qtd_total'] = detail[lead.team]['qtd_total'] + 1
                if lead.lead_status == 'Implemented':
                    detail[lead.team]['qtd_win'] = detail[lead.team]['qtd_win'] + 1

                if lead.country in detail[lead.team]['locations'].keys():
                    detail[lead.team]['locations'][lead.country]['qtd_total'] = detail[lead.team]['locations'][lead.country]['qtd_total'] + 1
                    if lead.lead_status == 'Implemented':
                        detail[lead.team]['locations'][lead.country]['qtd_win'] = detail[lead.team]['locations'][lead.country]['qtd_win'] + 1

        for lead in prev_qtr_leads:
            if lead.team in detail.keys():
                detail[lead.team]['end_qtr_total'] = detail[lead.team]['end_qtr_total'] + 1
                if lead.country in detail[lead.team]['locations'].keys():
                    detail[lead.team]['locations'][lead.country]['end_qtr_total'] = detail[lead.team]['locations'][lead.country]['end_qtr_total'] + 1
                    if lead.team in team_dict and lead.country in location_dict:
                        if "%s_%s_%s_%s" % (team_dict[lead.team], location_dict[lead.country], quarter, prev_qtr_year) not in target_leads.keys():
                            detail[lead.team]['locations'][lead.country]['end_qtr_target'] = 0
                        else:
                            detail[lead.team]['locations'][lead.country]['end_qtr_target'] = target_leads["%s_%s_%s_%s" % (team_dict[lead.team], location_dict[lead.country], quarter, prev_qtr_year)]
                        loc_out_vs_trgt = float(detail[lead.team]['locations'][lead.country]['end_qtr_total']) / detail[lead.team]['locations'][lead.country]['end_qtr_target'] if detail[lead.team]['locations'][lead.country]['end_qtr_target'] != 0 else 0
                        detail[lead.team]['locations'][lead.country]['out_vs_trgt'] = round(loc_out_vs_trgt, 2) * 100
                    else:
                        detail[lead.team]['locations'][lead.country]['end_qtr_target'] = 0
                        detail[lead.team]['locations'][lead.country]['out_vs_trgt'] = 0

        for program in detail.keys():
            program_target = list()
            for loc in detail[program]['locations'].keys():
                program_target.append(detail[program]['locations'][loc]['end_qtr_target'])
            detail[program]['end_qtr_target'] = sum(program_target)
            out_vs_trgt = float(detail[program]['end_qtr_total']) / detail[program]['end_qtr_target'] if detail[program]['end_qtr_target'] != 0 else 0
            detail[program]['out_vs_trgt'] = round(out_vs_trgt, 2) * 100
        return detail

    @staticmethod
    def get_region_report_by_program(countries, teams):
        """ Get reports for each Programs by all locations """
        week = int(time.strftime("%W")) + 1
        year = int(time.strftime("%Y"))
        week_start_date, week_end_date = get_week_start_end_days(year, week)
        quarter_start_date, quarter_end_date = get_quarter_date_slots(datetime.utcnow())
        quarter_end_date = datetime.utcnow()

        week_wise_leads = Leads.objects.filter(country__in=countries, team__in=teams,
                                               created_date__gte=week_start_date, created_date__lte=week_end_date)

        quarter_wise_leads = Leads.objects.filter(country__in=countries, team__in=teams,
                                                  created_date__gte=quarter_start_date, created_date__lte=quarter_end_date)

        prev_qtr_start_dt, prev_qtr_end_dt = prev_quarter_date_range(datetime.utcnow())

        prev_qtr_leads = Leads.objects.filter(country__in=countries, team__in=teams,
                                              created_date__gte=prev_qtr_start_dt, created_date__lte=prev_qtr_end_dt)

        prev_qtr_year = prev_qtr_start_dt.year

        quarter = ReportService.get_current_quarter(prev_qtr_start_dt)

        team_dict = {team.team_name: team.id for team in Team.objects.all()}

        location_dict = {location.location_name: location.id for location in Location.objects.all()}

        target_leads = QuarterTargetLeads.objects.filter(quarter=quarter, year=prev_qtr_year)

        target_leads = {"%s_%s_%s_%s" %(target_lead.location_id, target_lead.program_id, target_lead.quarter, target_lead.year): target_lead.target_leads for target_lead in target_leads}
        detail = dict()

        if '' in teams:
            teams.remove('')

        for location in countries:
            target_loc = list()
            detail[location] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'programs': {}, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0}
            for team in teams:
                if team in team_dict and location in location_dict:
                    target_key = "%s_%s_%s_%s" % (location_dict[location], team_dict[team], quarter, prev_qtr_year)
                    target_loc.append(target_leads.get(target_key, 0))
                    detail[location]['programs'][team] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'end_qtr_total': 0, 'end_qtr_target': target_leads.get(target_key, 0), 'out_vs_trgt': 0}
                else:
                    target_loc.append(0)
                    detail[location]['programs'][team] = {'week_total': 0, 'week_win': 0, 'qtd_total': 0, 'qtd_win': 0, 'end_qtr_total': 0, 'end_qtr_target': 0, 'out_vs_trgt': 0}

            detail[location]['end_qtr_target'] = sum(target_loc)

        for lead in week_wise_leads:
            if lead.country in detail.keys():
                detail[lead.country]['week_total'] = detail[lead.country]['week_total'] + 1
                if lead.lead_status == 'Implemented':
                    detail[lead.country]['week_win'] = detail[lead.country]['week_win'] + 1

                if lead.team in detail[lead.country]['programs'].keys():
                    detail[lead.country]['programs'][lead.team]['week_total'] = detail[lead.country]['programs'][lead.team]['week_total'] + 1
                    if lead.lead_status == 'Implemented':
                        detail[lead.country]['programs'][lead.team]['week_win'] = detail[lead.country]['programs'][lead.team]['week_win'] + 1

        for lead in quarter_wise_leads:
            if lead.country in detail.keys():
                detail[lead.country]['qtd_total'] = detail[lead.country]['qtd_total'] + 1
                if lead.lead_status == 'Implemented':
                    detail[lead.country]['qtd_win'] = detail[lead.country]['qtd_win'] + 1

                if lead.team in detail[lead.country]['programs'].keys():
                    detail[lead.country]['programs'][lead.team]['qtd_total'] = detail[lead.country]['programs'][lead.team]['qtd_total'] + 1
                    if lead.lead_status == 'Implemented':
                        detail[lead.country]['programs'][lead.team]['qtd_win'] = detail[lead.country]['programs'][lead.team]['qtd_win'] + 1

        for lead in prev_qtr_leads:
            if lead.country in detail.keys():
                detail[lead.country]['end_qtr_total'] = detail[lead.country]['end_qtr_total'] + 1
                if lead.team in detail[lead.country]['programs'].keys():
                    if lead.team in team_dict and lead.country in location_dict:
                        detail[lead.country]['programs'][lead.team]['end_qtr_total'] = detail[lead.country]['programs'][lead.team]['end_qtr_total'] + 1
                        pgm_out_vs_trgt = float(detail[lead.country]['programs'][lead.team]['end_qtr_total']) / detail[lead.country]['programs'][lead.team]['end_qtr_target'] if detail[lead.country]['programs'][lead.team]['end_qtr_target'] != 0 else 0
                        detail[lead.country]['programs'][lead.team]['out_vs_trgt'] = round(pgm_out_vs_trgt, 2) * 100
                    else:
                        detail[lead.country]['programs'][lead.team]['end_qtr_total'] = 0
                        detail[lead.country]['programs'][lead.team]['out_vs_trgt'] = 0

        for location in detail.keys():
            out_vs_trgt = float(detail[location]['end_qtr_total']) / detail[location]['end_qtr_target'] if detail[location]['end_qtr_target'] != 0 else 0
            detail[location]['out_vs_trgt'] = round(out_vs_trgt, 2) * 100

        return detail

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
    def get_lead_status_analysis(leads):
        lead_dict = settings.LEAD_STATUS_DICT
        lead_status_analysis = {lead_status: 0 for lead_status in lead_dict}
        for lead in leads:
            for key, value in lead_dict.items():
                if lead.lead_status in value:
                    lead_status_analysis[key] += 1
        lead_status_analysis['Total'] = len(leads)
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

    ########################################## TAT Reports Starts Here ####################################

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
            if lead.team in ['Services', 'Services (Traverwood)', 'Services Revenue Program (SRP)']:
                days += ReportService.get_tat_by_implemented_for_service(lead.date_of_installation, lead.created_date)
            else:
                days += ReportService.get_tat_by_implemented(lead.date_of_installation, lead.appointment_date, lead.created_date)

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

    ########################################## TAT Reports Ends Here ####################################

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

    ###################### Missed Appointments starts ###########################
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
    ###################### Missed Appointments ends #############################

    ###################### Number of Dials report starts ########################
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
    ###################### Number of Dials report ends ###########################


class DownloadLeads(object):

    def __init__(self):
        pass

    @staticmethod
    def get_leads_by_report_type(code_types, teams, countries, start_date, end_date, emails):
        if emails and teams and countries:
            leads = Leads.objects.filter(country__in=countries, team__in=teams, type_1__in=code_types,
                                         created_date__gte=start_date, created_date__lte=end_date,
                                         google_rep_email__in=emails)

        elif not emails and teams and countries:
            leads = Leads.objects.filter(country__in=countries, team__in=teams, type_1__in=code_types,
                                         created_date__gte=start_date, created_date__lte=end_date)

        elif emails and not teams and not countries:
            leads = Leads.objects.filter(type_1__in=code_types, google_rep_email__in=emails,
                                         created_date__gte=start_date, created_date__lte=end_date)

        elif not emails and not teams and countries:
            leads = Leads.objects.filter(country__in=countries, type_1__in=code_types,
                                         created_date__gte=start_date, created_date__lte=end_date)

        return leads
    
    @staticmethod
    def download_lead_report(leads, from_date, to_date, selected_fields):
        filename = "leads-%s-to-%s" % (datetime.strftime(from_date, "%d-%b-%Y"), datetime.strftime(to_date, "%d-%b-%Y"))
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
            row['Code Type'] = str(lead.type_1.encode('utf-8'))
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
            if lead.team in ['Services', 'Services (Traverwood)', 'Services Revenue Program (SRP)']:
                row['TAT'] = ReportService.get_tat_by_implemented_for_service(lead.date_of_installation, lead.created_date) if lead.date_of_installation else 'N/A'
            else:
                row['TAT'] = ReportService.get_tat_by_implemented(lead.date_of_installation, lead.appointment_date, lead.created_date)

            for field in selected_fields:
                if field in row.keys():
                    lead_dict[field] = row[field]

            results.append(lead_dict)

        return results

    @staticmethod
    def download_lead_data(from_date, to_date, fields_type):
        from_date = datetime.strptime(from_date, "%b %d, %Y")
        to_date = datetime.strptime(to_date, "%b %d, %Y")
        filename = "leads-%s-to-%s" % (datetime.strftime(from_date, "%d-%b-%Y"), datetime.strftime(to_date, "%d-%b-%Y"))
        leads = DownloadLeads.get_leads(from_date, to_date, fields_type)
        path = "/tmp/%s.csv" % (filename)
        if fields_type == 'REPORT':
            fields = ['Create Date', 'Google Account Manager', 'Lead Status', 'Location', 'Date of installation',
                      'Code Type', 'Team', 'Lead ID', '1st Contacted on', 'Appointment Date', 'Rescheduled Appointments',
                      'Lead Sub-Status', 'Dials']
        else:
            fields = ['Create Date', 'Google Account Manager', 'E-commerce', 'Lead Owner', 'Company / Account', 'Lead Status',
                      'Location', 'Customer ID', 'First Name', 'Last Name', 'Phone', 'Email', 'First Name - optional',
                      'Last Name - optional', 'Phone - optional', 'Email - optional', 'Date of installation', 'Time Zone',
                      'Regalix Comment', 'Google Comment', 'Code', 'URL', 'Code Type', 'Comment 1', 'Team', 'Lead ID',
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
            row['Code Type'] = str(lead.type_1.encode('utf-8'))
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
        Writer = csv.DictWriter(open(path, 'w'), fields, delimiter=',')
        Writer.writeheader()
        for row in rows:
            try:
                Writer.writerow(row)
            except Exception as e:
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
