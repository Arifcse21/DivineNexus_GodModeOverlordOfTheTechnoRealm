import os
from channels.generic.websocket import AsyncWebsocketConsumer
from techno_dominant.models import DominantCliModel
from asgiref.sync import sync_to_async
import json
import paho.mqtt.client as mqtt


class DominantConsumer(AsyncWebsocketConsumer):
    
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


    async def command(self, event):

        # Send command to WebSocket
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "data": event["data"],
        }))
    
    async def pub_topic(self, event):
        print(self)
        # Send command to WebSocket
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "data": event["data"],
        }))

    
    async def broadcast_message(self, save_stat=None):
        # print(f"save_stat: {save_stat}")
        if save_stat:
            pub_topic = await self.get_pub_topic(cli=save_stat)
            # print(type(pub_topic))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'pub_topic',
                    'data': pub_topic, 
                }
            )
        else:
            # print("save_stat is None")
            messages = await self.get_pub_topic()
            # print(messages)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'command', 
                    'data': 'Unknown command',
                    
                }
            )

    @sync_to_async
    def get_pub_topic(self, cli=None):
        # import pdb; pdb.set_trace()
        cli_id = cli.id if cli else 0
        result = DominantCliModel.objects.filter(id=cli_id)
        if result.exists():
            result = result.first()
            return str(result.pub_topic)
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
        
    async def broadcast_from_api(self, data):
       await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'pub_topic',
                    'data': data, 
                }
            )