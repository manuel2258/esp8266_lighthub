from src.date_time import *


class TaskHandler:

    def __init__(self, led_manager, time_manager):
        self.led_manager = led_manager
        self.time_manager = time_manager

    def on_new_task(self, data_dict):
        task_type = data_dict['type']
        data = data_dict['data']
        if task_type == "set_color":
            color_tuple = (data['r'], data['g'], data['b'])
            self.led_manager.set_color(color_tuple)
            print("Got task to add new time: ", color_tuple)
            self.led_manager.set_mode(0)
        if task_type == "add_time":
            new_data_range = DateRange(DateTime(data['start_d'], data['start_h'], data['start_m']),
                                       DateTime(data['end_d'], data['end_h'], data['end_m']))
            print("Got task to add new time: ", new_data_range)
            self.time_manager.add_time_range(new_data_range)
            self.time_manager.set_state(True)
            self.led_manager.set_mode(1)
