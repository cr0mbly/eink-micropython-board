import network
import time

from config import WIFI_CONNECTIONS
from exceptions import FailedToConnectToNetworkException

NETWORK_TRYS = 5  # number of attempts of each saved network to connect before attempting a new one


def connect_to_network():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    for essid, password in WIFI_CONNECTIONS:
        sta_if.connect(essid, password)

        current_try = 0
        while current_try < NETWORK_TRYS:
            time.sleep(10)

            if sta_if.isconnected():
                break

            current_try += 1

    if not sta_if.isconnected():
        raise FailedToConnectToNetworkException('Unable to connect to any available network')
