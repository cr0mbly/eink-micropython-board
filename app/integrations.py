from urequests import get as http_get
from utime import localtime

from config import TIMEZONE_DB_URL, TIMEZONE_DB_API_KEY
from exceptions import FailedCurrentTimeRequestException


def get_current_time(timezone: str):
    """
    :param timezone: plain text name of timezone e.g. `Pacific/Auckland`
    :return: datetime object with current time
    """
    settings = {'key': TIMEZONE_DB_API_KEY, 'format': 'json', 'fields': 'timestamp', 'zone': timezone}
    path_url = convert_fields_query_params('/v2.1/list-time-zone', settings)
    response_json = http_get(TIMEZONE_DB_URL + path_url).json()

    if response_json['status'] != 'OK':
        raise FailedCurrentTimeRequestException()

    timestamp = response_json['zones'][0]['timestamp']
    return localtime(timestamp)


def convert_fields_query_params(path: str, query_parameters: dict):
    """
    :param path: path of the current url
    :param query_parameters: dict containing query keys and values
    :return: built query url
    """
    return path + '?' + '&'.join('%s=%s' % (key, value) for key, value in query_parameters.items())
