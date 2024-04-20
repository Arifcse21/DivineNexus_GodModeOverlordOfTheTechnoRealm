from rest_framework import serializers
from techno_dominant.models import *
from techno_dominant.utils.local_timezone_convert_util import get_local_tz
from cron_descriptor import get_description


class DominantCliModelSerializer(serializers.ModelSerializer):
    cron_syntax_meaning = serializers.SerializerMethodField("get_cron_syntax_meaning")
    
    class Meta:
        model = DominantCliModel
        fields = [
            "id", "command", "pub_topic", "exec_response", "sub_topic", 
            "is_scheduled", "cron_syntax", "cron_syntax_meaning", "executed_at"
        ]
        read_only_fields = ["executed_at"]
    
    def get_cron_syntax_meaning(self, obj):
        if obj.cron_syntax:
            return get_description(obj.cron_syntax)
        else:
            return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        data["executed_at"] = get_local_tz(data["executed_at"], self.context["request"])

        return data
 


class ClearCliHistorySerializer(serializers.Serializer):
    command = serializers.CharField(help_text="Enter the sudo command")
    password = serializers.CharField(help_text="Enter the root password")
