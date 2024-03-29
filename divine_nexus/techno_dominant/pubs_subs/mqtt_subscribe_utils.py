import os
import random
from paho.mqtt import client as mqtt_client

class MQTTSubscriber:
    def __init__(
        self,
        topic: str,

    ) -> None:
        self.topic = topic

        self.broker = os.environ.get("MQTT_BROKER")
        self.port = int(os.environ.get("MQTT_PORT"))
        self.username = os.environ.get("RABBITMQ_DEFAULT_USER")
        self.password = os.environ.get("RABBITMQ_DEFAULT_PASS")

        # generate client ID with pub prefix randomly
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

        self.client = self.connect_mqtt()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {reason_code}")

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic with QoS `{msg.qos}`, userdata `{userdata}`, client `{client}`")

    def connect_mqtt(self) -> mqtt_client:
        client = mqtt_client.Client(
            callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
            client_id=self.client_id
        )
        client.username_pw_set(self.username, self.password)
        client.connect(self.broker, self.port)
        return client

    def subscribe(self):
        self.client.subscribe(self.topic)

    def run(self):
        self.subscribe()
        self.client.loop_forever()

# # Example usage:
# if __name__ == '__main__':
#     mqtt_subscriber = MQTTSubscriber("rpi/led_on")
#     mqtt_subscriber.run()
