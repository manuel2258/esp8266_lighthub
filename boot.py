import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

sta_if.ifconfig(("192.168.1.115", "255.255.255.0", "192.168.1.1", "192.168.1.1"))

sta_if.connect('TP-LINK_2.4GHz_B1FADE', '91979903')

while not sta_if.isconnected():
    pass

print(sta_if.ifconfig())
