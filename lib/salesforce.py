"""
Connect to Salesforce API
"""

from simple_salesforce import Salesforce


def connect_salesforce():
    """ Connect to Salesforce """

    sf = Salesforce(username='tkhan@regalix-inc.com.regalixdev', password='Regalixgoogle123', security_token='mwnt1pnuUdRrtCVx0YpgRW5p', sandbox=True)
    return sf
