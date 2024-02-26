from rest_framework import serializers
from techno_dominant.models import *


class DominantCliModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DominantCliModel
        fields = '__all__'
