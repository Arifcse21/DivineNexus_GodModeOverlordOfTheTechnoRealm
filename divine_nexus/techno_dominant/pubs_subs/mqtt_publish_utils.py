import os
import random
import time
from paho.mqtt import client as mqtt_client

class MQTTPublisher:
    def __init__(
        self,
        topic: str,
        msg_data: dict, 
    ) -> None:
        self.topic = topic
        self.msg_data = msg_data

        self.broker = os.environ.get("MQTT_BROKER")
        self.port = int(os.environ.get("MQTT_PORT"))
        self.username = os.environ.get("RABBITMQ_DEFAULT_USER")
        self.password = os.environ.get("RABBITMQ_DEFAULT_PASS")
        
        # generate client ID with pub prefix randomly
        self.client_id = f'rpi-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt_client.Client(
            callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
            client_id=self.client_id,
        )
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker, self.port)

    def on_connect(self, client, userdata, flags, reason_code, properties):

        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {reason_code} \n")

    def publish(self):
        msg_count = 0
        # while True:
            # time.sleep(1)
        msg = self.msg_data
        result = self.client.publish(self.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
        


    def run(self):
        self.client.loop_start()
        self.publish()

# # Example usage:
# if __name__ == "__main__":
#     mqtt_publisher = MQTTPublisher("test/topic", """{"data":"balchal"}""")
#     mqtt_publisher.run()
