import network
import usocket as socket
import ujson
import ubinascii
import os
import time
from cli_master import cli_master
from subscriber import MQTTSubscriber
from predefined_constants import predefined_topics


# Define your Wi-Fi credentials
wifi_ssid = "your_ssid"
wifi_password = "strong_wifi_pass_123"

# Function to connect to Wi-Fi
def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(wifi_ssid, wifi_password)
    while not wifi.isconnected():
        pass
    print("Connected to Wi-Fi")



# Main function to handle WebSocket communication
def main():
    connect_wifi()
    topics = predefined_topics
    print(f"topics_list: {topics}")
    mqtt_subscriber = MQTTSubscriber(topics)
    mqtt_subscriber.run()
    
# Run the main function
main()


