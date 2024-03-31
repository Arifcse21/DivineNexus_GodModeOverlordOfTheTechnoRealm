import json
from pytz import timezone
from datetime import datetime
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from techno_dominant.models import *
from techno_dominant.serializers import *
from techno_dominant.utils.custom_pagination_util import CustomPagination
from techno_dominant.utils.local_timezone_convert_util import get_tz_gmt_offset


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
            
            return Response(paginated_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:

            command = request.data["command"]
            is_scheduled = True if request.data.get("is_scheduled") == "true" else False
            scheduled_time = request.data.get("scheduled_time") if is_scheduled else None
            repeat_on = request.data.getlist("repeat_on", [])

            if is_scheduled:
                # print(f"repeat_on: {repeat_on}")
                gmt_offset = get_tz_gmt_offset(scheduled_time, request)
                scheduled_time = str(datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M')) + gmt_offset
                # print(f"scheduled_time: {scheduled_time}")

            instance = DominantCliModel.objects.create(
                command=command,
                is_scheduled=is_scheduled,
                scheduled_time=scheduled_time,
            )

            if repeat_on:
                # print(f"repeat_on: {repeat_on}")
                for r_o in repeat_on:
                    instance.repeat_on.add(r_o)

            ser_data = self.get_serializer(instance).data
            
            return Response(ser_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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