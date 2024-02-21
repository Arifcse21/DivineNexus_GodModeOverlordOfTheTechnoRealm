from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from techno_dominant.models import DominantCliModel
from datetime import datetime


class DominantConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_name = "domination"
        self.room_group_name = f'project_dominant'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        messages =  await self.get_messages()
        print(f"received messages: {messages}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'command',
                'message': messages
            }
        )

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # print(f"text_data: {text_data}")
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        print(f"message_type: {message_type}")

        if message_type == 'message':
            print("here i am ")
            save_stat = await self.save_message(text_data_json)
            if save_stat:
                await self.broadcast_message(save_stat=save_stat)
            else:
                await self.broadcast_message(save_stat=False)

    async def command(self, event):
        command = event['command']

        # Send command to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'command': command,
        }))

    async def broadcast_message(self, save_stat):
        print(f"save_stat: {save_stat}")
        if save_stat:
            messages =  await self.get_messages()
            print(type(messages))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'command',
                    'message': messages
                }
            )
        else:
            print("save_stat is False")
            messages =  await self.get_messages()
            print(messages, "False")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'command',
                    'message': {"messages":  "not saved"}
                }
            )
    
    @sync_to_async
    def get_messages(self):
        # try:
            result = list(DominantCliModel.objects.all().values())
            # print(f"result: {result}")
            if result:
                for r in result:
                    for key, value in r.items():
                        r[key] = str(value)
                        # if isinstance(value, datetime):
                        #     # print(key, value)
                        #     r[key] = str(value)         # value.strftime('%Y-%m-%d %H:%M:%S')

                # print(f"results: {result}")
                return result
            
        # except DominantCliModel.DoesNotExist:
        #     return None
        
    @sync_to_async
    def save_message(self, data):
        command_name = data.get('command_name')
        try:
            DominantCliModel.objects.create(command_name=command_name)
            return True
        except:
            return False