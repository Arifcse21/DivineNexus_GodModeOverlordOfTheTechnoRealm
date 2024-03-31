from rest_framework import serializers
from techno_dominant.models import *


class DominantCliModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DominantCliModel
        fields = '__all__'


class ClearCliHistorySerializer(serializers.Serializer):
    command = serializers.CharField(help_text="Enter the sudo command")
    password = serializers.CharField(help_text="Enter the root password")
