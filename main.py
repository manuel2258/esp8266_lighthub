from src.connection_handler import ConnectionHandler
from src.tasks_handler import TaskHandler
from src.led_manager import LedManager
from src.time_manager import TimeManager

# Static defines
LED_PIN = 0

# Initialize delegate objects
time_manager = TimeManager()
led_manager = LedManager(LED_PIN, time_manager)
task_handler = TaskHandler(led_manager, time_manager)
connection_handler = ConnectionHandler(task_handler)

# Goes into the mainloop of updating the connection_handler and the led_manager
while True:
    connection_handler.update_socket()
    led_manager.update()

