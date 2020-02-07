from machine import Pin
from neopixel import NeoPixel

import src.json_helper as json_helper


class LedManager:
    """
    Manages the LED color and the current LED State
    """

    def __init__(self, pin_number, time_manager):
        # Init the rgb strip
        pin = Pin(pin_number, Pin.OUT)
        self._neo_pixel = NeoPixel(pin, 48)
        self._current_mode = 0   # 0=static, 1=timed
        self._current_color = (0, 0, 0)
        self._time_manager = time_manager

        self._clear_color()

    # Public API

    def set_color(self, color_tuple, initializing=False):
        """
        Sets the current color
        :param color_tuple: The to set to color tuple (r,g,b)
        :param initializing: Whether the device is currently initializing
        :return: none
        """
        self._current_color = color_tuple
        if not initializing:
            json_helper.update_json_value('led_config', ['color'],
                                          {'r': color_tuple[0], 'g': color_tuple[1], 'b': color_tuple[2]})
        if self._current_mode == 0:
            self._apply_color()

    def get_color(self):
        """
        Returns a rgb dict of the current set color
        :return: The rgb dict
        """
        return {'r': self._current_color[0], 'g': self._current_color[1], 'b': self._current_color[2]}

    def get_color_tuple(self):
        """
        Returns the current rgb color as a tuple
        :return: The rgb tuple
        """
        return self._current_color

    def set_mode(self, mode, initializing=False):
        self._current_mode = int(mode)
        if self._current_mode == 0:
            self._apply_color()
            self._time_manager.set_state(False)
        else:
            self._time_manager.set_state(True)
        if not initializing:
            json_helper.update_json_value('led_config', ['mode'], mode)
        self.update()

    def get_mode(self):
        return self._current_mode

    def update(self):
        """
        Updates the LED Stripe. Should be called regularly
        :return:
        """
        if self._current_mode == 1:
            if self._time_manager.in_time():
                self._apply_color()
            else:
                self._clear_color()
        return self._time_manager.get_current_time()

    # Private Helpers

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
