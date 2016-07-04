from datetime import timedelta
import logging
import pytz
from datetime import datetime

from django.conf import settings

from reports.cron import create_or_update_picasso_leads
from lib.salesforce import SalesforceApi

# we need to use UTC as salesforce API requires this
end_date = datetime.now(pytz.UTC)
# make this as days 20 or 10 to get correct value
start_date = end_date - timedelta(minutes=10)
start_date = SalesforceApi.convert_date_to_salesforce_format(start_date)
end_date = SalesforceApi.convert_date_to_salesforce_format(end_date)
logging.info("Current Quarted Updated Leads from %s to %s" % (start_date, end_date))
logging.info("Connecting to SFDC %s" % (datetime.utcnow()))
sf = SalesforceApi.connect_salesforce()
logging.info("Connect Successfully")
select_items = settings.SFDC_FIELDS
tech_team_id = settings.TECH_TEAM_ID
code_type = 'Picasso'
where_clause_picasso = "WHERE (LastModifiedDate >= %s AND LastModifiedDate <= %s) AND LastModifiedById != '%s' " \
                       "AND Code_Type__c = '%s'" % (start_date, end_date, tech_team_id, code_type)
sql_query_picasso = "select %s from Lead %s" % (select_items, where_clause_picasso)
try:
    picasso_leads = sf.query_all(sql_query_picasso)
    logging.info("Updating PICASSO Leads count: %s " % (len(picasso_leads['records'])))
    create_or_update_picasso_leads(picasso_leads['records'], sf)
except Exception as e:
    print e