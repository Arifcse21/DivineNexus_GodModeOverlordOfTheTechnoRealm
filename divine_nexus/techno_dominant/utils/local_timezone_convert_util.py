import os
import pytz 
from datetime import datetime
import requests
import geoip2.database


def get_local_tz(datetime_string, request):
    user_ip = get_client_ip(request)
    timezone_name = get_timezone_from_ip(user_ip)
    local_tz = pytz.timezone(timezone_name)

    utc_datetime = parse_datetime(datetime_string)

    return str(utc_datetime.astimezone(local_tz))

def get_local_tz_ws(datetime_string, client_ip):
    timezone_name = get_timezone_from_ip(client_ip)
    local_tz = pytz.timezone(timezone_name)

    utc_datetime = parse_datetime(datetime_string)

    return str(utc_datetime.astimezone(local_tz))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')

def get_timezone_from_ip(ip_address):
    s3_geoip_url = 'https://s3.amazonaws.com/your-bucket-name/GeoLite2-City.mmdb'
    timezone_offset = get_timezone_offset_from_ip(ip_address, s3_geoip_url)
    return timezone_offset

def get_timezone_offset_from_ip(ip_address, s3_geoip_url):
    response = requests.get(s3_geoip_url)
    if response.status_code == 200:
       with geoip2.database.Reader(bytes=response.content) as reader:
        try:
            user_location = reader.city(ip_address)
            timezone_offset = user_location['time_zone']
            timezone = pytz.timezone(timezone_offset)
            timezone_name = timezone.zone
            return timezone_name
        except Exception as e:
            raise Exception(str(e))
            
    else:
        raise Exception(f"Failed to fetch GeoIP data from S3: {response.status_code}")

def parse_datetime(datetime_string):
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
            return datetime.strptime(str(datetime_string), fmt)
        except ValueError:
            continue

    # If none of the formats matched, return UTC datetime
    return datetime.strptime(str(datetime_string), "%Y-%m-%dT%H:%M:%S.%f%z")
