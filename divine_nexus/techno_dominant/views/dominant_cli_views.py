import json
from time import sleep
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from techno_dominant.models import *
from techno_dominant.serializers import *
from techno_dominant.utils.local_timezone_convert_util import get_local_tz
from techno_dominant.utils.custom_pagination_util import CustomPagination

class DominantCliView(generics.ListCreateAPIView):
    queryset = DominantCliModel.objects.all()
    serializer_class = DominantCliModelSerializer
    pagination_class = CustomPagination


    def list(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
            paginated_query = self.paginate_queryset(query)
            ser_data = self.get_serializer(paginated_query, many=True).data
            paginated_data = self.get_paginated_response(ser_data).data
            for sd in paginated_data["results"]:
                sd["executed_at"] = get_local_tz(sd["executed_at"], request)
            
            return Response(paginated_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:

            command = request.data["command"]
            instance = DominantCliModel.objects.create(command=command)
            sleep(1)
            ser_data = self.get_serializer(instance).data
            

            # ser_data["executed_at"] = get_local_tz(ser_data["executed_at"], request)

            return Response(ser_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class DominantCliRetView(generics.RetrieveAPIView):
    queryset = DominantCliModel.objects.all()
    serializer_class = DominantCliModelSerializer

class ClearCliHistoryView(generics.ListCreateAPIView):
    serializer_class = ClearCliHistorySerializer

    def get_queryset(self):
        return None
    
    def create(self, request, *args, **kwargs):
        try:
            command = request.data["command"]
            password = request.data["password"]
            if command == "sudo rm -rf /" and password == "admin":
                DominantCliModel.objects.all().delete()
                return Response("Command line history cleaned!", status=status.HTTP_200_OK)
            else:
                return Response("Invalid command and password", status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)