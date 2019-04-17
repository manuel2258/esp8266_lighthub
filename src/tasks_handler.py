import json

from src.date_time import *
import src.json_helper as json_helper


class TaskHandler:
    """
    Executes incoming requests and initializes components
    """

    def __init__(self, led_manager, time_manager):
        self.led_manager = led_manager
        self.time_manager = time_manager

        # Initializes the time and led manager with values saved in the config file

        config_data = json_helper.load_json_from_endpoint("led_config")

        self.led_manager.set_mode(config_data['mode'], initializing=True)

        for name, time_range in config_data['time_ranges'].items():
            new_time_range = DateRange(DateTime(0, 0, 0), DateTime(0, 0, 1))
            new_time_range.load_from_json(time_range)
            self.time_manager.add_time_range(new_time_range, initializing=True)

        color_data = config_data['color']
        color_tuple = (color_data['r'], color_data['g'], color_data['b'])
        self.led_manager.set_color(color_tuple, initializing=True)

        print("Initialized components from led_config file")

    def on_new_post(self, data_dict):
        """
        Gets called by the connection_handler when a post requests is incoming
        :param data_dict: The dict containing the load sector of the sent data
        :return:
        """
        task_type = data_dict['type']
        data = data_dict['data']
        if task_type == "set_mode":
            self.led_manager.set_mode(data['new_mode'])
        if task_type == "set_color":
            color_tuple = (data['r'], data['g'], data['b'])
            self.led_manager.set_color(color_tuple)
        if task_type == "add_time":
            new_data_range = DateRange(DateTime(data['start_d'], data['start_h'], data['start_m']),
                                       DateTime(data['end_d'], data['end_h'], data['end_m']))
            self.time_manager.add_time_range(new_data_range)
        if task_type == "remove_time":
            new_data_range = DateRange(DateTime(data['start_d'], data['start_h'], data['start_m']),
                                       DateTime(data['end_d'], data['end_h'], data['end_m']))
            self.time_manager.remove_time_range(new_data_range)
        if task_type == "clear_times":
            self.time_manager.clear_times()

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
