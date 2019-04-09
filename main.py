from src.socket_handler import SocketHandler
from src.tasks_handler import TaskHandler
from src.led_manager import LedManager
from src.time_manager import TimeManager

# Static defines
LED_PIN = 0

# Initialize delegate objects
socket_handler = SocketHandler()
time_manager = TimeManager()
led_manager = LedManager(LED_PIN, time_manager)
task_handler = TaskHandler(led_manager, time_manager)


while True:
    ok, data = socket_handler.update_socket()
    if ok:
        task_handler.on_new_task(data['load'])
    led_manager.update()

