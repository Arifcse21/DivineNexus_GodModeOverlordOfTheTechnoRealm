from rest_framework import serializers
from techno_dominant.models import *
from techno_dominant.utils.local_timezone_convert_util import get_local_tz


class DominantCliModelSerializer(serializers.ModelSerializer):
    repeat_on_names = serializers.SerializerMethodField("get_repeat_on_names")
    
    class Meta:
        model = DominantCliModel
        fields = [
            "id", "command", "pub_topic", "exec_response", 
            "sub_topic", "is_scheduled", "scheduled_time", 
            "repeat_on", "repeat_on_names", "executed_at"
        ]
        read_only_fields = ["executed_at"]
    
    def get_repeat_on_names(self, obj):
        return [weekday.name for weekday in obj.repeat_on.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "repeat_on" in data:
            data["repeat_on"] = data["repeat_on_names"]
            data.pop("repeat_on_names")

            # print(f"data: {data}")
            data["scheduled_time"] = get_local_tz(data["scheduled_time"], self.context["request"]) if data["is_scheduled"] else None
            data["executed_at"] = get_local_tz(data["executed_at"], self.context["request"])

        return data
 


class ClearCliHistorySerializer(serializers.Serializer):
    command = serializers.CharField(help_text="Enter the sudo command")
    password = serializers.CharField(help_text="Enter the root password")
