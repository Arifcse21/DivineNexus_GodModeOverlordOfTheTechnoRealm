import os
import random
import time
from umqtt.simple import MQTTClient


class MQTTPublisher:
    def __init__(
        self,
        topic: str,
        msg_data: str,
    ) -> None:
        self.topic = topic
        self.msg_data = msg_data

        self.broker = "192.168.0.102"
        self.port = 1883
        self.username = "admin"
        self.password = "admin"
        
        # generate client ID with pub prefix randomly
        self.client_id = f'rpi-mqtt-{random.randint(0, 1000)}'
        self.client = MQTTClient(
            client_id=self.client_id,
            server=self.broker,
            user=self.username,
            password=self.password
        )

    def on_connect(self, client):
        print("Connected to MQTT Broker!")

    def publish(self):
        self.client.connect()
        print("going to publish: ", self.topic, " ", self.msg_data)
        self.client.publish(self.topic, self.msg_data)
        self.client.disconnect()

    def run(self):
        self.publish()

# Example usage:
#if __name__ == "__main__":
#    topic = b"test/topic"  # Convert to bytes
#    msg_data = b'{"data":"balchal"}'  # Convert to bytes
#    mqtt_publisher = MQTTPublisher(topic, msg_data)
#    mqtt_publisher.run()


