from urequests import get as http_get
from utime import localtime

from config import TIMEZONE_DB_URL, TIMEZONE_DB_API_KEY
from exceptions import FailedCurrentTimeRequestException
from utils import convert_fields_query_params


def get_current_time(timezone):
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
