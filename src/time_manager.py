from machine import Timer
import urequests

class TimeManager:

    def __init__(self):
        # Timed LEDs
        self.request_new_time_timer = Timer(-1)

        start_time = self._get_current_time()

        self._last_time = start_time
        self._current_time = start_time
        self._start_time = 0
        self._end_time = 0
        self._is_active = False

    def set_state(self, state):
        self._set_timer_state(state)

    def in_time(self):
        if self._start_time <= self._current_time < self._end_time:
            if not self._is_active:
                self._is_active = True
            return True
        if self._is_active:
            self._is_active = False
            self._current_time -= 24
        return False

    def set_times(self, start_time, end_time):
        self._start_time = start_time
        self._end_time = end_time

    def _set_timer_state(self, state):
        if state:
            self.request_new_time_timer.init(period=60000, mode=Timer.PERIODIC, callback=self._update_time)
            self._update_time(0)
        else:
            self.request_new_time_timer.deinit()

    def _update_time(self, _):
        current_hour = self._get_current_time()
        if current_hour != self._last_time:
            self._current_time += 1
        print("Got new time: {} -> [{}-{}] == {}".format(self._current_time,
                                                         self._start_time,
                                                         self._end_time,
                                                         self.in_time()))

    def _get_current_time(self):
        """
        Gets the current time from the worldtimeapi
        :return:
        """
        response = urequests.get("http://worldtimeapi.org/api/ip")
        data = response.json()
        current_date = data["datetime"]
        _, current_date = self._split_string_at_char(current_date, 'T')
        current_hour, current_date = self._split_string_at_char(current_date, ':')
        return int(current_hour)


    @staticmethod
    def _split_string_at_char(string, char):
        index = string.find(char)
        return string[:index], string[index+1:]
