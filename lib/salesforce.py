"""
Connect to Salesforce API
"""

from simple_salesforce import Salesforce
from datetime import datetime, timedelta
from leads.models import Timezone, Location


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
                try:
                    date_format = datetime.strptime(_date, '%Y-%m-%d')
                except Exception:
                    date_format = None
        else:
            date_format = None

        if date_format:
            tz = Timezone.objects.get(zone_name='PST')
            us_zone = Location.objects.filter(location_name__in=['United States', 'Canada'])
            if us_zone:
                location = us_zone[0]
                if location.daylight_start and location.daylight_end:
                    daylight_start = datetime(location.daylight_start.year, location.daylight_start.month, location.daylight_start.day, 0, 0, 0)
                    daylight_end = datetime(location.daylight_end.year, location.daylight_end.month, location.daylight_end.day, 23, 59, 59)
                    if datetime.utcnow() >= daylight_start and datetime.utcnow() <= daylight_end:
                        tz = Timezone.objects.get(zone_name='PDT')
                    else:
                        tz = Timezone.objects.get(zone_name='PST')

            # Convert Date to PST/PDT timezone
            date_format = SalesforceApi.convert_utc_to_timezone(date_format, tz.time_value)

        return date_format

    @staticmethod
    def get_utc_date(date, t_zone):
        time_zone = t_zone.split(':')
        hours = int(time_zone[0])
        minutes = int(time_zone[1])

        diff_in_min = (abs(hours) * 60) + minutes

        if hours < 0:
            utc_date = date + timedelta(minutes=diff_in_min)
        else:
            utc_date = date - timedelta(minutes=diff_in_min)
        return utc_date

    @staticmethod
    def convert_utc_to_timezone(date, t_zone):
        time_zone = t_zone.split(':')
        hours = int(time_zone[0])
        minutes = int(time_zone[1])

        diff_in_min = (abs(hours) * 60) + minutes

        if hours < 0:
            zone_date = date - timedelta(minutes=diff_in_min)
        else:
            zone_date = date + timedelta(minutes=diff_in_min)

        return zone_date
