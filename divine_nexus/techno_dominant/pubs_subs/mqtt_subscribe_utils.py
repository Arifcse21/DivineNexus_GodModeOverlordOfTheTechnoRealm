import os
import random
from paho.mqtt import client as mqtt_client
from techno_dominant.models.dominant_cli_models import DominantCliModel

class MQTTSubscriber:
    def __init__(
        self,
        topics: list,

    ) -> None:
        self.topics = topics

        self.broker = os.environ.get("MQTT_BROKER")
        self.port = int(os.environ.get("MQTT_PORT"))
        self.username = os.environ.get("RABBITMQ_DEFAULT_USER")
        self.password = os.environ.get("RABBITMQ_DEFAULT_PASS")

        # generate client ID with pub prefix randomly
        self.client_id = f'rpi-mqtt-{random.randint(0, 1000)}'

        self.client = self.connect_mqtt()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("\n >>>>>> Subscriber loop connected to MQTT Broker! <<<<<< \n ")
        else:
            print(f"Failed to connect, return code {reason_code}")

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic with QoS `{msg.qos}`, userdata `{userdata}`")
        cli_id = msg.payload.decode().split("#")[0]
        exec_resp = msg.payload.decode().split("#")[1]
        print(f"cli_id: {cli_id}")
        print(f"exec_resp: {exec_resp}")
        query = DominantCliModel.objects.filter(id=cli_id)
        if query.exists():
            query.update(
                sub_topic=msg.topic,
                exec_response=exec_resp
            )
        else:
            print(f"cli_id: {cli_id} not found")

        
    def connect_mqtt(self) -> mqtt_client:
        client = mqtt_client.Client(
            callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
            client_id=self.client_id
        )
        client.username_pw_set(self.username, self.password)
        client.connect(self.broker, self.port)
        return client

    def subscribe(self):
        for topic in self.topics:
            self.client.subscribe(topic)

    def run(self):
        self.subscribe()
        self.client.loop_forever()

# Example usage:

# topics_to_sub_list = [
#     "rpi/led_on",
#     "rpi/led_off",
#     "rpi/board_temperature",
#     "rpi/command4",
#     "rpi/command5",
#     "rpi/command6",
#     "rpi/command7",
#     "rpi/command8",
#     "rpi/command9",
#     "rpi/command10",
#     "rpi/command11",
#     "rpi/command12",
# ]
# mqtt_subscriber = MQTTSubscriber(topics_to_sub_list)
# mqtt_subscriber.run()
