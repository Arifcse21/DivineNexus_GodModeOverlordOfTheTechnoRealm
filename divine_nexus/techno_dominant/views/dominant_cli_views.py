from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from techno_dominant.models import *
from techno_dominant.serializers import *


class DominantCliView(generics.ListCreateAPIView):
    queryset = DominantCliModel.objects.all()
    serializer_class = DominantCliModelSerializer


class DominantCliRetView(generics.RetrieveAPIView):
    queryset = DominantCliModel.objects.all()
    serializer_class = DominantCliModelSerializer