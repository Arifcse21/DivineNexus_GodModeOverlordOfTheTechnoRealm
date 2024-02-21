from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
from techno_dominant.models import DominantCliModel
from techno_dominant.serializers import DominantCliModelSerializer
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


@receiver(post_save, sender=DominantCliModel)
def broadcast_new_message(sender, instance, created, **kwargs):
    if created:
        # Serialize the new instance to JSON
        ser_data = DominantCliModelSerializer(instance).data
        
        # Broadcast the new message to the WebSocket consumers
        async_to_sync(channel_layer.group_send)(
            'project_dominant',
            {
                'type': 'message',
                'message': json.dumps(ser_data)
            }
        )
