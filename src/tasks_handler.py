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

        config_data, valid = json_helper.load_json_from_endpoint("led_config")

        if valid:
            try:
                self.led_manager.set_mode(config_data['mode'], initializing=True)
            except KeyError:
                print("KeyError while loading mode")

            try:
                for name, time_range in config_data['time_ranges'].items():
                    new_time_range = DateRange(DateTime(0, 0, 0), DateTime(0, 0, 1))
                    new_time_range.load_from_json(time_range)
                    self.time_manager.add_time_range(new_time_range, initializing=True)
            except KeyError:
                print("KeyError while loading time_ranges")

            try:
                color_data = config_data['color']
                color_tuple = (color_data['r'], color_data['g'], color_data['b'])
                self.led_manager.set_color(color_tuple, initializing=True)
            except KeyError:
                print("KeyError while loading color")

            print("Initialized components from led_config file")
        else:
            print("Invalid config file!")

    def on_request(self, data_dict):
        """
        Gets called by the connection_handler when a get requests is incoming
        :param data_dict: The dict containing the load sector of the sent data
        :return:
        """
        task_type = data_dict['type']
        data = data_dict['data']
        print("Got request with data: {}".format(data))
        if task_type == "get_times":
            return self.time_manager.get_times_response()
        elif task_type == "get_color":
            current_color = self.led_manager.get_color()
            return json.dumps({'load': {'type': "color", 'data': current_color}})
        elif task_type == "get_mode":
            current_mode = self.led_manager.get_mode()
            return json.dumps({'load': {'type': "mode", 'data': current_mode}})
        elif task_type == "is_lighthub":
            return json.dumps({"is_lighthub": True})
        elif task_type == "set_mode":
            self.led_manager.set_mode(data['new_mode'])
            return json.dumps({"received": True})
        elif task_type == "set_color":
            color_tuple = (data['r'], data['g'], data['b'])
            self.led_manager.set_color(color_tuple)
            return json.dumps({"received": True})
        elif task_type == "add_time":
            for time in data:
                print(time)
                new_data_range = DateRange(DateTime(time['s_d'], time['s_h'], time['s_m']),
                                           DateTime(time['e_d'], time['e_h'], time['e_m']))
                self.time_manager.add_time_range(new_data_range)
            return self.time_manager.get_times_response()
        elif task_type == "remove_time":
            for time in data:
                new_data_range = DateRange(DateTime(time['s_d'], time['s_h'], time['s_m']),
                                           DateTime(time['e_d'], time['e_h'], time['e_m']))
                self.time_manager.remove_time_range(new_data_range)
            return self.time_manager.get_times_response()
        elif task_type == "clear_times":
            self.time_manager.clear_times()
            return json.dumps({"received": True})
        else:
            print("Could not find task: {}".format(task_type))
