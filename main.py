import machine
import network

from src.connection_handler import ConnectionHandler
from src.tasks_handler import TaskHandler
from src.led_manager import LedManager
from src.time_manager import TimeManager
import src.json_helper as json_helper


# Static defines
LED_PIN = 0
RESET_PIN = 15

# Check if the reset button is pressed
reset_button = machine.Pin(RESET_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# If so erases the config files, therefor resets the device
if reset_button.value() == 1:
    print("ResetMode started!")
    with open("/configs/led_config.json", 'w') as f:
        f.write("")
    with open("/configs/credentials.json", 'w') as f:
        f.write("")
    machine.reset()

# Then tried to load the stored configs
wifi_credentials, credentials_loaded = json_helper.load_json_from_endpoint("credentials")

print("Loaded wifi_credentials:", credentials_loaded)

# If could load configs then go into operation mode
if credentials_loaded:
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if.connect(wifi_credentials['name'], wifi_credentials['password'])

    while not sta_if.isconnected():
        pass

    print("Connected to wifi with following configs: ", sta_if.ifconfig())
# Otherwise go into setup mode
else:
    import ubinascii

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    ap_if.config(essid="epsLightServer_{}".format(mac[:5]))
    ap_if.config(authmode=network.AUTH_OPEN)
    
    print("Created a new setup access point with following configs: ", ap_if.ifconfig())


# Initialize delegate objects
time_manager = TimeManager()
led_manager = LedManager(LED_PIN, time_manager)
task_handler = TaskHandler(led_manager, time_manager)
connection_handler = ConnectionHandler(task_handler, not credentials_loaded)

reset = False

# Goes into the mainloop of updating the connection_handler and the led_manager
while True:
    if reset:
        machine.reset()
    reset = connection_handler.update_socket()
    led_manager.update()

