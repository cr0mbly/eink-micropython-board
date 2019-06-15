from machine import Timer
from micropython import const

from app.display import StatusBar
from app.system import SystemManager


UPDATE_EVERY_SIXTY_SECONDS = const(60000)


def system_update(sys_manager: SystemManager, status_bar: StatusBar):
    """
    Queue a Task timer to trigger and redisplay app updates.
    :return:
    """

    def rerun(timer):
        sys_manager.update_system()
        status_bar.set_time(sys_manager.system_time)
        status_bar.redraw_status_bar()

    # Create virtual timer for periodic system updates.
    tim = Timer(-1)
    tim.init(
        period=UPDATE_EVERY_SIXTY_SECONDS,
        mode=Timer.PERIODIC,
        callback=rerun
    )