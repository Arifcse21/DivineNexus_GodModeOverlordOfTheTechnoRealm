import os
import pytz 
from datetime import datetime
from django.contrib.gis.geoip2 import GeoIP2


def get_local_tz(datetime_string, request):
    g = GeoIP2()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    user_ip = None
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    
    if request.META.get('HTTP_X_FORWARDED_PROTO', 'http') == "http":
        user_ip = "112.137.0.0"

    if user_ip:
        user_location = g.city(user_ip)
        timezone_offset = user_location['time_zone']
        timezone = pytz.timezone(timezone_offset)
        timezone_name = timezone.zone
        # print(f"timezone: {timezone_name}")

        local_tz = pytz.timezone(timezone_name)
        
        formats_to_try = [
            "%Y-%m-%dT%H:%M:%S.%f%z",   # Datetime with microseconds and timezone
            "%Y-%m-%dT%H:%M:%S%z",      # Datetime with timezone
            "%Y-%m-%d %H:%M:%S.%f%z",   # Datetime with microseconds and timezone
            "%Y-%m-%d %H:%M:%S%z",      # Datetime with timezone
            "%Y-%m-%d %H:%M:%S.%f",     # Datetime with microseconds
            "%Y-%m-%d %H:%M:%S",        # Datetime without microseconds
            "%Y-%m-%d",                 # Date only
            "%H:%M:%S.%f%z",            # Time with microseconds and timezone
            "%H:%M:%S%z",               # Time with timezone
            "%H:%M:%S.%f",              # Time with microseconds
            "%H:%M:%S"                  # Time without microseconds
        ]

        for fmt in formats_to_try:
            try:
                utc_datetime = datetime.strptime(str(datetime_string), fmt)
                break
            except ValueError:
                continue
        else:
            return datetime.strptime(str(datetime_string), "%Y-%m-%dT%H:%M:%S.%f%z")

        # if utc_datetime.tzinfo is None:
        #     utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)  # Assume UTC if no timezone is provided

        return str(utc_datetime.astimezone(local_tz))  # returns local datetime
    

def get_tz_gmt_offset(datetime_string, request):
    g = GeoIP2()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    user_ip = None
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    
    if request.META.get('HTTP_X_FORWARDED_PROTO', 'http') == "http":
        user_ip = "112.137.0.0"

    if user_ip:
        user_location = g.city(user_ip)
        timezone_offset = user_location['time_zone']
        timezone = pytz.timezone(timezone_offset)
        
        dt = datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M')
        
        localized_dt = timezone.localize(dt)
        
        gmt_offset = localized_dt.utcoffset()
        
        total_seconds = gmt_offset.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        
        # Format the GMT offset as +00:00
        gmt_offset_str = f"{hours:+03d}:{minutes:02d}"
        # print(f"gmt_offset_str: {gmt_offset_str}")
        return gmt_offset_str
    
    