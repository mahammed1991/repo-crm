from datetime import datetime
import MySQLdb as db
from simple_salesforce import Salesforce
import sys
import pytz

'''
    This script is written to update the picasso count in portal db.
'''


def convert_date_to_salesforce_format(_date):
    """ Convert python datetime to standard salesforce format """
    return datetime.strftime(_date, '%Y-%m-%dT%H:%M:%S-00:00')

# Bolt and Picasso
def get_all_picasso_leads():
    limit = 2000
    index = 1
    total_records = 0
    is_prod = False
    created_date = None
    end_date = datetime.now(pytz.UTC)  # end date in utc today
    end_date = convert_date_to_salesforce_format(end_date)
    lead_type = []
    """ Get all Picasso Bolt and Picasso Bolt Leads from SFDC """
    print "Connecting to SFDC...  \nStarted Time : %s" % (datetime.utcnow())
    if len(sys.argv) > 1:
        if sys.argv[1] == 'prod':
            is_prod = True
        else:
            print "Argument should be 'prod' for production, leave blank for staging and local"
            exit()
    sfdc_conn = sfdc_connection(is_prod)
    print "Connected! \nProcess started..."
    while True:

        if index == 1:
            sql_query_all_leads = "select Id, Code_Type__c, Picasso_Lead_Stage__c, CreatedDate  from Lead WHERE " \
                                  "(CreatedDate >= 2016-06-30T00:00:00-00:00 AND CreatedDate <= %s) " \
                                  "AND (Code_Type__c = 'Picasso' OR Code_Type__c = 'BOLT')  " \
                                  "ORDER BY CreatedDate LIMIT %s" % (end_date, limit)
        else:
            sql_query_all_leads = "select Id, Code_Type__c, Picasso_Lead_Stage__c, CreatedDate from Lead WHERE " \
                                  "(CreatedDate > %s AND CreatedDate <= %s) " \
                                  "AND (Code_Type__c = 'Picasso' OR Code_Type__c = 'BOLT')" \
                                  "ORDER BY CreatedDate LIMIT %s" % (created_date, end_date, limit)
        try:
            all_leads = sfdc_conn.query_all(sql_query_all_leads)
            #conn = db_connection()
            #cursor = conn.cursor()
            leads = all_leads['records']
            count = 0
            uiux_inqueue = 0
            bolt_inqueue = 0
            for lead in leads:
                created_date = lead.get('CreatedDate')
                lead_status = lead.get('Picasso_Lead_Stage__c')
                if lead_status not in ['Issue Case', 'Delivered', 'Unsupported Language']:
                    code_type = lead.get('Code_Type__c')
                    if code_type == 'Picasso':
                        uiux_inqueue += 1
                    else:
                        bolt_inqueue += 1


                    lead_type.append(lead.get('Code_Type__c'))
                if not lead_status:
                    lead_status = ""


                sql = "UPDATE leads_picassoleads SET lead_status = '"+lead_status+"' WHERE sf_lead_id = '"+lead.get('Id') + "';"
                #cursor.execute(sql)
                print sql
            records = len(leads)
            index += 1
            total_records += records
            if records < 2000:
                break
            total_records += records
        except Exception as e:
            print "Failed to get leads from SFDC"
            print "%s" % (e)
    print "Code Types : %s " % list(set(lead_type))
    print "Total Leads count: %s " % total_records
    print "UIUX Inqueue : %s " % uiux_inqueue
    print "Bolt Inqueue : %s " % bolt_inqueue
    print "Process completed... \nDisconecting from SFDC... \nEnding Time : %s" % (datetime.utcnow())


def db_connection():
    return db.connect(host="localhost", user="root", db="gtrack")


def sfdc_connection(is_prod):
    if is_prod:
        sfdc_conn = Salesforce(username='google.tech@regalix-inc.com',
                               password='portalsupport12345',
                               security_token='enfTcpWGlwx6ObKwksx3Bt9I')
    else:
        sfdc_conn = Salesforce(username='google.tech@regalix-inc.com.regalixdev',
                               password='portalsupport1234',
                               security_token='bZPoCobHAJQsdPFcjjDfEWHA2', sandbox=True)
    return sfdc_conn


get_all_picasso_leads()
