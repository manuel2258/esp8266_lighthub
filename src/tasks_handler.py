import json

from src.date_time import *


class TaskHandler:
    """
    Executes incoming requests
    """

    def __init__(self, led_manager, time_manager):
        self.led_manager = led_manager
        self.time_manager = time_manager

    def on_new_post(self, data_dict):
        """
        Gets called by the connection_handler when a post requests is incoming
        :param data_dict: The dict containing the load sector of the sent data
        :return:
        """
        task_type = data_dict['type']
        data = data_dict['data']
        if task_type == "set_color":
            color_tuple = (data['r'], data['g'], data['b'])
            self.led_manager.set_color(color_tuple)
            # print("Got task to set a new color: ", color_tuple)
            self.led_manager.set_mode(0)
        if task_type == "add_time":
            new_data_range = DateRange(DateTime(data['start_d'], data['start_h'], data['start_m']),
                                       DateTime(data['end_d'], data['end_h'], data['end_m']))
            # print("Got task to add new time: ", new_data_range)
            self.time_manager.add_time_range(new_data_range)
            self.time_manager.set_state(True)
            self.led_manager.set_mode(1)
        if task_type == "remove_time":
            new_data_range = DateRange(DateTime(data['start_d'], data['start_h'], data['start_m']),
                                       DateTime(data['end_d'], data['end_h'], data['end_m']))
            # print("Got task to remove the time: ", new_data_range)
            self.time_manager.remove_time_range(new_data_range)
        if task_type == "clear_times":
            self.time_manager.clear()

    def on_get_request(self, data_dict):
        """
        Gets called by the connection_handler when a get requests is incoming
        :param data_dict: The dict containing the load sector of the sent data
        :return:
        """
        task_type = data_dict['type']
        data = data_dict['data']
        if task_type == "get_time":
            data_body = {'load': {'type': "time_ranges", 'data': []}}
            time_ranges = self.time_manager.get_time_ranges()
            for time_range in time_ranges:
                data_body['load']['data'].append(time_range.get_time_dict())
            return json.dumps(data_body)
