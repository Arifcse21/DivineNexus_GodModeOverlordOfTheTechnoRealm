import os
import random
import network
from topic_director import mqtt_topic_cli
from umqtt.simple import MQTTClient
from publisher import MQTTPublisher
import time

# Define your Wi-Fi credentials
wifi_ssid = "your_ssid"
wifi_password = "strong_pass_123"


class MQTTSubscriber:
    def __init__(self, topics: list) -> None:
        self.topics = topics
        self.broker = "192.168.0.102"
        self.port = 1883
        self.username = "admin"
        self.password = "admin"

        # generate client ID with pub prefix randomly
        self.client_id = bytes(f'esp32-mqtt-{random.randint(0, 1000)}', 'utf-8')

        self.client = self.connect_mqtt()
        self.client.set_callback(self.on_message)
        self.subscribe()

    def on_connect(self, client):
        print("Connected to MQTT Broker!")

    def on_message(self, topic, msg):
        
        print(f"topic: {topic}, msg: {msg}")
        
        cli_id, cli, topic, exec_resp = mqtt_topic_cli(msg)
        print(f"topic subsciption resp: {exec_resp}")
        pub_topic = "rpi/" + topic.split("/")[1]
        print(f"topic_name to pub: {pub_topic} #######################")
        msg_data = f"{cli_id}#{exec_resp}#{pub_topic}"
        print(f"msg to publish from here: {msg_data}")
        mqtt_publisher = MQTTPublisher(pub_topic, msg_data)
        mqtt_publisher.run()

    def connect_mqtt(self) -> MQTTClient:
        client = MQTTClient(self.client_id, self.broker, self.port, self.username, self.password)
        client.connect()
        return client

    def subscribe(self):
        for topic in self.topics:
            self.client.subscribe(bytes(topic, 'utf-8'))  # Convert topic string to bytes

    def check_messages(self):
        self.client.check_msg()

    def run(self):
        while True:
            self.check_messages()
            # time.sleep(1)  # Adjust sleep time as needed




