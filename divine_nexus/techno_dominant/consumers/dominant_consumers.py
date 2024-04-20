from datetime import datetime
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from techno_dominant.serializers.dominant_cli_serializers import DominantCliModelSerializer
from techno_dominant.utils.local_timezone_convert_util import get_local_tz, get_tz_gmt_offset
from techno_dominant.models import *
from asgiref.sync import sync_to_async
import json
from django.http import HttpRequest
from time import sleep


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
    
    async def exec_response(self, event):
        print(self)
        # Send command to WebSocket
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "data": event["data"],
        }))

    
    async def broadcast_message(self, save_stat=None):
        print(f"save_stat: {save_stat}")
        if save_stat:
            response_data = await self.get_exec_response(cli=save_stat)
            # print(type(pub_topic))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'exec_response',
                    'data': response_data, 
                }
            )
        else:

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'command', 
                    'data': 'Unknown command',
                    
                }
            )

    @sync_to_async
    def get_exec_response(self, cli=None):
        # import pdb; pdb.set_trace()
        cli_id = cli if cli else 0
        result = DominantCliModel.objects.filter(id=cli_id)
        if result.exists():
            result = result.first()
            dummy_request = HttpRequest()
            ser_data = DominantCliModelSerializer(result, context={"request": dummy_request}).data
            print(f"ser data: {ser_data}")
            return ser_data
        else:
            return None
        
    @sync_to_async
    def save_message(self, data):
        command = data.get("command")
        is_scheduled = True if data.get("is_scheduled") == "true" else False
        cron_syntax = data.get("cron_syntax")
        scheduled_datetime = data.get("scheduled_datetime")


        try:
            dummy_request = HttpRequest()
            if is_scheduled and scheduled_datetime:

                
                gmt_offset = get_tz_gmt_offset(scheduled_datetime, dummy_request)
                
                print(f"scheduled_datetime: {scheduled_datetime}")

                scheduled_datetime = str(datetime.strptime(scheduled_datetime, '%Y-%m-%dT%H:%M:%S')) + gmt_offset
                # print(f"scheduled_datetime: {scheduled_datetime}")

            payload = {
                "command": command,
                "is_scheduled": is_scheduled,
                "cron_syntax": cron_syntax if cron_syntax else None,
                "scheduled_datetime": scheduled_datetime if scheduled_datetime else None
            }
            print(f"payload: {payload}")
            cli = DominantCliModelSerializer(data=payload, context={"request": dummy_request})
            cli.is_valid(raise_exception=True)
            instace = cli.save()
            ser_data = cli.data
            
            return instace.id
        except Exception as e:
            print(e)
            return False
        
