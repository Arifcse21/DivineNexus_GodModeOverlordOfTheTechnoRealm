import network
import time

wifi_ssid = "TheGreatFlat"
wifi_password = "TheGreatFlat8"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

while not wifi.isconnected():
    time.sleep(1)

print("Connected to wifi: ", wifi.isconnected())

import mip
mip.install("uwebsocket")
