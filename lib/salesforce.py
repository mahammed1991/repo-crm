"""
Connect to Salesforce API
"""

from simple_salesforce import (Salesforce, SFType, SalesforceMoreThanOneRecord, SalesforceMalformedRequest,
                               SalesforceExpiredSession, SalesforceRefusedRequest, SalesforceResourceNotFound,
                               SalesforceGeneralError
                               )
from datetime import datetime, timedelta
from leads.models import Timezone, Location
from django.conf import settings
import json


class CustomeSalesforce(Salesforce):

    def __init__(self, **kwargs):

        return super(CustomeSalesforce, self).__init__(**kwargs)

    def __getattr__(self, name):
        """Returns an `SFType` instance for the given Salesforce object type
        (given in `name`).
        The magic part of the SalesforceAPI, this function translates
        calls such as `salesforce_api_instance.Lead.metadata()` into fully
        constituted `SFType` instances to make a nice Python API wrapper
        for the REST API.
        Arguments:
        * name -- the name of a Salesforce object type, e.g. Lead or Contact
        """
        # fix to enable serialization (https://github.com/heroku/simple-salesforce/issues/60)
        if name.startswith('__'):
            return super(Salesforce, self).__getattr__(name)

        return SalesforceType(name, self.session_id, self.sf_instance, self.sf_version, self.proxies)


class SalesforceApi(object):
    """" Salesforce API Calls """

    @staticmethod
    def connect_salesforce():
        """ Connect to Salesforce """
        if settings.SFDC == 'STAGE':
            try:
                sf = CustomeSalesforce(username='google.tech@regalix-inc.com.regalixdev',
                                       password='1q2w3e4r',
                                       security_token='oJNwpDbgjDZTaaKefk9RCQuHe', sandbox=True)
                return sf
            except Exception, e:
                print Exception, e
                return None
        else:
            try:
                sf = CustomeSalesforce(username='google.tech@regalix-inc.com', password='1q2w3e4r', security_token='t5gGSv6yxcQm99gfso28RJV9I')
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
                    return date_format
                except Exception:
                    date_format = None
        else:
            date_format = None

        if date_format:
            tz = SalesforceApi.get_current_timezone_of_salesforce()

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

    @staticmethod
    def get_current_timezone_of_salesforce():
        """ Get Current salesfore timezone """

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

        return tz

    @staticmethod
    def convert_appointment_to_timezone(appointment_date, from_time_zone, to_time_zone):
        """ Convert Appointment to IST  """

        if not appointment_date:
            return None
        try:
            tz = Timezone.objects.get(zone_name=from_time_zone)
            utc_date = SalesforceApi.get_utc_date(appointment_date, tz.time_value)
            tz_ist = Timezone.objects.get(zone_name=to_time_zone)
            appointment_in_ist = SalesforceApi.convert_utc_to_timezone(utc_date, tz_ist.time_value)
            tz = SalesforceApi.get_current_timezone_of_salesforce()
            appointment_in_ist = SalesforceApi.get_utc_date(appointment_in_ist, tz.time_value)
            appointment_in_ist = SalesforceApi.convert_date_to_salesforce_format(appointment_in_ist)
            return appointment_in_ist
        except Exception as e:
            print e
            return None


class SalesforceType(SFType):

    def update(self, record_id, data, raw_response=False):
        """Updates an SObject using a PATCH to
        `.../{object_name}/{record_id}`.
        If `raw_response` is false (the default), returns the status code
        returned by Salesforce. Otherwise, return the `requests.Response`
        object.
        Arguments:
        * record_id -- the Id of the SObject to update
        * data -- a dict of the data to update the SObject from. It will be
                  JSON-encoded before being transmitted.
        * raw_response -- a boolean indicating whether to return the response
                          directly, instead of the status code.
        """

        result = self._call_salesforce('PATCH', self.base_url + record_id,
                                       data=json.dumps(data))
        return self._raw_response(result, raw_response)

    def _call_salesforce(self, method, url, **kwargs):
        """Utility method for performing HTTP call to Salesforce.
        Returns a `requests.result` object.
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.session_id,
            'X-PrettyPrint': '1',
            "Sforce-Auto-Assign": 'FALSE'
        }
        result = self.request.request(method, url, headers=headers, **kwargs)

        if result.status_code >= 300:
            _exception_handler(result, self.name)

        return result

    def _raw_response(self, response, body_flag):
        """Utility method for processing the response and returning either the
        status code or the response object.
        Returns either an `int` or a `requests.Response` object.
        """
        if not body_flag:
            return response.status_code
        else:
            return response


def _exception_handler(result, name=""):
    """Exception router. Determines which error to raise for bad results"""
    try:
        response_content = result.json()
    except Exception:
        response_content = result.text

    exc_map = {
        300: SalesforceMoreThanOneRecord,
        400: SalesforceMalformedRequest,
        401: SalesforceExpiredSession,
        403: SalesforceRefusedRequest,
        404: SalesforceResourceNotFound,
    }
    exc_cls = exc_map.get(result.status_code, SalesforceGeneralError)

    raise exc_cls(result.url, result.status_code, name, response_content)
