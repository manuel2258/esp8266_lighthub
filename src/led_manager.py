from machine import Pin, Timer
from neopixel import NeoPixel


class LedManager:
    """
    Manages the LED color and the current LED State
    """

    def __init__(self, pin_number, time_manager):
        # Init the rgb strip
        pin = Pin(pin_number, Pin.OUT)
        self._neo_pixel = NeoPixel(pin, 48)

        self._current_mode = 1   # 0=static, 1=timed, 2=timed_home, 3=home

        self._current_color = (0, 0, 0)

        self._time_manager = time_manager

        self._clear_color()

    # Public API

    def set_color(self, color_tuple):
        """
        Sets the current mode for the LED Stripe. Provide all needed values for each mode in the kwargs
        :param color_tuple:
        :return:
        """
        self._current_color = color_tuple

    def set_mode(self, mode):
        self._current_mode = mode
        if self._current_mode == 0:
            self._apply_color()

    def update(self):
        """
        Updates the LED Stripe. Call that one every frame!
        :return:
        """
        if self._current_mode == 1:
            if self._time_manager.in_time():
                self._apply_color()
            else:
                self._clear_color()
        elif self._current_mode == 2:
            pass
        elif self._current_mode == 3:
            pass

    def _apply_color(self):
        """
        Updates the LED Strip with the current color
        :return:
        """
        for i in range(48):
            self._neo_pixel[i] = self._current_color
        self._neo_pixel.write()

    def _clear_color(self):
        """
        Disables every LED
        :return:
        """
        for i in range(48):
            self._neo_pixel[i] = (0, 0, 0)
        self._neo_pixel.write()
