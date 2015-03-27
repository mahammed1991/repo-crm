"""
Connect to Salesforce API
"""

from simple_salesforce import Salesforce


def connect_salesforce():
    """ Connect to Salesforce """
    try:
        sf = Salesforce(username='rajuk@regalix-inc.com', password='raju@salesforce123', security_token='ZO34D4x7gHWFygngpCOu08gt', sandbox=True)
        return sf
    except Exception, e:
        print Exception, e
        return None
