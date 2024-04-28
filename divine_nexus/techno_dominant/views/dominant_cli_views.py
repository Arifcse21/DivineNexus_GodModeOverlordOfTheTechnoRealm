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
    serializer_class = DominantCliSerializer
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
            cron_expression = request.data.get("cron_expression")
            scheduled_datetime = request.data.get("scheduled_datetime")
            # print(f"scheduled_datetime: {scheduled_datetime}")

            if is_scheduled and scheduled_datetime:
                gmt_offset = get_tz_gmt_offset(scheduled_datetime, request)
                try:
                    scheduled_datetime = str(datetime.strptime(scheduled_datetime, '%Y-%m-%dT%H:%M:%S')) + gmt_offset
                except:
                    scheduled_datetime = str(datetime.strptime(scheduled_datetime, '%Y-%m-%dT%H:%M')) + gmt_offset
                # print(f"scheduled_time: {scheduled_datetime}")


            instance = DominantCliModel.objects.create(
                command=command,
                is_scheduled=is_scheduled,
                cron_expression=cron_expression if cron_expression else None,
                scheduled_datetime=scheduled_datetime if scheduled_datetime else None
            )

            ser_data = self.get_serializer(instance).data
            
            return Response(ser_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DominantCliRetView(generics.RetrieveAPIView):
    queryset = DominantCliModel.objects.all()
    serializer_class = DominantCliSerializer


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