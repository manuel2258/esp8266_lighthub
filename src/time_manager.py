from machine import Timer
import urequests
from src.date_time import DateTime
from src.helper import split_string_at_char


class TimeManager:
    """
    Manages and updates the current time and check if a given DateRange is currently active
    """

    def __init__(self):
        self.request_new_time_timer = Timer(-1)

        start_time = self._get_current_time()

        self._last_time = start_time
        self._current_time = start_time
        self._time_ranges = []
        self._is_active = False

        self._current_in_range = False

    def set_state(self, state):
        """
        Sets whether the time_manager is enabled or disable, therefor if it makes update requests
        :param state: Boolean if enabled or disabled
        :return:
        """
        self._set_timer_state(state)

    def in_time(self):
        """
        Checks whether the current
        :return:
        """
        return self._current_in_range

    def add_time_range(self, time_range):
        """
        Adds a new Time Range to the pool of checked Time Ranges
        :param time_range: TimeRange object
        :return:
        """
        print("Added a new DateRange: ", time_range)
        self._time_ranges.append(time_range)

    def remove_time_range(self, time_range):
        """
        Removes a given Time Range Object from the pool
        :param time_range: TimeRange object
        :return: True if removed, otherwise False
        """
        print("Removed a DateRange: ", time_range)
        return self._time_ranges.remove(time_range)

    def _set_timer_state(self, state):
        """
        Switches the update timer on / off
        :param state:
        :return:
        """
        if state:
            self.request_new_time_timer.init(period=60000, mode=Timer.PERIODIC, callback=self._update_time)
        else:
            self.request_new_time_timer.deinit()

    def _update_time(self, _):
        """
        Updates the current time and checks if it in range of any TimeRange objects
        :param _: Unimportant parameter needed by the Timer Callback
        :return:
        """
        self._current_time = self._get_current_time()
        for time_range in self._time_ranges:
            if time_range.in_range(self._current_time):
                self._current_in_range = True
                break
        else:
            self._current_in_range = False

        print("Got new time: ", self._current_time, " In Range: ", self._current_in_range)

    def _get_current_time(self):
        """
        Gets and parses the current time from the world time api
        :return: A DateTime objects representing the current time
        """
        response = urequests.get("http://worldtimeapi.org/api/ip")
        data = response.json()
        current_date = data["datetime"]
        _, current_date = split_string_at_char(current_date, 'T')
        current_hour, current_date = split_string_at_char(current_date, ':')
        current_minute, current_date = split_string_at_char(current_date, ':')
        current_time = DateTime(data['day_of_week'], current_hour, current_minute)
        return current_time
