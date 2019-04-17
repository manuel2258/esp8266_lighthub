from machine import Timer

from src.date_time import DateTime, DateRange
from src.helper import split_string_at_char
from src.connection_handler import ConnectionHandler
import src.json_helper as json_helper


class TimeManager:
    """
    Manages and updates the current time and check if a given DateRange is currently active
    """

    def __init__(self):
        self.request_new_time_timer = Timer(1)

        self._time_ranges = []
        self._current_in_range = False
        self._current_state = False

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

    def add_time_range(self, time_range, initializing=False):
        """
        Adds a new Time Range to the pool of checked Time Ranges
        :param time_range: TimeRange object
        :param initializing:
        :return: True if appended, otherwise False
        """
        containing, _ = self._get_equal_time_range_from_list(time_range)
        if not containing:
            self._time_ranges.append(time_range)
            print("Added a new DateRange:", time_range)
            if not initializing:
                json_helper.update_json_value("led_config",
                                              [
                                                  "time_ranges",
                                                  time_range.get_short_name()
                                              ],
                                              time_range.get_time_dict())
        else:
            print("Could not add a new DateRange, already containing: ", time_range)
        return not containing

    def remove_time_range(self, other):
        """
        Removes a given Time Range Object from the pool
        :param other: TimeRange object
        :return: True if removed, otherwise False
        """
        containing, time_range = self._get_equal_time_range_from_list(other)
        if containing:
            self._time_ranges.remove(time_range)
            print("Removed: ", other)
        else:
            print("Could not remove item: ", other)     # TODO Add config removal
        return containing

    def get_time_ranges(self):
        """
        Returns the Time Range list
        :return:
        """
        return self._time_ranges

    def clear_times(self):
        """
        Removes every Time Range from the local list
        :return:
        """
        self._time_ranges.clear()
        json_helper.update_json_value("led_config", ["time_ranges"], {})
        print("Removed all times")

    def _get_equal_time_range_from_list(self, other):
        for time_range in self._time_ranges:
            if time_range == other:
                return True, time_range
        return False, None

    def _set_timer_state(self, state):
        """
        Switches the update timer on / off
        :param state:
        :return:
        """
        print("New time state:", state)
        if state is self._current_state:
            return
        if state:
            print("Enabled time update Timer")
            self.request_new_time_timer.init(period=60 * 1000, mode=Timer.PERIODIC, callback=self._update_time)
        else:
            self.request_new_time_timer.deinit()
        self._current_state = state

    def _update_time(self, _):
        """
        Updates the current time and checks if it in range of any TimeRange objects
        :param _: Unimportant parameter needed by the Timer Callback
        :return:
        """
        current_time = self._get_current_time()
        for time_range in self._time_ranges:
            if time_range.in_range(current_time):
                self._current_in_range = True
                break
        else:
            self._current_in_range = False

        print("Got new time:", current_time, " In Range:", self._current_in_range)

    @staticmethod
    def _get_current_time():
        """
        Gets and parses the current time from the world time api
        :return: A DateTime objects representing the current time
        """
        data = ConnectionHandler.make_get_request("http://worldtimeapi.org/api/ip")
        current_date = data["datetime"]
        _, current_date = split_string_at_char(current_date, 'T')
        current_hour, current_date = split_string_at_char(current_date, ':')
        current_minute, current_date = split_string_at_char(current_date, ':')
        current_time = DateTime(data['day_of_week'], current_hour, current_minute)
        return current_time
