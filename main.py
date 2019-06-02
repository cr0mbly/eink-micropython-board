from app.display import EinkDisplay, StatusBar
from app.wlan_connection import connect_to_network
from app.integrations import get_current_time
from app.exceptions import (
    FailedToConnectToNetworkException,
    FailedCurrentTimeRequestException,
)


def main():
    display = EinkDisplay()
    display.initialize_display()

    status_bar = StatusBar(display)

    try:
        wlan_connection = connect_to_network()
    except FailedToConnectToNetworkException:
        wlan_connection = None

    local_time = None
    if wlan_connection.isconnected():
        try:
            local_time = get_current_time('Pacific/Auckland')
        except FailedCurrentTimeRequestException:
            pass

    status_bar.set_notification('This is a test notification')
    status_bar.set_time(local_time)
    status_bar.redraw_status_bar()


if __name__ == '__main__':
    main()
