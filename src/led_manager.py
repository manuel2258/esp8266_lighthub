from machine import Pin, Timer
from neopixel import NeoPixel
from src.time_manager import TimeManager


class LedManager:

    def __init__(self, pin_number):
        # Init the rgb strip
        pin = Pin(pin_number, Pin.OUT)
        self.neo_pixel = NeoPixel(pin, 48)

        # global variables for every mode
        self.current_color = (0, 0, 0)
        self.current_mode = 1   # 0=static, 1=timed, 2=timed_home, 3=home

        self.current_active = False
        self.last_active = False

        self.time_manager = TimeManager()

        self._clear_color()

    # Public API

    def set_new_mode(self, new_mode, kwargs):
        """
        Sets the current mode for the LED Stripe. Provide all needed values for each mode in the kwargs
        :param new_mode:
        :param kwargs:
        :return:
        """
        self.current_mode = new_mode
        if new_mode == 0:
            self._set_new_color((kwargs['r'], kwargs['g'], kwargs['b']))
            self._apply_color()
            self.time_manager.set_state(False)
        elif new_mode == 1:
            self._set_new_color((kwargs['r'], kwargs['g'], kwargs['b']))
            self.time_manager.set_times(kwargs['start_h'], kwargs['end_h'])
            self.time_manager.set_state(True)

    def update(self):
        """
        Updates the LED Stripe. Call that one every frame!
        :return:
        """
        if self.current_mode == 1:
            if self.time_manager.in_time():
                self.current_active = True
                if self.current_active is not self.last_active:
                    self._apply_color()
            else:
                self.current_active = False
                if self.current_active is not self.last_active:
                    self._clear_color()
        elif self.current_mode == 2:
            pass
        elif self.current_mode == 3:
            pass

        self.last_active = self.current_active

    # Private Helpers

    def _apply_color(self):
        """
        Updates the LED Strip with the current color
        :param rgb_tuple:
        :return:
        """
        for i in range(48):
            self.neo_pixel[i] = self.current_color
        self.neo_pixel.write()

    def _clear_color(self):
        for i in range(48):
            self.neo_pixel[i] = (0, 0, 0)
        self.neo_pixel.write()

    def _set_new_color(self, rgb_tuple):
        self.current_color = rgb_tuple
