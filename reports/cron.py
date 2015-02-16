import kronos
from reports.report_services import ReportService
from django.conf import settings
from datetime import datetime
from lib.helpers import get_quarter_date_slots
from reports.models import LeadSummaryReports
import logging

logging.basicConfig(filename='/tmp/cronjob.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%d/%b/%Y %H:%M:%S',
                    level=logging.DEBUG)


@kronos.register('0 * * * *')
def get_current_quarter_summary():
    logging.info("Initializing kronos")
    # Get all teams
    teams = ReportService.get_all_teams()

    # get all code types
    code_types = ReportService.get_all_code_type()

    #get all lead status
    lead_status = settings.LEAD_STATUS
    lead_status.extend(['Pending QC - DEAD LEAD', 'Pending QC - WIN', 'Rework Required', 'Appointment Set (GS)'])

    #get current quarter
    dt = datetime.now()
    start_date, end_date = get_quarter_date_slots(dt)
    logging.info("Get Current Quarter Report from %s to %s" % (datetime.strftime(start_date, "%d %b %Y"), datetime.strftime(end_date, "%d %b %Y")))

    # get all locations
    locations = ReportService.get_all_locations()
    reports = ReportService.get_summary_by_code_types_and_status('all', code_types, lead_status,
                                                                 start_date, end_date, teams, locations)
    code_type = reports.keys()
    for k in code_type:
        current_quarter = LeadSummaryReports.objects.filter(code_type=k)
        if current_quarter:
            current_quarter.code_type = k
            current_quarter.total_leads = reports[k]['total_leads']
            current_quarter.win = reports[k]['wins']
            current_quarter.implemented = reports[k]['Implemented']
            if 'In Queue' in reports[k]:
                current_quarter.in_queue = reports[k]['In Queue'] + reports[k].get('Appointment Set (GS)', 0)
            else:
                current_quarter.in_queue = 0

            if 'In Progress' in reports[k]:
                current_quarter.in_progress = reports[k]['In Progress'] + reports[k].get('Pending QC - DEAD LEAD', 0) \
                    + reports[k].get('Pending QC - WIN', 0) + reports[k].get('Rework Required', 0)
            else:
                current_quarter.in_progress = 0
            current_quarter.tat_implemented = reports[k]['tat_implemented']
            current_quarter.tat_first_contacted = reports[k]['tat_first_contacted']
            current_quarter.start_date = start_date
            current_quarter.end_date = end_date
            current_quarter.update()
        else:
            current_quarter = LeadSummaryReports()
            current_quarter.code_type = k
            current_quarter.total_leads = reports[k]['total_leads']
            current_quarter.win = reports[k]['wins']
            current_quarter.implemented = reports[k]['Implemented']
            if 'In Queue' in reports[k]:
                current_quarter.in_queue = reports[k]['In Queue'] + reports[k].get('Appointment Set (GS)', 0)
            else:
                current_quarter.in_queue = 0

            if 'In Progress' in reports[k]:
                current_quarter.in_progress = reports[k]['In Progress'] + reports[k].get('Pending QC - DEAD LEAD', 0) \
                    + reports[k].get('Pending QC - WIN', 0) + reports[k].get('Rework Required', 0)
            else:
                current_quarter.in_progress = 0
            current_quarter.tat_implemented = reports[k]['tat_implemented']
            current_quarter.tat_first_contacted = reports[k]['tat_first_contacted']
            current_quarter.start_date = start_date
            current_quarter.end_date = end_date
            current_quarter.save()
    logging.info("Cron job done")
