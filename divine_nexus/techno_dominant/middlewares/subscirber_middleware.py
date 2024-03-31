# middleware.py

from collections import OrderedDict
import logging
from threading import Thread
from techno_dominant.pubs_subs.mqtt_subscribe_utils import MQTTSubscriber
from divine_nexus.const import topics_to_sub_list
from techno_dominant.models.dominant_cli_models import DominantCliModel
from rest_framework.response import Response
from django.http import JsonResponse


class MQTTSubscriberMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.topics = topics_to_sub_list
        print(f"List of topics: {self.topics}")
        
        try:
            self.mqtt_subscriber = MQTTSubscriber(self.topics)

            # Start the MQTT subscriber in a separate thread
            self.mqtt_thread = Thread(target=self.run_mqtt_subscriber)
            self.mqtt_thread.daemon = True  # Ensure the thread exits when the main thread exits
            self.mqtt_thread.start()
            print("Subscriber started successfully")
        except Exception as e:
            print("Error initializing MQTT subscriber: %s", e)

    def run_mqtt_subscriber(self):
        try:
            self.mqtt_subscriber.run()
        except Exception as e:
            print("MQTT subscriber encountered an error: %s", e)

    def __call__(self, request):
        response = self.get_response(request)
        try:
            data = response.data
            print(f"full_data: {data}")
            
            if not isinstance(data, list):
                print(f"response.data>>>>> {data}")
                query = DominantCliModel.objects.filter(pk=data["id"])
                if query.exists():
                    print(f"query>>>>> {query.values()}")
                    query = query.first()

                    data["pub_topic"] = query.pub_topic
                    data["exec_response"] = query.exec_response
                    data["sub_topic"] = query.sub_topic

                    new_response = JsonResponse(data, status=response.status_code)
                    # Return the new response
                    return new_response
            else:
                return response
        except Exception as e:
            print(f"EEEEEEEEEEEEE>>>>> {str(e)}")
            return response
