import os
from channels.generic.websocket import AsyncWebsocketConsumer
from techno_dominant.models import DominantCliModel
from asgiref.sync import sync_to_async
import json
import paho.mqtt.client as mqtt


class DominantConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.username_pw_set(username=os.environ.get("RABBITMQ_DEFAULT_USER"), password=os.environ.get("RABBITMQ_DEFAULT_PASS"))

        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.connect(os.environ.get("RABBITMQ_HOST"), 1883, 60)
        self.mqtt_client.loop_start()

    def on_mqtt_connect(self, client, userdata, flags, reason_code, properties):
        print("Connected to RabbitMQ with result code " + str(properties))
        self.mqtt_client.subscribe("project_dominant")

    async def on_mqtt_message(self, client, userdata, msg):
        print("MQTT Message Received: " + msg.payload.decode())
        await self.send_to_websocket(msg.payload.decode())

    async def send_to_websocket(self, message):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'command',
            'message': message
        }))

    async def connect(self):
        self.room_group_name = 'project_dominant'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print(f"text_data: {text_data}")
        content = json.loads(text_data)
        print(f"full content: {content}")
        event_type = content.get('type')

        # print(f"event_type: {event_type}")

        if event_type == 'command':

            save_stat = await self.save_message(content)
            if save_stat:
                await self.broadcast_message(save_stat=save_stat)
            else:
                await self.broadcast_message()

        elif event_type == 'execution':
            await self.execution_response(content)

    async def command(self, event):

        # Send command to WebSocket
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "data": event["data"],
        }))
    
    async def execution(self, event):

        # Send command to WebSocket
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "data": event["data"],
        }))
    
    async def broadcast_message(self, save_stat=None):
        # print(f"save_stat: {save_stat}")
        if save_stat:
            messages = await self.get_messages(cli=save_stat)
            # print(type(messages))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'command',
                    'data': messages, 
                }
            )
        else:
            # print("save_stat is None")
            messages = await self.get_messages()
            # print(messages)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'command', 
                    'data': 'Unknown command',
                    
                }
            )
    
    async def execution_response(self, event):
        print(f"execution_response: {event}")
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'execution',
        #         'data': event["data"],
        #     }
        # )

    @sync_to_async
    def get_messages(self, cli=None):
        # import pdb; pdb.set_trace()
        cli_id = cli.id if cli else 0
        result = DominantCliModel.objects.filter(id=cli_id)
        if result.exists():
            result = result.values().first()
            # print("result: ", result)
            # print(result["executed_at"])
            # result["executed_at"] = get_local_tz_ws(str(result["executed_at"]), self.scope["client"][0])
            # print(result["executed_at"])
            for key, value in result.items():
                result[key] = str(value)
            return result
        else:
            return None
        
    @sync_to_async
    def save_message(self, data):
        command = data.get('command')
        try:
            cli = DominantCliModel.objects.create(command=command)
            return cli
        except Exception as e:
            print(e)
            return False
