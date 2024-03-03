from channels.generic.websocket import AsyncJsonWebsocketConsumer
from techno_dominant.models import DominantCliModel
from asgiref.sync import sync_to_async
# from techno_dominant.utils.local_timezone_convert_util import get_local_tz_ws


class DominantConsumer(AsyncJsonWebsocketConsumer):
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

    async def receive_json(self, content):
        message_type = content.get('type')

        print(f"message_type: {message_type}")

        if message_type == 'message':

            save_stat = await self.save_message(content)
            if save_stat:
                await self.broadcast_message(save_stat=save_stat)
            else:
                await self.broadcast_message()

    async def command(self, event):

        # Send command to WebSocket
        await self.send_json({
            "type": event["type"],
            "data": event["data"],

        })

    async def broadcast_message(self, save_stat=None):
        print(f"save_stat: {save_stat}")
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
            print("save_stat is None")
            messages = await self.get_messages()
            print(messages)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'command', 
                    'data': 'Unknown command',
                    
                }
            )
    
    @sync_to_async
    def get_messages(self, cli=None):
        # import pdb; pdb.set_trace()
        cli_id = cli.id if cli else 0
        result = DominantCliModel.objects.filter(id=cli_id)
        if result.exists():
            result = result.values().first()
            print("result: ", result)
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
