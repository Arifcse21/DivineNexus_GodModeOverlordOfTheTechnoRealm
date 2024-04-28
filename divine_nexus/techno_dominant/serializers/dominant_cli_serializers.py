from rest_framework import serializers
from techno_dominant.models import *
from techno_dominant.utils.local_timezone_convert_util import get_local_tz
from cron_descriptor import get_description


class DominantCliSerializer(serializers.ModelSerializer):
    cron_expression_meaning = serializers.SerializerMethodField("get_cron_expression_meaning")
    
    class Meta:
        model = DominantCliModel
        fields = [
            "id", "command", "pub_topic", "exec_response", "sub_topic", "is_scheduled", 
            "cron_expression", "cron_expression_meaning", "scheduled_datetime", 
            "execution_status", "created_at", "executed_at"
        ]
        read_only_fields = ["execution_status", "created_at", "executed_at"]
    
    def get_cron_expression_meaning(self, obj):
        try:
            return get_description(obj.cron_expression)
        except:
            return None

    def to_representation(self, instance):

        data = super().to_representation(instance)
        try:

            data["scheduled_datetime"] = get_local_tz(data["scheduled_datetime"], self.context["request"]) \
                if data["scheduled_datetime"] else None
            
            data["created_at"] = get_local_tz(data["created_at"], self.context["request"]) \
                if data["created_at"] else None
            
            data["executed_at"] = get_local_tz(data["executed_at"], self.context["request"]) \
                if data["executed_at"] else None

            return data
        except Exception as e:
            print(f"Exception: {e}")
            return data
 


class ClearCliHistorySerializer(serializers.Serializer):
    command = serializers.CharField(help_text="Enter the sudo command")
    password = serializers.CharField(help_text="Enter the root password")
