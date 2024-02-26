import json
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from techno_dominant.models import *
from techno_dominant.serializers import *
from techno_dominant.utils.local_timezone_convert_util import get_local_tz


class DominantCliView(generics.ListCreateAPIView):
    queryset = DominantCliModel.objects.all()
    serializer_class = DominantCliModelSerializer


    def list(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
            ser_data = self.get_serializer(query, many=True).data
            for sd in ser_data:
                sd["executed_at"] = get_local_tz(sd["executed_at"], request)
            
            return Response(ser_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:

            paylod = {
                "command": request.data["command"]
            }
            serializer = self.get_serializer(data=paylod)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            ser_data = serializer.data

            ser_data["executed_at"] = get_local_tz(ser_data["executed_at"], request)

            return Response(ser_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class DominantCliRetView(generics.RetrieveAPIView):
    queryset = DominantCliModel.objects.all()
    serializer_class = DominantCliModelSerializer