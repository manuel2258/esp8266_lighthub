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
