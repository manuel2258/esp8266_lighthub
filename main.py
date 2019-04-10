from src.connection_handler import ConnectionHandler
from src.tasks_handler import TaskHandler
from src.led_manager import LedManager
from src.time_manager import TimeManager

import network
import json

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

with open('/configs/if_config.json') as file:
    data = json.load(file)

if_config = data['if_config']
sta_if.ifconfig((if_config['ip4'], if_config['ip4_mask'], if_config['getaway'], if_config['dns']))

wifi_credentials = data['wifi_credentials']
sta_if.connect(wifi_credentials['name'], wifi_credentials['password'])


while not sta_if.isconnected():
    pass

print("Connected to wifi")

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

