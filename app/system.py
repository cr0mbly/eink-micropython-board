import ujson
from machine import RTC
from ntptime import settime

from app.wlan_connection import connect_to_network
from app.exceptions import (
    FailedToConnectToNetworkException,
    FailedCurrentTimeRequestException,
)


class SystemManager:
    """
    Manager to store and update state of the system.
    """

    wifi_connection = None
    system_time = None
    apps = None

    def update_system(self):
        """
        High level task to retrigger checks to keep system up to date.
        checks wifi connection, establishes system time etc.
        :return: None
        """
        self._check_connection()
        self._update_system_time()

    def _check_connection(self):
        """
        Attempt to connect and reconnect a wifi connection on nonexistence/ connection failure.
        :return: None
        """
        if not self.wifi_connection or not self.wifi_connection.isconnected():
            try:
                self.wlan_connection = connect_to_network()
            except FailedToConnectToNetworkException:
                self.wlan_connection = None

    def _update_system_time(self):
        """
        Pull down the latest NTP backed time and caches it locally.
        :return: None
        """
        try:
            settime()
        except FailedCurrentTimeRequestException:
            pass

        self.system_time = RTC().datetime()

    def load_apps(self):
        """
        Load the mapping of apps from system settings. stores result in
        SystemManager.apps for general use.
        :return: registered apps in app_name: app format
        """
        with open('./app_mapping.json') as f:
            self.apps = ujson.loads(f.read())

        return self.apps
