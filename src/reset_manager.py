import machine


class ResetManager:
    """
    Handles restarting and config reseting
    """

    def __init__(self, led_manager, TTR, reset_button):
        self._led_manager = led_manager

        self._hard_reset = False
        self._erase_reset = False

        self._reset_button = reset_button

        self._TTR = TTR
        self._reset_counter = TTR

        self._block = False

        self._silent_reset = False

    def set_hard_reset(self, hard_reset):
        """
        Sets whether a hard reset should happen in the next few cycles
        :param hard_reset:
        :return:
        """
        self._hard_reset = hard_reset

    def update(self, time):
        """
        Updates the reset based on the time
        :param time: The current time
        :return: Whether the device is currently resetting
        """
        if self._block:
            return False

        if time[1] == 4 and time[2] == 0:
            self._reset_counter = self._TTR
            self._silent_reset = True
            self.set_hard_reset(True)

        if self._reset_button.value() == 1 and self._erase_reset is False:
            self._erase_reset = True
            self._silent_reset = False
            self._led_manager.set_mode(0, True)

        if self._reset_button.value() == 0:
            self._erase_reset = False

        if self._hard_reset or self._erase_reset:
            print("Current reset counter: {}".format(self._reset_counter))
            if self._reset_counter == 1:
                if self._erase_reset:
                    print("Resetting device!")
                    with open("/configs/led_config.json", 'w') as f:
                        f.write("")
                    with open("/configs/credentials.json", 'w') as f:
                        f.write("")
                self._reset_counter -= 1
            elif self._reset_counter == 0:
                self._block = True
                machine.reset()
            else:
                self._reset_counter -= 1
                if not self._silent_reset:
                    if self._reset_counter % 2 == 0:
                        self._led_manager.set_color((100, 100, 100), True)
                    else:
                        self._led_manager.set_color((0, 0, 0), True)
            return True
        else:
            self._reset_counter = self._TTR
            return False
