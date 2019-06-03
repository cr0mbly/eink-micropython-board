from app.display import EinkDisplay, StatusBar
from app.system import SystemManager
from app.timer_tasks import system_update

sys_manager = SystemManager()

display = EinkDisplay()
status_bar = StatusBar(display)


def main():
    display.initialize_display()
    system_update()


if __name__ == '__main__':
    main()
