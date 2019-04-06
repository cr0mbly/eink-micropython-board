from integrations import get_current_time
from wlan_connection import connect_to_network


def main():
    connect_to_network()
    get_current_time('Pacific/Auckland')


if __name__ == '__main__':
    main()
