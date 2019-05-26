from framebuf import FrameBuffer, MONO_HLSB
from machine import Pin, SPI
from micropython import const
from utime import localtime

from app.external_dependencies.epaper2in9 import EPD

SPI_ID = const(1)
NUMBER_OF_BITS = const(8)

EINK_CS = Pin(0)  # GPIO 0
EINK_DC = Pin(4)  # GPIO 4
EINK_RESET = Pin(5)  # GPIO 5
EINK_BUSY = Pin(2)  # GPIO 2

COLOUR_WHITE = const(1)
COLOUR_BLACK = const(0)

DISPLAY_WIDTH = const(128)
DISPLAY_HEIGHT = const(296)
DEFAULT_X_COORD = const(0)
DEFAULT_Y_COORD = const(0)


class EinkDisplay:

    def __init__(self):
        """
        Driver for Eink display. Provides helper functionality for displaying data.
        Assumes a hardware SPI connection on GPIO 14 (HSCLK) and GPIO 13 (HMOSI)/
        """
        self.spi = SPI(SPI_ID)

        self.frame_byte_array = bytearray(DISPLAY_WIDTH * DISPLAY_HEIGHT // NUMBER_OF_BITS)
        self.frame_buffer = FrameBuffer(
            self.frame_byte_array,
            DISPLAY_WIDTH,
            DISPLAY_HEIGHT,
            MONO_HLSB,
        )

        self.eink_display = EPD(self.spi, EINK_CS, EINK_DC, EINK_RESET, EINK_BUSY)

    def initialize_display(self):
        """
        Initializer eink display
        :return: EinkDisplay object.
        """
        self.eink_display.init()
        return self

    def clear_display(self):
        """
        Wipe current display, clearing frame memory.
        :return: None
        """
        self.eink_display.clear_frame_memory(COLOUR_WHITE)
        self.frame_buffer.fill(COLOUR_WHITE)
        self.render_window()

    def render_window(self):
        """
        Render the current state of the frame_buffer on the Display.
        """
        # Reallocate frame from buffer.
        self.eink_display.set_frame_memory(
            self.frame_byte_array,
            DEFAULT_X_COORD,
            DEFAULT_Y_COORD,
            DISPLAY_WIDTH,
            DISPLAY_HEIGHT
        )

        # Redraw view.
        self.eink_display.display_frame()


class StatusBar:
    """
    Handles allocation of space and notification on the display Status Bar.
    """

    STATUS_BAR_HEIGHT = const(15)
    NOTIFICATION_WIDTH = const(50)
    STATUS_BAR_PADDING = const(5)

    notification = 'Test String to display'  # String containing notification message.
    time_display = None  # localtime object for display.

    def __init__(self, display: EinkDisplay):
        self.display = display

    def redraw_status_bar(self):
        self.display.clear_display()
        self.display.frame_buffer.hline(5, self.STATUS_BAR_HEIGHT, DISPLAY_WIDTH - 10, COLOUR_BLACK)
        self._draw_notification()
        self.display.render_window()

    def set_notification(self, notification: str):
        """
        Sets the currently displaying notification. Wipes the previous message on repeated calls.
        :param notification: String containing the notification for display.
        :return: None
        """
        self.notification = notification

    def set_time(self, time: localtime):
        """
        Sets the currently displaying time.
        :param time: localtime object. formats time into HH:MM format for display
        :return: None
        """
        self.time_display = time

    def _draw_notification(self):
        """
        Draws as many characters of the StatusBar.notification String as possible.
        Truncates off any characters exceeding the NOTIFICATION_WIDTH
        """
        cols = self.NOTIFICATION_WIDTH // 8
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
