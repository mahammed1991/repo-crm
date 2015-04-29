"""
Connect to Salesforce API
"""

from simple_salesforce import Salesforce
from datetime import datetime, timedelta


class SalesforceApi(object):
    """" Salesforce API Calls """

    @staticmethod
    def connect_salesforce():
        """ Connect to Salesforce """
        try:
            # sf = Salesforce(username='rajuk@regalix-inc.com', password='raju@salesforce123', security_token='ZO34D4x7gHWFygngpCOu08gt', sandbox=True)
            sf = Salesforce(username='google.tech@regalix-inc.com', password='1q2w3e4r', security_token='t5gGSv6yxcQm99gfso28RJV9I')
            return sf
        except Exception, e:
            print Exception, e
            return None

    @staticmethod
    def convert_date_to_salesforce_format(_date):
        """ Convert python datetime to standard salesforce format """
        return datetime.strftime(_date, '%Y-%m-%dT%H:%M:%S-00:00')

    @staticmethod
    def salesforce_date_to_datetime_format(_date):
        """ Get Formatted date to save in db """
        date_format = None
        if _date:
            try:
                date_format = datetime.strptime(_date[:-7], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=int(_date[-5:-3]), minutes=int(_date[-2:])) * int(_date[-6:-5] + '1')
            except Exception:
                date_format = None
        else:
            date_format = None

        return date_format
