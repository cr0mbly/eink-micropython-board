from framebuf import FrameBuffer, MONO_HLSB
from machine import Pin, SPI
from micropython import const

from app.external_dependencies.epaper2in9 import EPD

SPI_ID = const(1)
NUMBER_OF_BITS = const(8)

EINK_CS = Pin(0)
EINK_DC = Pin(4)
EINK_RESET = Pin(5)
EINK_BUSY = Pin(2)

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
        """
        self.spi = SPI(SPI_ID)

        self.frame_byte_array = bytearray(DISPLAY_WIDTH * DISPLAY_HEIGHT // NUMBER_OF_BITS)
        self.frame_buffer = FrameBuffer(self.frame_byte_array, DISPLAY_WIDTH, DISPLAY_HEIGHT, MONO_HLSB)

        self.eink_display = EPD(self.spi, EINK_CS, EINK_DC, EINK_RESET, EINK_BUSY)

    def initialize_display(self):
        self.eink_display.init()

    def render_window(self, start_x_coord, start_y_coord, end_x_coord, end_y_coord):
        self.frame_buffer.fill(COLOUR_WHITE)

        self.frame_buffer.rect(start_x_coord, start_y_coord, end_x_coord, end_y_coord, COLOUR_BLACK)

        self.eink_display.set_frame_memory(
            self.frame_byte_array,
            DEFAULT_X_COORD,
            DEFAULT_Y_COORD,
            DISPLAY_WIDTH,
            DISPLAY_HEIGHT
        )
        self.eink_display.display_frame()
