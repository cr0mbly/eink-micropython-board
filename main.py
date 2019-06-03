from app.display import EinkDisplay, StatusBar
from app.system import SystemManager


def main():
    sys_manager = SystemManager()
    sys_manager.update_system()

    display = EinkDisplay()
    display.initialize_display()

    status_bar = StatusBar(display)
    status_bar.set_notification('This is a test notification')
    status_bar.set_time(sys_manager.system_time)
    status_bar.redraw_status_bar()


if __name__ == '__main__':
    main()