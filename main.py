import machine
import network

from src.connection_handler import ConnectionHandler
from src.tasks_handler import TaskHandler
from src.led_manager import LedManager
from src.time_manager import TimeManager
from src.reset_manager import ResetManager
import src.json_helper as json_helper

print("\n")
print("--- LIGHTHUB SERVER V1.3 ---")

# Static defines
LED_PIN = 0
RESET_PIN = 15

# Check if the reset button is pressed
reset_button = machine.Pin(RESET_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

json_wrong_loaded = False

try:
    json_helper.load_json_from_endpoint("led_config")
    wifi_credentials, credentials_loaded = json_helper.load_json_from_endpoint("credentials")
except OSError:
    json_wrong_loaded = True

# If so erases the config files, therefor resets the device
if reset_button.value() == 1 or json_wrong_loaded:
    print("Got reset request while starting!")
    with open("/configs/led_config.json", 'w') as f:
        f.write("")
    with open("/configs/credentials.json", 'w') as f:
        f.write("")
    machine.reset()

print("Loaded wifi_credentials:", credentials_loaded)

# Initialize delegate objects
time_manager = TimeManager()
led_manager = LedManager(LED_PIN, time_manager)
reset_manager = ResetManager(led_manager, 35, reset_button)

skip_socket = False

# If could load configs then go into operation mode
if credentials_loaded:
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    sta_if.connect(wifi_credentials['name'], wifi_credentials['password'])

    connect_counter = 100000

    while not sta_if.isconnected():
        connect_counter -= 1
        if connect_counter % 1000 == 0:
            print("Connecting to wifi, cycles until reset: {}".format(connect_counter))
        if connect_counter <= 0:
            print("Could not connect to wifi, hard resetting!")
            with open("/configs/credentials.json", 'w') as f:
                f.write("")
            reset_manager.set_hard_reset(True)
            skip_socket = True
            break

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

    led_manager.set_mode(0, True)

    print("Created a new setup access point with following configs: ", ap_if.ifconfig())

task_handler = TaskHandler(led_manager, time_manager)
connection_handler = ConnectionHandler(task_handler, not credentials_loaded)

time = (0, 0, 0)

setup_flip = False

# Goes into the mainloop of updating the connection_handler and the led_manager
while True:
    if not skip_socket:
        new_reset = connection_handler.update_socket()
        reset_manager.set_hard_reset(new_reset)
        current_time = led_manager.update()
        time = current_time.get_time()
        if not credentials_loaded:
            setup_flip = not setup_flip
            if setup_flip:
                led_manager.set_color((25, 25, 25), True)
            else:
                led_manager.set_color((0, 0, 0), True)
    skip_socket = reset_manager.update(time)

