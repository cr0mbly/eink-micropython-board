from framebuf import FrameBuffer, MONO_HLSB
from machine import Pin, SPI
from micropython import const
from utime import localtime

from app.external_dependencies.epaper2in9 import EPD, EPD_WIDTH, EPD_HEIGHT
from app.system import system_manager

SPI_ID = const(1)
NUMBER_OF_BITS = const(8)

EINK_CS = Pin(0)  # GPIO 0
EINK_BUSY = Pin(2)  # GPIO 2
EINK_DC = Pin(4)  # GPIO 4
EINK_RESET = Pin(5)  # GPIO 5

COLOUR_WHITE = const(1)
COLOUR_BLACK = const(0)

DEFAULT_X_COORD = const(0)
DEFAULT_Y_COORD = const(0)


class EinkDisplay:

    def __init__(self):
        """
        Driver for Eink display. Provides helper functionality for displaying data.
        Assumes a hardware SPI connection on GPIO 14 (HSCLK) and GPIO 13 (HMOSI)/
        """
        self.spi = SPI(SPI_ID)
        self.frame_byte_array = bytearray(EPD_WIDTH * EPD_HEIGHT // NUMBER_OF_BITS)

        self.frame_buffer = FrameBuffer(
            self.frame_byte_array,
            EPD_WIDTH,
            EPD_HEIGHT,
            MONO_HLSB,
        )

        self.driver = EPD(self.spi, EINK_CS, EINK_DC, EINK_RESET, EINK_BUSY)

    def initialize_display(self):
        """
        Initializer eink display
        :return: EinkDisplay object.
        """
        self.driver.init()

    def clear_display(self):
        """
        Wipe current display, clearing frame memory.
        :return: None
        """
        self.driver.clear_frame_memory(COLOUR_WHITE)

    def render_window(self):
        """
        Render the current state of the frame_buffer on the Display.
        """
        # Reallocate frame from buffer.
        self.driver.set_frame_memory(
            self.frame_byte_array,
            DEFAULT_X_COORD,
            DEFAULT_Y_COORD,
            EPD_WIDTH,
            EPD_HEIGHT,
        )

        # Redraw view.
        self.driver.display_frame()


class StatusBar:
    """
    Handles allocation of space and notification on the display Status Bar.
    """

    # Style formatting for StatusBar.
    STATUS_BAR_HEIGHT = const(15)
    STATUS_BAR_PADDING = const(5)
    STATUS_BAR_TIME_SPACER = const(85)
    NOTIFICATION_WIDTH = const(85)

    notification = ''  # String containing notification message.
    time_display = '--:--'  # localtime object for display.

    def __init__(self, display: EinkDisplay):
        self.display = display

    def clear_status_bar(self):
        """
        Clear the framebuffer of any data. useful when redrawing the status bar.
        :return: None
        """
        self.display.frame_buffer.fill_rect(
            DEFAULT_X_COORD,
            DEFAULT_Y_COORD,
            EPD_WIDTH,
            self.STATUS_BAR_HEIGHT + self.STATUS_BAR_PADDING,
            COLOUR_WHITE
        )

    def redraw_status_bar(self):
        self.clear_status_bar()
        self.draw_notification()
        self.draw_time()
        self.display.render_window()

    def set_notification(self, notification: str):
        """
        Sets the currently displaying notification. Wipes the previous message on repeated calls.
        :param notification: String containing the notification for display.
        :return: None
        """
        self.notification = notification

    def draw_notification(self):
        """
        Draws as many characters of the StatusBar.notification String as possible.
        Truncates off any characters exceeding the NOTIFICATION_WIDTH
        """

        self.display.frame_buffer.hline(
            self.STATUS_BAR_PADDING,
            self.STATUS_BAR_HEIGHT,
            EPD_WIDTH - self.STATUS_BAR_PADDING * 2,
            COLOUR_BLACK
        )

        cols = self.NOTIFICATION_WIDTH // NUMBER_OF_BITS
        character_count = 0
        row_height = self.STATUS_BAR_HEIGHT - self.STATUS_BAR_PADDING * 2
        for i in range(0, len(self.notification), cols):
            self.display.frame_buffer.text(
                self.notification[i:i + cols],
                self.STATUS_BAR_PADDING,
                self.STATUS_BAR_PADDING + character_count,
                COLOUR_BLACK
            )

            character_count += 8

            # Stop drawing once character length has been exceeded.
            if character_count >= row_height:
                break

    def set_time(self, current_time: localtime):
        """
        Sets the currently displaying time.
        :param current_time: localtime object. formats time into HH:MM format for display
        :return: None
        """

        if current_time:
            self.time_display = '{4}:{5}'.format(*current_time)
        else:
            self.time_display = const('--:--')

    def draw_time(self):
        self.display.frame_buffer.text(
            self.time_display,
            self.STATUS_BAR_TIME_SPACER,
            self.STATUS_BAR_PADDING,
            COLOUR_BLACK
        )


class AppDrawer:
    # Style formatting for AppDrawer.
    APP_DRAWER_SPACER = const(20)
    ITEM_HEIGHT = const(50)
    TEXT_SPACER = const(6)

    def __init__(self, display: EinkDisplay):
        self.display = display
        self.app_drawer_width = display.driver.width
        self.app_drawer_height = display.driver.height
        self.selected_app = const(0)

    def redraw_app_drawer(self):
        self.clear_drawer()
        self.load_apps_for_display()
        self.display.render_window()

    def clear_drawer(self):
        """
        Clear the app drawer of any content.
        """
        self.display.frame_buffer.fill_rect(
            DEFAULT_X_COORD,
            DEFAULT_Y_COORD + self.APP_DRAWER_SPACER,
            self.app_drawer_width,
            self.app_drawer_height,
            COLOUR_WHITE
        )

    def load_apps_for_display(self):
        """
        Pull in all installs apps and displays the UI drawer for selection
        """
        apps = system_manager.load_apps()
        for app_position, current_app in enumerate(apps):
            self._draw_app_selector_box(
                current_app['app_name'],
                app_position,
                is_selected=app_position == self.selected_app
            )

    def select_app(self, app_position: int):
        self.selected_app = app_position
        self.redraw_app_drawer()

    def _draw_app_selector_box(self, app_name: str, app_position: int, is_selected=False):
        """
        Taking a selected app draw it's place on the app drawer.
        """
        box_parameters = [
            DEFAULT_X_COORD,
            DEFAULT_Y_COORD + self.APP_DRAWER_SPACER + app_position * self.APP_DRAWER_SPACER,
            self.app_drawer_width,
            self.APP_DRAWER_SPACER,
            COLOUR_BLACK,
        ]

        if is_selected:
            self.display.frame_buffer.fill_rect(*box_parameters)
        else:
            self.display.frame_buffer.rect(*box_parameters)

        self.display.frame_buffer.text(
            app_name,
            DEFAULT_X_COORD + self.TEXT_SPACER,
            DEFAULT_Y_COORD + self.APP_DRAWER_SPACER + app_position * self.APP_DRAWER_SPACER + self.TEXT_SPACER,
            COLOUR_WHITE if is_selected else COLOUR_BLACK,
        )
