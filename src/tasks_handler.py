from src.led_manager import LedManager


class TaskHandler:

    def __init__(self, led_manager):
        self.led_manager = led_manager

    def on_new_task(self, data_dict):
        task_type = data_dict['type']
        print("Got new data: ", data_dict)
        data = data_dict['data']
        if task_type == "set_color":
            print("Got task to set color to: ", data)
            self.led_manager.set_new_mode(0, data)
        if task_type == "set_timed_color":
            print("Got task to set new timed color to: ", data)
            self.led_manager.set_new_mode(1, data)
