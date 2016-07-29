from datetime import datetime
import MySQLdb as db
from simple_salesforce import Salesforce
import sys

'''
    This script is written to update the build eligible status in portal db. Since we
    were not storing build eligible status we are now getting it from SFDC and updating it.
'''


def get_all_picasso_leads():
    limit = 2000
    index = 1
    total_records = 0
    created_date = None
    is_prod = False
    """ Get all WPP Leads from SFDC """
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
        print "Fetching records...."
        if index == 1 and not created_date:
            sql_query_all_leads = "select Id, Code_Type__c, PICASSO_build_eligible__c, CreatedDate from Lead WHERE " \
                                  "Code_Type__c='WPP' OR Code_Type__c='WPP - Nomination' " \
                                  "ORDER BY CreatedDate LIMIT %s" % (limit)
        else:
            sql_query_all_leads = "select Id, Code_Type__c, PICASSO_build_eligible__c, CreatedDate from Lead WHERE " \
                                  "(Code_Type__c='WPP' OR Code_Type__c='WPP - Nomination') " \
                                  "AND createdDate > '%s' ORDER BY CreatedDate LIMIT %s" % (created_date, limit)
        try:
            all_leads = sfdc_conn.query_all(sql_query_all_leads)
            #conn = db_connection()
            #cursor = conn.cursor()
            lead_records = all_leads['records']
            print len(lead_records)
            for lead in lead_records:
                created_date = lead.get('CreatedDate')
                print
                if lead.get('PICASSO_build_eligible__c') is None:
                    lead['PICASSO_build_eligible__c'] = ''
                try:
                    sql = "UPDATE leads_wppleads SET is_build_eligible = '"+lead.get('PICASSO_build_eligible__c')+"' WHERE " \
                          "sf_lead_id = '"+lead.get('Id') + "';"
                    #cursor.execute(sql)
                    print sql
                except Exception as e:
                    print "Error %s" % (e)
            records = len(lead_records)
            if records < 2000:
                break
            else:
                index += 1
            total_records += records
        except Exception as e:
            print e
            print "Failed to get leads from SFDC"
            print "%s" % (e)

    print "Total Leads count: %s " % total_records
    print "Process completed... \nDisconecting from SFDC... \nEnding Time : %s" % (datetime.utcnow())


def db_connection():
    return db.connect(host= "localhost", user = "root", db = "gtrack")


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
