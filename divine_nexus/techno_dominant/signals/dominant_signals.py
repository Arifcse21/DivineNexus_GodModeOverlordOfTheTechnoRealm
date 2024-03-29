from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync, sync_to_async
import json
# from techno_dominant.utils.local_timezone_convert_util import get_local_tz_ws
from techno_dominant.models import DominantCliModel
from techno_dominant.serializers import DominantCliModelSerializer
from channels.layers import get_channel_layer
from techno_dominant.pubs_subs import MQTTPublisher

@receiver(post_save, sender=DominantCliModel)
def broadcast_new_message(sender, instance, created, **kwargs):  # Define the function as async
    if created:
        # print(instance)
        # ser_data = DominantCliModelSerializer(instance).data
        # print(ser_data, "here")
        MQTTPublisher(instance.mqtt_topic, f"{instance.id}#{instance.command}").publish()
        
        
        
        
        
        
        
        # ser_data["executed_at"] = get_local_tz_ws(ser_data["executed_at"], self.scope["client"][0])

        # channel_layer = get_channel_layer()
        # # print(f"channel_layer: {channel_layer}")

        # async_to_sync(channel_layer.group_send)(
        #     'project_dominant',
        #     {
        #         'type': 'command',
        #         'data': ser_data
        #     }
        # )
